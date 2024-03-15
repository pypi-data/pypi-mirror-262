import os
import shutil
import glob
import subprocess
import argparse

main_directory = os.path.dirname(os.path.abspath(__file__))

# Direktori untuk setiap modul
dock_directory = os.path.join(main_directory, "ladock")
md_directory = os.path.join(main_directory, "md")
getdata_directory = os.path.join(main_directory, "getdata")
dl_directory = os.path.join(main_directory, "dl")
test_directory = os.path.join(main_directory, "test")
egfr_directory = os.path.join(main_directory, "egfr")
alphagl_directory = os.path.join(main_directory, "alphagl")

# Fungsi untuk membuat direktori dan file konfigurasi
def create_dock():
    try:
        # Mendefinisikan direktori konfigurasi dan direktori tugas
        config_directory = os.path.join(dock_directory, "config")
        job_dir = os.path.join(os.getcwd(), 'dock')
        
        # Membuat direktori tugas jika belum ada
        if not os.path.exists(job_dir):
            os.mkdir(job_dir)
        
        # Menyalin file konfigurasi ke direktori tugas
        shutil.copy(os.path.join(config_directory, 'configdock.txt'), job_dir)
        
        # Membuat direktori untuk masukan ligand jika belum ada
        ligand_dir = os.path.join(job_dir, 'ligand_input')    
        if not os.path.exists(ligand_dir):    
            os.mkdir(ligand_dir)
        
        # Mengolah model dan ligand contoh
        for i in range(1, 4):  
            model_dir = f'model_{i:02d}'
            model_path = os.path.join(job_dir, model_dir)
            
            if not os.path.exists(model_path):
                os.mkdir(model_path)
        
        ligand_dir = os.path.join(job_dir, 'ligand_input')
        os.makedirs(ligand_dir, exist_ok=True)
                    
        model_in = os.path.join(config_directory, "model_example")
        model_out = os.path.join(job_dir, "model_example")
        shutil.copytree(model_in, model_out)
        
        ligands = glob.glob(os.path.join(config_directory, "example*"))
        for file in ligands:
            shutil.copy(file, ligand_dir)
        
        message = f"Sub-directories and example contents are successfully generated in the job directory: {job_dir}"
        print("Job Directory", message)
        
    except Exception as e:
        print("Error", f"An error occurred: {str(e)}")
    
    return job_dir
    
def create_md():
        try:
            
            current_dir = os.getcwd()
            job_dir = os.path.join(current_dir, 'md')
            prolig_dir = os.path.join(job_dir, 'prolig')
            liglig_dir = os.path.join(job_dir, 'liglig')
            
            # Use os.makedirs with exist_ok=True to create nested directories
            os.makedirs(job_dir, exist_ok=True)
            os.makedirs(prolig_dir, exist_ok=True)
            os.makedirs(liglig_dir, exist_ok=True)
       
            # Menyalin file konfigurasi ke direktori tugas
            config_directory = os.path.join(md_directory, "config")
            shutil.copy(os.path.join(config_directory, 'configmd.txt'), job_dir)
           
            # Use pathlib.Path to handle paths more conveniently
            source_directory = os.path.dirname(os.path.abspath(__file__))
            config_directory = os.path.join(source_directory, "md", "config")
            mdp_directory = os.path.join(source_directory, "md", "mdp")

            # Create model directories with f-strings for formatting
            for i in range(1, 4):
                model_prolig = os.path.join(prolig_dir, f'complex_{i:02d}')
                model_liglig = os.path.join(liglig_dir, f'complex_{i:02d}')
                os.makedirs(model_prolig, exist_ok=True)
                os.makedirs(model_liglig, exist_ok=True)

            # Use shutil.copytree for copying entire directories
            modelp_sr = os.path.join(config_directory, 'complex_example_prolig')
            modelp_ds = os.path.join(prolig_dir, 'complex_example_prolig')
            shutil.copytree(modelp_sr, modelp_ds)
            
            modell_sr = os.path.join(config_directory, 'complex_example_liglig')
            modell_ds = os.path.join(liglig_dir, 'complex_example_liglig')
            shutil.copytree(modell_sr, modell_ds)

            # Use os.path.join to create source_file paths
            for filename in os.listdir(mdp_directory):
                if filename.endswith(".mdp"):
                    source_file = os.path.join(mdp_directory, filename)
                    shutil.copy(source_file, liglig_dir)
                    shutil.copy(source_file, prolig_dir)
                    
            message = f"Sub-directories and example contents are successfully generated in the job directory: {job_dir}"
            print("Job Directory", message)

        except Exception as e:
            print("Error", f"An error occurred: {str(e)}")
        
        return job_dir
    
