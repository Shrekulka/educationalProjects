# !/usr/bin/env python3

import os
import sys
import traceback
from datetime import datetime

from document_processor import process_document
from font_utils import get_handwriting_fonts, load_fonts


def main() -> None:
    """Основная функция программы.

    Эта функция выполняет следующие действия:
    1. Проверяет наличие аргумента командной строки (входной файл).
    2. Создает выходной файл с уникальным именем на основе временной метки.
    3. Выводит список доступных рукописных шрифтов для выбора пользователем.
    4. Обрабатывает выбранный пользователем шрифт и применяет его к входному документу.
    5. Сохраняет изменённый документ в указанной директории.

    Возвращает:
        None: Функция ничего не возвращает.
    """
    # Проверяем, что передан один аргумент командной строки (имя файла)
    if len(sys.argv) != 2:
        print("Использование: python script.py <имя_файла>")
        sys.exit(1)  # Завершаем программу с кодом 1 (ошибка)

    # Получаем имя входного файла из аргументов командной строки
    input_file = sys.argv[1]
    # Получаем текущую временную метку для уникального имени выходного файла
    timestamp = str(round(datetime.now().timestamp()))
    # Создаем директорию для сохранения обновленных документов, если она не существует
    output_dir = 'updated_documents'
    os.makedirs(output_dir, exist_ok=True)

    # Формируем имя выходного файла, включая путь к директории и временную метку
    output_file = os.path.join(
        output_dir,
        f"updated_{os.path.splitext(os.path.basename(input_file))[0]}_{timestamp}.docx"
    )

    # Выводим список доступных рукописных шрифтов для выбора
    print("Выберите рукописный шрифт:")
    handwriting_fonts = get_handwriting_fonts()  # Получаем шрифты из новой функции

    for key, value in handwriting_fonts.items():
        print(f"{key}. {value}")
    print("6. Выход")

    # Запрашиваем у пользователя номер шрифта, пока не будет введен корректный номер
    while True:
        font_choice = input("Введите номер шрифта (1-6): ")

        # Проверяем, что выбранный шрифт корректен или пользователь хочет выйти
        if font_choice == '6':
            print("Выход из программы.")
            sys.exit(0)  # Завершаем программу с кодом 0 (успешно)
        elif font_choice in handwriting_fonts:
            break  # Выход из цикла, если выбор корректен
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

    # Получаем имя шрифта на основе выбора пользователя
    font_name = handwriting_fonts[font_choice]
    # Загружаем выбранный шрифт (если необходимо)
    load_fonts(font_name)
    # Обрабатываем документ, изменяем шрифт и сохраняем его под новым именем
    process_document(input_file, output_file, font_choice)
    print(f"Документ обработан и сохранен как {output_file}")  # Информируем пользователя о завершении


if __name__ == "__main__":
    try:
        # Запускаем основную функцию программы
        main()
    except KeyboardInterrupt:
        print("Приложение прервано пользователем")
    except Exception as error:
        # Обрабатываем и выводим любые неожиданные ошибки
        detailed_error = traceback.format_exc()
        print(f"Неожиданная ошибка приложения: {error}\n{detailed_error}")
