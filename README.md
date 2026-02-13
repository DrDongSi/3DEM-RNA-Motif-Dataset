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
2. Run the installer
3. Add ChimeraX to your system PATH if needed

**Phenix (for Q-Score and Z-Score computation)**

Installation instructions and source available from the official Phenix site - [https://www.phenix-online.org/about](https://www.phenix-online.org/about).

We use Phenix to compute CCmask (Z-Score) but for Q-Score we use chimerax plugin.

1. Download from: https://phenix-online.org/download/
2. Run the installer
3. Add Phenix to your system PATH: Add `export PATH="/opt/phenix/phenix-<version>/build/bin:$PATH"` to `~/.bashrc`
4. Restart your terminal

#### 3. Install mrcfile in ChimeraX

Run the following command to install `mrcfile` inside ChimeraX's Python environment:

```bash
chimerax --nogui --cmd "toolshed install https://pypi.org/project/mrcfile/; exit"
```

> **Note:** `mrcfile` must be installed inside ChimeraX's Python environment, not system Python.

#### 4. Verify Installation

Test that all tools are properly installed:

```bash
chimerax --nogui
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

**Syntax**

```bash
chimerax --nogui --cmd "runscript segment.py <pdb_id> [emdb_id] <chain:start-end[,start-end]> ..."
```

> **Note:** Execute commands from within the `src` directory.

**Examples**

To segment a hairpin with four residues at the location 1896-1903 chain positions in Chain A of _B. subtilis ApdA-stalled_ ribosomal complex with PDB ID 8QCQ:

```bash
cd src
chimerax --nogui --cmd "runscript segment.py 8QCQ A:1896-1903"
```

To segment a symmetric loop at positions 1490-1495,1424-1429 in Chain A of _B. subtilis ApdA-stalled_ ribosomal complex with PDB ID 8QCQ:

```bash
chimerax --nogui --cmd "runscript segment.py 8QCQ A:1490-1495,1424-1429"
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

```bash
cd src
python3 label.py <input.mrc> <input.pdb>
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

This research includes a classification of motifs using the 3D CNN deep learning model. This classification model is used to test and ensure that the created labelled dataset of motifs has the metadata and data in the files in a consistent format. The training is designed to classify RNA structures using a 3D based deep learning model that leverages both cryo-EM density maps (.mrc files). The dataset is first split into training and validation subsets (80% training and 20% validation), then wrapped into PyTorch DataLoader objects for efficient batching. The model, Motif3DCNN has 5 classes "symmetric_loop", "bulge", "hairpin", "asymmetric_loop","unknown", takes as input a volumetric density map and corresponding labelled 3D map to extract those voxels features. Training is performed using cross entropy loss for multi class classification, with the Adam optimizer managing parameter updates. After each epoch, the model's performance is evaluated on the validation set, and a checkpoint is saved so that training progress can be resumed or tested later.

### Training

To train the classification model we used segmented motif maps of 2.8 Å or higher. And grouped them into 5 classes symmetric, asymmetric, hairpin, bulges and unknown. The symmetric, asymmetric, hairpin, bulges are RNA motif structures and unknown is any background noise or structures anything that isn't a motif. We used 5 Folds each with approximately 1800 Training data and 450 validation dataset following the 80-20 rule. Each motif type contains about 90 samples that is each set of data contains 5 x 90 = 450 and hence the validation dataset of each fold contains 450. The default number of epochs used for training is 30.

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
