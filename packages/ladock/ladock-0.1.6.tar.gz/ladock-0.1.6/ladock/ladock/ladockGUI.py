import tkinter as tk
from tkinter import ttk, filedialog
import os
from ladock.utility import help_dock, browse_file, browse_dir
from ladock.ladock.docking import docking
import threading
from threading import Thread
from ladock.nogui import create_dock

def docking_conf(frame): 

        def generate_job_directory():
            job_dir = create_dock()
            print("Job Directory:", job_dir)
                   
        def start_thread():
            # Buat thread baru untuk menjalankan subprocess
            
            thread = Thread(target=run_ladock)                      
            thread.start()
        
        def run_ladock():
            progress_bar.start()  
            sf_types = [sf_var.get() for sf_var in sf_types_vars if sf_var.get()]
            sf_types = list(filter(lambda x: x != "", sf_types))
            listmode = [mode_var.get() for mode_var in listmode_vars if mode_var.get()]
            listmode = list(filter(lambda x: x != "", listmode))
            distance_of_flexible_residues = distance_var.get()
            elements = elements_var.get()
            arrangement_type = arrangement_var.get()
            box_size = box_size_var.get()
            spacing = spacing_var.get()
            n_poses = n_poses_var.get()
            exhaustiveness = exhaustiveness_var.get()
            cpu = cpu_var.get()
            parallel_simulation = parallel_var.get()
            input_file_saved = input_var.get()
            output_file_saved = output_var.get()
            vina_path = vina_entry.get()
            ad4_path = ad4_entry.get()
            ag4_path = ag4_entry.get()
            adfr_path = adfr_entry.get()
            mgl_path = mgl_entry.get()
            autodockgpu = autodockgpu_entry.get()
            vinagpu = vinagpu_entry.get()
            job_directory = job_dir_entry.get()
            descriptors_calculation = var_descriptors_calculation.get()
            descriptors_list = [descriptor_text.upper() for descriptor_var, descriptor_text in zip(descriptor_vars, descriptors_options) if descriptor_var.get() == "1"]
            optimize_method = entry_optimization_var.get()
            num_conformers = int(conformer_var.get())
            max_iters = int(max_iters_var.get())
            
            mgl_path = mgl_path + "/MGLToolsPckgs/AutoDockTools/Utilities24"      
                                        
            for mode in listmode:
                if mode == "Flexible":
                    distance_of_flexible_residues = distance_var.get()
                else:
                    pass
            
            max_workers = os.cpu_count() // cpu  
            agfr = adfr_path + "/agfr"
            adfr = adfr_path + "/adfr"
            prepare_ligand = os.path.join(mgl_path, "prepare_ligand4.py")
            prepare_receptor = os.path.join(mgl_path, "prepare_receptor4.py")
            prepare_gpf = os.path.join(mgl_path, "prepare_gpf4.py")
            prepare_flexreceptor = os.path.join(mgl_path, "prepare_flexreceptor4.py")
            
            result_text.delete(1.0, tk.END)

            # Title
            result_text.insert(tk.END, "Docking Configurations:\n\n")

            # Inserted Text
            result_text.insert(tk.END, f"SF Types: {sf_types}\n")
            result_text.insert(tk.END, f"List Mode: {listmode}\n")           
            result_text.insert(tk.END, f"Distance of Flexible Residues: {distance_of_flexible_residues}\n")
            result_text.insert(tk.END, f"Number of ligand(s): {elements}\n")
            result_text.insert(tk.END, f"Arrangement Type: {arrangement_type}\n")            
            result_text.insert(tk.END, f"Box Size: {box_size}\n")
            result_text.insert(tk.END, f"Spacing: {spacing}\n")
            result_text.insert(tk.END, f"N Poses: {n_poses}\n")
            result_text.insert(tk.END, f"Exhaustiveness: {exhaustiveness}\n")
            result_text.insert(tk.END, f"CPU: {cpu}\n")
            result_text.insert(tk.END, f"Parallel Simulation: {parallel_simulation}\n")
            result_text.insert(tk.END, f"Input File Saved: {input_file_saved}\n")
            result_text.insert(tk.END, f"Output File Saved: {output_file_saved}\n")
            result_text.insert(tk.END, f"Vina Path: {vina_path}\n")
            result_text.insert(tk.END, f"AD4 Path: {ad4_path}\n")
            result_text.insert(tk.END, f"AG4 Path: {ag4_path}\n")
            result_text.insert(tk.END, f"ADFR Path: {adfr_path}\n")
            result_text.insert(tk.END, f"MGL Path: {mgl_path}\n")
            result_text.insert(tk.END, f"AutoDockGPU: {autodockgpu}\n")
            result_text.insert(tk.END, f"VinaGPU: {vinagpu}\n")
            result_text.insert(tk.END, f"Job Directory: {job_directory}\n")
            result_text.insert(tk.END, f"MGL Path: {mgl_path}\n")
            result_text.insert(tk.END, f"Max Workers: {max_workers}\n")
            result_text.insert(tk.END, f"AGFR Path: {agfr}\n")
            result_text.insert(tk.END, f"ADFR Path: {adfr}\n")
            result_text.insert(tk.END, f"Prepare Ligand: {prepare_ligand}\n")
            result_text.insert(tk.END, f"Prepare Receptor: {prepare_receptor}\n")
            result_text.insert(tk.END, f"Prepare GPF: {prepare_gpf}\n")
            result_text.insert(tk.END, f"Prepare FlexReceptor: {prepare_flexreceptor}\n")
            result_text.insert(tk.END, f"Descriptors Calculation: {descriptors_calculation}\n")
            
            result_text.insert(tk.END, f"Descriptors List: {descriptors_list}\n")
            result_text.insert(tk.END, f"optimize_method: {optimize_method}\n")
            result_text.insert(tk.END, f"Number of conformers: {num_conformers}\n")
            result_text.insert(tk.END, f"Max iterations: {max_iters}\n")
            
            
            result_text.insert(tk.END, "\n\n")
            result_text.yview(tk.END)
             
            parameters = {
                'sf_types': sf_types,
                'listmode': listmode,
                'distance': distance_of_flexible_residues,
                'arrangement_type': arrangement_type,
                'elements': elements,
                'box_size': box_size,
                'spacing': spacing,
                'n_poses': n_poses,
                'exhaustiveness': exhaustiveness,
                'cpu': cpu,
                'parallel_simulation': parallel_simulation,
                'input_file_saved': input_file_saved,
                'output_file_saved': output_file_saved,
                'vina_path': vina_path,
                'ad4_path': ad4_path,
                'ag4_path': ag4_path,
                'autodockgpu': autodockgpu,
                'vinagpu': vinagpu,
                'job_directory': job_directory,
                'max_workers': max_workers,
                'agfr': agfr,
                'adfr': adfr,              
                'prepare_ligand': prepare_ligand,
                'prepare_receptor': prepare_receptor,
                'prepare_gpf': prepare_gpf,
                'prepare_flexreceptor': prepare_flexreceptor,
                'current_directory': job_directory, 
                'descriptors_calculation': descriptors_calculation,
                'descriptors': descriptors_list,
                'optimize_geometry': optimize_method,
                'num_conformers': num_conformers,
                'maxIters': max_iters,
            }                     
            print(parameters)
            docking(result_text, **parameters) 
            progress_bar.stop()
       
        current_directory = os.getcwd()
        jobdir = os.path.join(current_directory, 'dock')
        if os.path.exists(jobdir):
            default_jobdir = jobdir
        else:
            default_jobdir = "/path/to/job_directory"
       
        default_vinagpu = ""
        default_ad4 = "autodock4"
        default_ag4 = "autogrid4"
        default_vina = "vina"
        default_mgl = "/home/<user>/MGLTools-1.5.6"
        default_autodockgpu = ""
        default_adfr = "/home/<user>/ADFRsuite-1.0/bin"


 
        # Left Frame
        left_frame = ttk.Frame(frame, padding="10", width=350)
        left_frame.grid(column=0, row=0, pady=(10,5), sticky=(tk.W, tk.E, tk.N, tk.S))   
        
        # Score function section
        sf_label = ttk.Label(left_frame, text="Score Function", font=('TkDefaultFont', 10, 'bold'))
        sf_label.grid(column=0, row=0, pady=(5, 0), sticky="ew")
        sf_frame = ttk.Frame(left_frame)
        sf_frame.grid(column=0, row=1, pady=(5, 5), sticky="ew")
        
        sf_types = ["Vina", "Vinardo", "AD4", "Vina GPU", "Vinardo GPU", "AD4 GPU"]
        default_checked_sf_types = ["Vina", "Vinardo", "AD4"]
        sf_types_vars = []

        if not sf_types_vars:
            sf_types_vars = [tk.StringVar() if sf_type not in default_checked_sf_types else tk.StringVar(value=sf_type.lower()) for sf_type in sf_types]

        def create_score_function_checkbuttons():
            checkbuttons = []
            rows = 2
            columns = 3

            for idx, (sf_type, sf_var) in enumerate(zip(sf_types, sf_types_vars)):
                row = idx // columns
                col = idx % columns

                checkbutton = ttk.Checkbutton(sf_frame, text=sf_type, variable=sf_var, onvalue=sf_type.lower(), offvalue="")
                checkbutton.grid(row=row + 1, column=col, sticky=tk.W, padx=5, pady=5)  # Adjusted row value

                checkbuttons.append(checkbutton)

            return sf_types_vars

        sf_types_vars = create_score_function_checkbuttons()
 
        # Mode section
        mode_label = ttk.Label(left_frame, text="Receptor Mode", font=('TkDefaultFont', 10, 'bold'))
        mode_label.grid(column=0, row=2, pady=(10, 0), sticky="ew")
        mode_frame = ttk.Frame(left_frame)
        mode_frame.grid(column=0, row=3, pady=(5, 5), sticky="ew")

        listmode = ["Rigid", "Flexible"]
        default_checked_listmode = ["Rigid"]
        listmode_vars = []

        def print_change(*args):
            values = [var.get() for var in listmode_vars if var.get()]  # Only include non-empty values
            if 'flexible' in values:
                distance_entry["state"] = "normal"  
            else:
                distance_entry["state"] = "disabled"

        # Create the Checkbuttons
        if not listmode_vars:
            listmode_vars = [tk.StringVar() if mode not in default_checked_listmode else tk.StringVar(value=mode.lower()) for mode in listmode]

        def create_mode_checkbuttons():
            checkbuttons = []
            for idx, (mode, mode_var) in enumerate(zip(listmode, listmode_vars)):
                checkbutton = ttk.Checkbutton(mode_frame, text=mode, variable=mode_var, onvalue=mode.lower().replace(" ", ""), offvalue="")
                checkbutton.grid(column=idx, row=0, sticky=tk.W, padx=5, pady=5)  
                checkbuttons.append(checkbutton)

            return checkbuttons

        mode_checkbuttons = create_mode_checkbuttons()

        # Create the distance entry widget
        distance_label = ttk.Label(mode_frame, text="Distance of Flexible Residues", font=('TkDefaultFont', 9))
        distance_label.grid(column=1, row=4, sticky="ew", padx=5, pady=5)

        distance_var = tk.IntVar(value=2)
        distance_entry = ttk.Entry(mode_frame, textvariable=distance_var, state="disabled")
        distance_entry.grid(column=1, row=5, sticky="ew", pady=5, padx=5)

        # Add trace to each variable
        for var in listmode_vars:
            var.trace_add("write", print_change)

        # Initial call to print_change to set the initial state
        print_change()


        # Methods section
        methods_label = ttk.Label(left_frame, text="Single/Multiple Ligands Simultaneous Docking", font=('TkDefaultFont', 10, 'bold'))
        methods_label.grid(column=0, row=4, pady=(10, 0), sticky="ew")
        methods_frame = ttk.Frame(left_frame)
        methods_frame.grid(column=0, row=5, pady=(5, 5), sticky="ew")

        # Elements
        elements_label = ttk.Label(methods_frame, text="Number of Ligand(s)", font=('TkDefaultFont', 9))
        elements_label.grid(column=0, row=0, sticky="w", padx=5)

        elements_var = tk.StringVar(value="1")
        ttk.Entry(methods_frame, textvariable=elements_var).grid(column=1, row=0, sticky="ew", pady=5)

        # OptionMenu for Arrangement
        arrangement_label = ttk.Label(methods_frame, text="Arrangement Type", font=('TkDefaultFont', 9))
        arrangement_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        arrangement_options = ["combination", "permutation"]
        arrangement_var = tk.StringVar(value="combination")
        arrangement_option_menu = ttk.Combobox(methods_frame, textvariable=arrangement_var, values=arrangement_options, state="readonly")
        arrangement_option_menu.grid(row=  1, column=1, pady=5, sticky="ew")

        # Docking setting section
        docking_frame = ttk.Label(left_frame, text="Docking Setting", font=('TkDefaultFont', 10, 'bold'))
        docking_frame.grid(row=6, column=0, pady=(10, 5), sticky="ew")
        docking_frame = ttk.Frame(left_frame)
        docking_frame.grid(row=7, column=0, pady=(5, 5), sticky="ew")

        # Box Size Frame
        box_size_label = ttk.Label(docking_frame, text="Box Size")
        box_size_label.grid(column=0, row=0, sticky="e", pady=5, padx=5)
        box_size_var = tk.StringVar(value="40,40,40")
        ttk.Entry(docking_frame, textvariable=box_size_var).grid(column=1, row=0, sticky="ew", pady=5, padx=5)

        # Spacing Frame
        spacing_label = ttk.Label(docking_frame, text="Spacing")
        spacing_label.grid(column=0, row=1, sticky="e", pady=5, padx=5)
        spacing_var = tk.DoubleVar(value=0.75)
        ttk.Entry(docking_frame, textvariable=spacing_var).grid(column=1, row=1, sticky="ew", pady=5, padx=5)

        # N Poses Frame
        n_poses_label = ttk.Label(docking_frame, text="N Poses")
        n_poses_label.grid(column=0, row=2, sticky="e", pady=5, padx=5)
        n_poses_var = tk.IntVar(value=10)
        ttk.Entry(docking_frame, textvariable=n_poses_var).grid(column=1, row=2, sticky="ew", pady=5, padx=5)

        # Exhaustiveness Frame
        exhaustiveness_label = ttk.Label(docking_frame, text="Exhaustiveness")
        exhaustiveness_label.grid(column=0, row=3, sticky="e", pady=5, padx=5)
        exhaustiveness_var = tk.IntVar(value=1)
        ttk.Entry(docking_frame, textvariable=exhaustiveness_var).grid(column=1, row=3, sticky="ew", pady=5, padx=5)
        
        # CPU Frame
        cpu_label = ttk.Label(docking_frame, text="CPU")
        cpu_label.grid(column=0, row=4, sticky="e", pady=5, padx=5)
        cpu_var = tk.IntVar(value=6)
        ttk.Entry(docking_frame, textvariable=cpu_var).grid(column=1, row=4, sticky="ew", pady=5, padx=5)

        # Additional setting section
        add_setting_frame = ttk.Label(left_frame, text="Additional Setting", font=('TkDefaultFont', 10, 'bold'))
        add_setting_frame.grid(row=8, column=0, pady=(10, 5), sticky="ew")
        add_setting_frame = ttk.Frame(left_frame)
        add_setting_frame.grid(row=9, column=0, pady=(5, 5), sticky="ew")

        # Parallel Simulation
        parallel_label = ttk.Label(add_setting_frame, text="Parallel Simulation:")
        parallel_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        parallel_options = ["true", "false"]
        parallel_var = tk.StringVar(value="false")

        parallel_option_menu = ttk.Combobox(add_setting_frame, textvariable=parallel_var, values=parallel_options, state="readonly")
        parallel_option_menu.grid(row=0, column=1, pady=5, sticky="w")


        # Input file saved
        input_file_label = ttk.Label(add_setting_frame, text="Input File Saved:")
        input_file_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        input_file_options = ["true", "false"]  
        input_var = tk.StringVar(value="false")
        input_file_option_menu = ttk.Combobox(add_setting_frame, textvariable=input_var, values=input_file_options, state="readonly")
        input_file_option_menu.grid(row=1, column=1, sticky="w", pady=5)

        # Output file saved
        output_file_label = ttk.Label(add_setting_frame, text="Output File Saved:")
        output_file_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        output_file_options = ["true", "false"]  
        output_var = tk.StringVar(value="false")
        output_file_option_menu = ttk.Combobox(add_setting_frame, textvariable=output_var, values=output_file_options, state="readonly")
        output_file_option_menu.grid(row=2, column=1, sticky="w", pady=5)

        # Installation Path section
        import_frame = ttk.Label(left_frame, text="Installation Path", font=('TkDefaultFont', 10, 'bold'))
        import_frame.grid(row=10, column=0, pady=(10, 5), sticky="ew")        
        import_frame = ttk.Frame(left_frame)
        import_frame.grid(row=11, column=0, pady=(5, 5), sticky="ew")

        # Label - AD4 Path
        ad4_label = ttk.Label(import_frame, text="AutoDock4")
        ad4_label.grid(column=0, row=13, sticky=tk.E, pady=5, padx=5)
        ad4_entry = ttk.Entry(import_frame, width=20)
        ad4_entry.grid(column=1, row=13, pady=5, padx=5, sticky=tk.W)
        ad4_entry.insert(0, default_ad4)
        browse_button = ttk.Button(import_frame, text="Browse", command=lambda:browse_file(ad4_entry))
        browse_button.grid(column=2, row=13, sticky=tk.W, pady=5, padx=5)

        # Label - AG4 Path
        ag4_label = ttk.Label(import_frame, text="AutoGrid4")
        ag4_label.grid(column=0, row=14, sticky=tk.E, pady=5, padx=5)
        ag4_entry = ttk.Entry(import_frame, width=20)
        ag4_entry.grid(column=1, row=14, pady=5, padx=5, sticky=tk.W)
        ag4_entry.insert(0, default_ag4)
        browse_button = ttk.Button(import_frame, text="Browse", command=lambda:browse_file(ad4_entry))
        browse_button.grid(column=2, row=14, sticky=tk.W, pady=5, padx=5)

        # Label - Vina Path
        vina_label = ttk.Label(import_frame, text="Vina")
        vina_label.grid(column=0, row=15, sticky=tk.E, pady=5, padx=5)
        vina_entry = ttk.Entry(import_frame, width=20)
        vina_entry.grid(column=1, row=15, pady=5, padx=5, sticky=tk.W)
        vina_entry.insert(0, default_vina)
        browse_button = ttk.Button(import_frame, text="Browse", command=lambda:browse_file(vina_entry))
        browse_button.grid(column=2, row=15, sticky=tk.W, pady=5, padx=5)
        
        # Label - ADFR Path
        adfr_label = ttk.Label(import_frame, text="ADFR")
        adfr_label.grid(column=0, row=16, sticky=tk.E, pady=5, padx=5)
        adfr_entry = ttk.Entry(import_frame, width=20)
        adfr_entry.grid(column=1, row=16, pady=5, padx=5, sticky=tk.W)
        adfr_entry.insert(0, default_adfr)
        browse_button = ttk.Button(import_frame, text="Browse", command=lambda:browse_dir(adfr_entry))
        browse_button.grid(column=2, row=16, sticky=tk.W, pady=5, padx=5)

        # Label - MGL Path
        mgl_label = ttk.Label(import_frame, text="MGLTools")
        mgl_label.grid(column=0, row=17, sticky=tk.E, pady=5, padx=5)
        mgl_entry = ttk.Entry(import_frame, width=20)
        mgl_entry.grid(column=1, row=17, pady=5, padx=5, sticky=tk.W)
        mgl_entry.insert(0, default_mgl)
        browse_button = ttk.Button(import_frame, text="Browse", command=lambda:browse_dir(mgl_entry))
        browse_button.grid(column=2, row=17, sticky=tk.W, pady=5, padx=5)
        
        # Label - AD4GPU Path
        autodockgpu_label = ttk.Label(import_frame, text="AutoDock GPU")
        autodockgpu_label.grid(column=0, row=18, sticky=tk.E, pady=5, padx=5)
        autodockgpu_entry = ttk.Entry(import_frame, width=20)
        autodockgpu_entry.grid(column=1, row=18, pady=5, padx=5, sticky=tk.W)
        autodockgpu_entry.insert(0, default_autodockgpu)
        browse_button = ttk.Button(import_frame, text="Browse", command=lambda:browse_file(autodockgpu_entry))
        browse_button.grid(column=2, row=18, sticky=tk.W, pady=5, padx=5)
        
        # Label - Vina GPU
        vinagpu_label = ttk.Label(import_frame, text="Vina GPU")
        vinagpu_label.grid(column=0, row=19, sticky=tk.E, pady=5, padx=5)
        vinagpu_entry = ttk.Entry(import_frame, width=20)
        vinagpu_entry.grid(column=1, row=19, pady=5, padx=5, sticky=tk.W)
        vinagpu_entry.insert(0, default_vinagpu)
        browse_button = ttk.Button(import_frame, text="Browse", command=lambda:browse_file(vinagpu_entry))
        browse_button.grid(column=2, row=19, sticky=tk.W, pady=5, padx=5)

        # Job Directory
        job_dir_label = ttk.Label(import_frame, text="Job Directory")
        job_dir_label.grid(column=0, row=25, sticky=tk.E, pady=5, padx=5)
        job_dir_entry = ttk.Entry(import_frame, width=20)
        job_dir_entry.grid(column=1, row=25, pady=(0, 3), padx=5, sticky=tk.W)
        job_dir_entry.insert(0, default_jobdir)
        
        # Right Frame
        right_frame = ttk.Frame(frame, padding="10")
        right_frame.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        def toggle_descriptors():
            if var_descriptors_calculation.get():
                frame_molecules_descriptors.grid()
            else:
                frame_molecules_descriptors.grid_remove()

        label_molecules_descriptors = ttk.Label(right_frame, text="Descriptors Calculation", font=('TkDefaultFont', 10, 'bold'))
        label_molecules_descriptors.grid(row=0, column=0, padx=5, pady=(10,2), sticky="w")

        var_descriptors_calculation = tk.BooleanVar()
        checkbox_descriptors_calculation = ttk.Checkbutton(right_frame, text="Enabling Descriptors Calculation", variable=var_descriptors_calculation, command=toggle_descriptors)
        checkbox_descriptors_calculation.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        frame_molecules_descriptors = ttk.Frame(right_frame)
        frame_molecules_descriptors.grid(row=2, column=0, padx=5, pady=5, sticky="w") 
        frame_molecules_descriptors.grid_remove()           

        # Entry Optimization
        label_entry_optimization = ttk.Label(frame_molecules_descriptors, text="Optimization Method", font=('TkDefaultFont', 10))
        label_entry_optimization.grid(row=0, column=0, padx=5, pady=(5,2), sticky="w")
        frame_entry_optimization = ttk.Frame(frame_molecules_descriptors)
        frame_entry_optimization.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        optimization_options = ["2D", "3D", "UFF", "MMFF", "QM"]
        entry_optimization_var = tk.StringVar(value=optimization_options[0])

        for i, option in enumerate(optimization_options):
            ttk.Radiobutton(frame_entry_optimization, text=option, value=option, variable=entry_optimization_var).grid(row=i, column=0, padx=5, pady=2, sticky="w")

        # Descriptors
        label_descriptors = ttk.Label(frame_molecules_descriptors, text="Descriptors", font=('TkDefaultFont', 10))
        label_descriptors.grid(row=2, column=0, padx=5, pady=(5,2), sticky="w")
        frame_descriptors = ttk.Frame(frame_molecules_descriptors)
        frame_descriptors.grid(row=3, column=0, padx=5, pady=2, sticky="w")

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

        # Text Widget for Displaying Results
        result_frame = ttk.Frame(right_frame)        
        result_frame.grid(column=0, row=3, pady=5, padx=5, sticky="ew")
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
        frame_progress_run_cancel.grid(column=0, row=4, columnspan=4, pady=20, sticky="w")

        # Label for Progress
        progress_label = ttk.Label(frame_progress_run_cancel, text="Progress:")
        progress_label.grid(column=1, row=0, padx=5, sticky="w")

        # Progress Bar
        progress_bar = ttk.Progressbar(frame_progress_run_cancel, mode="indeterminate", length=100)
        progress_bar.grid(column=2, row=0, padx=5, sticky="ew")

        # Button - RUN1
        ttk.Button(frame_progress_run_cancel, text="RUN", command=start_thread).grid(column=0, row=0, padx=5, sticky="w")

        # Cancel Button1
        cancel_button1 = ttk.Button(frame_progress_run_cancel, text="Cancel", command=exit)
        cancel_button1.grid(column=3, row=0, padx=5, sticky="w")
        
        # HelpGen frame
        help_gen_frame = ttk.Frame(right_frame)
        help_gen_frame.grid(column=0, row=5, pady=30, sticky=tk.E)
        
        # Help Button1
        ttk.Button(help_gen_frame, text="?", command=help_dock).grid(column=0, row=0, pady=5, padx=5)

        # Generate Button1
        GEN_button1 = ttk.Button(help_gen_frame, text="Generate Job Directory", command=generate_job_directory)
        GEN_button1.grid(column=1, row=0, pady=5, padx=5)
 

         


        browse_button = ttk.Button(import_frame, text="Browse", command=lambda:browse_dir(job_dir_entry))
        browse_button.grid(column=2, row=25, sticky=tk.W, pady=(0, 3), padx=5)
        
