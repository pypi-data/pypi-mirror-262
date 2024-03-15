import os
import numpy as np
import pandas as pd
from chembl_webresource_client.new_client import new_client
import tkinter as tk

def search_targets(query_list, job_dir, result_text):
    target_list = []
    for search_term in query_list:
        np.random.seed(1)

        # Load target data
        target = new_client.target

        # Perform target search
        target_query = target.search(search_term)
        targets = pd.DataFrame.from_dict(target_query)

        # Select columns and include search_term
        search_term_formatted = search_term.replace(" ", "-")
        selected_columns = ['target_chembl_id', 'pref_name']
        targets['search_term'] = search_term_formatted  # Add search_term column
        targets = targets[selected_columns]

        # Save DataFrame to CSV
        targets_output_file_path = os.path.join(job_dir, f'targets_{search_term_formatted}.csv')
        targets.to_csv(targets_output_file_path, index=False)        

        # Cetak ke result_text
        if result_text is not None:
            result_text.insert(tk.END, f"{search_term.upper()}'s targets saved into {targets_output_file_path}\n")

            target_list.append(targets_output_file_path)
        
    return target_list

def main():
    query_file_path = 'chembl_query.txt'  # Update with the correct file path
    job_dir = os.getcwd()

    with open(query_file_path, 'r') as query_file:
        for search_term in query_file:
            search_term = search_term.strip()
            search_targets(search_term, job_dir)

