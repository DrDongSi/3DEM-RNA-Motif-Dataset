import os
import glob
import random
import numpy as np
import mrcfile
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import resample_mrc
import sys
import pandas as pd
import traceback

SYMMETRIC = {"1x1", "2x2", "3x3", "4x4", "5x5"}
BULGES = {"bulge1", "bulge2", "bulge3", "bulge4", "bulge5"}
HAIRPINS = {"hairpin3", "hairpin4", "hairpin5", "hairpin6", "hairpin7"}
ASYMMETRIC = {
    "1x2","1x3","1x4","1x5",
    "2x3","2x4","2x5",
    "3x4","3x5",
    "4x5"
}
UNKNOWN = {"unknown"}

CSV_LABEL_TO_CLASS = {
    "symmetricloop": 0,
    "bulge": 1,
    "hairpin": 2,
    "asymmetricloop": 3,
    "unknown": 4
}

def group_of_motif(motif):
    if motif in SYMMETRIC: return 0
    if motif in BULGES: return 1
    if motif in HAIRPINS: return 2
    if motif in ASYMMETRIC: return 3
    if motif in UNKNOWN: return 4
    raise ValueError(f"Unknown motif: {motif}")


motifs = [
    "1x1","2x2","3x3","4x4","5x5",
    "bulge1","bulge2","bulge3","bulge4","bulge5",
    "hairpin3","hairpin4","hairpin5","hairpin6","hairpin7",
    "1x2","1x3","1x4","1x5",
    "2x3","2x4","2x5",
    "3x4","3x5",
    "4x5",
    "unknown"
]


