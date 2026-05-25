# fontman/fdocument_processor.py

import os

from docx import Document
from docx.enum.style import WD_STYLE_TYPE

from font_utils import get_font_path, get_handwriting_fonts


def process_document(input_file: str, output_file: str, font_choice: str) -> None:
    """
    Обрабатывает документ Word, изменяя стиль шрифтов на выбранный рукописный шрифт.

    Функция загружает документ по указанному входному файлу, проверяет его существование,
    и затем применяет выбранный пользователем стиль шрифта ко всем параграфам в документе.
    Если входной файл не найден, выводится сообщение об ошибке. Изменённый документ
    сохраняется в указанный выходной файл.

    Аргументы:
        input_file (str): Путь к входному документу Word (.docx), который необходимо обработать.
        output_file (str): Путь к выходному документу Word (.docx), в который будут сохранены изменения.
        font_choice (str): Выбор пользователя, указывающий на номер шрифта из доступных рукописных шрифтов.

    Возвращает:
        None: Функция ничего не возвращает. Изменённый документ сохраняется на диск.
    """

    # Проверяем, существует ли входной файл
    if not os.path.exists(input_file):
        print(f"Входной файл {input_file} не найден.")
        return

    # Загружаем документ по указанному входному файлу
    doc = Document(input_file)

    handwriting_fonts = get_handwriting_fonts()  # Получаем шрифты из новой функции

    # Получаем имя шрифта на основе выбора пользователя
    font_name = handwriting_fonts[font_choice]
    # Получаем путь к шрифту (локальный или установленный)
    font_path = get_font_path(font_name)

    # Создаем новый стиль для параграфов с выбранным рукописным шрифтом
    style = doc.styles.add_style(f'Handwriting_{font_choice}', WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = font_path  # Устанавливаем шрифт для нового стиля

    # Применяем созданный стиль ко всем параграфам в документе
    for paragraph in doc.paragraphs:
        paragraph.style = style

    # Сохраняем измененный документ в указанный выходной файл
    doc.save(output_file)
