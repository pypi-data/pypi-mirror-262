import tkinter as tk
import os, glob
from tkinter import ttk, filedialog
from ladock.utility import help_test, browse_file, browse_dir
from threading import Thread
from ladock.utility import browse_dir, browse_file, help_test
from ladock.test.testing_dl import testing
from ladock.nogui import create_test

def test_conf(frame):
        def generate_job_directory():
            job_dir = create_test()
            print("Job Directory:", job_dir)

        def start_thread():            
            thread = Thread(target=run_test)
            thread.start()
            
               
        def run_test():
            progress_bar.start()
            model = model_var.get()
            datatest = datatest_var.get()
            descriptors = [descriptor_text.upper() for descriptor_var, descriptor_text in zip(descriptor_vars, descriptors_text) if descriptor_var.get() == "1"]
            method = methods_var.get()
            conformer = conformer_var.get()
            iteration = iteration_var.get()
            transformX = transformX_var.get()
            scalerX = scalerX_var.get()
            logarithmic = logarithmic_var.get()
            transformY = transformY_var.get()
            scalerY = scalerY_var.get()
            job_dir = job_dir_entry()
            
            result_text.delete(1.0, tk.END)  # Menghapus konten sebelumnya di result_text
            
            # Menambahkan konfigurasi ke dalam result_text
            result_text.insert(tk.END, "Configuration of Testing Deep Learning Model:\n\n")
            result_text.insert(tk.END, f"Model: {model}\n")
            result_text.insert(tk.END, f"Datatest Directory: {datatest}\n")
            result_text.insert(tk.END, f"Descriptors: {descriptors}\n")
            result_text.insert(tk.END, f"Methods: {method}\n")
            result_text.insert(tk.END, f"Conformer Numbers: {conformer}\n")
            result_text.insert(tk.END, f"Maximum Iteration: {iteration}\n")
            result_text.insert(tk.END, f"TransformX: {transformX}\n")
            result_text.insert(tk.END, f"ScalerX: {scalerX}\n")
            result_text.insert(tk.END, f"Logarithmic: {logarithmic}\n")
            result_text.insert(tk.END, f"TransformY: {transformY}\n")
            result_text.insert(tk.END, f"ScalerY: {scalerY}\n")
            result_text.insert(tk.END, f"Job directory: {job_dir}\n")
            
            result_text.insert(tk.END, "\n")  # Spasi antara konfigurasi dan hasil lainnya
            
            testing(model, datatest, descriptors, method, conformer, iteration, transformX, scalerX, logarithmic, transformY, scalerY, job_dir, progress_bar, result_text)
            progress_bar.stop()
   
        # Left Frame 
        left_frame = ttk.Frame(frame, padding="10")
        left_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        current_dir = os.getcwd()
        jobdir = os.path.join(current_dir, 'test')
        model_files = glob.glob(os.path.join(jobdir, "*.keras"))
        
        if model_files:
            default_model = model_files[0]
        else:
            default_model = "/path/to/model_file.keras" 

        model_label = ttk.Label(left_frame, text="Model Path", font=('TkDefaultFont', 10, 'bold'))
        model_label.grid(row=0, column=0, padx=5, pady=(10,5), sticky='w')
        model_frame = ttk.Frame(left_frame)
        model_frame.grid(row=1, column=0, padx=5, sticky='w')
        
        model_entry = ttk.Entry(model_frame)
        model_entry.grid(row=0, column=0, padx=5, sticky='w')
        model_entry.insert(0, default_model)
        
        model_button = ttk.Button(model_frame, text="Browse", command=lambda: browse_file(model_entry))
        model_button.grid(row=0, column=1, padx=5, sticky='w')

        datatest_label = ttk.Label(left_frame, text="Molecules Test Directory and Optimization Set", font=('TkDefaultFont', 10, 'bold'))
        datatest_label.grid(row=2, column=0, padx=5, pady=(10,5), sticky='w')
        datatest_frame = ttk.Frame(left_frame)
        datatest_frame.grid(row=3, column=0, padx=5, sticky='w')
        

        if os.path.exists(jobdir):
            default_jobdir = jobdir
        else:
            default_jobdir = "/path/to/job_directory"
            

        datatest_entry = ttk.Entry(datatest_frame)
        datatest_entry.grid(row=0, column=0, padx=5, sticky="ew")
        datatest_entry.insert(0, default_jobdir)
        
        datatest_button = ttk.Button(datatest_frame, text="Browse", command=lambda: browse_dir(datatest_entry))
        datatest_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        methods_label = ttk.Label(datatest_frame, text="Optimization Method:")
        methods_label.grid(row=1, column=0, padx=5, sticky='e')
        methods_text = ["2D", "3D", "UFF", "MFF", "QM"]
        methods_var = tk.StringVar(value="2D")

        for i, method in enumerate(methods_text):
            ttk.Radiobutton(datatest_frame, text=method, variable=methods_var, value=method).grid(row=i+1, column=1, padx=5, sticky='w')

        conformer_label = ttk.Label(datatest_frame, text="Conformer Numbers:")
        conformer_label.grid(row=6, column=0, padx=5, pady=5, sticky='e')
        conformer_var = tk.IntVar(value=20)
        conformer_entry = ttk.Entry(datatest_frame, textvariable=conformer_var)
        conformer_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        iteration_label = ttk.Label(datatest_frame, text="Maximum Iteration:")
        iteration_label.grid(row=7, column=0, padx=5, pady=5, sticky='e')
        iteration_var = tk.IntVar(value=300)
        iteration_entry = ttk.Entry(datatest_frame, textvariable=iteration_var)
        iteration_entry.grid(row=7, column=1, padx=5, pady=5, sticky='w')
        
        # Descriptors (X) Configuration section
        features_label = ttk.Label(left_frame, text="Descriptors (X)", font=('TkDefaultFont', 10, "bold"))
        features_label.grid(row=4, column=0, pady=(10,5), padx=5, sticky="ew")
        features_frame = ttk.Frame(left_frame)
        features_frame.grid(row=5, column=0, padx=5, sticky="ew")

        # Transform X
        transformX_var = tk.StringVar(value="true")
        transformX_label = ttk.Label(features_frame, text="Transform X:")
        transformX_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        transformX_options = ["true", "false"]    
        transformX_combobox = ttk.Combobox(features_frame, textvariable=transformX_var, values=transformX_options, state="readonly")
        transformX_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Scaler X
        scalerX_var = tk.StringVar(value="StandardScaler")
        scaler_label = ttk.Label(features_frame, text="Scaler X:")
        scaler_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        scaler_options = ["MinMaxScaler", "StandardScaler", "Normalizer", "PowerTransformer"]
        scalerX_combobox = ttk.Combobox(features_frame, textvariable=scalerX_var, values=scaler_options, state="readonly")
        scalerX_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        label_descriptors = ttk.Label(features_frame, text="Descriptors:")
        label_descriptors.grid(row=3, column=0, padx=5, sticky="e")
        frame_descriptors = ttk.Frame(features_frame)
        frame_descriptors.grid(row=3, column=1, padx=5, sticky="ew")
        
        descriptors_text = ["2D Descriptors", "3D Descriptors", "Lipinski Descriptors", "Morgan Fingerprints", "MACCS Fingerprints", "Daylight Fingerprints", "Avalon Fingerprints", "Torsion Fingerprints", "PubChem Fingerprints"]
        descriptor_vars = [tk.StringVar(value=descriptor.upper()) for descriptor in descriptors_text]

        for i, descriptor in enumerate(descriptors_text):
           ttk.Checkbutton(features_frame, text=descriptor, variable=descriptor_vars[i]).grid(row=i+3, column=1, padx=5, sticky="w")

        # Label (Y) Configuration section
        label_label = ttk.Label(left_frame, text="Label (Y) Configuration", font=('TkDefaultFont', 10, "bold"))
        label_label.grid(row=6, column=0, pady=(10,5), padx=5, sticky="ew")
        label_frame = ttk.Frame(left_frame)
        label_frame.grid(row=7, column=0, padx=5, sticky="ew")

        # Logarithmic
        logarithmic_var = tk.StringVar(value="true")
        logarithmic_label = ttk.Label(label_frame, text="Logarithmic:")
        logarithmic_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        logarithmic_options = ["true", "false"]
        logarithmic_combobox = ttk.Combobox(label_frame, textvariable=logarithmic_var, values=logarithmic_options, state="readonly")
        logarithmic_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Transform Y
        transformY_var = tk.StringVar(value="true")
        transformY_label = ttk.Label(label_frame, text="Transform Y:")
        transformY_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        transformY_options = ["true", "false"]
        transformY_combobox = ttk.Combobox(label_frame, textvariable=transformY_var, values=transformY_options, state="readonly")
        transformY_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Scaler Y
        scalerY_label = ttk.Label(label_frame, text="Scaler Y:")
        scalerY_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        scalerY_options = ["MinMaxScaler", "StandardScaler", "Normalizer", "PowerTransformer"]
        scalerY_var = tk.StringVar(value="StandardScaler")
        scalerY_combobox = ttk.Combobox(label_frame, textvariable=scalerY_var, values=scalerY_options, state="readonly")
        scalerY_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")



        # Menyesuaikan konfigurasi grid untuk menghindari tumpang tindih
        left_frame.grid_rowconfigure(8, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
  
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
        progress_bar = ttk.Progressbar(frame_progress_run_cancel, mode="indeterminate", length=100)
        progress_bar.grid(column=2, row=0, padx=5, sticky="ew")

        # Button - RUN
        ttk.Button(frame_progress_run_cancel, text="RUN", command=start_thread).grid(column=0, row=0, padx=5, sticky="w")

        # Cancel Button
        cancel_button = ttk.Button(frame_progress_run_cancel, text="Cancel", command=exit)
        cancel_button.grid(column=3, row=0, padx=5, sticky="w")
        
        # HelpGen frame
        help_gen_frame = ttk.Label(right_frame)
        help_gen_frame.grid(column=0, row=3, pady=30, sticky=tk.E)
        
        # Help Button
        ttk.Button(help_gen_frame, text="?", command=help_test).grid(column=0, row=3, pady=30, padx=5)
 
        # Generate Button
        GEN_button = ttk.Button(help_gen_frame, text="Generate Job Directory", command=generate_job_directory)
        GEN_button.grid(column=1, row=3, pady=5, padx=5)
