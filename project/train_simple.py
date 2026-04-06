import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from tqdm import tqdm
from sklearn.metrics import roc_auc_score
import numpy as np

# ---------------------------
# CONFIG
# ---------------------------
DATA_DIR   = "dataset"
BATCH_SIZE = 4          # safe for low GPU memory
EPOCHS     = 10
LR         = 1e-4
IMG_SIZE   = 224
PATIENCE   = 4          # early stopping

# ---------------------------
# DEVICE
# ---------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
if device.type == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# ---------------------------
# TRANSFORMS
# ---------------------------
train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ---------------------------
# DATASETS
# ---------------------------
train_data = datasets.ImageFolder(os.path.join(DATA_DIR, "train"),      transform=train_transform)
val_data   = datasets.ImageFolder(os.path.join(DATA_DIR, "validation"), transform=val_transform)
test_data  = datasets.ImageFolder(os.path.join(DATA_DIR, "test"),       transform=val_transform)

print(f"Classes : {train_data.class_to_idx}")
print(f"Train   : {len(train_data):,}  |  Val: {len(val_data):,}  |  Test: {len(test_data):,}")

# ---------------------------
# LOADERS
# ---------------------------
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True,  num_workers=0, pin_memory=True)
val_loader   = DataLoader(val_data,   batch_size=BATCH_SIZE, shuffle=False, num_workers=0, pin_memory=True)
test_loader  = DataLoader(test_data,  batch_size=BATCH_SIZE, shuffle=False, num_workers=0, pin_memory=True)

# ---------------------------
# MODEL
# ---------------------------
model = models.efficientnet_b0(weights="DEFAULT")

# Freeze backbone
for param in model.features.parameters():
    param.requires_grad = False

# Unfreeze last block only
for param in model.features[-1].parameters():
    param.requires_grad = True

# Custom head
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)
model = model.to(device)

total     = sum(p.numel() for p in model.parameters())
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Params  : total={total:,}  trainable={trainable:,}")

# ---------------------------
# LOSS + OPTIMIZER + SCHEDULER
# ---------------------------
criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=LR
)

# Reduce LR if val loss stops improving
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode="min", factor=0.5, patience=2
)

# ---------------------------
# EVALUATE FUNCTION
# ---------------------------
def evaluate(loader):
    model.eval()
    correct = total = loss_total = 0
    all_probs, all_labels = [], []

    with torch.no_grad():
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            outputs = model(imgs)
            loss    = criterion(outputs, labels)

            loss_total += loss.item()
            probs = torch.softmax(outputs, dim=1)[:, 1]
            _, pred = torch.max(outputs, 1)

            correct      += (pred == labels).sum().item()
            total        += labels.size(0)
            all_probs.extend(probs.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    acc = 100 * correct / total
    auc = roc_auc_score(all_labels, all_probs) if len(set(all_labels)) > 1 else 0.0
    return loss_total, acc, auc

# ---------------------------
# TRAINING LOOP
# ---------------------------
best_val_acc = 0.0
no_improve   = 0
os.makedirs("saved_model", exist_ok=True)

print(f"\n{'Epoch':<7} {'TR Loss':>9} {'TR Acc':>8} {'VL Loss':>9} {'VL Acc':>8} {'VL AUC':>8}")
print("-" * 55)

for epoch in range(1, EPOCHS + 1):
    model.train()
    running_loss = correct = total = 0

    for imgs, labels in tqdm(train_loader, desc=f"Epoch {epoch}/{EPOCHS}", leave=False):
        imgs, labels = imgs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(imgs)
        loss    = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, pred = torch.max(outputs, 1)
        correct += (pred == labels).sum().item()
        total   += labels.size(0)

    train_acc = 100 * correct / total
    val_loss, val_acc, val_auc = evaluate(val_loader)

    # Step scheduler
    scheduler.step(val_loss)

    marker = ""
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "saved_model/best_model.pth")
        no_improve = 0
        marker = "  <- best"
    else:
        no_improve += 1

    print(f"{epoch:<7} {running_loss:>9.4f} {train_acc:>7.2f}% {val_loss:>9.4f} {val_acc:>7.2f}% {val_auc:>8.4f}{marker}")

    if no_improve >= PATIENCE:
        print(f"\nEarly stopping at epoch {epoch}. Best val acc: {best_val_acc:.2f}%")
        break

