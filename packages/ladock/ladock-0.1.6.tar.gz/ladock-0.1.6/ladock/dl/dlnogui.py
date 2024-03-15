import os
from ladock.dl.tf import generate_tensor_model
from ladock.dl.knn import generate_knn_model

def read_config(config_file):
    # Inisialisasi kamus untuk menyimpan nilai variabel konfigurasi
    config = {}

    # Buka file konfigurasi
    with open(config_file, 'r') as file:
        # Baca setiap baris dalam file konfigurasi
        for line in file:
            # Lewati baris yang kosong atau dimulai dengan tanda pagar (#) sebagai komentar
            if line.strip() == '' or line.strip().startswith('#'):
                continue
            
            # Pisahkan kunci dan nilai menggunakan tanda ":" sebagai pemisah
            parts = line.strip().split(':', 1)
            if len(parts) != 2:
                continue  # Lewati baris yang tidak sesuai format
            
            key, value = parts
            
            # Hilangkan spasi ekstra pada nilai
            value = value.strip()
            
            # Jika nilai memiliki tanda koma, pisahkan menjadi daftar nilai
            if ',' in value:
                value = [item.strip() for item in value.split(',')]
            
            # Tambahkan pasangan kunci-nilai ke dalam kamus konfigurasi
            config[key.strip()] = value

    return config

def run_dl():
    # Mengambil nilai variabel dari config.txt
    job_directory_val = job_dir
    csv_val = config['csv']
    columns_to_remove_val = config['columns_to_remove']
    columns_to_remove_val = ','.join(columns_to_remove_val) if isinstance(columns_to_remove_val, list) else columns_to_remove_val
    transformX_val = config['transformX']
    transformX_val = transformX_val.lower()
    scalerX_val = config['scalerX']
    all_features_val = config['all_features']
    activity_column_val = config['activity']
    logarithmic_val = config['logarithmic']
    logarithmic_val = logarithmic_val.lower()
    transformY_val = config['transformY']
    transformY_val = transformY_val.lower()
    scalerY_val = config['scalerY']

    plot_label_val = config['plot_label']
    tool_val = config['tool']

    if tool_val == "TensorFlow":
        # Mengambil nilai variabel tambahan jika menggunakan TensorFlow
        epochs_val = config['epochs']
        batch_size_val = config['batch_size']
        optimizer_val = config['optimizer']
        learning_rate_val = config['learning_rate']
        loss_function_val = config['loss_function']
        dense_units = config['dense_units']
        dense_activations = config['dense_activations']
        patience_val = config['patience']

        # Menyusun parameter
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
        
        print(parameters)

        # Memanggil fungsi untuk menghasilkan model TensorFlow
        generate_tensor_model(result_text=None, **parameters)

    elif tool_val == "K-Nearest Neighbors":
        # Mengambil nilai variabel tambahan jika menggunakan K-Nearest Neighbors
        knn_val = int(config.get('knn_value', 0))

        # Menyusun parameter
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

        # Memanggil fungsi untuk menghasilkan model K-Nearest Neighbors
        generate_knn_model(result_text=None, **parameters)

current_dir = os.getcwd()
job_dir = os.path.join(current_dir, 'dl')
config = read_config(os.path.join (job_dir, 'configdl.txt'))
run_dl()
