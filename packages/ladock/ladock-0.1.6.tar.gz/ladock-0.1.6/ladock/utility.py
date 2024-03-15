import requests
from tqdm import tqdm
from retrying import retry
import os
import subprocess
import gzip
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from requests.exceptions import RequestException
from time import sleep
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from os.path import basename, splitext
from concurrent.futures import ThreadPoolExecutor, as_completed
from Bio import PDB
from Bio.PDB import PDBParser
from Bio.PDB import NeighborSearch
import shutil
from tkinter import messagebox, filedialog
import tkinter as tk
import numpy as np

source_directory = os.path.dirname(os.path.abspath(__file__))

dn = os.path.join(source_directory, "developerNote.txt")
with open(dn, 'r') as file:
    content = file.read()

# Pisahkan isi file menjadi blok-blok yang sesuai dengan variabel-variabel
blocks = content.split('\n\n')
# Inisialisasi variabel
developer_note = ""
developer_contact = ""
citation_list = ""

def browse_file_path(path_var):
        file_path = filedialog.askopenfilename()
        if file_path:
            path_var.set(file_path)

def browse_dir_path(path_var):
        path = filedialog.askdirectory()
        if path:
            path_var.set(path)

def help_dock():
    # Function to display help text in a messagebox
    help_text = """This is a module for molecular docking.
"""
    messagebox.showinfo("Help", help_text)

def help_md():
    # Function to display help text in a messagebox
    help_text = """This is a module for molecular dynamics using gromacs.
"""
    messagebox.showinfo("Help", help_text)

def help_getdata():
    # Function to display help text in a messagebox
    help_text = """This is a module for data retrieval from chembl and descriptors calculation.
"""
    messagebox.showinfo("Help", help_text)

def help_dl():
    # Function to display help text in a messagebox
    help_text = """This is a module for generate deep learning model.
"""
    messagebox.showinfo("Help", help_text)

def help_test():
    # Function to display help text in a messagebox
    help_text = """This is a module for dataset testing using AI model.
"""
    messagebox.showinfo("Help", help_text)

def help_egfr():
    # Function to display help text in a messagebox
    help_text = """This is a module for predicting the IC50 of molecule(s) as EGFR inhibitor by using LADOCK AI model.
"""
    messagebox.showinfo("Help", help_text)

def help_alphagl():
    # Function to display help text in a messagebox
    help_text = """.This is a module for predicting the IC50 of molecule(s) as Alpha Glucosidase inhibitor by using LADOCK AI model.
"""
    messagebox.showinfo("Help", help_text)

