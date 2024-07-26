# messages_to_images_and_back/cli.py

import argparse

from config import config
from steganography import Steganographer


def parse_arguments() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки.

    Возвращает:
        argparse.Namespace: Объект с аргументами командной строки, содержащий значения для 'action', 'image_path' и
        опционально 'message'.
    """
    # Создаем объект ArgumentParser для разбора аргументов командной строки.
    # description: Описание программы, которое будет отображаться при вызове помощи.
    parser = argparse.ArgumentParser(description="Steganography tool for hiding and extracting messages in images.")

    # Добавляем обязательный аргумент 'action'.
    # choices: Ограничивает значения аргумента до указанных опций ('hide' или 'extract').
    # help: Описание этого аргумента, которое будет показано при вызове помощи.
    parser.add_argument('action', choices=['hide', 'extract'], help="Action to perform: 'hide' or 'extract'")

    # Добавляем обязательный аргумент 'image_path'.
    # help: Описание этого аргумента, которое указывает, что нужно предоставить путь к изображению.
    parser.add_argument('image_path', help="Path to the image file")

    # Добавляем необязательный аргумент '--message'.
    # help: Описание этого аргумента, которое указывает, что этот аргумент используется для указания сообщения, которое
    # нужно скрыть.
    parser.add_argument('--message', help="Message to hide (use this option with 'hide' action)")

    # Парсим аргументы командной строки и возвращаем объект Namespace,
    # который содержит значения всех аргументов, введенных пользователем.
    return parser.parse_args()


def process_action(action, image_path, message=None) -> None:
    """
    Выполняет указанное действие (скрытие или извлечение сообщения) с изображением.

    Параметры:
        action (str): Действие для выполнения (может быть 'hide' или 'extract').
        image_path (str): Путь к изображению для обработки.
        message (str, опционально): Сообщение для скрытия (используется только при действии 'hide').

    Возвращает:
        None
    """
    # Создаем объект Steganographer с использованием секретного ключа из конфигурации.
    steganographer = Steganographer(config.secret_key)

    # Проверяем, какое действие нужно выполнить: 'hide' или 'extract'.
    if action == 'hide':
        # Если действие 'hide', проверяем, указано ли сообщение для скрытия.
        # Если сообщение не указано, используем сообщение по умолчанию из конфигурации.
        if message is None:
            message = config.default_payload

        # Вызываем метод hide_payload объекта Steganographer для скрытия сообщения в изображении.
        steganographer.hide_payload(image_path, message)

    # Если действие 'extract', извлекаем сообщение из изображения.
    elif action == 'extract':
        # Вызываем метод extract_payload объекта Steganographer для извлечения сообщения из изображения.
        steganographer.extract_payload(image_path)

