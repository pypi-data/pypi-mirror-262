import tkinter as tk
import os
from tkinter import filedialog, ttk
from ladock.utility import help_dl, browse_dir, browse_file
from ladock.dl.tf import  generate_tensor_model
from ladock.dl.knn import  generate_knn_model
from threading import Thread
from ladock.nogui import create_dl

class ScrollableFrame:
    def __init__(self, master):
        self.canvas = tk.Canvas(master)
        self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class RowIndex:
    def __init__(self, initial_value):
        self.value = initial_value

    def increment(self):
        self.value += 1
        return self.value

# Create an instance of the RowIndex class
rw = RowIndex(2)

def dl_conf(frame):

    def generate_job_directory():
        job_dir = create_dl()
        print("Job Directory:", job_dir)

    def start_thread():
        # Create a new thread to run the subprocess
        thread = Thread(target=run_dl)                      
        thread.start()
    
    def run_dl():        
        progress_bar.start()
        job_directory_val = job_dir 
        csv_val = path_csv_entry.get()
        columns_to_remove_val = columns_to_remove.get()  
        transformX_val = transformX_var.get()
        scalerX_val = scalerX_var.get()
        all_features_val = all_features_var.get()
        activity_column_val = activity_column.get() 
        logarithmic_val = logarithmic_var.get()
        transformY_val = transformY_var.get()
        scalerY_val = scalerY_var.get()
        plot_label_val = plot_label_var.get()  
        tool_val = tool_var.get()
                
        result_text_value = f"Job directory: {job_directory_val}\n"  
        result_text_value += f"CSV File Data: {csv_val}\n"
        result_text_value += f"Non Feature Columns: {columns_to_remove_val}\n"
        result_text_value += f"Transform X: {transformX_val}\n"
        result_text_value += f"Scaler X: {scalerX_val}\n"
        result_text_value += f"All Features: {all_features_val}\n"
        result_text_value += f"Activity column: {activity_column_val}\n"  
        result_text_value += f"Logarithmic the activity: {logarithmic_val}\n"
        result_text_value += f"Transform Y: {transformY_val}\n"
        result_text_value += f"Scaler Y: {scalerY_val}\n"
        result_text_value += f"Plot Label: {plot_label_val}\n"
        result_text_value += f"Tool Configuration: {tool_val}\n"

        if tool_val == "TensorFlow":  
            epochs_val = epochs_numbers.get()  
            batch_size_val = batch_size.get()
            optimizer_val = optimizer_var.get()
            learning_rate_val = learning_rate.get()
            loss_function_val =loss_var.get()
            
            hidden_units = [unit_entry.get() for unit_entry in units_entry_list]
            out_units = out_units_entry.get()        
            dense_units = hidden_units + [out_units]            
            activation0_val = activation0_var.get()
            
            hidden_activations = [activation_combobox.get() for activation_combobox in activation_combobox_list]
            out_activations = out_activation_var.get()
            dense_activations = hidden_activations + [out_activations]
            patience_val = patience.get()
            
            result_text_value += f"Epochs Numbers: {epochs_val}\n"
            result_text_value += f"Batch Size: {batch_size_val}\n"
            result_text_value += f"Learning Rate: {learning_rate_val}\n"
            result_text_value += f"Optimizer: {optimizer_val}\n"
            result_text_value += f"Loss Function: {loss_function_val}\n"
            result_text_value += f"Dense Units: {dense_units}\n"
            result_text_value += f"Dense Activations: {dense_activations}\n"
            result_text_value += f"Patience: {patience_val}\n"
            
            parameters = {
                'job_directory': job_directory_val,
                'csv': csv_val,
                'columns_to_remove': columns_to_remove_val,
                'transformX': transformX_val,
                'scalerX': scalerX_val,
                'all_features': all_features_val,
                'activity': activity_column_val,
                'logarithmic': logarithmic_val,
                'transformY': transformY_val,
                'scalerY': scalerY_val,
                'plot_label': plot_label_val,
                'epochs': epochs_val,
                'batch_size': batch_size_val,
                'dense_units': dense_units,
                'dense_activations': dense_activations,
                'optimizer': optimizer_val,
                'learning_rate': learning_rate_val,
                'loss_function': loss_function_val,
                'patience': patience_val
            }
            
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result_text_value)            
            generate_tensor_model(result_text, **parameters)
            progress_bar.stop()
                
        elif tool_val == "K-Nearest Neighbors":
            knn_val = int(knn.get())
            result_text_value += f"KNN: {knn_val}\n"
            parameters = {
                'job_directory': job_directory_val,
                'csv': csv_val,
                'columns_to_remove': columns_to_remove_val,
                'transformX': transformX_val,
                'scalerX': scalerX_val,
                'all_features': all_features_val,
                'activity': activity_column_val,
                'logarithmic': logarithmic_val,
                'transformY': transformY_val,
                'scalerY': scalerY_val,
                'plot_label': plot_label_val,
                'knn_value': knn_val
            }
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result_text_value)            
            generate_knn_model(result_text, **parameters)
            progress_bar.stop()
       
    # Left Frame 
    left_frame = ttk.Frame(frame, padding="10")
    left_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Job Directory section
    job_dir_label = ttk.Label(left_frame, text="Job Directory", font=('TkDefaultFont', 10, "bold"))
    job_dir_label.grid(row=0, column=0, padx=5, pady=(10,5), sticky="w")
    job_dir_frame = ttk.Frame(left_frame, )
    job_dir_frame.grid(row=1, column=0, padx=5, sticky="ew")
    job_dir_entry = ttk.Entry(job_dir_frame)
    job_dir_entry.grid(row=0, column=0, padx=5, sticky="ew")

    current_dir = os.getcwd()
    jobdir = os.path.join(current_dir, 'dl')
    if os.path.exists(jobdir):
        default_jobdir = jobdir
    else:
        default_jobdir = "/path/to/job_directory"
        
    job_dir_entry.insert(0, default_jobdir)

    browse_button = ttk.Button(job_dir_frame, text="Browse", command=lambda:browse_dir(job_dir_entry))
    browse_button.grid(row=0, column=1, padx=5)



    # CSV Path
    path_csv_label = ttk.Label(left_frame, text="CSV File Path", font=('TkDefaultFont', 10, "bold"))
    path_csv_label.grid(row=2, column=0, padx=5, pady=(10,5), sticky="w")   
    path_csv_frame = ttk.Frame(left_frame)
    path_csv_frame.grid(row=3, column=0, padx=5, sticky="w")

    path_csv_entry = ttk.Entry(path_csv_frame)
    path_csv_entry.grid(row=0, column=0, padx=5, sticky="ew")

    if not path_csv_entry.get():
        path_csv_entry.insert(0, "/path/to/csv_file.csv")

    browse_csv_button = ttk.Button(path_csv_frame, text="Browse", command=lambda:browse_file(path_csv_entry))
    browse_csv_button.grid(row=0, column=1, padx=5)

    # Features (X) Configuration section
    features_label = ttk.Label(left_frame, text="Features (X) Configuration", font=('TkDefaultFont', 10, "bold"))
    features_label.grid(row=4, column=0, pady=(10,5), padx=5, sticky="ew")
    features_frame = ttk.Frame(left_frame)
    features_frame.grid(row=5, column=0, padx=5, sticky="ew")

    columns_to_remove_label = ttk.Label(features_frame, text="Non Feature Columns:")
    columns_to_remove_label.grid(row=0, column=0, padx=5, sticky="e")

    columns_to_remove = ttk.Entry(features_frame)
    columns_to_remove.grid(row=0, column=1, padx=5, sticky="ew")

    if not columns_to_remove.get():
        columns_to_remove.insert(0, "molecule_chembl_id,standard_value,pref_name,search_term,canonical_smiles")

    # Transform X
    transformX_var = tk.StringVar(value="true")
    transformX_label = ttk.Label(features_frame, text="Transform X:")
    transformX_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    transformX_options = ["true", "false"]    
    transformX_combobox = ttk.Combobox(features_frame, textvariable=transformX_var, values=transformX_options, state="readonly")
    transformX_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    # Scaler X
    scalerX_var = tk.StringVar(value="StandardScaler")
    scaler_label = ttk.Label(features_frame, text="Scaler X:")
    scaler_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    scaler_options = ["MinMaxScaler", "StandardScaler", "Normalizer", "PowerTransformer"]
    scalerX_combobox = ttk.Combobox(features_frame, textvariable=scalerX_var, values=scaler_options, state="readonly")
    scalerX_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Enabled all features
    all_features_var = tk.StringVar(value="true")
    all_features_label = ttk.Label(features_frame, text="Enabled all features:")
    all_features_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    all_features_options = ["true", "false"]
    all_features_combobox = ttk.Combobox(features_frame, textvariable=all_features_var, values=all_features_options, state="readonly")
    all_features_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Label (Y) Configuration section
    label_label = ttk.Label(left_frame, text="Label (Y) Configuration", font=('TkDefaultFont', 10, "bold"))
    label_label.grid(row=6, column=0, pady=(10,5), padx=5, sticky="ew")
    label_frame = ttk.Frame(left_frame)
    label_frame.grid(row=7, column=0, padx=5, sticky="ew")
    activity_label = ttk.Label(label_frame, text="Activity Column:")
    activity_label.grid(row=0, column=0, padx=5, sticky="e")

    activity_column = ttk.Entry(label_frame)
    if not activity_column.get():   
        activity_column.insert(0, "standard_value")
    activity_column.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

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

    plot_label_label = ttk.Label(label_frame, text="Plot Label:")
    plot_label_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")

    plot_label_var = ttk.Entry(label_frame)
    plot_label_var.insert(0, "IC50")
    plot_label_var.grid(row=4, column=1, padx=5, pady=5, sticky="ew")    
 
    # Tools section
    tools_label = ttk.Label(left_frame, text="Tool Options", font=('TkDefaultFont', 10, "bold"))
    tools_label.grid(row=8, column=0, pady=(10,5), padx=5, sticky="ew")
    tools_frame = ttk.Frame(left_frame)
    tools_frame.grid(row=9, column=0, padx=5, sticky="ew")
    tool_options = ["TensorFlow", "K-Nearest Neighbors"]
    tool_var = tk.StringVar(value="TensorFlow")
    tool_combobox = ttk.Combobox(tools_frame, textvariable=tool_var, values=tool_options, state="readonly")
    tool_combobox.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Hyperparameter section (conditionally displayed based on selected tool)
    hyperparameter_frame = ttk.Frame(tools_frame)
    hyperparameter_frame.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

    def create_label_and_entry(parent_frame, row, label_text, default_value):
        label = ttk.Label(parent_frame, text=label_text)
        label.grid(row=row, column=0, padx=5, sticky="e")

        entry = ttk.Entry(parent_frame)
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        return entry

    def create_label_and_entry_ephocs(parent_frame, row, default_value):
        label_text = "Epochs Numbers:"
        return create_label_and_entry(parent_frame, row, label_text, default_value)

    def create_label_and_entry_batch(parent_frame, row, default_value):
        label_text = "Batch Size:"
        return create_label_and_entry(parent_frame, row, label_text, default_value)

    def create_label_and_entry_learning_rate(parent_frame, row, default_value):
        label_text = "Learning Rate:"
        return create_label_and_entry(parent_frame, row, label_text, default_value)
        
    def create_label_and_entry_patience(parent_frame, row, default_value):
        label_text = "Patience:"
        return create_label_and_entry(parent_frame, row, label_text, default_value)


    def show_hyperparameter_section(*args):
        if tool_var.get() == "TensorFlow":
            hyperparameter_frame.grid(pady=5)
        else:
            hyperparameter_frame.grid_remove()

    tool_var.trace("w", show_hyperparameter_section)

    # K-Nearest Neighbors section (conditionally displayed based on selected tool)
    
    def create_label_and_entry_knn(parent_frame, row, default_value):
        label_text = "K-Nearest Neighbors"
        label = ttk.Label(parent_frame, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="e")

        entry = ttk.Entry(parent_frame)
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        return entry
        
    # Inisialisasi variabel global sebelum if statements
    epochs_numbers = None
    batch_size = None
    learning_rate = None
    patience = None

    # Check jika epochs_numbers sudah didefinisikan
    if not epochs_numbers:
        epochs_numbers = create_label_and_entry_ephocs(hyperparameter_frame, 0, "50")
    else:
        entry = create_label_and_entry_ephocs(hyperparameter_frame, 0, "50")
        epochs_numbers.insert(0, entry.get())

    # Check jika batch_size sudah didefinisikan
    if not batch_size: 
        batch_size = create_label_and_entry_batch(hyperparameter_frame, 1, "128")
    else:
        entry = create_label_and_entry_batch(hyperparameter_frame, 1, "128")
        batch_size.insert(0, entry.get())

    # Check jika learning_rate sudah didefinisikan
    if not learning_rate:        
        learning_rate = create_label_and_entry_learning_rate(hyperparameter_frame, 2, "0.01")
    else:
        entry = create_label_and_entry_learning_rate(hyperparameter_frame, 2, "0.01")
        learning_rate.insert(0, entry.get())

   # Check jika learning_rate sudah didefinisikan
    if not patience:        
        patience = create_label_and_entry_patience(hyperparameter_frame, 3, "100")
    else:
        patience = create_label_and_entry_patience(hyperparameter_frame, 3, "100")
        patience.insert(0, entry.get())


    # Optimizer section
    optimizer_label = ttk.Label(hyperparameter_frame, text="Optimizer:")
    optimizer_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
    optimizer_options = ["SGD", "Adam", "RMSProp", "Adagrad", "Adadelta", "Nadam", "FTRL"]    
    optimizer_var = tk.StringVar(value="SGD")
    optimizer_combobox = ttk.Combobox(hyperparameter_frame, textvariable=optimizer_var, values=optimizer_options, state="readonly")
    optimizer_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    # Loss Function section
    loss_label = ttk.Label(hyperparameter_frame, text="Loss Function:")
    loss_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
    loss_options = ["MSE", "MAE", "Cross-entropy", "Hinge"]    
    loss_var = tk.StringVar(value="MSE")
    loss_combobox = ttk.Combobox(hyperparameter_frame, textvariable=loss_var, values=loss_options, state="readonly")
    loss_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

    # Create a new frame (dense_frame) within hyperparameter_frame
    dense_label = ttk.Label(hyperparameter_frame, text="Dense Units:")
    dense_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
    dense_frame = ttk.Frame(hyperparameter_frame)    
    dense_frame.grid(row=9, column=0, columnspan=4, padx=5, pady=5, sticky="ns")
    
    dense_scrollable_frame = ScrollableFrame(dense_frame)
    dense_frame = dense_scrollable_frame.scrollable_frame    
    dense_frame.grid_rowconfigure(0, weight=1)
    
    activation_options = ["relu", "sigmoid", "tanh", "softmax", "linear", "leaky_relu", "prelu", "swish"]
    activation_list = []
            

    def remove_row(row_index):
        units_entry_list[row_index].destroy()
        activation_combobox_list[row_index].destroy()
        remove_row_button_list[row_index].destroy()

        units_entry_list.pop(row_index)
        activation_combobox_list.pop(row_index)
        remove_row_button_list.pop(row_index)

        update_buttons()

    def add_row(row_index):
        global activation_var
        units_entry = ttk.Entry(dense_frame)
        units_entry.grid(row=row_index, column=0, padx=5, sticky="e")  
        units_entry.insert(0, "64")

        activation_var = tk.StringVar(value="relu")
        activation_combobox = ttk.Combobox(dense_frame, textvariable=activation_var, values=activation_options, state="readonly")
        activation_combobox.grid(row=row_index, column=1, padx=5)
        
        remove_row_button = ttk.Button(dense_frame, text="-", command=lambda i=row_index: remove_row(i))
        remove_row_button.grid(row=row_index, column=2, padx=5, sticky="w")

        units_entry_list.insert(row_index, units_entry)
        activation_combobox_list.insert(row_index, activation_combobox)
        remove_row_button_list.insert(row_index, remove_row_button)
        activation_list.insert(row_index, activation_var)
        
        rw.increment()
        update_buttons()
     
        return rw

    def update_buttons():
        for i, button in enumerate(remove_row_button_list):
            button.configure(command=lambda index=i: remove_row(index))

    # Labels for headers
    dense_label = ttk.Label(dense_frame, text="Units")
    dense_label.grid(row=0, column=0, padx=5, sticky="ns")
    activation_label = ttk.Label(dense_frame, text="Activation")
    activation_label.grid(row=0, column=1, padx=5, sticky="ns")
    dense_frame.grid_rowconfigure(0, weight=1)

    # Initial Entry and Combobox for hidden layers
    units_entry = ttk.Entry(dense_frame)
    units_entry.grid(row=1, column=0, padx=5)
    units_entry.insert(0, "64")

    activation0_var = tk.StringVar(value="relu")
    activation0_combobox = ttk.Combobox(dense_frame, textvariable=activation0_var, values=activation_options, state="readonly")
    activation0_combobox.grid(row=1, column=1, padx=5, sticky="ew")

    # Tombol "Add Row"
    add_row_button = ttk.Button(dense_frame, text="+", command=lambda i = rw: add_row(i.value))
    add_row_button.grid(row=1, column=2, padx=5, pady=1, sticky="w")

    # Lists to store objects for each row
    units_entry_list = [units_entry]
    activation_combobox_list = [activation0_combobox]
    remove_row_button_list = [ttk.Button()]

    # Initial Entry and Combobox for output layers
    out_units_entry = ttk.Entry(dense_frame)
    out_units_entry.grid(row=1000, column=0, padx=5, pady=(0,5))
    out_units_entry.insert(0, "1")

    out_activation_var = tk.StringVar(value="linear")
    out_activation_combobox = ttk.Combobox(dense_frame, textvariable=out_activation_var, values=activation_options, state="readonly")
    out_activation_combobox.grid(row=1000, column=1, padx=5, pady=(0,5), sticky="ew")
   
    # KNN section    
    knn_frame = ttk.Label(tools_frame)
    knn_frame.grid(row=2, column=0, pady=5, padx=5, sticky="ew")
    knn_frame.grid_remove()
    
    knn = None

    # Check jika knn sudah didefinisikan
    if not knn:
        knn = create_label_and_entry_knn(knn_frame, 0, "4")
    else:
        entry = create_label_and_entry_knn(knn_frame, 0, "4")
        knn.insert(0, entry.get())

    # Callback to show/hide the K-Nearest Neighbors section
    def show_knn_section(*args):
        if tool_var.get() == "K-Nearest Neighbors":
            knn_frame.grid(pady=5)
        elif tool_var.get() == "TensorFlow":
            knn_frame.grid_remove()

    tool_var.trace("w", show_knn_section)

    
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
    progress_label.grid(column=1, row=0, padx=4, sticky="w")

    # Progress Bar
    progress_bar = ttk.Progressbar(frame_progress_run_cancel, mode="indeterminate", length=100)
    progress_bar.grid(column=2, row=0, padx=5, sticky="ew")

    # Button - RUN
    ttk.Button(frame_progress_run_cancel, text="RUN", command=start_thread).grid(column=0, row=0, padx=5, sticky="w")

    # Cancel Button
    cancel_button = ttk.Button(frame_progress_run_cancel, text="Cancel", command=exit)
    cancel_button.grid(column=3, row=0, padx=5, sticky="w")

    # HelpGen Frame
    help_gen_frame = ttk.Frame(right_frame)
    help_gen_frame.grid(column=0, row=2, pady=30, sticky=tk.E)

    # Help Button
    ttk.Button(help_gen_frame, text="?", command=help_dl).grid(column=0, row=0, pady=5, padx=5)

    # Generate Button
    GEN_button = ttk.Button(help_gen_frame, text="Generate Job Directory", command=generate_job_directory)
    GEN_button.grid(column=1, row=0, pady=5, padx=5)
 