# ---------------------------
# TEST EVALUATION
# ---------------------------
print("\nLoading best model for test evaluation...")
model.load_state_dict(torch.load("saved_model/best_model.pth", map_location=device))
test_loss, test_acc, test_auc = evaluate(test_loader)

print("\n" + "=" * 40)
print(f"  Test Accuracy : {test_acc:.2f}%")
print(f"  Test ROC-AUC  : {test_auc:.4f}")
print("=" * 40)

# ---------------------------
# SAVE FINAL MODEL
# ---------------------------
torch.save(model.state_dict(), "saved_model/final_model.pth")
print("Final model saved -> saved_model/final_model.pth")







# import os
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader
# from torchvision import datasets, transforms, models
# from tqdm import tqdm
# from sklearn.metrics import roc_auc_score
# import numpy as np

# # ---------------------------
# # CONFIG
# # ---------------------------
# DATA_DIR   = "dataset"
# BATCH_SIZE = 4
# EPOCHS     = 15
# LR         = 5e-5       # lower LR = less overfitting
# IMG_SIZE   = 224
# PATIENCE   = 5

# # ---------------------------
# # DEVICE
# # ---------------------------
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")
# if device.type == "cuda":
#     print(f"GPU: {torch.cuda.get_device_name(0)}")

# # ---------------------------
# # TRANSFORMS  (stronger augmentation = less overfitting)
# # ---------------------------
# train_transform = transforms.Compose([
#     transforms.Resize((IMG_SIZE + 32, IMG_SIZE + 32)),
#     transforms.RandomCrop(IMG_SIZE),                        # crop instead of resize = more variety
#     transforms.RandomHorizontalFlip(),
#     transforms.RandomVerticalFlip(p=0.2),
#     transforms.RandomRotation(15),
#     transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2),
#     transforms.RandomGrayscale(p=0.05),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406],
#                          [0.229, 0.224, 0.225]),
#     transforms.RandomErasing(p=0.2),                        # randomly erase patches
# ])

# val_transform = transforms.Compose([
#     transforms.Resize((IMG_SIZE, IMG_SIZE)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406],
#                          [0.229, 0.224, 0.225])
# ])

# # ---------------------------
# # DATASETS
# # ---------------------------
# train_data = datasets.ImageFolder(os.path.join(DATA_DIR, "train"),      transform=train_transform)
# val_data   = datasets.ImageFolder(os.path.join(DATA_DIR, "validation"), transform=val_transform)
# test_data  = datasets.ImageFolder(os.path.join(DATA_DIR, "test"),       transform=val_transform)

# print(f"Classes : {train_data.class_to_idx}")
# print(f"Train   : {len(train_data):,}  |  Val: {len(val_data):,}  |  Test: {len(test_data):,}")

# # ---------------------------
# # LOADERS
# # ---------------------------
# train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True,  num_workers=0, pin_memory=True)
# val_loader   = DataLoader(val_data,   batch_size=BATCH_SIZE, shuffle=False, num_workers=0, pin_memory=True)
# test_loader  = DataLoader(test_data,  batch_size=BATCH_SIZE, shuffle=False, num_workers=0, pin_memory=True)

# # ---------------------------
# # MODEL
# # ---------------------------
# model = models.efficientnet_b0(weights="DEFAULT")

# # Unfreeze last 4 blocks (more learning capacity)
# # EfficientNet-B0 has 9 feature blocks (0-8)
# for i, block in enumerate(model.features):
#     for param in block.parameters():
#         param.requires_grad = (i >= 5)   # freeze 0-4, unfreeze 5-8

# # Custom head with extra dropout for regularisation
# in_features = model.classifier[1].in_features
# model.classifier = nn.Sequential(
#     nn.Dropout(p=0.5),                   # higher dropout = less overfitting
#     nn.Linear(in_features, 2)
# )

# model = model.to(device)

# total     = sum(p.numel() for p in model.parameters())
# trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
# print(f"Params  : total={total:,}  trainable={trainable:,}")

