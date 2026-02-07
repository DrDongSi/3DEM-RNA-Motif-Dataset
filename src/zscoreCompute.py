import os
import csv
import subprocess
import sys
import re

def getResolution(mrc_file):
    cmd = ["phenix.mtriage",mrc_file]
    print(f" Running: {' '.join(cmd)}")
    result = subprocess.run(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    match = re.search(r"Resolution set to \s*([\d\.]+)", result.stdout)

    if match:
        resolution = float(match.group(1))
        return resolution
    else:
        print("Could not find resolution in mtriage output.")
        print(result.stdout)
        return None
    
def computeZScore( mrc_file="outputMaps/segmentedMap.mrc", pdb_name = "outputPDBs/segmentedPDB.pdb", output_csv="output.csv"):
    with open(output_csv, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["resolution", "CC_mask", "CC_volume", "CC_peaks", "CC_box"])
        resolution = getResolution(mrc_file)
        if not resolution:
            print(f" No resolution found for {pdb_name}")
            return

        cmd = [
            "phenix.map_model_cc",
            f"./{pdb_name}",
            f"./{mrc_file}",
            f"resolution={resolution}",
        ]

        print(f" Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        cc_mask = re.search(r"CC_mask\s*:\s*([0-9.]+)", result.stdout)
        cc_volume = re.search(r"CC_volume\s*:\s*([0-9.]+)", result.stdout)
        cc_peaks = re.search(r"CC_peaks\s*:\s*([0-9.]+)", result.stdout)
        cc_box = re.search(r"CC_box\s*:\s*([0-9.]+)", result.stdout)

        writer.writerow([
            resolution,
            cc_mask.group(1) if cc_mask else "",
            cc_volume.group(1) if cc_volume else "",
            cc_peaks.group(1) if cc_peaks else "",
            cc_box.group(1) if cc_box else "",
        ])
        print(f"{resolution} done — CC_mask={cc_mask.group(1) if cc_mask else 'NA'} \n")
        print(result.stdout)

if sys.argv!=2:
    print("Usage missing folder names python3 zscoreCompute.py <rootDirectory> <csvfile_with_resolutions>")
else:
    root_dir = sys.argv[1]
    csv_root = sys.argv[2]
    print(f"Executing zscore at {root_dir} for {csv_root}")
    computeZScore(root_dir,csv_root)
