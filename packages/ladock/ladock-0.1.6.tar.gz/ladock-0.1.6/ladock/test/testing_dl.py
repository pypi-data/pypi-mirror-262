import os
import sys
import urllib.request
import pandas as pd
from tensorflow import keras
from tqdm import tqdm
from functools import partial
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
from urllib.parse import urlparse
import numpy as np
import traceback
from os.path import basename
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from ladock.utility import processing_ligand, process_smi, process_sdf, process_mol, process_csv, mol_mmff, mol_uff, mol_2d, mol_3d, download_file_with_retry, extract_gz, pdb_to_smiles
from ladock.PrepareData.calculate_descriptors import get_2d_descriptors, get_3d_descriptors, get_lipinski_descriptors, get_morgan_fp_descriptors, get_maccs_fp_descriptors, get_daylight_fp_descriptors, get_avalon_fp_descriptors, get_tt_fp_descriptors, get_pubchem_fp_descriptors
from keras.models import load_model
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler, Normalizer
import csv

def write_to_csv(csv_path, lig_id, smi, log_pred, act_pred):
    with open(csv_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([lig_id, smi, log_pred, act_pred])

def using_model(mol, descriptors, model_path, scaler_X, scaler_Y, transformX, transformY):
    # Load model
    model = keras.models.load_model(model_path)

    # Initialize scaler_X and scaler_Y
    if scaler_X == 'StandardScaler':
        scaler_X = StandardScaler()
    elif scaler_X == 'RobustScaler':
        scaler_X = RobustScaler()
    elif scaler_X == 'MinMaxScaler':
        scaler_X = MinMaxScaler()
    elif scaler_X == 'Normalizer':
        scaler_X = Normalizer()

    if scaler_Y == 'StandardScaler':
        scaler_Y = StandardScaler()
    elif scaler_Y == 'RobustScaler':
        scaler_Y = RobustScaler()
    elif scaler_Y == 'MinMaxScaler':
        scaler_Y = MinMaxScaler()
    elif scaler_Y == 'Normalizer':
        scaler_Y = Normalizer()

    # Iterate over descriptors
    for mode in descriptors:
        if mode == "2D DESCRIPTORS":
            descriptors_result = get_2d_descriptors(mol)           
        elif mode == "3D DESCRIPTORS":
            descriptors_result = get_3d_descriptors(mol)
        elif mode == "LIPINSKI DESCRIPTORS":
            descriptors_result = get_lipinski_descriptors(mol)
        elif mode == "MORGAN FINGERPRINTS":
            descriptors_result = get_morgan_fp_descriptors(mol)
        elif mode == "MACCS FINGERPRINTS":
            descriptors_result = get_maccs_fp_descriptors(mol)
        elif mode == "DAYLIGHT FINGERPRINTS":
            descriptors_result = get_daylight_fp_descriptors(mol)
        elif mode == "AVALON FINGERPRINTS":
            descriptors_result = get_avalon_fp_descriptors(mol)
        elif mode == "TORSION FINGERPRINTS":
            descriptors_result = get_tt_fp_descriptors(mol)
        elif mode == "PUBCHEM FINGERPRINTS":
            descriptors_result = get_pubchem_fp_descriptors(mol)
        
        # Transform descriptors if required
        if transformX:
            descriptors_result_np = np.array(descriptors_result)
            descriptors_result_scaled = scaler_X.fit_transform(descriptors_result_np.reshape(-1, 1))
        else:
            descriptors_result_scaled = descriptors_result


        # Predict using the model
        pred = model.predict(np.array([descriptors_result_scaled]))

        # Inverse transform if required
        if transformY:
            scaler_Y.fit(pred)
            pred_original_scale = scaler_Y.inverse_transform(pred.reshape(-1, 1)).flatten()
        else:
            pred_original_scale = pred.flatten()

    return pred_original_scale

def testing(model_path, input_dir, descriptors, methods, conformer, iteration, transformX, scaler_X, logarithmic, transformY, scaler_Y, job_dir, progress_bar, result_text):
    
    # Get the number of available CPU cores
    total_threads = os.cpu_count()
    desired_threads = max(1, total_threads)

    model_name = os.path.splitext(os.path.basename(model_path))[0]
    output_dir = job_dir
    csv_path = os.path.join(output_dir, f'{model_name}_predicted.csv')
    

    # Create header for CSV if the file doesn't exist
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['lig_id', 'smi', 'LaScore'])


    for f in os.listdir(input_dir):  
        print(f'Processing: {f}')
        f_path = os.path.join(input_dir, f)
                  
        if f_path.endswith('.uri'):
            with open(f_path, 'r') as file:
                ligand_links = [line.strip() for line in file.readlines() if 'http' in line and not line.strip().startswith('#')]
                                
            for ligand_link in ligand_links:
                ligand_file_base = basename(ligand_link)
                download_file_with_retry(ligand_link, ligand_file_base) 
                                
                if ligand_file_base.endswith('.gz'):
                    try:
                        ligand_file = extract_gz(ligand_file_base)
                        ligand_file_path = os.path.join(output_dir, ligand_file)                        
                        smiles_list = processing_ligand(ligand_file_path)
                        smiles_df = pd.DataFrame(smiles_list)
                        print(smiles_df)
                        if not smiles_df.empty:
                            lig_ids = smiles_df['ligand_id']
                            smi_list = smiles_df['smiles']
                            for lig_id, smi in zip(lig_ids, smi_list):
                                pdb_file = os.path.join(output_dir, f'{lig_id}.pdb')
                                mol = Chem.MolFromPDBFile(pdb_file)
                                if mol:
                                    log_pred = using_model(mol, descriptors, model_path, scaler_X, scaler_Y, transformX, transformY)
                                    if logarithmic:
                                        act_pred = np.power(10, -log_pred[0]) / 1e-9
                                        act_pred = "{:.3f}".format(act_pred)
                                    else:
                                        act_pred = log_pred[0]
                                        act_pred = "{:.3f}".format(act_pred)
                                    result_dict = {'lig_id': lig_id, 'smi': smi, 'LaScore': act_pred}
        
                                    # Menambahkan hasil ke file CSV secara bertahap
                                    with open(csv_path, 'a') as csv_file:
                                        pd.DataFrame([result_dict]).to_csv(csv_file, mode='a', header=False, index=False)  
                                        
                                    
                    except Exception as e:
                        continue                                
                else:
                    ligand_file_path = os.path.join(output_dir, ligand_file_base)
                    smiles_list = processing_ligand(ligand_file_path)
                    smiles_df = pd.DataFrame(smiles_list)
                    print(smiles_df)
                    if not smiles_df.empty:
                        lig_ids = smiles_df['ligand_id']
                        smi_list = smiles_df['smiles']
                        for lig_id, smi in zip(lig_ids, smi_list):
                            if methods == "2D":
                                mol = mol_2d(smi)
                            elif methods == "3D":
                                mol = mol_3d(smi)
                            elif methods == "UFF":
                                mol = mol_uff(smi, conformer, iteration)
                            elif methods == "MFF":
                                mol = mol_mmff(smi, conformer, iteration)
                            elif methods == "QM":
                                mol = mol_mmff(smi, conformer, iteration)      
                            print(lig_id)
                            if mol:
                                log_pred = using_model(mol, descriptors, model_path, scaler_X, scaler_Y, transformX, transformY)
                                if logarithmic:
                                    act_pred = np.power(10, -log_pred[0]) / 1e-9
                                    act_pred = "{:.3f}".format(act_pred)
                                else:
                                    act_pred = log_pred[0]
                                    act_pred = "{:.3f}".format(act_pred)
                                result_dict = {'lig_id': lig_id, 'smi': smi, 'LaScore': act_pred}
        
                                # Menambahkan hasil ke file CSV secara bertahap
                                with open(csv_path, 'a') as csv_file:
                                    pd.DataFrame([result_dict]).to_csv(csv_file, mode='a', header=False, index=False)  
                                                 
                    
        elif f_path.endswith('.smi') or f_path.endswith('.csv'):
            f_path = os.path.join(input_dir, f)
            smiles_list = processing_ligand(f_path)
            smiles_df = pd.DataFrame(smiles_list)
            print(smiles_df)
            if not smiles_df.empty:
                lig_ids = smiles_df['ligand_id']
                smi_list = smiles_df['smiles']
                for lig_id, smi in zip(lig_ids, smi_list):
                    if methods == "2D":
                        mol = mol_2d(smi)
                    elif methods == "3D":
                        mol = mol_3d(smi)
                    elif methods == "UFF":
                        mol = mol_uff(smi, conformer, iteration)
                    elif methods == "MFF":
                        mol = mol_mmff(smi, conformer, iteration)
                    elif methods == "QM":
                        mol = mol_mmff(smi, conformer, iteration)                    
                    if mol:
                        log_pred = using_model(mol, descriptors, model_path, scaler_X, scaler_Y, transformX, transformY)
                        if logarithmic:
                            act_pred = np.power(10, -log_pred[0]) / 1e-9
                            act_pred = "{:.3f}".format(act_pred)
                        else:
                            act_pred = log_pred[0]
                            act_pred = "{:.3f}".format(act_pred)
                            
                        result_dict = {'lig_id': lig_id, 'smi': smi, 'LaScore': act_pred}
        
                        # Menambahkan hasil ke file CSV secara bertahap
                        with open(csv_path, 'a') as csv_file:
                            pd.DataFrame([result_dict]).to_csv(csv_file, mode='a', header=False, index=False)  
    
        else:
            f_path = os.path.join(input_dir, f)
            smiles_list = processing_ligand(f_path)
            smiles_df = pd.DataFrame(smiles_list)
            print(smiles_df)
            if not smiles_df.empty:
                lig_ids = smiles_df['ligand_id']
                smi_list = smiles_df['smiles']
                for lig_id, smi in zip(lig_ids, smi_list):
                    pdb_file = os.path.join(output_dir, f'{lig_id}.pdb')
                    mol = Chem.MolFromPDBFile(pdb_file)
                    if mol:
                        log_pred = using_model(mol, descriptors, model_path, scaler_X, scaler_Y, transformX, transformY)
                        if logarithmic:
                            act_pred = np.power(10, -log_pred[0]) / 1e-9
                            act_pred = "{:.3f}".format(act_pred)
                        else:
                            act_pred = log_pred[0]
                            act_pred = "{:.3f}".format(act_pred)
                        
                        result_dict = {'lig_id': lig_id, 'smi': smi, 'LaScore': act_pred}
        
                        # Menambahkan hasil ke file CSV secara bertahap
                        with open(csv_path, 'a') as csv_file:
                            pd.DataFrame([result_dict]).to_csv(csv_file, mode='a', header=False, index=False)  

if __name__ == "__main__":
    current_dir = os.getcwd()
    testing()