def extract_molecule(pdb_file_path):
    startsWith = []
    endsWith = []
    atom_coordinates = []

    try:
        with open(pdb_file_path, 'r') as file:
            for line in file:
                if line.startswith('ATOM') or line.startswith('HETATM'):
                    startWith = str(line[0:29].strip()) 
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    endWith = str(line[55:80].strip())    

                    startsWith.append(startWith)
                    endsWith.append(endWith)
                    atom_coordinates.append((x, y, z))
    except FileNotFoundError:
        print(f"Error: File '{pdb_file_path}' not found.")
        return None
    except ValueError as ve:
        print(f"Error: Unable to convert coordinates to float. {ve}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    return startsWith, atom_coordinates, endsWith

def calculate_molecule_center(atom_coordinates):
    try:
        # Hitung pusat massa molekul
        num_atoms = len(atom_coordinates)
        if num_atoms == 0:
            return None

        center = [sum(coord[i] for coord in atom_coordinates) / num_atoms for i in range(3)]
        return center
    except ZeroDivisionError:
        print("Error: Number of atoms is zero. Unable to calculate molecule center.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def move_molecule_to_target_center(atom_coordinates, target_box_center):
    try:
        # Calculate the translation vector
        current_molecule_center = calculate_molecule_center(atom_coordinates)
        if current_molecule_center is None:
            return None

        translation_vector = [target - current for target, current in zip(target_box_center, current_molecule_center)]

        # Move each atom
        moved_atom_coordinates = []
        for atom in atom_coordinates:
            moved_atom = tuple(coord + translation for coord, translation in zip(atom, translation_vector))
            moved_atom_coordinates.append(moved_atom)

        return moved_atom_coordinates
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Loop melalui blok-blok dan mengisi variabel yang sesuai
for block in blocks:
    if block.startswith("developer_note ="):
        developer_note = block[block.find("=") + 1:].strip()
    elif block.startswith("developer_contact ="):
        developer_contact = block[block.find("=") + 1:].strip()
    elif block.startswith("citation_list ="):
        citation_list = block[block.find("=") + 1:].strip()

def get_residues_within_distance(protein_pdb, ligand_pdb, distance):
    # Membaca struktur protein dari file PDB
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('protein', protein_pdb)
    
    # Membaca struktur ligan dari file PDB
    ligand_structure = parser.get_structure('ligand', ligand_pdb)
    
    # Membuat objek NeighborSearch untuk mencari tetangga dalam jarak tertentu
    ns = NeighborSearch(list(structure.get_atoms()))
    
    # Mendapatkan koordinat atom ligan
    ligand_atoms = list(ligand_structure.get_atoms())
   
    # Menyimpan residu yang berada dalam jarak tertentu dari ligan   
    nearby_residues = set()

    for ligand_atom in ligand_atoms:
       neighbors = ns.search(ligand_atom.coord, distance)       
       nearby_residues.update([f"{neighbor.get_parent().get_resname()}{neighbor.get_parent().get_full_id()[3][1]}" for neighbor in neighbors])
    return nearby_residues

def adfr_energy(input_file):
    # Buka file untuk membaca    
    with open(input_file, 'r') as file:
        content = file.read()
        
    energy = None
    # Cari baris keempat setelah "Refining results"
    lines = content.split('\n')
    for i in range(len(lines)):
        if "Refining results" in lines[i]:
            start_index = i + 4  # Ambil baris keempat setelah "Refining results"
            try:
                # Ambil nilai energi dari kolom kedua pada baris tersebut
                energy = float(lines[start_index].split()[1])
                break
            except (ValueError, IndexError):
                pass       
    return energy

def get_molecule_name(molecule):
    if molecule.HasProp("_Name"):
        return molecule.GetProp("_Name")
    else:
        # Handle the case where the property "_Name" is not found
        # You can return a default value or raise an exception based on your requirements
        return "UnknownName" 

def write_molecule_to_pdb(molecule, output_file):
    """
    Write a molecule to a PDB file.

    Parameters:
        molecule (rdkit.Chem.Mol): RDKit molecule object.
        output_file (str): Output PDB file path.
    """
    writer = Chem.PDBWriter(output_file)
    writer.write(molecule)
    writer.close()
    

def processing_ligand(ligand_file):
    if ligand_file.endswith(".sdf"):
        smiles_list = process_sdf(ligand_file)
        return smiles_list
    
    elif ligand_file.endswith(".smi"):

        smiles_list = process_smi(ligand_file)
        return smiles_list
   
    elif ligand_file.endswith(".mol2"):

        smiles_list = process_mol2(ligand_file)
        return smiles_list
   
    elif ligand_file.endswith(".mol"):

        smiles_list = process_mol(ligand_file)
        return smiles_list
        
    elif ligand_file.endswith(".pdb"):
        smiles_list = process_pdb(ligand_file)
        return smiles_list
    
    elif ligand_file.endswith(".csv"):
        smiles_list = process_csv(ligand_file)
        return smiles_list

def process_csv(ligand_file): 
    smiles_list = pd.read_csv(ligand_file, header=0)  
    smiles_list = smiles_list.rename(columns=lambda x: 'ligand_id' if 'id' in x else x)
    smiles_list = smiles_list.rename(columns=lambda x: 'smiles' if 'smiles' in x else x)
    smiles_list = smiles_list.rename(columns=lambda x: 'activity' if 'value' in x else x)
    new_column_order = ['ligand_id', 'smiles', 'activity'] + [col for col in smiles_list.columns if col not in ['ligand_id', 'smiles', 'activity']]
    smiles_list = smiles_list.reindex(columns=new_column_order)
    return smiles_list
    	
def process_pdb(ligand_file):
    lig_id_list = []
    smi_list = []
    activity_list = []

    # Use Chem.SDMolSupplier to obtain molecules from the PDB file
    suppl = Chem.SDMolSupplier(ligand_file)

    for idx, mol in enumerate(suppl):
        if mol:
            lig_id = get_molecule_name(mol)
            if not lig_id:
                lig_id = f"{os.path.splitext(os.path.basename(ligand_file))[0]}_{idx}"
            lig_id_list.append(lig_id)

            smi = Chem.MolToSmiles(mol)
            smi_list.append(smi)

            activity_list.append('NaN')
            pdb_filename = f'{lig_id}.pdb'
            write_molecule_to_pdb(mol, pdb_filename)

    smiles_list = pd.DataFrame({'ligand_id': lig_id_list, 'smiles': smi_list, 'activity': activity_list})
    return smiles_list

def process_mol(ligand_file):
    lig_id_list = []
    smi_list = []
    activity_list = []

    suppl_mol = Chem.SDMolSupplier(ligand_file)

    for idx, mol in enumerate(suppl_mol):
        if mol:
             lig_id = get_molecule_name(mol)
             if not lig_id:
                lig_id = f"{os.path.splitext(os.path.basename(ligand_file))[0]}_{idx}"
             lig_id_list.append(lig_id)
              
             pdb_filename = f'{lig_id}.pdb'
             write_molecule_to_pdb(mol, pdb_filename)

             smi = Chem.MolToSmiles(mol)
             smi_list.append(smi)
                
             activity_list.append('NaN')

    smiles_list = pd.DataFrame({'ligand_id': lig_id_list, 'smiles': smi_list, 'activity': activity_list})
    return smiles_list

def process_sdf(ligand_file):
    lig_id_list = []
    smi_list = []
    activity_list = []

    suppl_mol = Chem.SDMolSupplier(ligand_file)

    for idx, mol in enumerate(suppl_mol):
        if mol:
             lig_id = get_molecule_name(mol)                          
             if not lig_id:
                lig_id = f"{os.path.splitext(os.path.basename(ligand_file))[0]}_{idx}"
             lig_id_list.append(lig_id)
              
             pdb_filename = f'{lig_id}.pdb'
             write_molecule_to_pdb(mol, pdb_filename)

             smi = Chem.MolToSmiles(mol)
             smi_list.append(smi)
                
             activity_list.append('NaN')

    smiles_list = pd.DataFrame({'ligand_id': lig_id_list, 'smiles': smi_list, 'activity': activity_list})
    return smiles_list
    
def process_smi(smi_file_path):
    activity_list = []
    lig_id_list = []
    smi_list = []

    with open(smi_file_path, 'r') as smi_file:
        smiles_lines = [line for line in smi_file.read().splitlines() if "smi" not in line.lower() or "id" not in line.lower()]

    for idx, line in enumerate(smiles_lines):
            parts = line.split()
            if len(parts) >= 2:
                lig_id = parts[1]
                smi = parts[0]
                try:
                    mol = Chem.MolFromSmiles(smi)
                    if mol:
                        lig_id_list.append(lig_id)
                        smi_list.append(smi)
                        activity_list.append('NaN')
                except Exception as e:
                    print(f"Error in line {idx + 1}: {e}")

    smiles_list = pd.DataFrame({'ligand_id': lig_id_list, 'smiles': smi_list, 'activity': activity_list})
    return smiles_list

def process_mol2(mol2_file):
    lig_id_list = []
    smi_list = []
    activity_list = []

    try:
        with open(mol2_file, 'r') as file:
            lines = file.readlines()
            mol_block = ''

            for line in lines:
                if line.startswith('@<TRIPOS>MOLECULE'):
                    if mol_block.strip():
                        mol = Chem.MolFromMol2Block(mol_block)
                        if mol:
                            lig_id = get_molecule_name(mol)                             
                            if not lig_id:
                                lig_id = f"{os.path.splitext(os.path.basename(ligand_file))[0]}_{idx}"
                            lig_id_list.append(lig_id)

                            pdb_filename = f'{lig_id}.pdb'
                            write_molecule_to_pdb(mol, pdb_filename)

                            smi = Chem.MolToSmiles(mol)
                            smi_list.append(smi)

                            activity_list.append('NaN')

                    mol_block = line  # Start a new block
                else:
                    mol_block += line

            # Process the last molecule in the file
            if mol_block.strip():
                mol = Chem.MolFromMol2Block(mol_block)
                if mol:
                    lig_id = get_molecule_name(mol)
                    if not lig_id:
                        lig_id = os.path.splitext(os.path.basename(ligand_file))[0]
                    lig_id_list.append(lig_id)

                    pdb_filename = f'{lig_id}.pdb'
                    write_molecule_to_pdb(mol, pdb_filename)

                    smi = Chem.MolToSmiles(mol)
                    smi_list.append(smi)

                    activity_list.append('NaN')

        smiles_list = pd.DataFrame({'ligand_id': lig_id_list, 'smiles': smi_list, 'activity': activity_list})
        return smiles_list

    except Exception as e:
        print(f"Error processing MOL2 file: {e}")
        return None


def column_to_list(file_path, column):
    if file_path.endswith('.txt'):
        df = pd.read_csv(file_path, delimiter='\t')
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.smi'):
        df = pd.read_csv(file_path, delimiter=' ')
    else:
        raise ValueError("File format not supported. Use txt or csv.")

    smiles_list = df[column].tolist()

    return smiles_list

    return smiles_list

def mol_2d(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        return mol
    
    except Exception as e:
        logging.error(f"Error in mol_2d for SMILES '{smiles}': {str(e)}")
        return None

def mol_3d(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)
        return mol
        
    except Exception as e:
        logging.error(f"Error in mol_3d for SMILES '{smiles}': {str(e)}")
        return None 
        
def mol_mmff(smiles, num_conformers, maxIters):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Failed to create RDKit molecule for SMILES: {smiles}")
        
        mol = Chem.AddHs(mol)
        AllChem.EmbedMultipleConfs(mol, numConfs=num_conformers, randomSeed=42)

        if mol.GetNumConformers() == 0:            
            return mol

        lowest_energy = float('inf')
        lowest_energy_conf_id = None

        for conf_id in range(mol.GetNumConformers()):
             initial_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id, ignoreInterfragInteractions=False).CalcEnergy()
             
             AllChem.MMFFOptimizeMolecule(mol, confId=conf_id, maxIters=maxIters)
             optimized_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id).CalcEnergy()
             if optimized_energy < lowest_energy:
                lowest_energy = optimized_energy
                lowest_energy_conf_id = conf_id

        # Extract the lowest energy conformer
        if lowest_energy_conf_id is not None:
            optimized_mol = Chem.Mol(mol)
            optimized_mol.RemoveAllConformers()
            optimized_mol.AddConformer(mol.GetConformer(lowest_energy_conf_id))

            return optimized_mol
        else:
            raise ValueError("Failed to find the lowest energy conformer.")

    except Exception as e:
        print(f"Error in mol_mmff for SMILES '{smiles}': {str(e)}")
        return None

def mol_uff(smiles, num_conformers, maxIters):
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMultipleConfs(mol, numConfs=num_conformers, randomSeed=42)
        
        if mol.GetNumConformers() == 0:            
            return mol
        
        lowest_energy = float('inf')
        lowest_energy_conf_id = None

        for conf_id in range(mol.GetNumConformers()):
            initial_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id, ignoreInterfragInteractions=False).CalcEnergy()

            AllChem.UFFOptimizeMolecule(mol, confId=conf_id, maxIters=200)
            optimized_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id).CalcEnergy()
            if optimized_energy < lowest_energy:
                lowest_energy = optimized_energy
                lowest_energy_conf_id = conf_id
                optimized_molecule = mol 

        return optimized_molecule
                    
    except Exception as e:
        logging.error(f"Error in mol_uff for SMILES '{smiles}': {str(e)}")
        return None

