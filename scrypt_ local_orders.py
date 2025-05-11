import os
import zipfile
from datetime import datetime

base_path = r'D:\Unic_ftp'
output_folder = r'D:\Unic_ftp\script_result'

os.makedirs(output_folder, exist_ok=True)

def extract_files_from_zip(zip_path, formatted_date):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            print(f'Содержимое архива {os.path.basename(zip_path)}:')
            for file_info in zip_ref.infolist():
                print(f' - {file_info.filename}')  # Выводим список файлов в архиве

            files_to_extract = [
                'AKBA_Manual/fxba_net_srv.log',
                'AKBA_Manual/cl_srv2-trade',
                'AKBA_Manual/local_orders.log'
            ]

            for log_filename in files_to_extract:
                if log_filename in zip_ref.namelist():
                    new_file_name = f'{formatted_date}_{os.path.basename(log_filename)}'
                    new_file_path = os.path.join(output_folder, new_file_name)

                    with zip_ref.open(log_filename) as source_file, open(new_file_path, 'wb') as target_file:
                        target_file.write(source_file.read())
                        print(f'Файл {new_file_name} сохранён в {output_folder}')
                else:
                    print(f'Файл {log_filename} не найден в архиве {os.path.basename(zip_path)}.')
    except zipfile.BadZipFile:
        print(f'Ошибка: файл {zip_path} не является ZIP архивом или он поврежден.')

def process_zip_files(month):
    month_str = f'{month:02d}' 
    folder_path = os.path.join(base_path, month_str)

    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.zip'):
                zip_path = os.path.join(folder_path, filename)

                try:
                    zip_date = filename[:10]
                    date_obj = datetime.strptime(zip_date, '%Y.%m.%d')
                    formatted_date = date_obj.strftime('%Y_%m_%d')

                    extract_files_from_zip(zip_path, formatted_date)
                except ValueError as ve:
                    print(f'Ошибка разбора даты в файле {filename}: {ve}')
    else:
        print(f'Папка {folder_path} не найдена.')

def main():
    for month in range(1, 13):
        process_zip_files(month)

if __name__ == '__main__':
    main()