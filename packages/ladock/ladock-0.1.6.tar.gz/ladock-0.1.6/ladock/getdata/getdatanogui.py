import os
from ladock.getdata.getData_S1 import search_targets  
from ladock.getdata.getData_S2 import search_molecules
from ladock.PrepareData.prepare_data import prepareData 

def read_config(config_file):
    config = {}
    with open(config_file, 'r') as f:
        for line in f:
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                continue
            parts = line.strip().split(': ')
            if len(parts) == 2:
                key, value = parts
                config[key.strip()] = value.strip()
            else:
                print(f"Ignoring malformed line: {line.strip()}")
    return config

def start_target(config):
    query_list = config['query_list'].split(',')  
    query_list = [file.strip() for file in query_list]
      
    search_targets(query_list, job_dir, result_text=None)       

def start_molecules(config):  
    search_molecules(job_dir, result_text=None)       

def start_calculate(config):
    csv_files = config['csv_files'].split(',')
    csv_files = [file.strip() for file in csv_files]
    descriptors_list = [descriptor.upper() for descriptor in config['descriptors_list'].split(', ')]
    mol_column = config['molecule_column']
    optimize_method = config['optimization_method'].lower()
    num_conformers = int(config['num_conformers'])
    max_iters = int(config['max_iterations'])
    
    output_dir = os.path.join(job_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    for csv_file in csv_files:
        prepareData(csv_file, job_dir, output_dir, descriptors_list, mol_column, optimize_method, num_conformers, max_iters)

current_dir = os.getcwd()    
job_dir = os.path.join(current_dir, 'getdata')
config = read_config(os.path.join(job_dir, 'configgetdata.txt'))
getdata_type = config.get('getdata_type')
    
if getdata_type == "step1":
    start_target(config)

elif getdata_type == "step2":
    start_molecules(config)

elif getdata_type == "step3":
    start_calculate(config)