def pad_to_same_box(a, b):
    assert a.ndim == 3 and b.ndim == 3
    target = (max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1]), max(a.shape[2], b.shape[2]))
    def pad_to_target(x, target):
        padz = target[0] - x.shape[0]; pady = target[1] - x.shape[1]; padx = target[2] - x.shape[2]
        pad = ((padz//2, padz - padz//2), (pady//2, pady - pady//2), (padx//2, padx - padx//2))
        return np.pad(x, pad, mode='constant', constant_values=0)
    return pad_to_target(a, target), pad_to_target(b, target)


class CryoVoxelMotifDataset(Dataset):
    def __init__(self, csv_file, use_labeled_maps=False):
        self.df = pd.read_csv(csv_file)
        self.use_labeled_maps = use_labeled_maps

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        density_path = row["filepath"]
        try:
            label_name = row["label"].lower()
            outputPath = f"./norm/{density_path.split('/')[4]}_Norm.mrc"
            # print(f"Executing training {density_path}")
            class_id = CSV_LABEL_TO_CLASS[label_name]
            is_unknown = (label_name == "unknown")

            label_path = None
            if self.use_labeled_maps and not is_unknown:
                # expected convention: backbone_label.mrc next to density
                label_path = density_path.replace(
                    "densityMap", "labelMap"
                ).replace(".mrc", "/backbone_label.mrc")

                if not os.path.isfile(label_path):
                    print(f"[WARN] Missing label map: {label_path}")
                    label_path = None

            density_resampled = resample_mrc.resample_mrc(
                0, density_path, outputPath, resample_mrc.TARGET_VOXEL
            )

            use_labels = self.use_labeled_maps and (not is_unknown)
            if use_labels:
                label_path = density_path.replace(
                    "densityMap", "labelMap"
                ).replace(".mrc", "/backbone_label.mrc")

                if not os.path.isfile(label_path):
                    use_labels = False

            if use_labels:
                label_resampled = resample_mrc.resample_mrc(
                    0, label_path, "tmp_lab.mrc", resample_mrc.TARGET_VOXEL
                )

                label_resampled, density_resampled = pad_to_same_box(
                    label_resampled, density_resampled
                )

                coords = np.argwhere(label_resampled > 0)

                if len(coords) == 0:
                    use_labels = False
                else:
                    cx, cy, cz = coords[random.randint(0, len(coords)-1)]
                    final = np.where(label_resampled > 0, density_resampled, 0)

            if not use_labels:
                final = (density_resampled - density_resampled.mean()) / (
                    density_resampled.std() + 1e-6
                )
                cx, cy, cz = np.array(final.shape) // 2
                patch = self.extract_patch(final, cx, cy, cz, 64)

                patch = torch.tensor(patch, dtype=torch.float32).unsqueeze(0)
                return patch, torch.tensor(class_id, dtype=torch.long)

        except Exception as e:
            traceback.print_exc()
            print(f"Dataset {density_path}")
            print("Dataset error:", e)
            return None

    def extract_patch(self, volume, cx, cy, cz, size):
        half = size // 2
        vol = np.pad(volume, size, mode="constant")
        cx += size; cy += size; cz += size
        return vol[cx-half:cx+half, cy-half:cy+half, cz-half:cz+half]

def train_motif_classifier(train_csv,validation_csv,destination_dir):
    USE_LABELED_MAPS = False

    train_ds = CryoVoxelMotifDataset(
        csv_file=train_csv,
        use_labeled_maps=USE_LABELED_MAPS
    )

    val_ds = CryoVoxelMotifDataset(
        csv_file=validation_csv,
        use_labeled_maps=USE_LABELED_MAPS
    )

    train_loader = DataLoader(
        train_ds,
        batch_size=4,
        shuffle=True,
        num_workers=2,
        pin_memory=True,
        collate_fn=collate_skip_none
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=4,
        shuffle=False,
        num_workers=2,
        pin_memory=True,
        collate_fn=collate_skip_none
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Motif3DCNN(num_classes=5).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(1, 30):
        model.train()
        train_loss = 0.0

        for batch in train_loader:
            if batch is None:
                continue

            patches, labels = batch
            patches, labels = patches.to(device), labels.to(device)

            preds = model(patches)
            loss = loss_fn(preds, labels)

            opt.zero_grad()
            loss.backward()
            opt.step()

            train_loss += loss.item()

        model.eval()
        correct = total = 0
        with torch.no_grad():
            for batch in val_loader:
                if batch is None:
                    continue
                patches, labels = batch
                patches, labels = patches.to(device), labels.to(device)

                preds = model(patches)
                correct += (preds.argmax(1) == labels).sum().item()
                total += labels.size(0)

        acc = correct / total if total else 0
        print(f"Epoch {epoch} | TrainLoss {train_loss:.4f} | ValAcc {acc:.4f}")

        torch.save(model.state_dict(), f"./{destination_dir}/label_less_classifier_epoch{epoch}.pth")

class Motif3DCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv3d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool3d(2),
            nn.Conv3d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool3d(2),
            nn.Conv3d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool3d(2),
        )
        flatten_dim = 64 * 8 * 8 * 8
        self.classifier = nn.Sequential(
            nn.Linear(flatten_dim, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.reshape(x.size(0), -1)
        return self.classifier(x)
def collate_skip_none(batch):
    batch = [b for b in batch if b is not None]
    if len(batch) == 0:
        return None  # entire batch is bad
    patches, labels = zip(*batch)
    return torch.stack(patches), torch.tensor(labels)

# def train_motif_classifier():
#     root = "./train"
#     val = "./validation"

#     train_ds = CryoVoxelMotifDataset(root, motifs)
#     val_ds   = CryoVoxelMotifDataset(val, motifs)

#     train_loader = DataLoader(train_ds, batch_size=4, shuffle=True, num_workers=2, pin_memory=True,collate_fn=collate_skip_none)
#     val_loader   = DataLoader(val_ds,   batch_size=4, shuffle=False, num_workers=2, pin_memory=True,collate_fn=collate_skip_none)

#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model = Motif3DCNN(num_classes=5).to(device)
#     opt = torch.optim.Adam(model.parameters(), lr=1e-3)
#     loss_fn = nn.CrossEntropyLoss()

#     for epoch in range(1,30):
#         model.train()
#         train_loss = 0.0
#         for batch in train_loader:
#             if batch is None:
#                 continue
#             patches, labels = batch
#             patches = patches.to(device)
#             labels = labels.to(device)

#             preds = model(patches)
#             loss = loss_fn(preds, labels)

#             opt.zero_grad()
#             loss.backward()
#             opt.step()

#             train_loss += loss.item()

#         model.eval()
#         val_loss = 0.0; correct = 0; total = 0
#         with torch.no_grad():
#             for patches, labels in val_loader:
#                 patches = patches.to(device)
#                 labels = labels.to(device)
#                 preds = model(patches)
#                 val_loss += loss_fn(preds, labels).item()
#                 correct += (preds.argmax(1) == labels).sum().item()
#                 total += labels.size(0)

#         acc = correct / total if total>0 else 0.0
#         print(f"Epoch {epoch}: TrainLoss={train_loss:.4f}, ValLoss={val_loss:.4f}, ValAcc={acc:.4f}")

#         save_path = f"coarse_classifier_epoch{epoch}.pth"
#         torch.save(model.state_dict(), save_path)
#         print("Saved", save_path)

if __name__ == "__main__":
    train_csv=sys.argv[1]
    val_csv = sys.argv[2]
    destination_dir = sys.argv[3]
    train_motif_classifier(train_csv,val_csv,destination_dir)
