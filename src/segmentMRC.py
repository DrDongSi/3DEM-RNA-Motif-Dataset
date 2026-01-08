import os
import csv
import requests
import json
from chimerax.core.commands import run
import sys
import traceback
import io
import re


with open("config.json", "r") as config_file:
    config = json.load(config_file)
BASE_URL = config.get("rcsb_api_base_url", "https://data.rcsb.org/rest/v1/core/entry")

def get_emdb_id_from_pdb(pdb_id):
    url = f"{BASE_URL}/{pdb_id.lower()}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"RCSB API error for PDB {pdb_id}: {response.status_code}")
            return None

        data = response.json()
        references = data.get("rcsb_external_references", [])
        for ref in references:
            if ref.get("id", "").startswith("EMD"):
                return ref["id"]
        print(f"No EMDB reference found for {pdb_id}")
        return None
    except Exception as e:
        print(f"Error retrieving EMDB ID for {pdb_id}: {e}")
        return None
    
def get_model_by_id(session, target_id):
    for model in session.models.list():
        model_str = str(model)
        # Extract substring starting with '#' and followed by digits and optional .digits
        match = re.search(r'#\d+(\.\d+)?', model_str)
        if match:
            model_id = match.group(0)
            if model_id == target_id:
                return model
    return None

# def get_volume_level_from_info(session, model_id):
#     from io import StringIO
#     import re

#     # Capture the output of "info #model_id"
#     from chimerax.core.commands import CmdLog
#     log_capture = StringIO()
#     session.logger = CmdLog(log_capture)

#     run(session, f"info {model_id}")
#     output = log_capture.getvalue()
    
#     # Parse level using regex
#     match = re.search(r'level\s+([0-9.eE+-]+)', output)
#     if match:
#         level = float(match.group(1))
#         print(f"Found level: {level}")
#         return level
#     else:
#         print("Level not found in info output.")
#         return None
def cleanupfiles(pdb_id,emdb_id):
    try:
        emdb_file = os.path.expanduser(f"~/Downloads/ChimeraX/EMDB/emd_{emdb_id[4:]}.map")
        if os.path.exists(emdb_file):
            os.remove(emdb_file)
            print(f"Deleted EMDB file: {emdb_file}")
    except Exception as e:
        print(f"Failed to delete EMDB file: {emdb_file}. Error: {e}")

    try:
        pdb_file = os.path.expanduser(f"~/Downloads/ChimeraX/PDB/{pdb_id.lower()}.cif")
        if os.path.exists(pdb_file):
            os.remove(pdb_file)
            print(f"Deleted PDB file: {pdb_file}")
    except Exception as e:
        print(f"Failed to delete PDB file: {pdb_file}. Error: {e}")


def segment_density_map(session, pdb_id, aseq, bseq, internal_id, motif_type):
    emdb_id = get_emdb_id_from_pdb(pdb_id)
    if not emdb_id:
        print(f"No EMDB map found for {pdb_id}")
        return

    try:
        run(session, "close all")
        run(session, f"open {pdb_id}")
        run(session, f"select /{aseq} /{bseq}")

        os.makedirs("outputPDBs", exist_ok=True)
        filename = f"outputPDBs/{pdb_id}_{motif_type}_{internal_id}.pdb"
        run(session, f"save {filename} format pdb selectedOnly true")

        run(session, f"open emdb:{emdb_id[4:]}")
        structure_model = None
        volume_model = None
        for m in session.models.list():
            if "atomicstructure" in str(type(m)).lower():
                structure_model = m
            elif "volume" in str(type(m)).lower():
                volume_model = m

        if not structure_model or not volume_model:
            print(f"Failed to identify structure or volume models for {pdb_id}")
            return

        volume_model_id = volume_model.id_string.split('.')[0]
        run(session, f"volume zone #{volume_model_id} near sel range 5.0 newMap true")

        from chimerax.map import Volume
        import numpy as np

        volumes = [m for m in session.models.list() if isinstance(m, Volume)]
        v = volumes[1]
        data = v.full_matrix()
        nonzero_indices = np.argwhere(data != 0)

        if nonzero_indices.size == 0:
            print("All voxels are zero.")
        else:
            min_z, min_y, min_x = nonzero_indices.min(axis=0)
            max_z, max_y, max_x = nonzero_indices.max(axis=0)
            run(session, f"volume copy #3 subregion {min_x},{min_y},{min_z},{max_x},{max_y},{max_z} step 1 modelId #4")

            os.makedirs("outputMaps", exist_ok=True)
            output_path = f"outputMaps/{emdb_id}_{pdb_id}_{motif_type}_{internal_id}.mrc"
            run(session, f"save {output_path} #4")
            print(f"Segmented map saved to: {output_path}")

    except Exception as e:
        print(f"Segmentation failed for {pdb_id}: {e}")
        traceback.print_exc()

def run_all_from_csv(session, csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        current_pdb = None
        current_emdb = None
        batch = []

        for row in reader:
            pdb_id = row['pdb'].strip()
            aseq = row['Aseq_selection'].strip()
            bseq = row['Bseq_selection'].strip()
            internal_id = row['InternalID'].strip()
            motif_type = row['motif_type'].strip()

            if current_pdb is None:
                current_pdb = pdb_id

            if pdb_id != current_pdb:
                cleanupfiles(current_pdb, current_emdb)
                current_pdb = pdb_id
                current_emdb = None  # reset EMDB after cleanup

            if current_emdb is None:
                current_emdb = get_emdb_id_from_pdb(pdb_id)
                if not current_emdb:
                    print(f"Skipping {pdb_id} due to missing EMDB ID.")
                    continue

            print(f"\n--- Processing {pdb_id} ---")
            segment_density_map(session, pdb_id, aseq, bseq, internal_id, motif_type)

        # Final cleanup after last batch
        if current_pdb and current_emdb:
            cleanupfiles(current_pdb, current_emdb)


#def run_all_from_csv(session, csv_path):
#    with open(csv_path, newline='') as csvfile:
#        reader = csv.DictReader(csvfile)
#        for row in reader:
#            # aseq = row['aseq'].strip()
#            # bseq = row['bseq'].strip()
#            pdb_id = row['pdb'].strip()
#            # motif_type = "1x1" #row['Motif_type'].strip()
#            aseq = row['Aseq_selection'].strip()
#            bseq = row['Bseq_selection'].strip()
#            internal_id = row['InternalID'].strip()
#            # output_prefix = f"{pdb_id}_{aseq}_{bseq}"
#            print(f"\n--- Processing {pdb_id} ---")
#            segment_density_map(session, pdb_id, aseq, bseq,internal_id)

#run_all_from_csv(session, "Sample1.csv")
if len(sys.argv) != 2:
    print("Usage: chimerax --script \"runscript segmentMRC.py <input_filename|path>.csv\"")
else:
    csv_file = sys.argv[1]
    print(f"file{csv_file}")
    run_all_from_csv(session, csv_file)
