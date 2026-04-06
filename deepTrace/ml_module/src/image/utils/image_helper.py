# import cv2
# from PIL import Image

# def load_image(img_path):
#     """
#     Loads an image from disk and converts it to RGB (PIL Image).
#     Raises an error if the image cannot be loaded.
#     """
#     img = cv2.imread(img_path)
#     if img is None:
#         raise ValueError(f"Cannot read image: {img_path}")
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     return Image.fromarray(img)

# src/image/utils/image_helper.py


# import cv2
# from PIL import Image
# from facenet_pytorch import MTCNN
# import torch

# # Device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# mtcnn = MTCNN(keep_all=False, device=device)

# def detect_and_crop_face(img_path):
#     # Load full image
#     img_bgr = cv2.imread(img_path)
#     if img_bgr is None:
#         return None

#     img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
#     img_pil = Image.fromarray(img_rgb)

#     # Detect and crop face
#     face_tensor = mtcnn(img_pil)
#     if face_tensor is None:
#         # If face not detected, fallback to full image
#         return img_rgb

#     # Convert tensor back to PIL Image for consistency with transforms
#     face_img = face_tensor.permute(1, 2, 0).int().numpy()
#     return face_img


# import cv2
# from PIL import Image
# from facenet_pytorch import MTCNN
# import torch
# import numpy as np

# # Device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # MTCNN
# mtcnn = MTCNN(keep_all=False, device=device)

# def detect_and_crop_face(img_path):
#     img_bgr = cv2.imread(img_path)

#     if img_bgr is None:
#         raise ValueError(f"Cannot read image: {img_path}")

#     img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
#     img_pil = Image.fromarray(img_rgb)

#     # Detect face
#     face_tensor = mtcnn(img_pil)

#     if face_tensor is None:
#         # fallback: return full image as PIL
#         return img_pil

#     # Convert tensor → PIL
#     face_img = face_tensor.permute(1, 2, 0).byte().cpu().numpy()
#     return Image.fromarray(face_img)

import cv2
from PIL import Image
from facenet_pytorch import MTCNN
import torch
from torchvision import transforms

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# MTCNN (fixed size, same as training)
mtcnn = MTCNN(image_size=224, keep_all=False, device=device)

# Normalization (same as training)
normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

# Transform to tensor
to_tensor = transforms.ToTensor()

def detect_and_crop_face(img_path):
    # Load image
    img_bgr = cv2.imread(img_path)
    if img_bgr is None:
        raise ValueError(f"Cannot read image: {img_path}")

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    # Detect face
    face_tensor = mtcnn(img_pil)

    if face_tensor is None:
        # fallback: resize full image to 224x224
        img_pil = img_pil.resize((224, 224))
        face_tensor = to_tensor(img_pil)

    # Normalize (same as training)
    face_tensor = normalize(face_tensor)

    return face_tensor