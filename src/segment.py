import os
import json
import requests
from chimerax.core.commands import run
import traceback
import re
from chimerax.map import Volume
import numpy as np

from qscoreCompute import computeQscore
from zscoreCompute import computeZScore
from label import generateLabelMap
# Load config
with open("config.json", "r") as config_file:
    config = json.load(config_file)
BASE_URL = config.get("rcsb_api_base_url", "https://data.rcsb.org/rest/v1/core/entry")

#Return EMDB ID for a given PDB ID using RCSB API.
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

#Download CryoEM map for a PDB ID and return local file path. You may also modify this to fetch command and run on any map file that is already prefetched
def fetch_emdb_map(session, pdb_id):
    emdb_id = get_emdb_id_from_pdb(pdb_id)
    if not emdb_id:
        return None
    try:
        run(session, f"open emdb:{emdb_id[4:]}")
        emdb_file = os.path.expanduser(f"~/Downloads/ChimeraX/EMDB/emd_{emdb_id[4:]}.map")
        if os.path.exists(emdb_file):
            return emdb_file
        else:
            print(f"Map file not found after download: {emdb_file}")
            return None
    except Exception as e:
        print(f"Failed to fetch EMDB map: {e}")
        return None

#Download PDB file for a given PDB ID and return local file path. Same as the map file you may modify it to fetch an already downloaded pdb file
def fetch_pdb_file(session, pdb_id):
    try:
        run(session, f"open {pdb_id}")
        pdb_file = os.path.expanduser(f"~/Downloads/ChimeraX/PDB/{pdb_id.lower()}.cif")
        if os.path.exists(pdb_file):
            return pdb_file
        else:
            print(f"PDB file not found after download: {pdb_file}")
            return None
    except Exception as e:
        print(f"Failed to fetch PDB file: {e}")
        return None

#Load PDB and EMDB map, select residues, and return path to segmented map.
def segment_map(session, pdb_file_path, emdb_file_path, chain_id, residue_ranges):
    try:
        run(session, "close all")
        run(session, f"open {pdb_file_path}")
        
        # Build selection string
        selections = []
        for start, end in residue_ranges:
            selections.append(f"/{chain_id}:{start}-{end}")
        sel_str = " ".join(selections)
        run(session, f"select {sel_str}")
        
        os.makedirs("outputPDBs", exist_ok=True)
        filename = f"outputPDBs/segmentedPDB.pdb"
        run(session, f"save {filename} format pdb selectedOnly true")
        
        run(session, f"open {emdb_file_path}")

        structure_model = None
        volume_model = None
        for m in session.models.list():
            if "atomicstructure" in str(type(m)).lower():
                structure_model = m
            elif "volume" in str(type(m)).lower():
                volume_model = m
        if not structure_model or not volume_model:
            print("Failed to identify structure or volume models.")
            return None

        volume_model_id = volume_model.id_string.split('.')[0]
        run(session, f"volume zone #{volume_model_id} near sel range 5.0 newMap true")

        # Find the new volume (zoned map)
        volumes = [m for m in session.models.list() if isinstance(m, Volume)]
        if len(volumes) < 2:
            print("No zoned volume found.")
            return None
        v = volumes[1]

        data = v.full_matrix()
        nonzero_indices = np.argwhere(data != 0)
        if nonzero_indices.size == 0:
            print("All voxels are zero.")
            return None

        min_z, min_y, min_x = nonzero_indices.min(axis=0)
        max_z, max_y, max_x = nonzero_indices.max(axis=0)
        run(session, f"volume copy #{v.id_string} subregion {min_x},{min_y},{min_z},{max_x},{max_y},{max_z} step 1 modelId #99")

        # Save segmented map
        os.makedirs("outputMaps", exist_ok=True)
        output_path = f"outputMaps/segmentedMap.mrc"
        run(session, f"save {output_path} #99")

        computeQscore(session,filename, output_path, f"qscoreOutput.csv")
        computeZScore(output_path, filename, f"zscoreOutput.csv")
        generateLabelMap(output_path,filename,f"backboneLabel.mrc","backbone")
        generateLabelMap(output_path,filename,f"riboseLabel.mrc","ribose")
        generateLabelMap(output_path,filename,f"sugarLabel.mrc","sugar")
        return output_path

    except Exception as e:
        print(f"Segmentation failed: {e}")
        traceback.print_exc()
        return None