def mol_qm(smiles, num_conformers, maxIters):
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMultipleConfs(mol, numConfs=num_conformers, randomSeed=42)
        
        lowest_energy = float('inf')
        lowest_energy_conf_id = None

        for conf_id in range(mol.GetNumConformers()):
            initial_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id, ignoreInterfragInteractions=False).CalcEnergy()

            AllChem.UFFOptimizeMolecule(mol, confId=conf_id, maxIters=200)
            optimized_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id).CalcEnergy()
            if optimized_energy < lowest_energy:
                lowest_energy = optimized_energy
                lowest_energy_conf_id = conf_id
                optimized_molecule = mol 

        return optimized_molecule
                    
    except Exception as e:
        logging.error(f"Error in mol_uff for SMILES '{smiles}': {str(e)}")
        return None

def vina_energy(pdbqt_output):               
    with open(pdbqt_output, 'r') as vina_output:
        lines = vina_output.readlines()

    energy = None
    for line in lines:
        if line.startswith("REMARK VINA RESULT:"):
            energy = float(line.split()[3])
            break  # Stop reading after the first matching line
    return energy
    
def ad4_energy(input_file):
    # Buka file untuk membaca    
    with open(input_file, 'r') as file:
        content = file.read()
    energy = None
    # Cari baris yang mengandung "RMSD TABLE"
    in_rmsd_table = False
    for line in content.split('\n'):
        if "RMSD TABLE" in line:
            in_rmsd_table = True
            continue
            
        if in_rmsd_table:
            if line.strip():
                words = line.split()
                try:
                    energy = float(words[3])
                    break
                except (ValueError, IndexError):
                    pass
    else:
        print("Tabel RMSD tidak ditemukan atau tidak ada nilai energy pada baris pertama kolom keempat.")
        
    return energy



