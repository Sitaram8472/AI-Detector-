# import torch
# import torch.nn as nn
# from torchvision import models, transforms
# from ..utils.image_helper import load_image

# # ------------------------------
# # Device
# # ------------------------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # ------------------------------
# # Transform
# # ------------------------------
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         mean=[0.485, 0.456, 0.406],
#         std=[0.229, 0.224, 0.225]
#     )
# ])

# # ------------------------------
# # Class names
# # ------------------------------
# CLASS_NAMES = ["Real", "Fake"]

# # ------------------------------
# # Load model
# # ------------------------------
# model = models.efficientnet_b0(weights="DEFAULT")
# model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)
# model.load_state_dict(torch.load("models/image/image_model.pth", map_location=device))
# model = model.to(device)
# model.eval()

# # ------------------------------
# # Prediction function
# # ------------------------------
# def predict_image(img_path):
#     img = load_image(img_path)
#     img_tensor = transform(img).unsqueeze(0).to(device)

#     with torch.no_grad():
#         outputs = model(img_tensor)
#         probs = torch.softmax(outputs, dim=1)
#         pred = torch.argmax(probs, dim=1).item()

#     return {
#         "label": CLASS_NAMES[pred],
#         "confidence": round(probs[0][pred].item(), 4)
#     }

# Example usage:
# result = predict_image("dataset/image/real/sample1.jpg")
# print(result)

# import torch
# import torch.nn as nn
# from torchvision import models, transforms
# from ..utils.image_helper import detect_and_crop_face

# # ------------------------------
# # Device
# # ------------------------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # ------------------------------
# # Transform
# # ------------------------------
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         mean=[0.485, 0.456, 0.406],
#         std=[0.229, 0.224, 0.225]
#     )
# ])

# # ------------------------------
# # Class names
# # ------------------------------
# CLASS_NAMES = ["Fake", "Real"]

# # ------------------------------
# # Load model
# # ------------------------------
# model = models.efficientnet_b0(weights="DEFAULT")
# model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)

# # ⚠️ Make sure this matches your saved model
# model.load_state_dict(
#     torch.load("models/image/image_model_mtcnn.pth", map_location=device)
# )

# model = model.to(device)
# model.eval()

# # ------------------------------
# # Prediction function
# # ------------------------------
# def predict_image(img_path):
#     img = detect_and_crop_face(img_path)

#     img_tensor = transform(img).unsqueeze(0).to(device)

#     with torch.no_grad():
#         outputs = model(img_tensor)
#         probs = torch.softmax(outputs, dim=1)
#         pred = torch.argmax(probs, dim=1).item()

#     return {
#         "label": CLASS_NAMES[pred],
#         "confidence": round(probs[0][pred].item(), 4)
#     }
    
    
import torch
import torch.nn as nn
from torchvision import models
from ..utils.image_helper import detect_and_crop_face

# ------------------------------
# Device
# ------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ------------------------------
# Class names
# ------------------------------
CLASS_NAMES = ["Real", "Fake"]

# ------------------------------
# Load model
# ------------------------------
model = models.efficientnet_b0(weights="DEFAULT")
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)

# Load trained weights
model.load_state_dict(
    torch.load("models/image/image_model_mtcnn.pth", map_location=device)
)

model = model.to(device)
model.eval()

# ------------------------------
# Prediction function
# ------------------------------
def predict_image(img_path):
    # detect_and_crop_face already returns a normalized tensor
    img_tensor = detect_and_crop_face(img_path).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.softmax(outputs, dim=1)
        pred = torch.argmax(probs, dim=1).item()

    return {
        "label": CLASS_NAMES[pred],
        "confidence": round(probs[0][pred].item(), 4)
    }

# Example usage:
# result = predict_image("dataset/image/real/real_561.jpg")
# print(result)