import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from ..utils.image_helper import load_image

# ------------------------------
# Device
# ------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# ------------------------------
# Transform
# ------------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ------------------------------
# Dataset
# ------------------------------
class FaceDataset(Dataset):
    def __init__(self, root_dir):
        self.samples = []
        self.class_map = {"real": 0, "fake": 1}

        for label_name in ["real", "fake"]:
            folder = os.path.join(root_dir, label_name)
            if not os.path.exists(folder):
                continue
            for file in os.listdir(folder):
                if file.lower().endswith((".jpg", ".png", ".jpeg")):
                    self.samples.append((os.path.join(folder, file), self.class_map[label_name]))

        print(f"✅ Total samples: {len(self.samples)}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        img = load_image(img_path)
        img_tensor = transform(img)
        return img_tensor, torch.tensor(label, dtype=torch.long)

# ------------------------------
# Load dataset
# ------------------------------
dataset = FaceDataset("dataset/image")
loader = DataLoader(dataset, batch_size=8, shuffle=True, num_workers=0, pin_memory=False)

# ------------------------------
# Model
# ------------------------------
model = models.efficientnet_b0(weights="DEFAULT")
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)
model = model.to(device)

# ------------------------------
# Loss & Optimizer
# ------------------------------
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

# ------------------------------
# Training
# ------------------------------
epochs = 10

for epoch in range(epochs):
    model.train()
    running_loss = 0
    for batch_idx, (images, labels) in enumerate(loader):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if batch_idx % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}] Batch [{batch_idx}] Loss: {loss.item():.4f}")

    print(f"✅ Epoch {epoch+1} Complete | Loss: {running_loss:.4f}")

# ------------------------------
# Save model
# ------------------------------
os.makedirs("models/image", exist_ok=True)
torch.save(model.state_dict(), "models/image/image_model.pth")
print("🎉 Training finished!")