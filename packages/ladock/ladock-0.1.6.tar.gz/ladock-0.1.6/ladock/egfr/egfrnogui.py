from tensorflow import keras
from ladock.utility import mol_mmff, process_csv
from ladock.PrepareData.calculate_descriptors import get_morgan_fp_descriptors
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

def read_config(config_file):
    # Inisialisasi kamus untuk menyimpan nilai variabel konfigurasi
    config = {}

    # Buka file konfigurasi
    with open(config_file, 'r') as file:
        # Baca setiap baris dalam file konfigurasi
        for line in file:
            # Lewati baris yang kosong atau dimulai dengan tanda pagar (#) sebagai komentar
            if line.strip() == '' or line.strip().startswith('#'):
                continue
            
            # Pisahkan kunci dan nilai menggunakan tanda ":" sebagai pemisah
            parts = line.strip().split(':', 1)
            if len(parts) != 2:
                continue  # Lewati baris yang tidak sesuai format
            
            key, value = parts
            
            # Hilangkan spasi ekstra pada nilai
            value = value.strip()
            
            # Jika nilai memiliki tanda koma, pisahkan menjadi daftar nilai
            if ',' in value:
                value = [item.strip() for item in value.split(',')]
            
            # Tambahkan pasangan kunci-nilai ke dalam kamus konfigurasi
            config[key.strip()] = value

    return config

def egfr_conf(csv_val):
    script_directory = os.path.dirname(os.path.realpath(__file__))
    model_filename = "egfr.keras"
    model_path = os.path.join(script_directory, model_filename)  
    
    def using_model(mol):
        model = keras.models.load_model(model_path)
        scaler_X = StandardScaler()
        scaler_Y = StandardScaler()
        descriptors_result = get_morgan_fp_descriptors(mol)
        descriptors_result_np = np.array(descriptors_result)
        descriptors_result_scaled = scaler_X.fit_transform(descriptors_result_np.reshape(-1, 1))
        pred = model.predict(np.array([descriptors_result_scaled]))
        scaler_Y.fit(pred)
        pred_original_scale = scaler_Y.inverse_transform(pred.reshape(-1, 1)).flatten()
        score = np.power(10, -pred_original_scale) / 1e-9
        score = "{:.3f}".format(score[0])

        return score

    def run_task():
        conformers = 10
        max_iters = 300
        
        file_path = os.path.join(job_dir, 'erbb_result.csv')
        
        # Menulis header kolom jika file belum ada
        with open(file_path, 'w') as file:
                file.write("lig_id,smiles,LaScore(EGFR Inhibitor)\n")
        
        smiles_list = process_csv(csv_val)
        # Ubah struktur DataFrame
        smiles_list = smiles_list.rename(columns={smiles_list.columns[0]: 'ligand_id', smiles_list.columns[1]: 'smiles'})
        smiles_list['other'] = smiles_list.apply(lambda row: ','.join(row.drop(['ligand_id', 'smiles']).astype(str)),
                                                 axis=1)
        
        
        for i, (lig_id, smi, other) in enumerate(smiles_list[['ligand_id', 'smiles', 'other']].values):
                mol = mol_mmff(smi, conformers, max_iters)
                score = using_model(mol)
                # Menyimpan baris baru ke file CSV
                
                print(f"{lig_id}\t{smi}\t{score}")  
                with open(file_path, 'a') as file:
                    file.write(f"{lig_id},{smi},{score}\n")

    run_task()

# Menjalankan fungsi egfr_conf()
current_dir = os.getcwd()
job_dir = os.path.join(current_dir, 'egfr')
config_file=os.path.join(job_dir, 'configegfr.txt')
config=read_config(config_file)
csv_val = config['csv_input']
print(csv_val)

egfr_conf(csv_val)
