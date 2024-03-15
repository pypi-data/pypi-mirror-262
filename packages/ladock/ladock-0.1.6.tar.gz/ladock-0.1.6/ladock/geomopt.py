import pandas as pd
from pyscf import gto, scf, grad
from rdkit import Chem
from rdkit.Chem import AllChem
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import pyscf
from pyscf.geomopt.geometric_solver import optimize as geometric_opt
from pyscf.geomopt.berny_solver import optimize as pyberny_opt

def geometric_solver(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)
        mol = geometric_opt(mol)
        return mol
    
    except Exception as e:
        logging.error(f"Error in geometric_solver for SMILES '{smiles}': {str(e)}")
        return None

def berny_solver(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)
        mol = pyberny_opt(mol)
        return mol
    
    except Exception as e:
        logging.error(f"Error in geometric_solver for SMILES '{smiles}': {str(e)}")
        return None

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

def mol_uff(smiles, num_conformers=10):
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

def mol_mmff(smiles, num_conformers=10, maxIters=200):
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMultipleConfs(mol, numConfs=num_conformers, randomSeed=42)
        
        lowest_energy = float('inf')
        lowest_energy_conf_id = None

        for conf_id in range(mol.GetNumConformers()):
             initial_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id, ignoreInterfragInteractions=False).CalcEnergy()
             
             AllChem.MMFFOptimizeMolecule(mol, confId=conf_id, maxIters=maxIters)
             optimized_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id).CalcEnergy()                        
             if optimized_energy < lowest_energy:
                lowest_energy = optimized_energy
                lowest_energy_conf_id = conf_id
                optimized_molecule = mol

        return mol
                          
    except Exception as e:
        logging.error(f"Error in mol_mmff for SMILES '{smiles}': {str(e)}")
        return None

def smiles_to_pyscf_input(smiles, basis_set):
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)

        # Mengumpulkan informasi atom dari molekul RDKit
        atom_symbols = [a.GetSymbol() for a in mol.GetAtoms()]
        atom_positions = mol.GetConformer().GetPositions()

        # Membuat molekul PySCF dari informasi atom
        mol_pyscf = gto.M(atom=list(zip(atom_symbols, atom_positions)),
                          basis=basis_set)

        return mol_pyscf

    except Exception as e:
        logging.error(f"Error in smiles_to_pyscf_input for SMILES '{smiles}': {str(e)}")
        return None

def create_rdkit_mol_from_coordinates(optimized_coordinates, molecule_chembl_id):
    try:
        mol_rdkit = Chem.Mol()

        for i, coord in enumerate(optimized_coordinates):
            atom = Chem.Atom(6)  # Karbon, Anda mungkin perlu menyesuaikan jenis atom
            atom.SetAtomMapNum(i + 1)
            atom.SetProp('xCoord', str(coord[0]))
            atom.SetProp('yCoord', str(coord[1]))
            atom.SetProp('zCoord', str(coord[2]))
            mol_rdkit.AddAtom(atom)

        # Set 'molecule_chembl_id' sebagai properti RDKit
        mol_rdkit.SetProp('molecule_chembl_id', str(molecule_chembl_id))

        # Buat 3D conformer dari koordinat
        AllChem.EmbedMolecule(mol_rdkit)

        return mol_rdkit
    
    except Exception as e:
        logging.error(f"Error in create_rdkit_mol_from_coordinates for molecule_chembl_id '{molecule_chembl_id}': {str(e)}")
        return None

def mol_qm(smiles, basis_set='STO-3G'):
    try:
        # Konversi SMILES ke input PySCF
        mol = smiles_to_pyscf_input(smiles, basis_set)

        # Menghitung energi dan gradien
        mf = scf.RHF(mol)

        # geometric
        from pyscf.geomopt.geometric_solver import optimize
        mol_eq_geom = optimize(mf, maxsteps=100)
        print("\n\nmol_eq_geom:")        
        print(mol_eq_geom)

        # pyberny
        from pyscf.geomopt.berny_solver import optimize
        mol_eq_berny = optimize(mf, maxsteps=100)
        print("\n\nmol_eq_berny:")
        print(mol_eq_berny)
        
        return mol_eq_geom, mol_eq_berny
        
    except Exception as e:
        print(f"Error in mol_qm for SMILES '{smiles}': {e}")
        return None, None

