import sys
import os
import re
from chimerax.core.commands import run

def computeQscore(session,pdb_file,mrc_file,output_file="output.csv"):
    run(session,f"open {pdb_file}")
    run(session,f"open {mrc_file}")
    run(session,f"qscore #4 toVolume #5 useGui false pointsPerShell 8 shellRadiusStep 0.100 maxShellRadius 2.00 referenceGaussianSigma 0.60 logDetails true assignAttr false outputFile {output_file}")
    run(session,"close all")

def extract_info(mrc_filename):
    match = re.match(r"(EMD-\d+)_([A-Z0-9]+)_([a-zA-Z0-9x]+)_(\d+)\.mrc", mrc_filename)
    print(f"{mrc_filename} extract match {match}")
    if match:
        emdb_id, pdb_id, motif_type, suffix = match.groups()
        print(f" {emdb_id} {pdb_id} ")
        return emdb_id, pdb_id, motif_type, suffix
    return None, None, None, None

def find_QScore(session, folderName, mrcFolder, pdbFolder,motif_folder,output_file_prefix):
    volumefiles = os.listdir(f"./{folderName}/{mrcFolder}/{motif_folder}")
    print(f" Folder path ./{folderName}/{mrcFolder}/{motif_folder}")
    mrc_files = [f for f in volumefiles if f.endswith(".mrc")]
    print(f" Folder files {mrc_files}")
    for mrc_file in mrc_files:
        print(f" Folder files {mrc_file}")
        emdb_id, pdb_id, motif_type, suffix = extract_info(mrc_file)
        if not all([emdb_id, pdb_id, motif_type, suffix]):
            print(f"Skipping malformed filename: {mrc_file}")
            continue

        pdb_file = f"./{folderName}/{pdbFolder}/{motif_folder}/{pdb_id}_{motif_type}_{suffix}.pdb"
        if not os.path.exists(pdb_file):
            print(f"Missing PDB file: {pdb_file}")
            continue

        try:
            mrc_file_fullpath = f"./{folderName}/{mrcFolder}/{motif_folder}/{mrc_file}"
            computeQscore(session, pdb_file, mrc_file_fullpath, f"{output_file_prefix}_{pdb_id}_{suffix}.csv")

        except Exception as e:
            print(f"Error processing {mrc_file} and {pdb_file}: {e}")

        run(session, "close all")

# def computeZscore(session,pdf_file,mrc_file,output_file="outputZ.csv"):
#     run(session,)

if len(sys.argv) != 6:
    print("Usage chimerax qscoreCompute.py <root_folder> <mrc_folder> <pdb_folder> <output.csv> <motif_type>")
else:
    root_folder = sys.argv[1]
    mrc_folder = sys.argv[2]
    pdb_folder = sys.argv[3]
    output_file_prefix =  sys.argv[4]
    motif_type = sys.argv[5]
    print(f"{pdb_folder}= {mrc_folder}= {output_file_prefix}= ")
    # computeQscore(session,pdb_file,mrc_file,output_file)
    find_QScore(session, root_folder, mrc_folder, pdb_folder, motif_type, output_file_prefix)

