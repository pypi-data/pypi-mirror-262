import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ladock.getdata.getData_S1 import search_targets  
from ladock.getdata.getData_S2 import search_molecules
from ladock.PrepareData.prepare_data import prepareData 
from ladock.utility import browse_file, browse_dir, help_getdata
from threading import Thread
import shutil
import pandas as pd
from ladock.nogui import create_getdata

def getdata_conf(frame):
    
    def generate_job_directory():
        job_dir = create_getdata()
        print("Job Directory:", job_dir)
    
    def delete_directory_contents(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')
        
    def start_thread1():                 
        thread = Thread(target=start_target)                      
        thread.start()

    def start_thread2():                
        thread = Thread(target=start_molecules)                      
        thread.start()
    
    def start_thread3():                   
        thread = Thread(target=start_calculate)                      
        thread.start()        
       
    def start_target():
        job_dir = job_dir_entry.get()
        query_search = query_entry.get()
        progress_bar.start()
        
        try:
            delete_directory_contents(job_dir)            
        except Exception as e:
            print(f'Error deleting contents of directory {job_dir}: {e}')
            
        query_list = [query.strip() for query in query_search.split(',') if query.strip()]        
        result_text.insert(tk.END, f"Query List: {query_list}\n")
        result_text.insert(tk.END, f"Job Directory: {job_dir}\n")
        
        search_targets(query_list, job_dir, result_text)
        progress_bar.stop()

    def start_molecules():
        job_dir = job_dir_entry.get()
        progress_bar.start()
        thread = Thread(target=search_molecules)
        molecules_files = search_molecules(job_dir, result_text)                    
        progress_bar.stop()
            
    def start_calculate():
        job_dir = job_dir_entry.get()
        progress_bar.start()
        csv_files = entry_molecules_file.get()
        csv_files = csv_files.split(',')
        csv_files = [file.strip() for file in csv_files]
        input_dir = job_dir
        output_dir = os.path.join(input_dir, "output")
        
        # Membuat direktori output jika belum ada
        os.makedirs(output_dir, exist_ok=True)      
        
        descriptors_list = [descriptor_text.upper() for descriptor_var, descriptor_text in zip(descriptor_vars, descriptors_options) if descriptor_var.get() == "1"]

        mol_column = entry_molecule_column.get()
        optimize_method = entry_optimization_var.get()
        num_conformers = int(conformer_var.get())
        max_iters = int(max_iters_var.get())
        
        # Mencetak semua variabel
        result_text.insert("end", f"csv_file: {csv_file}\n"
                                   f"input_dir: {input_dir}\n"
                                   f"output_dir: {output_dir}\n"
                                   f"descriptors_list: {descriptors_list}\n"
                                   f"mol_column: {mol_column}\n"
                                   f"optimize_method: {optimize_method}\n"
                                   f"num_conformers: {num_conformers}\n"
                                   f"max_iters: {max_iters}\n")

        try:
            for csv_file in csv_files: 
                csv_output = prepareData(csv_file, input_dir, output_dir, descriptors_list, mol_column, optimize_method, num_conformers, max_iters)
            df = pd.read_csv(csv_output)

            result_text.insert("end", f"\n\nDataFrame Head:\n{df.head()}\n\nDataFrame Tail:\n{df.tail()}\n\nDataFrame Info:\n{df.info()}\n")
            messagebox.showinfo("Calculation Complete", "Descriptors calculation is complete.")
            progress_bar.stop()
        
        except Exception as e:
            result_text.insert("end", f"\n\nError: {str(e)}\n")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            progress_bar.stop()

    # Left Frame 
    left_frame = ttk.Frame(frame, padding="10")
    left_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))   

    # Job Directory
    current_dir = os.getcwd()
    jobdir = os.path.join(current_dir, 'getdata')
    if os.path.exists(jobdir):
        default_jobdir = jobdir
    else:
        default_jobdir = "/path/to/job_directory"
        
    label_job_dir = ttk.Label(left_frame, text="Job Directory", font=('TkDefaultFont', 10, 'bold'))
    label_job_dir.grid(row=0, column=0, padx=5, pady=(5,2), sticky="ew")   
    frame_job_dir = ttk.Frame(left_frame)
    frame_job_dir.grid(row=1, column=0, padx=5, pady=2, sticky="ew")       
    job_dir_entry = ttk.Entry(frame_job_dir)
    job_dir_entry.grid(row=0, column=0, padx=5, pady=2, sticky="w")
    job_dir_entry.insert(0, default_jobdir)      
    button_browse_job_dir = ttk.Button(frame_job_dir, text="Browse", command=lambda: browse_dir(job_dir_entry))
    button_browse_job_dir.grid(row=0, column=1, padx=5, pady=2, sticky="w")
 
    # Step - 1 Interface
    query_label = ttk.Label(left_frame, text="Get Data from ChEMBL", font=('TkDefaultFont', 10, 'bold'))
    query_label.grid(row=2, column=0, padx=5, pady=(10,2), sticky="ew")    
    query_frame = ttk.Frame(left_frame)
    query_frame.grid(row=3, column=0, padx=5, pady=2, sticky="ew")
   
    label_query_entry = ttk.Label(query_frame, text="Queries:")
    label_query_entry.grid(row=0, column=0, padx=5, pady=2, sticky="e")
    query_entry = ttk.Entry(query_frame)
    query_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    query_entry.insert(0, "hsp90")
    
    button_search_targets = ttk.Button(query_frame, text="Targets Search", command=lambda: start_thread1())
    button_search_targets.grid(row=1, column=0, padx=5, pady=2, sticky="ew")
    button_search_target = ttk.Button(query_frame, text="Molecules Search", command=lambda: start_thread2())
    button_search_target.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    
    label_molecules_descriptors = ttk.Label(left_frame, text="Descriptors Calculation", font=('TkDefaultFont', 10, 'bold'))
    label_molecules_descriptors.grid(row=6, column=0, padx=5, pady=(10,2), sticky="w")
    frame_molecules_descriptors = ttk.Frame(left_frame)
    frame_molecules_descriptors.grid(row=7, column=0, padx=5, pady=2, sticky="w")            

    # Molecule Files
    label_molecules_file = ttk.Label(frame_molecules_descriptors, text="Molecules File", font=('TkDefaultFont', 10))
    label_molecules_file.grid(row=0, column=0, padx=5, pady=2, sticky="w")
    frame_molecules_file = ttk.Frame(frame_molecules_descriptors)
    frame_molecules_file.grid(row=1, column=0, padx=5, pady=2, sticky="w")           

    # default_molecules_file = molecules_files
    entry_molecules_file = ttk.Entry(frame_molecules_file)
    entry_molecules_file.grid(row=0, column=0, padx=5, pady=5)
    button_browse_molecules = ttk.Button(frame_molecules_file, text="Browse", command=lambda: browse_file(entry_molecules_file))
    button_browse_molecules.grid(row=0, column=1, padx=5, pady=2, sticky="w")

    # Entry Optimization
    label_entry_optimization = ttk.Label(frame_molecules_descriptors, text="Optimization Method", font=('TkDefaultFont', 10))
    label_entry_optimization.grid(row=2, column=0, padx=5, pady=(5,2), sticky="w")
    frame_entry_optimization = ttk.Frame(frame_molecules_descriptors)
    frame_entry_optimization.grid(row=3, column=0, padx=5, pady=2, sticky="w")
    optimization_options = ["2D", "3D", "UFF", "MMFF", "QM"]
    entry_optimization_var = tk.StringVar(value=optimization_options[0])

    for i, option in enumerate(optimization_options):
        ttk.Radiobutton(frame_entry_optimization, text=option, value=option, variable=entry_optimization_var).grid(row=i, column=0, padx=5, pady=2, sticky="w")

    # Descriptors
    label_descriptors = ttk.Label(frame_molecules_descriptors, text="Descriptors", font=('TkDefaultFont', 10))
    label_descriptors.grid(row=4, column=0, padx=5, pady=(5,2), sticky="w")
    frame_descriptors = ttk.Frame(frame_molecules_descriptors)
    frame_descriptors.grid(row=5, column=0, padx=5, pady=2, sticky="w")

    descriptors_options = ["2D Descriptors", "3D Descriptors", "Lipinski Descriptors", "Morgan Fingerprints", "MACCS Fingerprints", "Daylight Fingerprints", "Avalon Fingerprints", "Torsion Fingerprints", "PubChem Fingerprints"]
    descriptor_vars = [tk.StringVar(value="1" if i == 0 else "") for i, descriptor in enumerate(descriptors_options)]

    for i, descriptor in enumerate(descriptors_options):
        ttk.Checkbutton(frame_descriptors, text=descriptor, variable=descriptor_vars[i]).grid(row=i, column=0, padx=5, pady=2, sticky="w")

    # Conformer Numbers and Maximum Iteration
    frame_conformer = ttk.Frame(frame_molecules_descriptors)
    frame_conformer.grid(row=6, column=0, padx=5, pady=5, sticky="ew")
    
    ttk.Label(frame_conformer, text="Conformer Numbers:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    default_conformer_number = "10"
    #global conformer_var
    conformer_var = ttk.Entry(frame_conformer)
    conformer_var.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    conformer_var.insert(0, default_conformer_number)

    # Maximum Iteration
    ttk.Label(frame_conformer, text="Maximum Iteration:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    default_max_iteration = "200"
    
    #global max_iters_var
    max_iters_var = ttk.Entry(frame_conformer)
    max_iters_var.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    max_iters_var.insert(0, default_max_iteration)

    # Molecule column
    label_molecule_column = ttk.Label(frame_conformer, text="Molecule Column:")
    label_molecule_column.grid(row=2, column=0, padx=5, pady=2, sticky="w")
    default_molecule_column = "canonical_smiles"
    #global entry_molecule_column 
    entry_molecule_column = ttk.Entry(frame_conformer)
    entry_molecule_column.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
    entry_molecule_column.insert(0, default_molecule_column)

    button_descriptor_calculation = ttk.Button(frame_molecules_descriptors, text="CALCULATE", command=lambda:start_thread3())
    button_descriptor_calculation.grid(row=10, column=0, padx=20, pady=20)

    # Right Frame 
    right_frame = ttk.Frame(frame, padding="10")
    right_frame.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Text Widget for Displaying Results
    result_text = tk.Text(right_frame, wrap="none", bg="#300a24", fg="white", font=("Monospace", 11))
    result_text.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
    
    # Scrollbar Y-axis
    scrollbar_y = ttk.Scrollbar(right_frame, command=result_text.yview)
    result_text.config(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=0, column=1, pady=10, sticky="ns")  # Adjusted column

    # Scrollbar X-axis
    scrollbar_x = ttk.Scrollbar(right_frame, command=result_text.xview, orient=tk.HORIZONTAL)
    result_text.config(xscrollcommand=scrollbar_x.set)
    scrollbar_x.grid(row=1, column=0, padx=10, sticky="ew")  

    # Frame for Progress, Run, Cancel
    frame_progress_run_cancel = ttk.Frame(right_frame)
    frame_progress_run_cancel.grid(column=0, row=2, columnspan=4, pady=20, sticky="w")

    # Label for Progress
    progress_label = ttk.Label(frame_progress_run_cancel, text="Progress:")
    progress_label.grid(column=1, row=0, padx=5, sticky="w")

    # Progress Bar
    progress_bar = ttk.Progressbar(frame_progress_run_cancel, mode="indeterminate", length=200)
    progress_bar.grid(column=2, row=0, padx=5, sticky="ew")

    # Cancel Button
    cancel_button = ttk.Button(frame_progress_run_cancel, text="Cancel", command=exit)
    cancel_button.grid(column=3, row=0, padx=5, sticky="w")
        
    # HelpGen Frame
    help_gen_frame = ttk.Frame(right_frame)
    help_gen_frame.grid(column=0, row=5, pady=30, sticky=tk.E)
        
    # Help Button
    ttk.Button(help_gen_frame, text="?", command=help_getdata).grid(column=0, row=0, pady=5, padx=5)

    # Generate Button
    GEN_button = ttk.Button(help_gen_frame, text="Generate Job Directory", command=generate_job_directory)
    GEN_button.grid(column=1, row=0, pady=5, padx=5)
      
