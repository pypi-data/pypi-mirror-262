import tkinter as tk
from tkinter import ttk, filedialog
from ladock.utility import help_md, browse_file, browse_dir
from ladock.md.gmxprolig import prolig
from ladock.md.gmxliglig import liglig
from ladock.nogui import create_md
import os

def md_conf(frame):
    def generate_job_directory():
        job_dir = create_md()
        print("Job Directory:", job_dir)
    
    def start_thread():
        # Buat thread baru untuk menjalankan subprocess
        thread = Thread(target=run_md)
        thread.start()
        
    def run_md():
        
        # Mengambil nilai variabel-variabel dari widget-widget terkait
        progress_bar.start()
        md_type = md_type_var.get()
        box_type = box_type_var.get()
        distance = distance_entry.get()
        solvent = solvent_entry.get()
        rdd = rdd_entry.get()
        dds = dds_entry.get()
        job_dir = job_dir_entry_var.get()
        if md_type == "Protein-Ligand":
            job_dir = os.path.join(job_dir, "prolig")
        elif md_type == "Ligand-Ligand":
            job_dir = os.path.join(job_dir, "liglig")

        # Simulasikan eksekusi dengan menampilkan nilai variabel-variabel
        result_text_value = f"Configuration Setting:\n\n"        
        result_text_value += f"Simulation Type: {md_type}\nBox Type: {box_type}\nDistance: {distance}\nSolvent: {solvent}\nRDD: {rdd}\nDDS: {dds}\nJob Directory: {job_dir}"

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result_text_value)

        
        # Menyusun parameter untuk fungsi prolig
        parameters = {    
            'box_type': box_type,
            'distance': distance,
            'solvent': solvent,
            'rdd': rdd,
            'dds': dds,
            'current_directory': job_dir, 
        }

        # Memanggil fungsi prolig dengan parameter-parameter yang sudah disusun
        if md_type == "Protein-Ligand":
            prolig(progress_bar, result_text, **parameters)
        elif md_type == "Ligand-Ligand":
            liglig(progress_bar, result_text, **parameters)
        progress_bar.stop()
        
    # Left Frame
    left_frame = ttk.Frame(frame, padding="10", width=350)
    left_frame.grid(column=0, row=0, pady=(10,5), sticky=(tk.W, tk.E, tk.N, tk.S))    
    
    conf_label = ttk.Label(left_frame, text="Molecular Dyamics Configuration", font=('TkDefaultFont', 10, 'bold'))
    conf_label.grid(row=0, column=0, pady=5, padx=5, sticky="ew")    
    conf_frame = ttk.Frame(left_frame)
    conf_frame.grid(column=0, row=1, pady=5, padx=5, sticky="ew")

    # Simulation Type
    md_type_label = ttk.Label(conf_frame, text="Simulation Type")
    md_type_label.grid(row=0, column=0, pady=(5,5), sticky="e")
    md_type_options = ["Protein-Ligand", "Ligand-Ligand"]
    md_type_var = tk.StringVar(value="Protein-Ligand")
    md_type_combobox = ttk.Combobox(conf_frame, textvariable=md_type_var, values=md_type_options, state="readonly")
    md_type_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Box Type
    box_type_label = ttk.Label(conf_frame, text="Box Type")
    box_type_label.grid(row=2, column=0, pady=5, sticky="e")
    box_type_options = ["Triclinic", "Cubic", "Dodecahedron", "Octahedron"]
    box_type_var = tk.StringVar(value="Cubic")
    box_type_combobox = ttk.Combobox(conf_frame, textvariable=box_type_var, values=box_type_options, state="readonly")
    box_type_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")


    # Entry for -d (distance)
    distance_label = ttk.Label(conf_frame, text="Distance")
    distance_label.grid(row=3, column=0, pady=5, sticky="e")
    distance_entry = ttk.Entry(conf_frame)
    distance_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
    distance_entry.insert(0, "1.0")

    # Entry for -cs (coordinate file for solvent)
    solvent_label = ttk.Label(conf_frame, text="Solvent Model")
    solvent_label.grid(row=4, column=0, pady=5, sticky="e")
    solvent_entry = ttk.Entry(conf_frame)
    solvent_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    solvent_entry.insert(0, "spc216.gro")

    # Entry for -rdd
    rdd_frame = ttk.Label(conf_frame, text="RDD")
    rdd_frame.grid(row=5, column=0, pady=5, sticky="e")
    rdd_entry = ttk.Entry(conf_frame)
    rdd_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
    rdd_entry.insert(0, "0")

    # Entry for -dds
    dds_frame = ttk.Label(conf_frame, text="DDS")
    dds_frame.grid(row=6, column=0, pady=5, sticky="e")
    dds_entry = ttk.Entry(conf_frame)
    dds_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
    dds_entry.insert(0, "0.8")
    
    # Entry for job directory with browse button
    job_dir_label = ttk.Label(conf_frame, text="Job Directory")
    job_dir_label.grid(row=7, column=0, pady=5, sticky="w")
    
    current_dir = os.getcwd()
    jobdir = os.path.join(current_dir, 'md')
    if os.path.exists(jobdir):
        default_jobdir = jobdir
    else:
        default_jobdir = "/path/to/job_directory"
    
    job_dir_entry = ttk.Entry(conf_frame, textvariable=default_jobdir)
    job_dir_entry.grid(row=7, column=1, padx=5, pady=(5,0), sticky="ew")
    job_dir_entry.insert(0, default_jobdir)
    
    browse_button = ttk.Button(conf_frame, text="Browse", command=lambda:browse_dir(job_dir_entry))
    browse_button.grid(row=8, column=1, padx=5, sticky="w")

    # Right Frame
    right_frame = ttk.Frame(frame, padding="10")
    right_frame.grid(column=1, row=0, sticky="ew")

    # Text Widget for Displaying Results
    result_frame = ttk.Frame(right_frame)
    result_frame.grid(column=0, row=0, pady=5, padx=5, sticky="ew")
    result_text = tk.Text(result_frame, wrap="none", bg="#300a24", fg="white", font=("Monospace", 11))
    result_text.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
    
    # Scrollbar Y-axis
    scrollbar_y = ttk.Scrollbar(result_frame, command=result_text.yview)
    result_text.config(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=0, column=1, pady=10, sticky="ns")  # Adjusted column

    # Scrollbar X-axis
    scrollbar_x = ttk.Scrollbar(result_frame, command=result_text.xview, orient=tk.HORIZONTAL)
    result_text.config(xscrollcommand=scrollbar_x.set)
    scrollbar_x.grid(row=1, column=0, padx=10, sticky="ew")  

    # Frame for Progress, Run, Cancel
    frame_progress_run_cancel = ttk.Frame(right_frame)
    frame_progress_run_cancel.grid(column=0, row=1, columnspan=4, pady=20, sticky="w")

    # Label for Progress
    progress_label = ttk.Label(frame_progress_run_cancel, text="Progress:")
    progress_label.grid(column=1, row=0, padx=5, sticky="w")

    # Progress Bar
    progress_bar = ttk.Progressbar(frame_progress_run_cancel, mode="indeterminate", length=100)
    progress_bar.grid(column=2, row=0, padx=5, sticky="ew")

    # Button - RUN
    ttk.Button(frame_progress_run_cancel, text="RUN", command=run_md).grid(column=0, row=0, padx=5, sticky="w")

    # Cancel Button
    cancel_button = ttk.Button(frame_progress_run_cancel, text="Cancel", command=exit)
    cancel_button.grid(column=3, row=0, padx=5, sticky="w")

    # HelpGen Frame
    help_gen_frame = ttk.Frame(right_frame)
    help_gen_frame.grid(column=0, row=2, pady=30, sticky=tk.E)

    # Help Button
    ttk.Button(help_gen_frame, text="?", command=help_md).grid(column=0, row=0, pady=5, padx=5)

    # Generate Button
    GEN_button = ttk.Button(help_gen_frame, text="Generate Job Directory", command=generate_job_directory)
    GEN_button.grid(column=1, row=0, pady=5, padx=5)