def process_smiles(smiles):
    mol = None

    try:
        mol = mol_uff(smiles)

    except Exception as e:
        logging.error(f"Failed to get an optimized molecule for {smiles}: {str(e)}")

    return mol

def visualize_molecule(molecule_info):
    if isinstance(molecule_info, tuple):
        mol = molecule_info[0]
    else:
        mol = molecule_info

    mol_block = Chem.MolToMolBlock(mol)
    viewer = py3Dmol.view(width=400, height=400)
    viewer.addModel(mol_block, "mol")
    viewer.setStyle({"stick": {}})
    viewer.setBackgroundColor("white")
    viewer.zoomTo()
    return viewer.show()

def save_molecule_to_sdf(molecule, sdf_file):
    if molecule is not None:
        # Buat conformer baru jika belum ada
        if molecule.GetNumConformers() == 0:
            AllChem.EmbedMolecule(molecule)

        # Tulis molekul ke dalam file SDF
        writer = Chem.SDWriter(sdf_file)
        writer.write(molecule, confId=0)
        writer.close()
    else:
        print("Molecule is None. Unable to save to SDF.")

def optimize_mol_geometry(smiles, forcefield):
    if forcefield == 'uff':
        mol = mol_uff(smiles)
        return mol
    elif forcefield == 'mmff':
        mol = mol_mmff(smiles)
        return mol
    elif forcefield == '2d':
        mol = mol_2d(smiles)
        return mol
    elif forcefield == '3d':    
        mol = mol_3d(smiles)
        return mol
    elif forcefield == 'qm':
        mol = mol_qm(smiles)
        return mol
    elif forcefield == 'geometric_solver':
        mol = geometric_solver(smiles)
        return mol
    elif forcefield == 'berny_solver':
        mol = berny_solver(smiles)
        return mol
        
    else:
        raise ValueError(f"Unsupported force field: {forcefield}")
        return None

if __name__ == "__main__":

    smiles_list = [
    'CCO',
    'N#C/C(=C\\c1ccc([N+](=O)[O-])cc1)C(=O)O',
    'Cn1cc(-c2ccnc(Nc3ccc(NC(=O)CCCCCCC(=O)NO)cc3)n2)c2ccccc21',
    'Cc1ccc(Oc2ccc(NC(=O)[C@@H]3[C@@H]4C[C@@H]5[C@@H]3C(=O)O[C@@H]5C4)cc2)cc1C',
    'O=C(Nc1ccc(Oc2ccccc2Cl)cc1)[C@H]1[C@@H]2C[C@@H]3[C@@H]1C(=O)O[C@@H]3C2',
    'O=C[C@]1(Cc2ccccc2)[C@@H]2[C@@H]3CC[C@H]4[C@@H]5[C@H]6CC[C@@H]7[C@H]6[C@H]6[C@@H]5[C@@H]([C@@H]34)[C@@H]2[C@@H]6[C@@H]71',
    'Fc1c(F)c2c(F)c(F)c1CCc1c(F)c(F)c(c(F)c1F)CC2',
    'CCCCNC(=O)NCC1=[NH+][C@H]2C=CC=C[C@@H]2N1',
    'CCCCNC(=O)NCC1=[NH+][C@@H]2C=CC=C[C@H]2N1'
    ]
    
    forcefield = "qm"

    for idx, smiles in enumerate(smiles_list):
        try:
          print(idx)
          print(smiles)
          mol = optimize_mol_geometry(smiles, forcefield)
              
        except Exception as e:
          logging.error(f"Failed to get an optimized molecule for {smiles}: {str(e)}")
          
     #   if mol is not None:
            #visualize_molecule(mol)
      #      save_molecule_to_sdf(mol, f'mol_{idx}.sdf')