# # ---------------------------
# # LOSS + OPTIMIZER + SCHEDULER
# # ---------------------------
# criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

# optimizer = optim.AdamW(                 # AdamW has better weight decay than Adam
#     filter(lambda p: p.requires_grad, model.parameters()),
#     lr=LR,
#     weight_decay=1e-3                    # weight decay = regularisation
# )

# # Cosine annealing — smoothly reduces LR over training
# scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=1e-6)

# # ---------------------------
# # EVALUATE FUNCTION
# # ---------------------------
# def evaluate(loader):
#     model.eval()
#     correct = total = loss_total = 0
#     all_probs, all_labels = [], []

#     with torch.no_grad():
#         for imgs, labels in loader:
#             imgs, labels = imgs.to(device), labels.to(device)
#             outputs = model(imgs)
#             loss    = criterion(outputs, labels)

#             loss_total += loss.item()
#             probs = torch.softmax(outputs, dim=1)[:, 1]
#             _, pred = torch.max(outputs, 1)

#             correct      += (pred == labels).sum().item()
#             total        += labels.size(0)
#             all_probs.extend(probs.cpu().numpy())
#             all_labels.extend(labels.cpu().numpy())

#     acc = 100 * correct / total
#     auc = roc_auc_score(all_labels, all_probs) if len(set(all_labels)) > 1 else 0.0
#     return loss_total, acc, auc

# # ---------------------------
# # TRAINING LOOP
# # ---------------------------
# best_val_auc = 0.0        # track AUC instead of acc (more reliable)
# no_improve   = 0
# os.makedirs("saved_model", exist_ok=True)

# print(f"\n{'Epoch':<7} {'TR Loss':>9} {'TR Acc':>8} {'VL Loss':>9} {'VL Acc':>8} {'VL AUC':>8}  {'LR':>10}")
# print("-" * 70)

# for epoch in range(1, EPOCHS + 1):
#     model.train()
#     running_loss = correct = total = 0

#     for imgs, labels in tqdm(train_loader, desc=f"Epoch {epoch}/{EPOCHS}", leave=False):
#         imgs, labels = imgs.to(device), labels.to(device)

#         optimizer.zero_grad()
#         outputs = model(imgs)
#         loss    = criterion(outputs, labels)
#         loss.backward()

#         # Gradient clipping = training stability
#         torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

#         optimizer.step()

#         running_loss += loss.item()
#         _, pred = torch.max(outputs, 1)
#         correct += (pred == labels).sum().item()
#         total   += labels.size(0)

#     train_acc = 100 * correct / total
#     val_loss, val_acc, val_auc = evaluate(val_loader)
#     current_lr = optimizer.param_groups[0]["lr"]
#     scheduler.step()

#     marker = ""
#     if val_auc > best_val_auc:       # save best by AUC not accuracy
#         best_val_auc = val_auc
#         torch.save(model.state_dict(), "saved_model/best_model.pth")
#         no_improve = 0
#         marker = "  <- best"
#     else:
#         no_improve += 1

#     print(f"{epoch:<7} {running_loss:>9.4f} {train_acc:>7.2f}% {val_loss:>9.4f} {val_acc:>7.2f}% {val_auc:>8.4f}  {current_lr:>10.2e}{marker}")

#     if no_improve >= PATIENCE:
#         print(f"\nEarly stopping at epoch {epoch}. Best val AUC: {best_val_auc:.4f}")
#         break

# # ---------------------------
# # TEST EVALUATION
# # ---------------------------
# print("\nLoading best model for test evaluation...")
# model.load_state_dict(torch.load("saved_model/best_model.pth", map_location=device))
# test_loss, test_acc, test_auc = evaluate(test_loader)

# print("\n" + "=" * 40)
# print(f"  Test Accuracy : {test_acc:.2f}%")
# print(f"  Test ROC-AUC  : {test_auc:.4f}")
# print("=" * 40)

# # ---------------------------
# # SAVE FINAL MODEL
# # ---------------------------
# torch.save(model.state_dict(), "saved_model/final_model.pth")
# print("Final model saved -> saved_model/final_model.pth")