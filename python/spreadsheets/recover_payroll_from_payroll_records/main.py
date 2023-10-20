import os
import requests
import zipfile
import pandas as pd
from typing import List


def archive_download(url: str, extract_folder: str) -> str:
    """
    Скачивает архив по указанной ссылке и сохраняет его в указанную папку.

    :param url: Ссылка на архив для скачивания.
    :param extract_folder: Папка для распаковки архива.
    :return: Полный путь к скачанному архиву.
    """
    # Создаем папку для распаковки архива, если она не существует.
    os.makedirs(extract_folder, exist_ok=True)

    # Формируем полный путь к файлу архива.
    archive_path = os.path.join(extract_folder, 'archive.zip')

    # Загружаем архив по указанной URL.
    response = requests.get(url)

    # Открываем файл архива в режиме записи бинарных данных ('wb') и записываем содержимое ответа в файл.
    with open(archive_path, 'wb') as zip_file:
        zip_file.write(response.content)

    # Возвращаем полный путь к скачанному архиву.
    return archive_path


def archive_unpack(archive_path: str, extract_folder: str) -> None:
    """
    Распаковывает архив в указанной папке и удаляет скачанный архив.

    :param archive_path: Полный путь к архиву.
    :param extract_folder: Папка для распаковки архива.
    """
    # Открываем архивный файл в режиме чтения ('r') с использованием библиотеки zipfile.
    # zip_ref будет представлять собой объект, позволяющий работать с содержимым архива.
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        # Распаковываем все файлы из архива в указанную папку (extract_folder).
        zip_ref.extractall(extract_folder)

    # Удаляем скачанный архив, так как он больше не нужен.
    os.remove(archive_path)


def combine_and_save_data(excel_folder: str, output_file: str) -> None:
    """
    Комбинирует данные из файлов Excel в указанной папке и сохраняет результат в Excel и текстовом форматах.

    :param excel_folder: Папка с файлами Excel.
    :param output_file: Полный путь к файлу для сохранения результата.
    """
    # Создаем пустой список all_data, который будет содержать данные о ФИО и начислениях зарплат.
    all_data: List[List[str]] = []

    # Проходим по всем файлам в папке excel_folder.
    for filename in os.listdir(excel_folder):
        # Проверяем, что файл имеет расширение .xlsx.
        if filename.endswith('.xlsx'):
            # Полный путь к файлу.
            file_path = os.path.join(excel_folder, filename)

            # Загружаем содержимое файла Excel в DataFrame df с использованием библиотеки pandas.
            # Задаем header=None, чтобы не использовать автоматический заголовок.
            # Используем engine='openpyxl' для работы с форматом xlsx.
            df = pd.read_excel(file_path, header=None, engine='openpyxl')

            # Переменные для хранения текущего ФИО и начисления зарплаты.
            current_name = None
            current_salary = None

            # Проходим по строкам и колонкам DataFrame.
            for index, row in df.iterrows():
                for col_index, cell in enumerate(row):
                    # Если текущая строка - вторая и текущая колонка - вторая,
                    # то сохраняем значение в current_name.
                    if index == 1 and col_index == 1:
                        current_name = cell
                    # Если текущая строка - вторая и текущая колонка - четвертая,
                    # то сохраняем значение в current_salary.
                    elif index == 1 and col_index == 3:
                        current_salary = cell

            # Если оба значения (ФИО и начисление зарплаты) не пусты,
            # то добавляем их в список all_data.
            if current_name and current_salary:
                all_data.append([current_name, int(current_salary)])

    # Создаем DataFrame combined_data из списка all_data с указанием столбцов.
    combined_data = pd.DataFrame(all_data, columns=['ФИО', 'Начислено'])

    # Сортируем данные по столбцу 'ФИО'.
    combined_data = combined_data.sort_values(by=['ФИО'])

    # Сохраняем DataFrame combined_data в файл Excel с именем output_file.
    # Задаем index=False, чтобы не сохранять индексы строк.
    combined_data.to_excel(output_file, index=False)

    # Создаем текстовый файл с тем же названием, но с расширением .txt.
    # В этот файл записываем данные из DataFrame combined_data в формате "ФИО Начислено".
    with open(output_file.replace('.xlsx', '.txt'), 'w') as f:
        for _, row in combined_data.iterrows():
            line = f"{row['ФИО']} {row['Начислено']}\n"
            f.write(line)


def main() -> None:
    """
    Основная функция для выполнения скрипта.
    """
    # URL архива для скачивания.
    url = 'https://stepik.org/media/attachments/lesson/245299/rogaikopyta.zip'

    # Путь к папке для распаковки архива.
    folder = 'data'

    # Скачиваем архив и сохраняем путь к нему.
    archive_path = archive_download(url, folder)

    # Распаковываем архив в указанную папку.
    archive_unpack(archive_path, folder)

    # Указываем папку с файлами Excel после распаковки.
    excel_folder = folder

    # Полный путь к файлу Excel, в который будут объединены и сохранены данные.
    output_file = os.path.join(folder, 'combined_data.xlsx')

    # Вызываем функцию для объединения и сохранения данных.
    combine_and_save_data(excel_folder, output_file)


if __name__ == '__main__':
    main()