def calculate_gridbox_center(pdb_file):
    print(f"  Calculating GridBox Center")    
    
    parser = PDBParser()
    structure = parser.get_structure("ligand", pdb_file)
    
    model = structure[0]  # Get the first model from the PDB structure
    atoms = model.get_atoms()  # Get the list of atoms in the model
    
    x_sum = y_sum = z_sum = 0.0
    num_atoms = 0
    
    for atom in atoms:
        x, y, z = atom.get_coord()
        x_sum += x
        y_sum += y
        z_sum += z
        num_atoms += 1
    
    x_center = round(x_sum / num_atoms, 3)
    y_center = round(y_sum / num_atoms, 3)
    z_center = round(z_sum / num_atoms, 3)
    
    return x_center, y_center, z_center

def create_vina_config(ligand_pdb, box_size):
    x_center, y_center, z_center = calculate_gridbox_center(ligand_pdb)    
    config_file='config.txt'
    size_x = {box_size[0]}
    size_y = {box_size[1]}
    size_z = {box_size[2]}
    
    with open(config_file, 'w') as config_file:
        config_file.write(f"size_x = {size_x}\n")
        config_file.write(f"size_y = {size_y}\n")
        config_file.write(f"size_z = {size_z}\n")
        config_file.write(f"center_x = {x_center}\n")
        config_file.write(f"center_y = {y_center}\n")
        config_file.write(f"center_z = {z_center}\n")
        config_file.write("# Script written by:\n")
        config_file.write("# La Ode Aman\n")
        config_file.write("# laodeaman.ai@gmail.com\n")
        config_file.write("# laode_aman@ung.ac.id\n")
        config_file.write("# Universitas Negeri Gorontalo, Indonesia\n")

    print("  Docking parameter:")
    print("\tsize_x = {}".format(size_x))
    print("\tsize_y = {}".format(size_y))
    print("\tsize_z = {}".format(size_z))
    print("\tcenter_x = {}".format(x_center))
    print("\tcenter_y = {}".format(y_center))
    print("\tcenter_z = {}".format(z_center))

    return size_x, size_y, size_z, x_center, y_center, z_center, config_file

