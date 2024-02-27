# bot_rock_paper_scissors/services/file_handling.py

import os
import sys

from logger_config import logger

BOOK_PATH = "book/book.txt"
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    # Знаки препинания, которые могут быть в конце страницы
    punctuation_marks = ['.', ',', '!', ':', ';', '?']

    # Начало страницы
    end_index = start + page_size

    # Пока последний символ страницы - знак препинания, уменьшаем размер страницы
    while text[end_index: end_index + 1] in punctuation_marks:
        end_index -= 1

    # Получаем текст страницы с учетом знаков препинания в конце
    page_text = text[start:end_index]

    # Находим индекс последнего знака препинания в тексте страницы
    last_punctuation_index = max(map(page_text.rfind, punctuation_marks)) + 1

    # Обрезаем текст страницы до последнего знака препинания
    page_text = page_text[:last_punctuation_index]

    return page_text, len(page_text)


# Функция, формирующая словарь книги из текстового файла
def prepare_book(file_path: str) -> None:
    logger.info(f"path: {file_path}")
    # Открываем файл с заданным путем для чтения
    with open(file=file_path, mode='r', encoding='utf-8') as file:
        # Считываем текст книги из файла
        text = file.read()

    # Инициализируем начальное положение чтения текста и номер страницы
    current_position, page_number = 0, 1

    # Пока не дочитали весь текст
    while current_position < len(text):
        # Получаем текст и размер следующей страницы
        page_text, page_size = _get_part_text(text, current_position, PAGE_SIZE)

        # Обновляем текущее положение чтения текста
        current_position += page_size

        # Добавляем текст страницы в словарь книги, убирая лишние пробелы в начале и конце
        book[page_number] = page_text.strip()

        # Увеличиваем номер страницы для следующей итерации
        page_number += 1


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
