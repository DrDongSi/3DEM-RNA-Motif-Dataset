# Cryo-EM and Secondary Structure Segmentation & Labelling (CLI Tool)

This repository provides a **command-line workflow** for downloading cryo-EM density maps and atomic structures from the RCSB PDB and **segmenting density maps around specific RNA residues** using **UCSF ChimeraX**.

It is designed to be run **inside ChimeraX’s Python environment** (not system Python).

---

## Repository

Clone the dataset and scripts:

```bash
git clone https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset
```

```
cd 3DEM-RNA-Motif-Dataset
```

---

## Dependencies

### Required Tools

- **UCSF ChimeraX (v1.9 or higher)**  
  Download: https://www.cgl.ucsf.edu/chimerax/download.html

- **Phenix**  
  Installation instructions and source available from the official Phenix site.

- **mrcfile (inside ChimeraX)**  
  Even if installed via `pip`, ChimeraX will **not** see it. Install it via ChimeraX toolshed:

```bash
/Applications/ChimeraX-1.9.app/Contents/bin/ChimeraX   --nogui --cmd "toolshed install https://pypi.org/project/mrcfile/; exit"
```

> **Note:** Installing `mrcfile` through system Python is insufficient. It must be installed inside ChimeraX.

---

## Installing UCSF ChimeraX

1. Visit: https://www.cgl.ucsf.edu/chimerax/download.html  
2. Download the installer for your OS (Windows / macOS / Linux)
3. Follow platform-specific installation steps
4. Verify installation:
```bash
chimerax --nogui
```

---

## Project Structure

```text
src/
│── segment.py          # Core reusable segmentation functions
│── test_segment.py     # Demo / driver script
│── config.json         # RCSB API configuration
```

---

## segment.py Overview

This file defines **three key functions**:

### fetch_emdb_map(session, pdb_id)
- Downloads the cryo-EM density map corresponding to a PDB ID
- Returns the local path to the `.map` file

### fetch_pdb_file(session, pdb_id)
- Downloads the atomic structure for the given PDB ID
- Returns the local path to the PDB/CIF file

### segment_map(session, pdb_file_path, emdb_file_path, chain_id, residue_ranges)
- Loads the PDB and EMDB map into ChimeraX
- Selects residues from the specified chain and residue ranges
- Segments the cryo-EM density around the selection
- Saves:
  - Segmented density map (`.mrc`)
  - Segmented atomic model (`.pdb`)

**Important Note**  
The segmented map filename is currently **hardcoded** (e.g., `outputMaps/segmentedMap.mrc`).  
Running the script multiple times will overwrite previous outputs unless renamed or modified.

---

## config.json

The scripts optionally read the RCSB API base URL from `config.json`.

Create the file in the same directory as the scripts:

```json
{
  "rcsb_api_base_url": "https://data.rcsb.org/rest/v1/core/entry"
}
```

If this file is missing, the script will fall back to the default URL defined in the code.

---

## Demo Script: test_segment.py

This script demonstrates the full workflow by calling the three functions in sequence.

Key parameters:

```python
pdb_id = "6VXX"
chain_id = "A"
residue_ranges = [(50, 60), (150, 160)]
```

To test other structures:
- Change **only** these three parameters
- No other code modifications are required

---

## How to Run

These scripts must be executed inside **ChimeraX’s Python runtime**.

```bash
cd my_project
chimerax --nogui --script test_segment.py
```

This will:
1. Download the EMDB cryo-EM density map  
2. Download the PDB atomic structure  
3. Segment the density map around the specified chain and residues  
4. Save the segmented outputs to disk  

---

## Output Files

### Default Locations

- **Downloaded PDB files**  
  ```text
  ~/Downloads/ChimeraX/PDB/
  ```

- **Downloaded EMDB maps**  
  ```text
  ~/Downloads/ChimeraX/EMDB/
  ```

- **Segmented density map**
  ```text
  outputMaps/segmentedMap.mrc
  ```

- **Segmented atomic model**
  ```text
  outputPDBs/segmented.pdb
  ```

Filenames are fixed by default. Modify `segment_map()` to generate unique names if needed.

---

## Cleanup

To prevent your `Downloads` directory from filling up:

- `segment.py` includes a `cleanupfiles(pdb_id, emdb_id)` function
- You can adapt or enable it to remove downloaded PDB and EMDB files after segmentation

---

## Summary

This tool enables **automated cryo-EM map segmentation around RNA motifs** by:
- Fetching structures directly from the RCSB PDB
- Running entirely inside ChimeraX
- Producing segmented `.mrc` and `.pdb` files suitable for downstream ML or structural analysis

Some sample segmented motifs of 
![3DEM-RNA-Motif-Dataset = 250x250](sample/images/Asymmetric%20Loop%20Segments%202.png)

And some sample segmented motifs and their atomic models, labeled maps

# RNA Motif Classification

This repository provides scripts for training and evaluating a coarse-grained
RNA 3D motif classifier using cryo-EM density maps.

## Usage

Two main workflows are supported:

1. Training a coarse-grained RNA motif classifier
2. Validating a trained classifier on a folder of `.mrc` files


## 1. Training the Motif Classifier

This script trains a **5-class coarse motif classifier** with the following labels:

- `symmetricloop`
- `bulge`
- `hairpin`
- `asymmetricloop`
- `unknown`

### Input Requirements

Training and validation data must be provided as CSV files with at least the
following columns:

| Column     | Description |
|------------|-------------|
| `filepath` | Path to the input `.mrc` density map |
| `label`    | Coarse motif label |

### Command

```bash
python train_motif_classifier.py <train.csv> <validation.csv> <output_dir>
```

### Example

```bash
python train_motif_classifier.py data/train.csv data/val.csv checkpoints/
```

### Output

- Model checkpoints are written to `<output_dir>` after every epoch:
  ```
  label_less_classifier_epoch1.pth
  label_less_classifier_epoch2.pth
  ...
  ```
- Training runs for 30 epochs by default.
- GPU is used automatically if available.


## 2. Folder-Level Validation

This script evaluates a trained model on `.mrc` files organized by ground-truth
class folders.

### Required Folder Structure

```text
evaluation_data/
├── symmetricloop/
├── bulge/
├── hairpin/
├── asymmetricloop/
└── unknown/
```

Each subfolder should contain `.mrc` files belonging to that class.
A maximum of **90 files per class** are randomly sampled.

### Command

```bash
python validate_folder.py <evaluation_folder> <checkpoint.pth>
```

### Example

```bash
python validate_folder.py evaluation_data/ checkpoints/label_less_classifier_epoch30.pth
```

### Output

- Per-file predictions (true label vs predicted label)
- Confusion matrix (rows = true, columns = predicted)
- Per-class sensitivity and specificity
- Macro-averaged sensitivity and specificity

## Notes

- `.mrc` files are automatically resampled and normalized.
- Labeled voxel maps are currently disabled by default.
- Ensure the following modules are available in your Python path:
  - `resample_mrc.py`
  - `inference_single.py`

