import os
from ladock.md.gmxprolig import prolig
from ladock.md.gmxliglig import liglig

def read_config(config_file):
    config = {}
    with open(config_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore empty lines and comments
                parts = line.split(': ', 1)  # Split only once
                if len(parts) == 2:
                    key, value = parts
                    config[key.strip()] = value.strip()
                else:
                    print(f"Ignoring line: {line}. It does not follow the expected format.")
    return config

def run_md(config_file):        
    # Membaca nilai variabel-variabel dari config.txt
    config = read_config(config_file)
    md_type = config['md_type'].lower()
    box_type = config['box_type'].lower()
    distance = config['distance']
    solvent = config['solvent']
    rdd = config['rdd']
    dds = config['dds']    
        
    # Memeriksa dan mengubah job directory sesuai dengan md_type
    if md_type == "protein-ligand":
        job_dir = os.path.join(md_dir, "prolig")
    elif md_type == "ligand-ligand":
        job_dir = os.path.join(md_dir, "liglig")

    parameters = {    
        'box_type': box_type,
        'distance': distance,
        'solvent': solvent,
        'rdd': rdd,
        'dds': dds,
        'current_directory': job_dir, 
    }
    
    # Memanggil fungsi prolig atau liglig sesuai dengan md_type
    if md_type == "Protein-Ligand":
        prolig(progress_bar=None, result_text=None, **parameters)
    elif md_type == "Ligand-Ligand":
        liglig(progress_bar=None, result_text=None, **parameters)

# Contoh pemanggilan
current_dir = os.getcwd()
md_dir = os.path.join(current_dir, "md")
config_file = os.path.join(md_dir, 'configmd.txt')
run_md(config_file)
