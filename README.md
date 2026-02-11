<!-- ===================== Header ===================== -->

<p align="center">
  <img src="https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/blob/chandramathi/images/Logo.png" alt="DAIS Research Lab" width="720">
</p>

<!-- Note: The above is official Seed information. -->

<p align="center">
  AI for Science and Structural Biology
</p>

<p align="center">
  Large Scale cryo-EM RNA-Motif Dataset and Benchmark for Machine Learning and Structure Modeling
</p>

<h1 align="center">
  Cryo-EM Dataset of RNA-Motif and Open Sourced Tool for cryo-EM Motif Segmentation and Validation
</h1>

<!-- <p align="center">
  <a href="https://bytedance-seed.github.io/cryofm/">
    <img src="https://img.shields.io/badge/Website-cryofm-3b82f6?style=flat&logo=googlechrome&labelColor=111827" alt="Website" draggable="false">
  </a>
  <a href="https://bytedance-seed.github.io/cryofm/docs">
    <img src="https://img.shields.io/badge/Docs-Guide-2e3440?style=flat&logo=readthedocs&labelColor=111827" alt="Docs" draggable="false">
  </a>
  <a href="https://github.com/ByteDance-Seed/cryofm/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-Apache--2.0-64748b?style=flat&logo=apache&labelColor=111827" alt="License" draggable="false">
  </a>
</p> -->

<!-- =================================================== -->


We introduce, a pipeline for cryo-electron microscopy (cryo-EM) density maps and structure map segmentation of known structural motif occurences in an RNA and a benchmarked dataset for classification tasks. RNA plays essential roles in gene regulation, viral replication, and cellular function, where its three-dimensional (3D) structure is tightly coupled to biological activity. Unlike proteins, RNA exhibits high conformational flexibility, folding into complex 3D architectures through base pairing and long-range interactions. These structures are composed of recurring elements such as helices, hairpins, bulges, internal loops, and junctions. Such recurring elements, known as RNA structural motifs, form conserved building blocks of RNA tertiary structure. This repository provides a computational pipeline for RNA motif segmentation from cryo-EM density maps. The segmented regions are further used for motif-level classification based on local structural and density features. The framework enables standardized motif extraction across diverse RNA molecules and resolutions. It supports reproducible analysis and scalable dataset generation for downstream learning tasks. The method is designed to integrate structural data with machine-learning-based classification. Confusion-matrix–based benchmarking results are provided to evaluate classification performance. 

## Resources

