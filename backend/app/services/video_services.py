import json
import os
from urllib import error, request

from app.workers.video_task import analyze_video_task


def _extract_truthscan_result(payload):
    # Normalize possible TruthScan response shapes into one predictable format.
    verdict = (
        payload.get("verdict")
        or payload.get("label")
        or payload.get("prediction")
        or payload.get("result")
        or "Unknown"
    )

    fake_probability = (
        payload.get("fake_probability")
        or payload.get("score")
        or payload.get("confidence")
        or 0
    )

    try:
        fake_probability = float(fake_probability)
    except (TypeError, ValueError):
        fake_probability = 0.0

    if fake_probability > 1:
        fake_probability = fake_probability / 100.0

    return {
        "status": "completed",
        "verdict": str(verdict),
        "fake_probability": round(fake_probability, 4),
        "confidence_percentage": round(fake_probability * 100, 2),
        "model_used": "truthscan_api",
        "raw": payload,
    }


def _truthscan_enabled():
    return bool(os.getenv("TRUTHSCAN_API_URL"))


def _analyze_video_with_truthscan(path):
    api_url = os.getenv("TRUTHSCAN_API_URL", "").strip()
    api_key = os.getenv("TRUTHSCAN_API_KEY", "").strip()
    timeout_seconds = int(os.getenv("TRUTHSCAN_TIMEOUT_SECONDS", "60"))

    if not api_url:
        return {
            "status": "failed",
            "error": "TRUTHSCAN_API_URL is not configured.",
        }

    with open(path, "rb") as file:
        video_bytes = file.read()

    req = request.Request(
        api_url,
        data=video_bytes,
        method="POST",
        headers={
            "Content-Type": "application/octet-stream",
            "Authorization": f"Bearer {api_key}" if api_key else "",
        },
    )

    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            response_text = response.read().decode("utf-8")
            payload = json.loads(response_text) if response_text else {}
            return _extract_truthscan_result(payload)
    except error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8")
        except Exception:
            detail = str(exc)

        return {
            "status": "failed",
            "error": f"TruthScan request failed with status {exc.code}: {detail}",
        }
    except Exception as exc:
        return {
            "status": "failed",
            "error": f"TruthScan request error: {exc}",
        }


def process_video(path):
    if _truthscan_enabled():
        return _analyze_video_with_truthscan(path)

    try:
        task = analyze_video_task.delay(path)
        return {
            "message": "Processing started",
            "task_id": task.id
        }
    except Exception as exc:
        return {
            "status": "failed",
            "error": f"Unable to queue video task. Check Redis/Celery services. Details: {exc}",
        }


def get_video_result(task_id):
    try:
        task = analyze_video_task.AsyncResult(task_id)

        if task.failed():
            return {
                "status": "failed",
                "task_id": task_id,
                "error": str(task.result),
            }

        if task.ready():
            result = task.result or {}

            if not isinstance(result, dict):
                result = {"raw_result": result}

            fake_probability = float(result.get("fake_probability", 0.0))
            verdict = result.get("verdict") or ("Fake" if fake_probability > 0.5 else "Real")

            return {
                "status": "completed",
                "task_id": task_id,
                "verdict": verdict,
                "fake_probability": fake_probability,
                "confidence_percentage": round(fake_probability * 100, 2),
                "frames_analyzed": result.get("frames_analyzed", 0),
                "frame_stride": result.get("frame_stride"),
                "max_frames_limit": result.get("max_frames_limit"),
                "model_used": result.get("model_used", "image_model"),
                "error": result.get("error"),
            }

        return {
            "status": "processing",
            "task_id": task_id,
            "message": "Video analysis in progress",
        }
    except RuntimeError as exc:
        return {
            "status": "failed",
            "task_id": task_id,
            "error": "Celery result backend temporarily unavailable. Restart Celery worker and ensure Redis is running.",
            "details": str(exc),
        }
    except Exception as exc:
        return {
            "status": "failed",
            "task_id": task_id,
            "error": f"Unexpected video result error: {exc}",
        }