def create_getdata():
    try:
        current_dir = os.getcwd()
        config_directory = os.path.join(getdata_directory, "config")
        job_dir = os.path.join(current_dir, 'getdata')
        
        # Membuat direktori tugas jika belum ada
        if not os.path.exists(job_dir):
            os.mkdir(job_dir)
        
        # Menyalin file konfigurasi ke direktori tugas
        shutil.copy(os.path.join(config_directory, 'configgetdata.txt'), job_dir)
       
        message = f"Configuration file for getdata are successfully generated in the job directory: {job_dir}"
        print("Job Directory", message)
        
    except Exception as e:
        print("Error", f"An error occurred: {str(e)}")
        print("Error", f"An error occurred: {str(e)}")
    
    return job_dir
    
def create_dl():
    try:
        current_dir = os.getcwd()
        config_directory = os.path.join(dl_directory, "config")
        job_dir = os.path.join(current_dir, 'dl')
        
        # Membuat direktori tugas jika belum ada
        if not os.path.exists(job_dir):
            os.mkdir(job_dir)
        
        # Menyalin file konfigurasi ke direktori tugas
        shutil.copy(os.path.join(config_directory, 'configdl.txt'), job_dir)
      
        message = f"Directories and configuration file for deep learning modeling are successfully generated in the job directory: {job_dir}"
        print("Job Directory", message)
        
    except Exception as e:
        print("Error", f"An error occurred: {str(e)}")
    return job_dir
    
def create_test():
    try:
        current_dir = os.getcwd()
        config_directory = os.path.join(test_directory, "config")
        job_dir = os.path.join(current_dir, 'test')
        
        # Membuat direktori tugas jika belum ada
        if not os.path.exists(job_dir):
            os.mkdir(job_dir)
        
        # Menyalin file konfigurasi ke direktori tugas
        shutil.copy(os.path.join(config_directory, 'configtest.txt'), job_dir)
        
        message = f"Directories and configuration file for testing are successfully generated in the job directory: {job_dir}"
        print("Job Directory", message)
        
    except Exception as e:
        print("Error", f"An error occurred: {str(e)}")
    return job_dir
    
def create_egfr():
    try:
        current_dir = os.getcwd()
        job_dir = os.path.join(current_dir, 'egfr')
        
        # Membuat direktori tugas jika belum ada
        if not os.path.exists(job_dir):
            os.mkdir(job_dir)
        
        # Menyalin file konfigurasi ke direktori tugas
        shutil.copy(os.path.join(egfr_directory, 'configegfr.txt'), job_dir)
        
        message = f"Directories and configuration file for EGFR are successfully generated in the job directory: {job_dir}"
        print("Job Directory", message)
        
    except Exception as e:
        print("Error", f"An error occurred: {str(e)}")
        print("Error", f"An error occurred: {str(e)}")
    return job_dir
    
