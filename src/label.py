import os
import sys
import numpy as np
import mrcfile
from Bio import PDB
from copy import deepcopy

# Normalize an MRC map by its 95th percentile and clips values to [0,1].
def normalize_map(input_mrc_path, output_mrc_path):
    print(f"### Normalizing {input_mrc_path} ###")
    with mrcfile.open(input_mrc_path, mode='r') as clean_map:
        map_data = deepcopy(clean_map.data)

        try:
            percentile = np.percentile(map_data[np.nonzero(map_data)], 95)
            map_data /= percentile
        except IndexError:
            print("Warning: Empty map or invalid data for normalization.")
        
        map_data[map_data < 0] = 0
        map_data[map_data > 1] = 1

        with mrcfile.new(output_mrc_path, overwrite=True) as mrc:
            mrc.set_data(map_data.astype(np.float32))
            mrc.voxel_size = clean_map.voxel_size
            mrc.header.origin = clean_map.header.origin
            mrc.update_header_stats()

    print(f"### Wrote normalized map to {output_mrc_path}")
    return output_mrc_path

#Convert atomic coordinate to MRC voxel indexes since the 3D coordinates of atomic model is in angstroms.
def get_index(coord, origin, voxel_size):
    return round((coord - origin) / voxel_size)


def generateLabelMap(segmented_map, pdb_structure, output_mrc_path,label_type):
    error_list = set()
    org_map = mrcfile.open(segmented_map, mode='r')
    data = np.copy(org_map.data).astype('float32')
    label_map = np.zeros_like(data, dtype=np.float32)

    x_origin = org_map.header.origin['x']
    y_origin = org_map.header.origin['y']
    z_origin = org_map.header.origin['z']
    x_voxel = org_map.voxel_size['x']
    y_voxel = org_map.voxel_size['y']
    z_voxel = org_map.voxel_size['z']

    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("model", pdb_structure)

    print(f"Generating {label_type} label map using {pdb_structure}")

    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    atom_name = atom.get_name()
                    x, y, z = atom.get_coord()
                    iz = int(get_index(z, z_origin, z_voxel))
                    jy = int(get_index(y, y_origin, y_voxel))
                    kx = int(get_index(x, x_origin, x_voxel))

                    try:
                        if label_type == "backbone":# Phosphates and backbone oxygens
                            if atom_name == "P" or atom_name in ["O5'", "O3'", "O1P", "O2P"]:
                                label_map[iz, jy, kx] = 1.0

                        elif label_type == "ribose":# Ribose carbons and oxygens
                            if atom_name in ["C1'", "C2'", "C3'", "C4'", "C5'", "O2'", "O4'"]:
                                label_map[iz, jy, kx] = 1.0

                        elif label_type == "sugar":# All ribose-related atoms (carbons + oxygens)
                            if atom_name in ["C1'", "C2'", "C3'", "C4'", "C5'", "O2'", "O4'"]:
                                label_map[iz, jy, kx] = 1.0

                        else:
                            raise ValueError(f"Unknown label_type: {label_type}")

                    except IndexError:
                        error_list.add((iz, jy, kx))

    # Save labeled map
    output_file = f"{output_mrc_path}_{label_type}.mrc"
    with mrcfile.new(output_file, overwrite=True) as mrc:
        mrc.set_data(label_map)
        mrc.voxel_size = org_map.voxel_size
        mrc.header.origin = org_map.header.origin
        mrc.nstart = org_map.nstart
        mrc.update_header_stats()

    org_map.close()

    if error_list:
        print(f" {len(error_list)} atoms were outside map bounds.")
    print(f" {label_type.capitalize()} map saved to: {output_file}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 label.py input.mrc input.pdb")
        sys.exit(1)

    input_mrc, input_pdb = sys.argv[1:3]

    normalized_mrc = os.path.splitext(input_mrc)[0] + "_normalized.mrc"
    normalize_map(input_mrc, normalized_mrc)

    generateLabelMap(input_mrc,input_pdb,f"backboneLabel.mrc","backbone")
    generateLabelMap(input_mrc,input_pdb,f"riboseLabel.mrc","ribose")
    generateLabelMap(input_mrc,input_pdb,f"sugarLabel.mrc","sugar")


if __name__ == "__main__":
    main()
