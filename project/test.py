import os
import sys
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

# ---------------------------
# CONFIG
# ---------------------------
MODEL_PATH = "saved_model/best_model.pth"
IMG_SIZE   = 224
label_map  = {0: "FAKE", 1: "REAL"}   # matches {'fake': 0, 'real': 1}

# ---------------------------
# DEVICE
# ---------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------------------
# TRANSFORM  (same as val_transform used during training)
# ---------------------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ---------------------------
# LOAD MODEL  — matches your trained model exactly
# ---------------------------
def load_model():
    model = models.efficientnet_b0(weights=None)

    # Freeze all
    for param in model.features.parameters():
        param.requires_grad = False

    # Unfreeze last block only  (matches trainable=414,722)
    for param in model.features[-1].parameters():
        param.requires_grad = True

    # Same head as training
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)

    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()

    print(f"Model loaded  : {MODEL_PATH}")
    print(f"Device        : {device}\n")
    return model

# ---------------------------
# PREDICT SINGLE IMAGE
# ---------------------------
def predict_image(model, image_path):
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return

    img    = Image.open(image_path).convert("RGB")
    tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        probs   = torch.softmax(outputs, dim=1)[0]
        pred    = torch.argmax(probs).item()

    label      = label_map[pred]
    confidence = probs[pred].item() * 100
    fake_prob  = probs[0].item() * 100
    real_prob  = probs[1].item() * 100

    print(f"Image      : {os.path.basename(image_path)}")
    print(f"Prediction : {label}")
    print(f"Confidence : {confidence:.2f}%")
    print(f"Fake prob  : {fake_prob:.2f}%")
    print(f"Real prob  : {real_prob:.2f}%")
    print("-" * 35)

    return label, confidence

# ---------------------------
# PREDICT ENTIRE FOLDER
# ---------------------------
def predict_folder(model, folder_path):
    valid_ext = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    images = [
        f for f in os.listdir(folder_path)
        if os.path.splitext(f)[1].lower() in valid_ext
    ]

    if not images:
        print(f"No images found in: {folder_path}")
        return

    print(f"Found {len(images)} images in '{folder_path}'\n")
    print(f"{'Image':<40} {'Result':<8} {'Confidence':>12}  {'Fake%':>7}  {'Real%':>7}")
    print("-" * 82)

    real_count = fake_count = 0

    for fname in sorted(images):
        fpath  = os.path.join(folder_path, fname)
        img    = Image.open(fpath).convert("RGB")
        tensor = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(tensor)
            probs   = torch.softmax(outputs, dim=1)[0]
            pred    = torch.argmax(probs).item()

        label      = label_map[pred]
        confidence = probs[pred].item() * 100
        fake_prob  = probs[0].item() * 100
        real_prob  = probs[1].item() * 100

        if pred == 0:
            fake_count += 1
        else:
            real_count += 1

        print(f"{fname:<40} {label:<8} {confidence:>11.2f}%  {fake_prob:>6.2f}%  {real_prob:>6.2f}%")

    print("-" * 82)
    print(f"\nTotal : {len(images)}  |  REAL : {real_count}  |  FAKE : {fake_count}")

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    model = load_model()

    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isdir(path):
            predict_folder(model, path)
        elif os.path.isfile(path):
            predict_image(model, path)
        else:
            print(f"Path not found: {path}")
    else:
        print("Usage:")
        print("  Single image  ->  python test.py path\\to\\image.jpg")
        print("  Folder        ->  python test.py path\\to\\folder\\")
        print("")
        print("Quick test on your existing dataset:")
        print("  python test.py dataset\\test\\fake\\")
        print("  python test.py dataset\\test\\real\\")