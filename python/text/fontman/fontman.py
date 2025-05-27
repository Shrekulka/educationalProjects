#!/usr/bin/env python3

import os
import sys
from datetime import datetime

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from matplotlib import font_manager


def load_fonts(font_name):
    if is_font_installed(font_name):
        return

    font_dir = 'fonts'
    font_file = get_font_file(font_name)
    if font_file:
        font_path = os.path.join(font_dir, font_file)
        font_manager.fontManager.addfont(font_path)
        font_manager._load_fontmanager(try_read_cache=False)
        print(f"Шрифт {font_name} загружен из локальных файлов.")
    else:
        print(f"Шрифт {font_name} не найден в локальных файлах.")


def get_font_file(font_name):
    font_files = {
        'Segoe Script': 'segoe_script.ttf',
        'Brush Script MT': 'brush_script_mt.otf',
        'Mistral': 'mistral_regular.ttf',
        'Bradley Hand': 'bradleys_pen.ttf',
        'Ink Free': 'ink_free.ttf',
    }
    return os.path.join('fonts', font_files.get(font_name, ''))


def is_font_installed(font_name):
    try:
        font_path = font_manager.findfont(font_name)
        return font_path is not None and font_path != ''
    except:
        return False


def get_font_path(font_name):
    if is_font_installed(font_name):
        return font_name  # Возвращаем имя шрифта, если он установлен в системе
    else:
        local_font_path = get_font_file(font_name)
        if os.path.exists(local_font_path):
            return local_font_path
        else:
            print(f"Шрифт {font_name} не найден ни в системе, ни локально. Используется шрифт по умолчанию.")
            return 'Calibri'


def process_document(input_file, output_file, font_choice):
    doc = Document(input_file)

    handwriting_fonts = {
        '1': 'Segoe Script',
        '2': 'Brush Script MT',
        '3': 'Mistral',
        '4': 'Bradley Hand',
        '5': 'Ink Free',
    }

    font_name = handwriting_fonts[font_choice]
    font_path = get_font_path(font_name)

    style = doc.styles.add_style(f'Handwriting_{font_choice}', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = font_path

    for paragraph in doc.paragraphs:
        paragraph.style = style

    doc.save(output_file)


def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <имя_файла>")
        sys.exit(1)

    input_file = sys.argv[1]
    timestamp = str(round(datetime.now().timestamp()))

    # Создаем директорию для сохранения обновленных документов, если она не существует
    output_dir = 'updated_documents'
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir,
                               f"updated_{os.path.splitext(os.path.basename(input_file))[0]}_{timestamp}.docx")

    print("Выберите рукописный шрифт:")
    print("1. Segoe Script")
    print("2. Brush Script MT")
    print("3. Mistral")
    print("4. Bradley Hand")
    print("5. Ink Free")

    font_choice = input("Введите номер шрифта (1-5): ")

    handwriting_fonts = {
        '1': 'Segoe Script',
        '2': 'Brush Script MT',
        '3': 'Mistral',
        '4': 'Bradley Hand',
        '5': 'Ink Free',
    }

    if font_choice not in handwriting_fonts:
        print("Неверный выбор. Используется шрифт по умолчанию (Segoe Script).")
        font_choice = '1'

    font_name = handwriting_fonts[font_choice]
    load_fonts(font_name)

    process_document(input_file, output_file, font_choice)
    print(f"Документ обработан и сохранен как {output_file}")


if __name__ == "__main__":
    main()
