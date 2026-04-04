import cv2
import torch
from app.model_loader import image_model, image_model_error

def preprocess_image(path):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Unable to read image: {path}")

    # Resize
    img = cv2.resize(img, (224, 224))

    # Normalize (0–1)
    img = img / 255.0

    # Convert to tensor
    img = torch.tensor(img).permute(2, 0, 1).float()

    # Add batch dimension
    img = img.unsqueeze(0)

    return img


def analyze_image(path):
    if image_model is None:
        return {"error": f"Image model unavailable: {image_model_error}"}

    img = preprocess_image(path)

    with torch.no_grad():
        pred = image_model(img)

    if pred.ndim == 2 and pred.shape[1] >= 2:
        probs = torch.softmax(pred, dim=1)
        fake_probability = float(probs[0, 1].item())
    else:
        fake_probability = float(torch.sigmoid(pred).reshape(-1)[0].item())

    return {
        "fake_probability": fake_probability
    }