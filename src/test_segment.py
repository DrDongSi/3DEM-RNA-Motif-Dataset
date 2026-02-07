import sys
import os
from chimerax.core.session import Session
from chimerax.core.commands import run
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from segment import fetch_emdb_map, fetch_pdb_file, segment_map

try:
    from Bio import PDB
    import mrcfile
except ImportError as e:
    raise RuntimeError(
        "Required packages not found in ChimeraX Python. "
        "Install with:\n"
        "/Applications/ChimeraX-1.9.app/Contents/Library/Frameworks/"
        "Python.framework/Versions/3.11/bin/python3 "
        "-m pip install biopython mrcfile --no-user --break-system-packages"
    ) from e


def run(session):
    pdb_id = "9J1M"
    chain_id = "a"
    residue_ranges = [(619, 625), (595, 603)]

#    session = Session()

    print("\n[Step 1] Fetching EMDB map...")
    emdb_file_path = fetch_emdb_map(session, pdb_id)
    if not emdb_file_path:
        print("Failed to fetch EMDB map.")
        return
    print(f"EMDB map saved at: {emdb_file_path}")

    print("\n[Step 2] Fetching PDB file...")
    pdb_file_path = fetch_pdb_file(session, pdb_id)
    if not pdb_file_path:
        print("Failed to fetch PDB file.")
        return
    print(f"PDB file saved at: {pdb_file_path}")

    print("\n[Step 3] Segmenting density map...")
    segmented_path = segment_map(session, pdb_file_path, emdb_file_path, chain_id, residue_ranges)
    if not segmented_path:
        print(" Failed to segment map.")
        return
    print(f" Segmented map saved at: {segmented_path}")


run(session)
