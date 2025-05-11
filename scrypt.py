# Скрипт по массовому разархивированию файлов и их переименованию в формат ГГГГ_ММ_ДД

import os
import zipfile
from datetime import datetime

# Указываем папки откуда будем брать данные и куда ложить.
base_path = r'D:\Unic_ftp'
output_folder = r'D:\Unic_ftp\script_result'

# Создаем папку для выводимых файлов, если она не существует
os.makedirs(output_folder, exist_ok=True)

# Цикл по всем месяцам от 01 до 12
for month in range(1, 13):
    month_str = f'{month:02d}'  # Форматируем номер месяца как 02 (01, 02, ..., 12)
    folder_path = os.path.join(base_path, month_str)

    if os.path.exists(folder_path):
        # Получаем список всех zip файлов в папке
        for filename in os.listdir(folder_path):
            if filename.endswith('.zip'):  # Проверяем, что файл - это zip
                zip_path = os.path.join(folder_path, filename)

                try:
                    # Извлекаем дату из имени zip файла
                    zip_date = filename[:10]  # Предполагается, что дата в формате YYYY.MM.DD
                    date_obj = datetime.strptime(zip_date, '%Y.%m.%d')  # Изменяем формат на '%Y.%m.%d'
                    formatted_date = date_obj.strftime('%Y_%m_%d')  # Форматируем дату как год_месяц_дата

                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        # Извлекаем только файл db_operations.log
                        for file_info in zip_ref.infolist():
                            if 'local_orders.log' in file_info.filename:
                                # Формируем новое имя файла, используя только дату
                                new_file_name = f'{formatted_date}.log'
                                new_file_path = os.path.join(output_folder, new_file_name)

                                # Извлекаем файл и сохраняем в новую папку
                                with zip_ref.open(file_info) as source_file, open(new_file_path, 'wb') as target_file:
                                    target_file.write(source_file.read())
                                    print(f'Файл {new_file_name} сохранён в {output_folder}')
                except zipfile.BadZipFile:
                    print(f'Ошибка: файл {zip_path} не является ZIP архивом или он поврежден.')
                except ValueError as ve:
                    print(f'Ошибка разбора даты в файле {filename}: {ve}')
    else:
        print(f'Папка {folder_path} не найдена.')
