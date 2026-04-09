from app.core.celery_app import celery_app
import os
import cv2
from app.model_loader import image_model, image_model_error
from app.services.image_services import preprocess_image_array, predict_fake_probability


@celery_app.task
def analyze_video_task(path):

    if image_model is None:
        return {"error": f"Image model unavailable for video analysis: {image_model_error}"}

    cap = cv2.VideoCapture(path)

    predictions = []
    frame_count = 0
    frame_stride = max(1, int(os.getenv("VIDEO_FRAME_STRIDE", "5")))
    max_frames_to_analyze = max(1, int(os.getenv("VIDEO_MAX_FRAMES", "120")))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_stride != 0:
            frame_count += 1
            continue

        frame_tensor = preprocess_image_array(frame)
        predictions.append(predict_fake_probability(image_model, frame_tensor))

        if len(predictions) >= max_frames_to_analyze:
            frame_count += 1
            break

        frame_count += 1

    cap.release()

    if len(predictions) == 0:
        return {"error": "No frames processed"}

    final_score = sum(predictions) / len(predictions)

    return {
        "fake_probability": final_score,
        "verdict": "Fake" if final_score > 0.5 else "Real",
        "frames_analyzed": len(predictions),
        "frame_stride": frame_stride,
        "max_frames_limit": max_frames_to_analyze,
        "model_used": "image_model"
    }