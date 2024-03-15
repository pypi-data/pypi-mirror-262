import pandas as pd
import numpy as np
import os
from chembl_webresource_client.new_client import new_client
from rdkit import Chem
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from glob import glob
from tkinter import ttk
import tkinter as tk


# Function to validate smiles
def validate_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        return Chem.MolToSmiles(mol)
    else:
        return None

def combine_csv_files(target, target_dir, result_text):
    # Read all CSV files in the directory
    csv_files = glob(os.path.join(target_dir, '*.csv'))
    
    if not csv_files:
        result_text.insert("end", "No CSV files found in the directory.\n")
        return None  # Return None if no files found

    # Read each file and combine them into one DataFrame
    dfs = [pd.read_csv(file) for file in csv_files if os.path.getsize(file) > 0]        
    
    if not dfs:
        if result_text is not None:
            result_text.insert("end", f"No data in CSV files in the directory {target_dir}.\n")
        return None  # Return None if no data in files
        
    combined_df = pd.concat(dfs, ignore_index=True)
    output_file = os.path.join(target_dir, f'{target}.csv')
    
    # Save the combined DataFrame to one CSV file
    combined_df.to_csv(output_file, index=False)
    if result_text is not None:
        result_text.insert("end", f"Data {target_dir} saved in {output_file}\n")
    return combined_df

def process_chembl_id(chembl_id, target, target_dir, other, others_column):
    try:
        # Load data
        activity = new_client.activity
        res = activity.filter(target_chembl_id=chembl_id).filter(standard_type="IC50")
        df = pd.DataFrame.from_dict(res)

        # Extract columns
        if 'molecule_chembl_id' in df.columns:
            mol_cid = list(df.molecule_chembl_id)
        else:
            mol_cid = []

        if 'canonical_smiles' in df.columns:
            canonical_smiles = list(df.canonical_smiles)
        else:
            canonical_smiles = []

        if 'standard_value' in df.columns:
            standard_value = list(df.standard_value)
        else:
            standard_value = []

        # Create DataFrame with all columns
        data_tuples = list(zip(mol_cid, canonical_smiles, standard_value))
        df = pd.DataFrame(data_tuples, columns=['molecule_chembl_id', 'canonical_smiles', 'standard_value'])

        # Clean and remove duplicates
        df = df.dropna(subset=['molecule_chembl_id'])
        df = df.dropna(subset=['canonical_smiles'])
        df['canonical_smiles'] = df['canonical_smiles'].apply(validate_smiles)
        df = df.drop_duplicates(subset=['molecule_chembl_id'], keep='first', ignore_index=True)

        # Add a new column others and 'target' with the value {target}
        df[others_column] = other
        df['search_term'] = target

        output_file_path = os.path.join(target_dir, f'{chembl_id}.csv')
        df.to_csv(output_file_path, index=False)

        return f"Processed {chembl_id}"

    except Exception as e:
        return f"Error processing {chembl_id}: {str(e)}"


def search_molecules(job_dir, result_text):
    # Set the random seed for reproducibility
    np.random.seed(1)

    df_all_target = []  
    targets = []
    all_results = []

    targets_files = glob(os.path.join(job_dir, 'targets_*.csv'))

    for targets_file_path in targets_files:
        df_targets = pd.read_csv(targets_file_path)
        target_chembl_ids = df_targets['target_chembl_id']
        others_columns = df_targets.columns.difference(['target_chembl_id'])  # Get columns other than 'target_chembl_id'
        target = os.path.splitext(os.path.basename(targets_file_path))[0].replace("targets_", "")
        target_dir = os.path.join(job_dir, target)
        targets.append(target)

        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

        max_workers = os.cpu_count()
        futures = []
        if result_text is not None:
            result_text.insert("end", f"Processing {target}:\n")

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Process chembl_ids in parallel
            for chembl_id in target_chembl_ids:
                other_values = df_targets[df_targets['target_chembl_id'] == chembl_id][others_columns].iloc[0]
                if result_text is not None:
                    result_text.insert("end", f"\t{chembl_id}\n")
                future = executor.submit(process_chembl_id, chembl_id, target, target_dir, other_values, others_columns)
                futures.append(future)

            # Wait for all tasks to complete
            results = [future.result() for future in futures]

        combined_df = combine_csv_files(target, target_dir, result_text)
        print(combined_df)        
                
        if not combined_df.empty:  # Check if DataFrame is not empty before appending
            df_all_target.append(combined_df)
            # Remove the following lines as DataFrame doesn't have 'head' and 'info' methods
            print(df_all_target)

    if df_all_target:
        # Combine all DataFrames in the list
        df_all_target_combined = pd.concat(df_all_target, ignore_index=True)

        # Save the combined DataFrame to one CSV file
        csv_molecules = os.path.join(job_dir, 'merging_' + '_'.join(targets) + '.csv')
        df_all_target_combined.to_csv(csv_molecules, index=False)
        if result_text is not None:
            result_text.insert("end", f"Data all targets saved in {csv_molecules}\n")
        return csv_molecules

    # Move progress_bar update here if needed
    if result_text is not None:
        result_text.insert("end", "No data to combine.\n")
    
    return csv_molecules

    
if __name__ == "__main__":
    job_dir = os.getcwd()
    search_molecule(job_dir)