def sort_and_add_number(csv_file, sorted_by):
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()
    df_sorted = df.sort_values(by=sorted_by, ascending=[True])
    df_sorted.to_csv(csv_file, index=False)
    print(df_sorted)

# Define the maximum number of retries and delay between retries (in seconds)
max_retries = 3
retry_delay = 1  # 1 second

def download_file_with_retry(url, destination):
    for attempt in range(max_retries):
        try:
            print(f"Downloading URL: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024000  # 1000 KB
            t = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading', dynamic_ncols=True)

            with open(destination, 'wb') as file:
                for data in response.iter_content(chunk_size=block_size):
                    file.write(data)
                    t.update(len(data))

            t.close()
            return  # Successful download, exit the function

        except RequestException as e:
            print(f"Attempt {attempt + 1} failed. Error: {e}")

        except Exception as e:
            print(f"Unexpected error during file download. Error: {e}")

        # Wait before the next retry
        sleep(retry_delay)

    print(f"Failed to download {url} after {max_retries} attempts.")

def extract_gz(gz_path):
    try:
        extracted_file = os.path.basename(gz_path)[:-3]  
        with gzip.open(gz_path, 'rb') as f_in, open(extracted_file, 'wb') as f_out:
            f_out.write(f_in.read())
        os.remove(gz_path)
        return extracted_file
    except Exception as e:
            print(f"Error: {e}")           
   
def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}. Output:\n{e.stderr.decode()}")
        pass

def is_smiles_valid(smiles_string):
    try:
        mol = Chem.MolFromSmiles(smiles_string)
        if mol is not None and Chem.SanitizeMol(mol):
            return True
        else:
            return False
    except:
        return False