def create_alphagl():
    try:
        current_dir = os.getcwd()
        job_dir = os.path.join(current_dir, 'alphagl')
        
        # Membuat direktori tugas jika belum ada
        if not os.path.exists(job_dir):
            os.mkdir(job_dir)
        
        # Menyalin file konfigurasi ke direktori tugas
        shutil.copy(os.path.join(alphagl_directory, 'configalphagl.txt'), job_dir)
        
        message = f"Directories and configuration file for Alpha Glucosidase are successfully generated in the job directory: {job_dir}"
        print("Job Directory", message)
        
    except Exception as e:
        print("Error", f"An error occurred: {str(e)}")
    return job_dir
    
# Fungsi utama untuk menjalankan simulasi berdasarkan jenis simulasi
def run_simulation(simulation_type):
    try:
        if simulation_type == 'dock':
            path = os.path.join(dock_directory, 'ladocknogui.py')
        
        elif simulation_type == 'md':
            path = os.path.join(md_directory, 'gmxnogui.py')
        
        elif simulation_type == 'getdata':
            path = os.path.join(getdata_directory, 'getdatanogui.py')
        
        elif simulation_type == 'dl':
            path = os.path.join(dl_directory, 'dlnogui.py')
       
        elif simulation_type == 'test':
            path = os.path.join(test_directory, 'testnogui.py')

        elif simulation_type == 'egfr':
            path = os.path.join(egfr_directory, 'egfrnogui.py')

        elif simulation_type == 'alphagl':
            path = os.path.join(alphagl_directory, 'alphaglnogui.py')
        
        subprocess.run(['python3', path])

    except Exception as e:
        print("Error", f"An error occurred: {str(e)}")

# Fungsi utama untuk membuat direktori dan file konfigurasi berdasarkan jenis simulasi
def create_input(simulation_type):
    try:
        if simulation_type == 'dock':
            create_dock()
            print("dock and sub directories, 'config.txt', and 'ligand_link.txt' files have been successfully created. Please edit them according to your needs.")
            
        elif simulation_type == 'md':
            create_md()
            print("LADOCK_gmxprolig and subdirectory created successfully.")
           
        elif simulation_type == 'getdata':
            create_getdata()
            print("conflig file, and input, output directories for prepare-data created successfully.")
            
        elif simulation_type == 'dl':
            create_dl()
            print("conflig file and input, output directories for deep learning modeling created successfully.")

        elif simulation_type == 'test':
            create_test()
            print("conflig file and job directories for predicting activity using AI model created successfully.")

        elif simulation_type == 'egfr':
            create_egfr()
            print("conflig file and job directories for predicting EGFR inhibitor activity using LADOCK AI model created successfully.")

        elif simulation_type == 'alphagl':
            create_alphagl()
            print("conflig file and job directories for predicting Alpha Glucosidase inhibitor activity using LADOCK AI model created successfully.")

    except Exception as e:
        print("Error", f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Run LADOCK modules')
    parser.add_argument('--create', help='Create directories and configuration files. Options: dock, md, getdata, dl, test, egfr, alphagl. Notes: "dock" is a docking module, "md" is molecular dynamics module, "getdata" is a module for data retrieval from chembl and descriptors calculation, "dl" is a module for generate deep learning model, "test" is a module for dataset testing by using AI model, "egfr" is a module for predicting the IC50 of molecule(s) as EGFR inhibitor by using LADOCK model, and "alphagl" is a module for predicting the IC50 of molecule(s) as Alpha Glucosidase inhibitor by using LADOCK model.', type=str)
    parser.add_argument('--run', help='Run simulation for the specified module. Options: dock, md, getdata, dl, test, egfr, alphagl.', type=str)
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.6')
    args = parser.parse_args()

    if args.create:
        create_input(args.create)
    elif args.run:
        run_simulation(args.run)
    else:
        print("Please provide valid arguments. 'ladock --run CREATE' for creating directories and configuration files, or 'ladock --create RUN' for running simulation, or 'ladock --help' or 'ladock -h' for help, or 'ladockgui' for running ladock in GUI mode")

if __name__ == "__main__":
    main()
