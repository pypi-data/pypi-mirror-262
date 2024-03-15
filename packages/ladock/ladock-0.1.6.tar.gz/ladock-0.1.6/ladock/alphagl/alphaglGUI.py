import tkinter as tk
import os
from tkinter import ttk
from tensorflow import keras
from ladock.utility import browse_file, mol_mmff, process_csv, help_alphagl
from ladock.PrepareData.calculate_descriptors import get_morgan_fp_descriptors
from threading import Thread
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler, Normalizer
from ladock.nogui import create_alphagl

def alphagl_conf(frame):
    script_directory = os.path.dirname(os.path.realpath(__file__))
    model_filename = "alphagl.keras"
    model_path = os.path.join(script_directory, model_filename)   
    
    def generate_job_directory():
        job_dir = create_alphagl()
        print("Job Directory:", job_dir) 
    
    def using_model(mol, model_path):
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

    def run_task_thread():
        thread = Thread(target=run_task)
        thread.start()

    result_df = pd.DataFrame(columns=["lig_id", "smiles", "score"])

    def run_task():
        csv_path = csv_input.get()
        smiles_data_text = smiles_input.get("1.0", tk.END)
        
        conformers = 10  
        max_iters = 300  
        
        result_text.config(state=tk.NORMAL) 
        result_text.insert(tk.END, f'lig_id, smiles, score\n')
        result_text.config(state=tk.DISABLED) 
        
        if csv_path:
            smiles_list = process_csv(csv_path)
            # Ubah struktur DataFrame
            smiles_list = smiles_list.rename(columns={smiles_list.columns[0]: 'ligand_id', smiles_list.columns[1]: 'smiles'})
            smiles_list['other'] = smiles_list.apply(lambda row: ','.join(row.drop(['ligand_id', 'smiles']).astype(str)), axis=1)
            progress_bar["maximum"] = len(smiles_list)
            progress_bar["value"] = 0
            for i, (lig_id, smi, other) in enumerate(smiles_list[['ligand_id', 'smiles', 'other']].values):
                progress_bar["value"] = i
                mol = mol_mmff(smi, conformers, max_iters)
                score = using_model(mol, model_path)           
                result_df.loc[len(result_df)] = {'lig_id': lig_id, 'smiles': smi, 'score': score}

                # Display the result in the result_text widget
                result_text.config(state=tk.NORMAL) 
                result_text.insert(tk.END, f'{lig_id}, {smi}, {score}\n')
                result_text.see(tk.END)
                result_text.config(state=tk.DISABLED) 
                
                
            # Tugas selesai, reset ProgressBar
            progress_bar["value"] = 0

        elif smiles_data_text.strip():
            smiles_list = [line.split(',') for line in smiles_data_text.split('\n') if line.strip()]
            
            progress_bar["maximum"] = len(smiles_list)
            progress_bar["value"] = 0
            for i, (lig_id, smi) in enumerate(smiles_list):
                progress_bar["value"] = i
                mol = mol_mmff(smi, conformers, max_iters)
                score = using_model(mol, model_path)                
                result_df.loc[len(result_df)] = {'lig_id': lig_id, 'smiles': smi, 'score': score}
                
                # Display the result in the result_text widget
                result_text.config(state=tk.NORMAL) 
                result_text.insert(tk.END, f'{lig_id}, {smi}, {score}\n')
                result_text.see(tk.END)
                result_text.config(state=tk.DISABLED) 
                

            # Tugas selesai, reset ProgressBar
            progress_bar["value"] = 0

    # Fungsi untuk membatalkan tugas
    def cancel_task():
        # Implementasikan logika pembatalan tugas Anda di sini
        print("Task canceled")
        # Reset ProgressBar
        progress_bar["value"] = 0

    def download_result():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            result_df.to_csv(file_path, index=False)

    def copy_result():
        result_text.clipboard_clear()
        result_text.clipboard_append(result_df.to_string(index=False))
        result_text.update()
        
    # CSV Frame
    csv_frame = ttk.Frame(frame, padding="10")
    csv_frame.grid(column=0, row=0, columnspan=1, sticky="ew")
    csv_frame.columnconfigure(0, weight=1)
    csv_frame.rowconfigure(0, weight=1)

    # CSV Input Frame
    csv_input_frame = ttk.Frame(frame, padding="10")
    csv_input_frame.grid(column=0, row=0, columnspan=1, sticky="ew")
    csv_input_frame.columnconfigure(0, weight=1)
    csv_input_frame.rowconfigure(0, weight=1)

    # Label untuk input dalam format smiles
    smiles_label = ttk.Label(csv_input_frame, text="Input molecules in SMILES format:")
    smiles_label.grid(column=0, row=0, padx=5, pady=5, sticky="nw")
    
    # Text input untuk SMILES
    smiles_input = tk.Text(csv_input_frame, wrap="none", font=("Monospace", 11))
    smiles_input.grid(row=1, column=0, pady=5, sticky="news")
    
    # Scrollbar Y-axis
    scrollbar_y = ttk.Scrollbar(csv_input_frame, command=smiles_input.yview)
    smiles_input.config(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=1, column=1, sticky="ns", pady=5, padx=5)  

    # Scrollbar X-axis
    scrollbar_x = ttk.Scrollbar(csv_input_frame, command=smiles_input.xview, orient=tk.HORIZONTAL)
    smiles_input.config(xscrollcommand=scrollbar_x.set)
    scrollbar_x.grid(row=2, column=0, sticky="ew")  

    # CSV File Frame
    csv_file_frame = ttk.Frame(frame, padding="10")
    csv_file_frame.grid(column=0, row=1, columnspan=1, sticky="ew")
    csv_file_frame.columnconfigure(0, weight=1)
    csv_file_frame.rowconfigure(0, weight=1)

    # Label untuk input melalui file CSV
    csv_label = ttk.Label(csv_file_frame, text="Input molecules from CSV file:")
    csv_label.grid(column=0, row=0, padx=5, pady=5, sticky="nw")

    # Text input untuk path file CSV
    csv_input = ttk.Entry(csv_file_frame)
    csv_input.grid(column=0, row=1, padx=5, pady=5, sticky="ew")

    # Button untuk memilih file CSV
    browse_button = ttk.Button(csv_file_frame, text="Browse", command=lambda: browse_file(csv_input))
    browse_button.grid(column=1, row=1, padx=5, pady=5, sticky="ew")

    # Result Frame
    result_frame = ttk.Frame(frame, padding="10")
    result_frame.grid(column=0, row=2, columnspan=1, sticky="ew")
    result_frame.columnconfigure(0, weight=1)
    result_frame.rowconfigure(0, weight=1)

    # Text Widget for Displaying Results
    result_text = tk.Text(result_frame, wrap="none", background="#300a24", foreground="white", font=("Monospace", 11))
    result_text.grid(row=0, column=0, pady=5, sticky="news")
    result_text.config(state="disabled")

    # Scrollbar Y-axis
    scrollbar_y = ttk.Scrollbar(result_frame, command=result_text.yview)
    result_text.config(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=0, column=1, sticky="ns", pady=5, padx=5)  

    # Scrollbar X-axis
    scrollbar_x = ttk.Scrollbar(result_frame, command=result_text.xview, orient=tk.HORIZONTAL)
    result_text.config(xscrollcommand=scrollbar_x.set)
    scrollbar_x.grid(row=1, column=0, sticky="ew")  
   
    # RUN Frame
    run_frame = ttk.Frame(frame, padding="10")
    run_frame.grid(column=0, row=3, columnspan=3, sticky="ew")  
    run_frame.columnconfigure(1, weight=1)
    run_frame.rowconfigure(0, weight=1)

    # Button untuk RUN
    run_button = ttk.Button(run_frame, text="RUN", command=lambda: run_task_thread())
    run_button.grid(column=0, row=0, padx=5, pady=5)

    # ProgressBar
    progress_bar = ttk.Progressbar(run_frame, mode="determinate")
    progress_bar.grid(column=1, row=0, padx=5, pady=5, sticky="ew") 

    # Button untuk CANCEL
    cancel_button = ttk.Button(run_frame, text="Cancel", command=cancel_task)
    cancel_button.grid(column=2, row=0, padx=5, pady=5)
    
     # Button untuk Download Result
    download_button = ttk.Button(run_frame, text="Download", command=download_result)
    download_button.grid(column=3, row=0, padx=5, pady=5)

    # Button untuk Copy Result
    copy_button = ttk.Button(run_frame, text="Copy", command=copy_result)
    copy_button.grid(column=4, row=0, padx=5, pady=5)

    # HelpGen frame
    help_gen_frame = ttk.Label(frame)
    help_gen_frame.grid(column=0, row=4, pady=30, sticky=tk.E)
        
    # Help Button
    ttk.Button(help_gen_frame, text="?", command=help_alphagl).grid(column=0, row=3, pady=30, padx=5)

    # Generate Button
    GEN_button = ttk.Button(help_gen_frame, text="Generate Job Directory", command=generate_job_directory)
    GEN_button.grid(column=1, row=3, pady=5, padx=5)
