import os
import pandas as pd
import concurrent.futures
from tqdm import tqdm
from rdkit import Chem
from rdkit.Chem import AllChem
from ladock.PrepareData.calculate_descriptors import get_2d_descriptors, get_3d_descriptors, get_lipinski_descriptors, get_morgan_fp_descriptors, get_maccs_fp_descriptors, get_daylight_fp_descriptors, get_avalon_fp_descriptors, get_tt_fp_descriptors, get_pubchem_fp_descriptors
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
from ladock.utility import mol_mmff, mol_uff, mol_qm, mol_2d, mol_3d

def geom_opt(smiles, other, num_conformers, maxIters, optimize_geometry):   

    try:
        num_conformers = int(num_conformers)
        maxIters = int(maxIters)

        if optimize_geometry == "uff":
            mol = mol_uff(smiles, num_conformers, maxIters)
        elif optimize_geometry == "mmff":
            mol = mol_mmff(smiles, num_conformers, maxIters)
        elif optimize_geometry == "qm":
            mol = mol_qm(smiles, num_conformers, maxIters)
        elif optimize_geometry == "2d":
            mol = mol_2d(smiles)
        elif optimize_geometry == "3d":
            mol = mol_3d(smiles)
        
        return mol, smiles, other

    except Exception as e:
        print(f"Error in calculate_descriptors_parallel for {smiles}: {e}")
        return None

def calculate_descriptors(num_conformers, maxIters, optimize_geometry, listmode, smiles_column, others_column, other, smiles):
    mol, smiles, other = geom_opt(smiles, other, num_conformers, maxIters, optimize_geometry)

    # Initialize dictionaries for each row
    descriptors_data = {}
    other_data = {}
    smiles_data = {}

    for mode in listmode:
        if mode == "2D DESCRIPTORS":
            descriptors_data = get_2d_descriptors(mol)
        elif mode == "3D DESCRIPTORS":
            descriptors_data = get_3d_descriptors(mol)
        elif mode == "LIPINSKI DESCRIPTORS":
            descriptors_data = get_lipinski_descriptors(mol)
        elif mode == "MORGAN FINGERPRINTS":
            descriptors_data = get_morgan_fp_descriptors(mol)
        elif mode == "MACCS FINGERPRINTS":
            descriptors_data = get_maccs_fp_descriptors(mol)
        elif mode == "DAYLIGHT FINGERPRINTS":
            descriptors_data = get_daylight_fp_descriptors(mol)
        elif mode == "AVALON FINGERPRINTS":
            descriptors_data = get_avalon_fp_descriptors(mol)
        elif mode == "TORSION FINGERPRINTS":
            descriptors_data = get_tt_fp_descriptors(mol)
        elif mode == "PUBCHEM FINGERPRINTS":
            descriptors_data = get_pubchem_fp_descriptors(mol)
   
    # Membuat DataFrame setelah seluruh loop selesai
    other_data = dict(zip(others_column, other))
    smiles_data[smiles_column] = smiles

    return other_data, smiles_data, descriptors_data

def prepareData(csv_file, input_dir, output_dir, listmode, input_column, optimize_geometry, num_conformers, maxIters):
    # Mendapatkan nama berkas tanpa ekstensi
    print("Descriptors calculation...")
    fn_csv = os.path.splitext(os.path.basename(csv_file))[0]

    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()
    modes = '_'.join(listmode)
    csv_output = os.path.join(output_dir, fn_csv + f"_{modes.lower()}.csv")

    # Mencari nama kolom yang cocok dengan keyword
    matching_columns = [col for col in df.columns if input_column.lower() in col.lower()]

    # Memeriksa apakah ada kolom yang cocok
    if matching_columns:
        # Menggunakan kolom pertama yang cocok
        selected_column = matching_columns[0]
        smiles_list = df[selected_column].tolist()
        smiles_column = selected_column
        others = df.drop(columns=[selected_column]).values.tolist()
        others_column = df.drop(columns=[selected_column]).columns.tolist()

        # Get the number of available CPU cores
        total_threads = os.cpu_count()
        max_workers = total_threads - 2

        start_time = time.time()
        optimize_geometry = optimize_geometry.lower()

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            header_written = False  
            for other, smiles in zip(others, smiles_list):
                result = executor.submit(calculate_descriptors, int(num_conformers), int(maxIters), optimize_geometry, listmode, smiles_column, others_column, other, smiles)
                other_data, smiles_data, descriptors_data = result.result()
                other_df = pd.DataFrame([other_data])
                smiles_df = pd.DataFrame([smiles_data])
                descriptors_df = pd.DataFrame([descriptors_data])
                df_combined = pd.concat([other_df, smiles_df, descriptors_df], axis=1)
                # Menulis header hanya pada iterasi pertama
                if not header_written:
                    df_combined.to_csv(csv_output, mode='a', header=True, index=False)
                    header_written = True
                else:
                    df_combined.to_csv(csv_output, mode='a', header=False, index=False)

        end_time = time.time()
        total_execution_time = end_time - start_time
        print("\nUsing", max_workers, "of", total_threads, "cpu")
        print(f"Calculation time of descriptors: {total_execution_time:.2f} seconds")
        
        return csv_output


        
        