| **Category**                      | **Description**                                                                 |             **Link** |
|-------------------------------|-----------------------------------------------------------------------------|-----------------------|
| Classification Model Weights  | Pretrained weights for the classification models used in experiments.      |  <a href="https://zenodo.org/uploads/18409492"><img src="" draggable="false">Zenodo Dataset</a> |
| Classification Fold Dataset  | Dataset organized into folds for training, validation, and testing.        |[Zenodo Dataset](https://zenodo.org/records/18409492) |
| Motif Dataset                | Dataset containing motif-level samples used for pattern or feature analysis. | |
| Benchmark Results            | Benchmark results for classification of RNA Motifs | [Results](https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/main/README.md#benchmark)| 


## Getting started (For end users)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset
cd 3DEM-RNA-Motif-Dataset
```

#### 2. Install Required Software

**UCSF ChimeraX (v1.9 or higher)**

1. Download from: https://www.cgl.ucsf.edu/chimerax/download.html
2. Run the installer for your operating system
3. **Windows:** During installation, ensure ChimeraX is added to your system PATH, or manually add `C:\Program Files\ChimeraX <version>\bin` to your PATH environment variable

**Phenix (for Q-Score and Z-Score computation)**

1. Download from: https://phenix-online.org/download/
2. Run the installer for your operating system
3. Add Phenix to your system PATH:
   - **Windows:** Add `C:\Users\<YourUsername>\phenix-<version>\phenix_bin` to system PATH via Environment Variables
   - **macOS:** Add `export PATH="/Applications/phenix-<version>/build/bin:$PATH"` to `~/.zshrc`
   - **Linux:** Add `export PATH="/opt/phenix/phenix-<version>/build/bin:$PATH"` to `~/.bashrc`
4. Restart your terminal

#### 3. Install mrcfile in ChimeraX

Run the following command to install `mrcfile` inside ChimeraX's Python environment:

**macOS:**

```bash
/Applications/ChimeraX-1.9.app/Contents/bin/ChimeraX --nogui --cmd "toolshed install https://pypi.org/project/mrcfile/; exit"
```

**Windows (PowerShell):**

```powershell
ChimeraX --nogui --cmd "toolshed install https://pypi.org/project/mrcfile/; exit"
```

**Linux:**

```bash
chimerax --nogui --cmd "toolshed install https://pypi.org/project/mrcfile/; exit"
```

> **Note:** `mrcfile` must be installed inside ChimeraX's Python environment, not system Python.

#### 4. Verify Installation

Test that all tools are properly installed:

**macOS/Linux:**

```bash
chimerax --nogui
phenix.mtriage --version
```

**Windows (PowerShell):**

```powershell
ChimeraX --nogui
phenix.mtriage --version
```

---

## Usage

### Segmentation

Segmentation aligns atomic RNA structures to their corresponding cryo-EM density maps, extracts local density around user-specified residue ranges, and crops the result into compact subvolumes for analysis and classification.

The occurrence information for motifs in this dataset is obtained from [CossMosDB](https://drive.google.com/drive/folders/1hHA16pI2Vi6p6EgbGSfCZ9rksYzvBifN?usp=sharing). A [Jupyter notebook](https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/blob/chandramathi/src/process_cossmos.ipynb) is provided for fetching motif sequence information.

<p align="center">
  <img src="https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/blob/chandramathi/Segmentation.png" alt="RNA Motif Segmentation" width="720">
</p>

#### Architecture

PDB structures and density maps are loaded into ChimeraX via public REST APIs. Cryo-EM density data (MRC/map formats) are processed to generate and label 25 motif types. Density maps are fitted to RNA 3D structures, and voxels within 5 Å of selected RNA chain regions are segmented as regions of interest.

<p align="center">
  <img src="https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/blob/chandramathi/images/Architecture%20diagram.png" alt="RNA Motif Architecture" width="720">
</p>

---

## Project Structure

```text
src/
│── segment.py          # Core reusable segmentation functions
│── test_segment.py     # Demo / driver script
configurations/
│── config.json         # RCSB API configuration
```

---

### Segmentation Command Line Tool

> **Windows PowerShell Note:** To see console output in PowerShell, add `2>&1 | Out-Host` to the end of ChimeraX commands.

**Syntax**

```bash
chimerax --nogui --cmd "runscript segment.py <pdb_id> [emdb_id] <chain:start-end[,start-end]> ..."
```

> **Note:** Execute commands from within the `src` directory.

**Examples**

Segment a hairpin at positions 1896-1903 in Chain A of PDB ID 8QCQ:

**macOS/Linux:**

```bash
cd src
chimerax --nogui --cmd "runscript segment.py 8QCQ A:1896-1903"
```

**Windows (PowerShell):**

```powershell
cd src
ChimeraX --nogui --cmd "runscript segment.py 8QCQ A:1896-1903" 2>&1 | Out-Host
```

Segment a symmetric loop at positions 1490-1495,1424-1429 in Chain A of PDB ID 8QCQ:

**macOS/Linux:**

```bash
chimerax --nogui --cmd "runscript segment.py 8QCQ A:1490-1495,1424-1429"
```

**Windows (PowerShell):**

```powershell
ChimeraX --nogui --cmd "runscript segment.py 8QCQ A:1490-1495,1424-1429" 2>&1 | Out-Host
```

**Output**

Segmented files are saved to `outputMaps/` and `outputPDBs/` directories (created automatically). Q-Score and CCmask results are printed to console, and `mask.ccp4` is written to the current directory.

---

### Labeling

Labeling projects atomic model information into 3D voxel space of cryo-EM maps. Atomic coordinates are converted to voxel indices and assigned labels within a defined radius. The result is a labeled MRC file with voxel-level annotations for motif recognition and deep learning training.

<p align="center">
  <img src="https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/blob/chandramathi/images/LabelFlow.png" alt="RNA Labeling Illustration" width="720">
</p>

**Usage**

**macOS/Linux:**

```bash
cd src
python3 label.py <input.mrc> <input.pdb>
```

**Windows:**

```powershell
cd src
python label.py <input.mrc> <input.pdb>
```

**Example**

```bash
python3 label.py ./outputMaps/segmentedMap.mrc ./outputPDBs/segmentedPDB.pdb
```

**Output**

Three labeled MRC files are created:
- `backbone_label_segmentedMap.mrc`
- `ribose_label_segmentedMap.mrc`
- `sugar_label_segmentedMap.mrc`

Sample outputs are available [here](https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/tree/chandramathi/sample).

---

## Classification

A 3D CNN deep learning model (Motif3DCNN) classifies RNA motifs into 5 classes: symmetric_loop, bulge, hairpin, asymmetric_loop, and unknown. The model uses cryo-EM density maps and is trained with cross-entropy loss and Adam optimizer.

### Training

The classification model uses segmented motif maps of 2.8 Å resolution or higher. The dataset is organized into 5 folds with approximately 1800 training samples and 450 validation samples (80-20 split) per fold. Training runs for 30 epochs by default.

**Usage**

```bash
cd src
python3 train.py <training_csv> <validation_csv> <output_directory>
```

**Parameters:**
- `training_csv` - CSV file listing training density files
- `validation_csv` - CSV file listing validation density files
- `output_directory` - Directory to save trained model weights

Training/validation CSV files: [trainingCSVs/](https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/tree/main/src/trainingCSVs)  
Training dataset: [Zenodo](https://zenodo.org/records/18396353)

**Example:**

```bash
python3 train.py ./trainingCSVs/fold1_train.csv ./trainingCSVs/fold1_val.csv SET1
```

**Output:** Model weights saved as `.pth` files in the specified directory.

---

### Testing

Test trained models using the `validate_folder.py` utility.

**Usage**

```bash
cd src
python3 validate_folder.py <test_directory> <model_weights>
```

**Parameters:**
- `test_directory` - Directory containing test MRC files (must follow naming convention: `<emdb_id>_<pdb_id>_<motif_type>_<sequenceNumber>.mrc`)
- `model_weights` - Path to trained model `.pth` file

Pretrained models: [Zenodo](https://zenodo.org/records/18409492)

**Example:**

```bash
python3 validate_folder.py ./testSET/ ./models/fold5Model.pth
```

**Output:** Confusion matrix, specificity, and selectivity scores.

---

### Classification Benchmark 

<table>
  <tr>
    <!-- <th>Sl.No</th> -->
    <th>Fold</th>
    <th>Training Set</th>
    <th>Validation Set</th>
    <th>Model</th>
    <th>Confusion Matrix (sym, bul, hp, asymm, unk)</th>
    <th style="background-color:#d4f8d4;">Macro Sensitivity</th>
    <th style="background-color:#d4f8d4;">Macro Specificity</th>
  </tr>

  <!-- Fold 1 -->
  <tr>
    <!-- <td>1</td> -->
    <td>Fold 1</td>
    <td>SET1, SET2, SET3, SET4</td>
    <td>SET5</td>
    <td>fold1Model.pth</td>
    <td>
      <table border="1">
        <tr><th>True\Pred</th><th>sym</th><th>bul</th><th>hp</th><th>asymm</th><th>unk</th></tr>
        <tr><td>sym</td><td style="background:#b6fcb6;">🟢 <b>7</b></td><td>1</td><td>3</td><td>12</td><td>0</td></tr>
        <tr><td>bul</td><td>0</td><td style="background:#b6fcb6;">🟢 <b>80</td><td>10</td><td>0</td><td>0</td></tr>
        <tr><td>hp</td><td>5</td><td>9</td><td style="background:#b6fcb6;">🟢 <b>71</td><td>5</td><td>0</td></tr>
        <tr><td>asymm</td><td>15</td><td>1</td><td>4</td><td style="background:#b6fcb6;">🟢 <b>69</td><td>0</td></tr>
        <tr><td>unk</td><td>0</td><td>0</td><td>0</td><td>0</td><td style="background:#b6fcb6;">🟢 <b>79</td></tr>
      </table>
    </td>
    <td style="background-color:#d4f8d4;">0.855</td>
    <td style="background-color:#d4f8d4;">0.963</td>
  </tr>

  <!-- Fold 2 -->
  <tr>
    <!-- <td>2</td> -->
    <td>Fold 2</td>
    <td>SET1, SET2, SET3, SET5</td>
    <td>SET4</td>
    <td>fold2Model.pth</td>
    <td>
      <table border="1">
        <tr><th>True\Pred</th><th>sym</th><th>bul</th><th>hp</th><th>asymm</th><th>unk</th></tr>
        <tr><td>sym</td><td style="background:#b6fcb6;">🟢 <b>70</td><td>0</td><td>4</td><td>16</td><td>0</td></tr>
        <tr><td>bul</td><td>1</td><td style="background:#b6fcb6;">🟢 <b>75</td><td>14</td><td>0</td><td>0</td></tr>
        <tr><td>hp</td><td>5</td><td>10</td><td style="background:#b6fcb6;">🟢 <b>70</td><td>5</td><td>0</td></tr>
        <tr><td>asymm</td><td>20</td><td>1</td><td>7</td><td style="background:#b6fcb6;">🟢 <b>61</td><td>0</td></tr>
        <tr><td>unk</td><td>0</td><td>0</td><td>0</td><td>1</td><td style="background:#b6fcb6;">🟢 <b>78</td></tr>
      </table>
    </td>
    <td style="background-color:#d4f8d4;">0.812</td>
    <td style="background-color:#d4f8d4;">0.952</td>
  </tr>

  <!-- Fold 3 -->
  <tr>
    <!-- <td>3</td> -->
    <td>Fold 3</td>
    <td>SET1, SET2, SET4, SET5</td>
    <td>SET3</td>
    <td>fold3Model.pth</td>
    <td>
      <table border="1">
        <tr><th>True\Pred</th><th>sym</th><th>bul</th><th>hp</th><th>asymm</th><th>unk</th></tr>
        <tr><td>sym</td><td style="background:#b6fcb6;">🟢 <b>72</td><td>1</td><td>1</td><td>16</td><td>0</td></tr>
        <tr><td>bul</td><td>1</td><td style="background:#b6fcb6;">🟢 <b>78</td><td>11</td><td>0</td><td>0</td></tr>
        <tr><td>hp</td><td>4</td><td>14</td><td style="background:#b6fcb6;">🟢 <b>62</td><td>10</td><td>0</td></tr>
        <tr><td>asymm</td><td>14</td><td>1</td><td>5</td><td style="background:#b6fcb6;">🟢 <b>69</td><td>0</td></tr>
        <tr><td>unk</td><td>0</td><td>0</td><td>0</td><td>0</td><td style="background:#b6fcb6;">🟢 <b>79</td></tr>
      </table>
    </td>
    <td style="background-color:#d4f8d4;">0.826</td>
    <td style="background-color:#d4f8d4;">0.955</td>
  </tr>

  <!-- Fold 4 -->
  <tr>
    <!-- <td>4</td> -->
    <td>Fold 4</td>
    <td>SET1, SET3, SET4, SET5</td>
    <td>SET2</td>
    <td>fold4Model.pth</td>
    <td>
      <table border="1">
        <tr><th>True\Pred</th><th>sym</th><th>bul</th><th>hp</th><th>asymm</th><th>unk</th></tr>
        <tr><td>sym</td><td style="background:#b6fcb6;">🟢 <b>71</td><td>0</td><td>5</td><td>14</td><td>0</td></tr>
        <tr><td>bul</td><td>1</td><td style="background:#b6fcb6;">🟢 <b>77</td><td>12</td><td>0</td><td>0</td></tr>
        <tr><td>hp</td><td>3</td><td>13</td><td style="background:#b6fcb6;">🟢 <b>66</td><td>8</td><td>0</td></tr>
        <tr><td>asymm</td><td>16</td><td>0</td><td>4</td><td style="background:#b6fcb6;">🟢 <b>69</td><td>0</td></tr>
        <tr><td>unk</td><td>0</td><td>0</td><td>1</td><td>0</td><td style="background:#b6fcb6;">🟢 <b>78</td></tr>
      </table>
    </td>
    <td style="background-color:#d4f8d4;">0.828</td>
    <td style="background-color:#d4f8d4;">0.956</td>
  </tr>

  <!-- Fold 5 -->
  <tr>
    <td>Fold 5</td>
    <td>SET2, SET3, SET4, SET5</td>
    <td>SET1</td>
    <td>fold3Model.pth</td>
    <td>
      <table border="1">
        <tr><th>True\Pred</th><th>sym</th><th>bul</th><th>hp</th><th>asymm</th><th>unk</th></tr>
        <tr><td>sym</td> <td>🟢 <b>71</td><td>1</td><td>2</td><td>16</td><td>0</td></tr>
        <tr><td>bul</td><td>0</td><td style="background:#b6fcb6;">🟢 <b>85</td><td>5</td><td>0</td><td>0</td></tr>
        <tr><td>hp</td><td>2</td><td>15</td><td style="background:#b6fcb6;">🟢 <b>67</td><td>6</td><td>0</td></tr>
        <tr><td>asymm</td><td>9</td><td>0</td><td>5</td><td style="background:#b6fcb6;">🟢 <b>75</td><td>0</td></tr>
        <tr><td>unk</td><td>0</td><td>2</td><td>0</td><td>1</td><td style="background:#b6fcb6;"> 🟢 <b>76</td></tr>
      </table>
    </td>
    <td style="background-color:#d4f8d4;">0.856</td>
    <td style="background-color:#d4f8d4;">0.963</td>
  </tr>
</table>


## About [DAIS Team](https://sites.google.com/uw.edu/dais-uw/home)

The DAIS (Data Analysis & Intelligent Systems) research group at the University of Washington, led by Dr. Dong Si, specializes in developing advanced AI and data science solutions for smart healthcare and next-generation biomedicine.

Their research portfolio includes high-impact projects like DeepTracer for 3D protein modeling from cryo-EM data and iCare, which utilizes conversational AI and natural language processing to support mental and behavioral health.

The group is also deeply committed to outreach and diversity, actively mentoring students from various backgrounds and working to encourage underrepresented minorities to pursue careers in STEM.
<div>
  Contributors
  <a href="Chandramathi Murugadass">
    <img src="[https://img.shields.io/badge/Website-%231e37ff?style=for-the-badge&logo=bytedance&logoColor=white](https://github.com/chandramathi)"></a>
</div>
