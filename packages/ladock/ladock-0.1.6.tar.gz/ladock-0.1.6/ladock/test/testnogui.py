import os
from ladock.test.testing_dl import testing

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
            key, value = line.strip().split(':', 1)
            
            # Hilangkan spasi ekstra pada nilai
            value = value.strip()
            
            # Jika nilai memiliki tanda koma, pisahkan menjadi daftar nilai
            if ',' in value:
                value = [item.strip() for item in value.split(',')]
            
            # Tambahkan pasangan kunci-nilai ke dalam kamus konfigurasi
            config[key.strip()] = value

    return config

def run_test():
    # Mengambil nilai variabel dari config.txt
    model = config['model']
    datatest = config['datatest']
    descriptors = config['descriptors']
    descriptors = [descriptor.strip().upper() for descriptor in descriptors.split(',')]
    method = config['method']
    conformer = config['conformer']
    iteration = config['iteration']
    transformX = config['transformX']
    scalerX = config['scalerX']
    logarithmic = config['logarithmic']
    transformY = config['transformY']
    scalerY = config['scalerY']
            
    # Mencetak semua variabel
    print("Model:", model)
    print("Datatest:", datatest)
    print("Descriptors:", descriptors)
    print("Method:", method)
    print("Conformer:", conformer)
    print("Iteration:", iteration)
    print("TransformX:", transformX)
    print("ScalerX:", scalerX)
    print("Logarithmic:", logarithmic)
    print("TransformY:", transformY)
    print("ScalerY:", scalerY)
            
    # Memanggil fungsi testing dengan parameter dari config.txt
    testing(model, datatest, descriptors, method, conformer, iteration, transformX, scalerX, logarithmic, transformY, scalerY, job_dir, progress_bar=None, result_text=None)

current_dir = os.getcwd()
job_dir = os.path.join(current_dir, 'test')
config = read_config(os.path.join (job_dir, 'configtest.txt'))
run_test()