def read_energy_and_save_to_csv(counter, output_file, csv_path, lig_name, input_file):
    # Buka file untuk membaca    
    smiles = convert_to_smiles(input_file)
    with open(output_file, 'r') as file:
        content = file.read()

    # Cari baris yang mengandung "RMSD TABLE"
    in_rmsd_table = False
    for line in content.split('\n'):
        if "RMSD TABLE" in line:
            in_rmsd_table = True
            continue
        if in_rmsd_table:
            if line.strip():
                words = line.split()
                try:
                    energy = float(words[3])
                    break
                except (ValueError, IndexError):
                    pass
    else:
        print("Tabel RMSD tidak ditemukan atau tidak ada nilai energy pada baris pertama kolom keempat.")
    
    return energy    

def pdb_to_smiles(pdb_file):
    mol_supplier = Chem.MolFromPDBFile(pdb_file)
    AllChem.Compute2DCoords(mol_supplier)
    smiles = Chem.MolToSmiles(mol_supplier)
    return smiles

def delete_files_except_pdb(job_dir):
    for filename in os.listdir(job_dir):
        file_path = os.path.join(job_dir, filename)
        
        if os.path.isdir(file_path):
            try:
                shutil.rmtree(file_path)
                
            except Exception as e:
                print(f"Error deleting directory {file_path}: {e}")
                
        elif os.path.isfile(file_path) and not filename.endswith('.pdb'):
            try:
                os.remove(file_path)
                
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

def split_sdf_file(input_file, output_dir, molecules_per_file=500):
    print(input_file)
    suppl = Chem.SDMolSupplier(input_file)

    total_molecules = len(suppl)
    total_files = total_molecules // molecules_per_file + 1

    if total_molecules >= molecules_per_file:
        for file_num, start_idx in enumerate(range(0, total_molecules, molecules_per_file)):
            end_idx = start_idx + molecules_per_file

            output_file = os.path.join(output_dir, f"output_{file_num + 1}.sdf")
            with Chem.SDWriter(output_file) as writer:
                for mol_idx in range(start_idx, min(end_idx, total_molecules)):
                    mol = suppl[mol_idx]
                    if mol is not None:
                        writer.write(mol)
            print(f"Successfully split {input_file} into {output_file}")

    else:
        # Jika jumlah molekul kurang dari batas per file, salin saja file ke direktori output
        output_file = os.path.join(output_dir, "output_1.sdf")
        with Chem.SDWriter(output_file) as writer:
            for mol in suppl:
                if mol is not None:
                    writer.write(mol)
        print(f"Successfully copied {input_file} to {output_file}")

def split_smiles_file(input_file, output_dir, lines_per_file=100):
    print(f"Input file: {input_file}")
    
    if not os.path.isfile(input_file):
        print("Error: Input file not found.")
        return
    
    with open(input_file, 'r') as file:
        smiles_data = file.read().splitlines()

    total_files = len(smiles_data) // lines_per_file + 1
    print(f"Total files: {total_files}, Total lines: {len(smiles_data)}")

    if total_files >= 1:
        for file_num, start_idx in enumerate(range(0, len(smiles_data), lines_per_file)):
            end_idx = start_idx + lines_per_file

            output_file = os.path.join(output_dir, f"output_{file_num + 1}.smi")
            with open(output_file, 'w') as output:
                for smiles_line in smiles_data[start_idx:end_idx]:
                    output.write(smiles_line + '\n')
            print(f"Successfully split {input_file} into {output_file}")

    else:
        # Jika jumlah baris kurang dari batas per file, salin saja file ke direktori output
        output_file = os.path.join(output_dir, "output_1.smi")
        with open(output_file, 'w') as output:
            for smiles_line in smiles_data:
                output.write(smiles_line + '\n')
        print(f"Successfully copied {input_file} to {output_file}")

def print_dev(developer_note, developer_contact, citation_list):
    print("")
    print(developer_note)
    print("")
    print(developer_contact)
    print("")
    print(citation_list)
    print("")

def browse_file(entry):
    current_dir = os.getcwd()  # Dapatkan direktori kerja saat ini
    file_path = filedialog.askopenfilename(initialdir=current_dir)
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(tk.END, file_path)

def browse_dir(entry):
    current_dir = os.getcwd()  # Dapatkan direktori kerja saat ini
    dir_path = filedialog.askdirectory(initialdir=current_dir)
    if dir_path:
        entry.delete(0, tk.END)
        entry.insert(tk.END, dir_path)
