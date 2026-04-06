# import os
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, Dataset
# from torchvision import transforms, models
# from PIL import Image
# from facenet_pytorch import MTCNN
# from tqdm import tqdm


# # ---------------------------
# # Dataset
# # ---------------------------
# class FaceDataset(Dataset):
#     def __init__(self, root_dir, transform=None):
#         self.root_dir = root_dir
#         self.transform = transform
#         self.images = []
#         self.labels = []
        
#         classes = ["real", "fake"]
#         for idx, cls in enumerate(classes):
#             cls_dir = os.path.join(root_dir, cls)

#             if not os.path.exists(cls_dir):
#                 print(f"⚠️ Warning: {cls_dir} not found")
#                 continue

#             for f in os.listdir(cls_dir):
#                 if f.lower().endswith((".png", ".jpg", ".jpeg")):
#                     self.images.append(os.path.join(cls_dir, f))
#                     self.labels.append(idx)

#         print(f"✅ Total images: {len(self.images)}")

#     def __len__(self):
#         return len(self.images)
    
#     def __getitem__(self, idx):
#         img_path = self.images[idx]
#         label = self.labels[idx]

#         img = Image.open(img_path).convert("RGB")

#         # Face detection
#         face = mtcnn(img)

#         if face is None:
#             # fallback: use full image
#             img = self.transform(img)
#         else:
#             img = face  # already tensor (224x224)

#         return img, label


# # ---------------------------
# # Device
# # ---------------------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)


# # ---------------------------
# # MTCNN (FIXED SIZE HERE)
# # ---------------------------
# mtcnn = MTCNN(
#     image_size=224,     # 🔥 ensures consistent size
#     keep_all=False,
#     device=device
# )


# # ---------------------------
# # Transforms
# # ---------------------------
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         mean=[0.485, 0.456, 0.406],
#         std=[0.229, 0.224, 0.225]
#     )
# ])


# # ---------------------------
# # Dataset & Loader
# # ---------------------------
# train_dataset = FaceDataset("dataset/image", transform=transform)

# train_loader = DataLoader(
#     train_dataset,
#     batch_size=16,
#     shuffle=True,
#     num_workers=0  # keep 0 for Windows stability
# )


# # ---------------------------
# # Model
# # ---------------------------
# model = models.efficientnet_b0(weights="DEFAULT")
# model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)
# model = model.to(device)


# # ---------------------------
# # Training Setup
# # ---------------------------
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=1e-4)

# num_epochs = 10


# # ---------------------------
# # Training Loop
# # ---------------------------
# for epoch in range(num_epochs):
#     model.train()
#     running_loss = 0.0
#     correct = 0
#     total = 0
    
#     for imgs, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}"):
#         imgs, labels = imgs.to(device), labels.to(device)
        
#         optimizer.zero_grad()
#         outputs = model(imgs)
#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()
        
#         running_loss += loss.item()
#         _, predicted = torch.max(outputs, 1)
#         total += labels.size(0)
#         correct += (predicted == labels).sum().item()
    
#     train_acc = 100 * correct / total
#     print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader):.4f}, Accuracy: {train_acc:.2f}%")


# # ---------------------------
# # Save Model
# # ---------------------------
# os.makedirs("models/image", exist_ok=True)
# torch.save(model.state_dict(), "models/image/image_model_mtcnn.pth")

# print("✅ Model saved at models/image/image_model_mtcnn.pth")

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from PIL import Image
from facenet_pytorch import MTCNN
from tqdm import tqdm

# ---------------------------
# Device
# ---------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# ---------------------------
# MTCNN (fixed size)
# ---------------------------
mtcnn = MTCNN(
    image_size=224,
    keep_all=False,
    device=device
)

# ---------------------------
# Transforms (normalize same as ImageNet)
# ---------------------------
normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

# ---------------------------
# Dataset
# ---------------------------
class FaceDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.images = []
        self.labels = []
        
        classes = ["real", "fake"]
        for idx, cls in enumerate(classes):
            cls_dir = os.path.join(root_dir, cls)
            if not os.path.exists(cls_dir):
                print(f"⚠️ Warning: {cls_dir} not found")
                continue
            for f in os.listdir(cls_dir):
                if f.lower().endswith((".png", ".jpg", ".jpeg")):
                    self.images.append(os.path.join(cls_dir, f))
                    self.labels.append(idx)
        print(f"✅ Total images: {len(self.images)}")

    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        label = self.labels[idx]

        img = Image.open(img_path).convert("RGB")

        # Detect face
        face = mtcnn(img)

        if face is None:
            # fallback: resize full image and convert to tensor
            img_resized = img.resize((224, 224))
            face = transforms.ToTensor()(img_resized)

        # Ensure tensor is normalized
        face = normalize(face)

        return face, label

# ---------------------------
# Dataset & Loader
# ---------------------------
train_dataset = FaceDataset("dataset/image")
train_loader = DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True,
    num_workers=0
)

# ---------------------------
# Model
# ---------------------------
model = models.efficientnet_b0(weights="DEFAULT")
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)
model = model.to(device)

# ---------------------------
# Training Setup
# ---------------------------
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)
num_epochs = 10

# ---------------------------
# Training Loop
# ---------------------------
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for imgs, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}"):
        imgs, labels = imgs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    train_acc = 100 * correct / total
    print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader):.4f}, Accuracy: {train_acc:.2f}%")

# ---------------------------
# Save Model
# ---------------------------
os.makedirs("models/image", exist_ok=True)
torch.save(model.state_dict(), "models/image/image_model_mtcnn.pth")
print("✅ Model saved at models/image/image_model_mtcnn.pth")