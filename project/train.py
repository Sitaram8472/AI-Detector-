import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from tqdm import tqdm

# ---------------------------
# CONFIG
# ---------------------------
DATA_DIR = "dataset"
BATCH_SIZE = 4        # 🔥 smaller = better for low GPU
EPOCHS = 10           # 🔥 more training
LR = 1e-4
IMG_SIZE = 224

# ---------------------------
# DEVICE
# ---------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# ---------------------------
# TRANSFORMS (better accuracy)
# ---------------------------
train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

val_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# ---------------------------
# DATASETS
# ---------------------------
train_data = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=train_transform)
val_data   = datasets.ImageFolder(os.path.join(DATA_DIR, "validation"), transform=val_transform)
test_data  = datasets.ImageFolder(os.path.join(DATA_DIR, "test"), transform=val_transform)

print("Classes:", train_data.classes)

# ---------------------------
# LOADERS
# ---------------------------
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
val_loader   = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)
test_loader  = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

# ---------------------------
# MODEL
# ---------------------------
model = models.efficientnet_b0(weights="DEFAULT")

# Freeze all layers
for param in model.features.parameters():
    param.requires_grad = False

# 🔥 Unfreeze LAST block (important)
for param in model.features[-1].parameters():
    param.requires_grad = True

# Replace classifier
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)
model = model.to(device)

# ---------------------------
# LOSS + OPTIMIZER
# ---------------------------
criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=LR
)

# ---------------------------
# VALIDATION FUNCTION
# ---------------------------
def evaluate(loader):
    model.eval()
    correct = 0
    total = 0
    loss_total = 0

    with torch.no_grad():
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)

            outputs = model(imgs)
            loss = criterion(outputs, labels)

            loss_total += loss.item()
            _, pred = torch.max(outputs, 1)

            correct += (pred == labels).sum().item()
            total += labels.size(0)

    acc = 100 * correct / total
    return loss_total, acc

# ---------------------------
# TRAIN LOOP
# ---------------------------
best_val_acc = 0

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0
    correct = 0
    total = 0

    for imgs, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS}"):
        imgs, labels = imgs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(imgs)

        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, pred = torch.max(outputs, 1)

        correct += (pred == labels).sum().item()
        total += labels.size(0)

    train_acc = 100 * correct / total
    val_loss, val_acc = evaluate(val_loader)

    print(f"\nEpoch {epoch+1}")
    print(f"Train Loss: {running_loss:.4f} | Train Acc: {train_acc:.2f}%")
    print(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")

    # Save best model
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        os.makedirs("saved_model", exist_ok=True)
        torch.save(model.state_dict(), "saved_model/best_model.pth")
        print("✅ Best model saved")

# ---------------------------
# TEST EVALUATION
# ---------------------------
test_loss, test_acc = evaluate(test_loader)

print("\n========================")
print(f"Test Accuracy: {test_acc:.2f}%")
print("========================")

# ---------------------------
# SAVE FINAL MODEL
# ---------------------------
torch.save(model.state_dict(), "saved_model/final_model.pth")
print("✅ Final model saved")