import os
import sys
import random
import numpy as np
import inference_single

COARSE_LABELS = [
    "symmetricloop",
    "bulge",
    "hairpin",
    "asymmetricloop",
    "unknown"
]

LABEL_TO_IDX = {l: i for i, l in enumerate(COARSE_LABELS)}
IDX_TO_LABEL = {i: l for l, i in LABEL_TO_IDX.items()}
NUM_CLASSES = len(COARSE_LABELS)


def extract_true_motif(filepath):
    name = os.path.basename(filepath)
    parts = name.split("_")
    if len(parts) < 3:
        return None

    fine = parts[2].lower()

    if fine in ["1x1", "2x2", "3x3", "4x4", "5x5"]:
        return "symmetricloop"
    if fine in ["1x3", "1x2", "1x4", "1x5",
                "2x3", "2x4", "2x5",
                "3x4", "3x5", "4x5"]:
        return "asymmetricloop"
    if fine in ["hairpin3", "hairpin4", "hairpin5", "hairpin6", "hairpin7"]:
        return "hairpin"
    if fine in ["bulge1", "bulge2", "bulge3", "bulge4", "bulge5"]:
        return "bulge"

    return "unknown"


def confusion_matrix(y_true, y_pred, num_classes):
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1
    return cm


def sensitivity_specificity(cm):
    metrics = {}

    for i, label in enumerate(COARSE_LABELS):
        TP = cm[i, i]
        FN = cm[i, :].sum() - TP
        FP = cm[:, i].sum() - TP
        TN = cm.sum() - (TP + FN + FP)

        sensitivity = TP / (TP + FN + 1e-8)
        specificity = TN / (TN + FP + 1e-8)

        metrics[label] = {
            "sensitivity": sensitivity,
            "specificity": specificity
        }

    return metrics

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_folder.py <folder_path> <checkpoint.pth>")
        sys.exit(1)

    folder_path = sys.argv[1]
    checkpoint_path = sys.argv[2]

    MAX_PER_CLASS = 90
    all_files = []

    for label in COARSE_LABELS:
        class_dir = os.path.join(folder_path, label)

        if not os.path.isdir(class_dir):
            print(f"Warning: missing folder {class_dir}")
            continue

        class_files = [
            os.path.join(class_dir, f)
            for f in os.listdir(class_dir)
            if f.lower().endswith(".mrc")
        ]

        if len(class_files) == 0:
            print(f"Warning: no .mrc files in {class_dir}")
            continue

        random.shuffle(class_files)
        class_files = class_files[:MAX_PER_CLASS]

        all_files.extend(
            [(path, label) for path in class_files]
        )

        print(f"{label:15s}: using {len(class_files)} files")

    if len(all_files) == 0:
        print("No .mrc files found in class folders.")
        sys.exit(1)

    random.shuffle(all_files)
    eval_files = all_files

    print(f"Evaluating {len(eval_files)} files...\n")

    model = inference_single.load_model(checkpoint_path)

    y_true = []
    y_pred = []

    for path, true_label in eval_files:
        try:
            vol = inference_single.load_mrc_as_numpy(path)
            pred_label, _ = inference_single.classify_vol(vol, model)

            y_true.append(LABEL_TO_IDX[true_label])
            y_pred.append(LABEL_TO_IDX[pred_label])

            print(os.path.basename(path))
            print(f"  True: {true_label}")
            print(f"  Pred: {pred_label}")
            print(f"  Match: {true_label == pred_label}\n")

        except Exception as e:
            print(f"Error processing {path}: {e}\n")

    cm = confusion_matrix(y_true, y_pred, NUM_CLASSES)

    print("\nConfusion Matrix")
    print("Rows = True, Cols = Pred")
    print("Labels:", COARSE_LABELS)
    print(cm)

    metrics = sensitivity_specificity(cm)

    print("\nPer-class Sensitivity & Specificity:")
    for label, m in metrics.items():
        print(f"{label:15s} "
              f"Sensitivity: {m['sensitivity']:.3f} "
              f"Specificity: {m['specificity']:.3f}")

    macro_sens = np.mean([m["sensitivity"] for m in metrics.values()])
    macro_spec = np.mean([m["specificity"] for m in metrics.values()])

    print(f"\nMacro Sensitivity: {macro_sens:.3f}")
    print(f"Macro Specificity: {macro_spec:.3f}")