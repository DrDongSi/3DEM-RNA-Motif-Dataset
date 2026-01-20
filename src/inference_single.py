import torch
import numpy as np
import mrcfile
import sys
import os
import train
import resample_mrc

COARSE_LABELS = [
    "symmetricloop",
    "bulge",
    "hairpin",
    "asymmetricloop",
    "unknown"
]
NUM_CLASSES = len(COARSE_LABELS)

def safe_load_mrc(path):
    try:
        with mrcfile.open(path, permissive=True) as m:
            vol = m.data
            if vol is not None and vol.size > 0:
                return vol.astype(np.float32)
    except Exception:
        pass

    from mrcfile.mrcmemmap import MrcMemmap

    with MrcMemmap(path, permissive=True, header_only=False) as m:
        vol = m.data
        if vol is None or vol.size == 0:
            raise ValueError(f"Could not read volume data from {path}")
        return vol.astype(np.float32)

    

def center_crop_64(vol):
    c = np.array(vol.shape) // 2
    size = 64
    half = size // 2
    vol = np.pad(vol, size, mode="constant")
    c += size
    return vol[c[0]-half:c[0]+half,
               c[1]-half:c[1]+half,
               c[2]-half:c[2]+half]


def load_model(checkpoint_path):
    model = train.Motif3DCNN(num_classes=NUM_CLASSES)

    # build model weights
    dummy = torch.zeros(1, 1, 64, 64, 64)
    model(dummy)

    state = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    return model

def load_mrc_as_numpy(path):
    tmp_out = "/tmp/infer_tmp.mrc"
    vol = resample_mrc.resample_mrc(
        0, path, tmp_out, resample_mrc.TARGET_VOXEL
    )

    mean = vol.mean()
    std = vol.std()
    vol = (vol - mean) / (std + 1e-6)

    vol = center_crop_64(vol)
    return vol




def classify_vol(vol_np, model):
    t = torch.from_numpy(vol_np).unsqueeze(0).unsqueeze(0)  # 1×1×64×64×64
    with torch.no_grad():
        logits = model(t)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
        idx = int(np.argmax(probs))

    return COARSE_LABELS[idx], probs


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python inference.py <patch.mrc> <checkpoint.pth>")
        sys.exit(1)

    patch_path = sys.argv[1]
    checkpoint_path = sys.argv[2]

    vol = load_mrc_as_numpy(patch_path)

    model = load_model(checkpoint_path)

    label, probs = classify_vol(vol, model)
    print("Prediction:", label)
    print("Probabilities:", probs)
