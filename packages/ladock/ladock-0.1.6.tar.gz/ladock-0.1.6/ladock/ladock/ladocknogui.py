import os
from ladock.ladock.docking import docking

def read_config(config_file):
    config = {}
    with open(config_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                try:
                    key, value = line.strip().split(': ')
                    config[key] = value
                except ValueError:
                    print(f"Issue with line: {line}")
    return config

def docking_conf(config_file):
    config = read_config(config_file)
    mgl_path = os.path.join(config['mgl_path'], "MGLToolsPckgs/AutoDockTools/Utilities24")
    parallel_simulation = str(config['parallel_simulation']).lower()
    
    parameters = {
        'sf_types': [x.strip().lower() for x in config['sf_types'].split(',')],
        'listmode': [x.strip().lower() for x in config['listmode'].split(',')],
        'distance': int(config['distance_of_flexible_residues']),
        'arrangement_type': config['arrangement_type'],
        'elements': config['elements'],
        'box_size': config['box_size'],
        'spacing': config['spacing'],
        'n_poses': int(config['n_poses']),
        'exhaustiveness': int(config['exhaustiveness']),
        'cpu': int(config['cpu']),
        'parallel_simulation': parallel_simulation,
        'input_file_saved': config['input_file_saved'],
        'output_file_saved': config['output_file_saved'],
        'vina_path': config['vina_path'],
        'ad4_path': config['ad4_path'],
        'ag4_path': config['ag4_path'],
        'autodockgpu': config['autodockgpu'],
        'vinagpu': config['vinagpu'],
        'job_directory': job_dir,
        'max_workers': os.cpu_count() // int(config['cpu']),
        'agfr': os.path.join(config['adfr_path'], "agfr"),
        'adfr': os.path.join(config['adfr_path'], "adfr"),
        'prepare_ligand': os.path.join(mgl_path, "prepare_ligand4.py"),
        'prepare_receptor': os.path.join(mgl_path, "prepare_receptor4.py"),
        'prepare_gpf': os.path.join(mgl_path, "prepare_gpf4.py"),
        'prepare_flexreceptor': os.path.join(mgl_path, "prepare_flexreceptor4.py"),
        'current_directory': job_dir,
        
    }    
    docking(result_text=None, **parameters)

# Contoh pemanggilan
current_dir = os.getcwd()
job_dir = os.path.join(current_dir, "dock")

config_file = 'configdock.txt'
docking_conf(os.path.join(job_dir, config_file))

