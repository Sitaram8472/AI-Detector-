from app.core.celery_app import celery_app
import cv2
import torch
from app.model_loader import video_model, video_model_error

def preprocess_frame(frame):
    frame = cv2.resize(frame, (224, 224))
    frame = frame / 255.0
    frame = torch.tensor(frame).permute(2, 0, 1).float()
    frame = frame.unsqueeze(0)
    return frame

@celery_app.task
def analyze_video_task(path):

    if video_model is None:
        return {"error": f"Video model unavailable: {video_model_error}"}

    cap = cv2.VideoCapture(path)

    predictions = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 5 != 0:
            frame_count += 1
            continue

        frame = preprocess_frame(frame)

        with torch.no_grad():
            pred = video_model(frame)

        predictions.append(pred.item())
        frame_count += 1

    cap.release()

    if len(predictions) == 0:
        return {"error": "No frames processed"}

    final_score = sum(predictions) / len(predictions)

    return {
        "fake_probability": final_score,
        "verdict": "Fake" if final_score > 0.5 else "Real"
    }