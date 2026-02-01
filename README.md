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
| Motif Dataset                | Dataset containing motif-level samples used for pattern or feature analysis. | [RNA Motif Dataset](https://zenodo.org/records/18396353) |
| Labelled Motif Dataset            | Dataset containing backbone, nucleobase and ribose sugar labels  | [Labelled Dataset](https://zenodo.org/records/18437991)| 
| Benchmark Results            | Benchmark results for classification of RNA Motifs | [Results](https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/main/README.md#benchmark)| 


## Getting started (For end users)

### Installation - Repository

Clone the dataset and scripts:

```bash
git clone https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset
```

```
cd 3DEM-RNA-Motif-Dataset
```
---

### Dependencies

#### Required Tools

- **UCSF ChimeraX (v1.9 or higher)**  
  Download: https://www.cgl.ucsf.edu/chimerax/download.html

- **Phenix**  
  Installation instructions and source available from the official Phenix site - [https://www.phenix-online.org/about](https://www.phenix-online.org/about).

- **mrcfile (inside ChimeraX)**  
  Even if installed via `pip`, ChimeraX will **not** see it. Install it via ChimeraX toolshed:

```bash
/Applications/ChimeraX-1.9.app/Contents/bin/ChimeraX   --nogui --cmd "toolshed install https://pypi.org/project/mrcfile/; exit"
```

> **Note:** Installing `mrcfile` through system Python is insufficient. It must be installed inside ChimeraX.

---
#### Installing UCSF ChimeraX

1. Visit: https://www.cgl.ucsf.edu/chimerax/download.html  
2. Download the installer for your OS (Windows / macOS / Linux)
3. Follow platform-specific installation steps
4. Verify installation:
```bash
chimerax --nogui
```

---

### Quick Start

### Segmentation
Segmentation is performed by aligning atomic RNA structures to their corresponding cryo-EM density maps, selecting user-specified residue ranges, and extracting local density using spatial zoning around the selected atoms. The resulting non-zero voxel regions are cropped into compact subvolumes, producing motif-specific density maps suitable for quantitative analysis and classification.
As show in the following figure segmenting a hairpin with four residues at the location 1896 - 1903 chain positions in Chain A of _B. subtilis ApdA-stalled_ ribosomal complex with PDB ID 8QCQ, by selecting the density voxels around the atomic map of the hairpin. The occurrence information of the motifs for the dataset collected in this project is obtained from CossMosDB and the jupyter notebook found here can be used to collect all the motif information.   You can  find the information of motif sequences already fetched [here](https://drive.google.com/drive/folders/1hHA16pI2Vi6p6EgbGSfCZ9rksYzvBifN?usp=sharing). And you may use this information in segmentation and labelling tool testing and usage. You can also use the dataset for ML or deeplearning modeling. You can the jupyter notebook is only used to fetch the motif sequence information from CossMos [here](https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/blob/chandramathi/src/process_cossmos.ipynb) if you require testing of motif information fetch process. For which create a directory RNAmotifproject under MyDrive in google drive and copy [this](https://drive.google.com/drive/folders/1yDI5FakBihkRMw4z_5mmrnz_stLHZc0o?usp=drive_link) folder under the same name inside the RNAmotifproject directory.

<p align="center">
  <img src="https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/blob/chandramathi/Segmentation.png" alt="RNA Motif Architecture" width="720">
</p>


#### Architecture Overview
PDB structures and density maps are loaded into ChimeraX via public REST APIs without authentication, followed by segmentation. Cryo-EM density data stored in MRC/map formats are processed to generate and label 25 motif types, forming a dataset. The density maps are fitted to RNA 3D structures, and voxels within 5 Å of selected RNA chain regions are segmented as regions of interest.
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

## Segmentation Command Line Tool Overview

**Usage**

```bash
chimerax --nogui --script segment.py -- \
  <pdb_id> [emdb_id(optional)] \
  <chain:start-end[,start-end]> [<chain:start-end> ...]
```

**Example: Segmentation of a RNA-Motif density map**

To segment a hairpin with four residues at the location 1896 - 1903 chain positions in Chain A of _B. subtilis ApdA-stalled_ ribosomal complex with PDB ID 8QCQ. Note: execute the command line tool from within the src directory.

```bash
# Single sequence style
chimerax --nogui --cmd "runscript segment.py 8QCQ A:1896-1903"
```
To segment a symmetrice loop of order 2x2 at the location 1490-1495,1424-1429 chain positions in Chain A of _B. subtilis ApdA-stalled_ ribosomal complex with PDB ID 8QCQ.
```bash
# Multiple sequence style
chimerax --nogui --cmd "runscript segment.py 8QCQ A:1490-1495,1424-1429"
```

**Output**

The segmented files will be stored in the directory outputMaps and outputPDBs (the folders will be created if not already present). The Q-Score, CCmask results will be printed to the console and mask.ccp4 written to the current directory. 


---

## Labeling 

Labeling MRC density maps projects atomic model information into the 3D voxel space of cryo-EM maps. Atomic coordinates are aligned, converted to voxel indices, and assigned labels within a defined radius to account for density blur. Overlapping labels are resolved by nearest-atom assignment. The result is a labeled MRC file with biologically meaningful voxel-level annotations, useful for motif recognition, segmentation, and training deep learning models.

**Usage**
```bash
python label.py input.mrc input.pdb
```
<p align="center">
  <img src="https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/blob/chandramathi/images/LabelFlow.png" alt="RNA Labeling Illustration" width="720">
</p>


**Example**

```bash
python3 label.py ./outputMaps/segmentedMap.mrc ./outputPDBs/segmentedPDB.pdb
```
**Output**

By default creates files of the name 
Backbone Label - backbone_label_segmentedMap.mrc
Ribose Label - ribose_label_segmentedMap.mrc
Sugar Label - sugar_label_segmentedMap.mrc

You can find the sample response [here](https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/tree/chandramathi/sample)

---
## Classification

This research includes a classification of motifs using the 3D CNN deep learning model. This classification model is used to test and ensure that the created labelled dataset of motifs has the metadata and data in the files in a consistent format. The training is designed to classify RNA structures using a 3D based deep learning model that leverages both cryo-EM density maps (.mrc files). The dataset is first split into training and validation subsets (80% training and 20 % validation), then wrapped into PyTorch DataLoader objects for efficient batching. The model, Motif3DCNN has 5 classes "symmetric_loop", "bulge", "hairpin", "asymmetric_loop","unknown", takes as input a volumetric density map and corresponding labelled 3D map to extract those voxels  features. Training is performed using cross entropy loss for multi class classification, with the Adam optimizer managing parameter updates. After each epoch, the model’s performance is evaluated on the validation set, and a checkpoint is saved so that training progress can be resumed or tested later.

### Training
To train the classification model we used segmented motif maps of 2.8 Å or higher. And grouped them into  5 classes symmetric, asymmetric, hairpin. bulges and unknown. The symmetric, asymmetric, hairpin. bulges are RNA motif structures and unknown is any background noise or structures anything that isn't a motif. We used 5 Folds each with approximately 1800 Training data and 450 validation dataset following the 80-20 rule. Each motif type contains about 90 samples that is each set of data contains 5 x 90 = 450 and hence the validation dataset of each fold contains 450. 
The default number of epochs used for training is 30.

**Usage**
Assuming the current directory is the source directory
```bash
python3 train.py <CSVOfTrainingDataset> <CSVOfValidationDataset> <Destination Directory>
```
    **CSVOfTrainingDataset** - A csv file containing a list of the density files that are to be used for training of the classification model
    **CSVOfValidationDataset** - A csv file containing a list the density files that are to be used for validation of the classification model
    **Destination Directory** - The location were all the trained models are saved.

You can find all the curated training and validation input CSV files [here](https://github.com/DrDongSi/3DEM-RNA-Motif-Dataset/tree/main/src/trainingCSVs) and the filtered dataset needed for training [here](https://zenodo.org/records/18396353)

```bash
cd ./src
python3 train.py ./trainingCSVs/fold1_train.csv ./trainingCSVs/fold1_val.csv SET1
```

**Output**
Model weights stored as .pth files in the directory given as command line argument.

---
**Testing**
To test the trained classification model you can use the utility validate_folder.py

**Usage**
Assuming the current directory is the source directory

```bash
  python validate_folder.py <testFilesDirectory> <modelWeights>
```
**testFilesDirectory** - The folder path of the directory containing all the files that are going to be used in testing the trained classification model. Ensure that the files follow the naming convention <emdb_id>_<pdb_id>_<motif_type>_<sequenceNumber>.mrc followed in this project and 
**modelWeights** - The file path of the trained classification model.

Download the trained models used for benchmarking from [here](https://zenodo.org/records/18409492) 
```bash
  python validate_folder.py ./testSET/ ./models/fold5Model.pth
```

**Output**
It will give the confusion matrix, specificity and selectivity scores.

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
        <tr><td>sym</td><td style="background:#b6fcb6;">🟢 <b>74</b></td><td>1</td><td>3</td><td>12</td><td>0</td></tr>
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
