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
