# messages_to_images_and_back/steganography.py

import base64
import hashlib
import os
from datetime import datetime
from pathlib import Path

from cryptography.fernet import Fernet
from stegano import exifHeader

from config import config
from logger_config import logger


class Steganographer:
    """
    Класс для выполнения стеганографии на изображениях. Он может скрывать и извлекать сообщения, используя изображения.

    Атрибуты:
        secret_key (str): Секретный ключ для генерации шифрования.

    Методы:
        generate_key: Генерирует ключ для шифрования на основе секретного ключа.
        generate_filename: Генерирует имя файла для выходного изображения на основе содержимого сообщения и временной
                           метки.
        hide_payload: Скрывает сообщение в изображении и сохраняет его в указанной директории.
        extract_payload: Извлекает сообщение из изображения.
        process_directory: Обрабатывает одно изображение в указанной директории, выполняя указанное действие
                           (скрытие или извлечение сообщений).

    """

    def __init__(self, secret_key: str):
        """
        Инициализирует объект Steganographer.

        Параметры:
        secret_key (str): Секретный ключ для шифрования и дешифрования.
        """
        # Сохраняем переданный секретный ключ в атрибуте объекта
        self.secret_key = secret_key
        # Создаем объект Fernet для шифрования и дешифрования на основе сгенерированного ключа
        self.fernet = Fernet(self.generate_key())

    def generate_key(self) -> bytes:
        """
        Генерирует ключ для шифрования на основе секретного ключа.

        Возвращает:
            bytes: Ключ для шифрования в формате байтов.
        """
        # Создаем ключ для шифрования, используя SHA-256 хэш от секретного ключа
        return base64.urlsafe_b64encode(hashlib.sha256(self.secret_key.encode()).digest())

    def generate_filename(self, content: str) -> str:
        """
        Генерирует имя файла для выходного изображения.

        Параметры:
            content (str): Содержимое сообщения, которое используется для генерации имени файла.

        Возвращает:
            str: Имя выходного файла.
        """
        # Получаем текущую дату в формате YYYYMMDD
        timestamp = datetime.now().strftime("%Y%m%d")
        # Генерируем хэш от содержимого сообщения и берем первые 16 символов
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
        # Формируем имя файла с префиксом, датой и хэшем содержимого
        return f"{config.filename_prefix}{timestamp}_{content_hash}.jpg"

    def hide_payload(self, image_path: str, payload: str) -> str:
        """
        Скрывает сообщение в изображении и сохраняет его в указанной директории.

        Параметры:
            image_path (str): Путь к исходному изображению.
            payload (str): Сообщение, которое нужно скрыть в изображении.

        Возвращает:
            str: Путь к выходному изображению с скрытым сообщением, или пустую строку в случае ошибки.
        """
        image_path = Path(image_path)
        output_directory = Path(config.output_directory)
        try:
            # Проверяем, существует ли исходное изображение
            if not image_path.exists():
                logger.error(f"Source file does not exist: {image_path}")
                return ""

            # Создаем выходную директорию, если она не существует
            output_directory.mkdir(parents=True, exist_ok=True)

            # Шифруем сообщение
            encrypted_payload = self.fernet.encrypt(payload.encode())
            # Генерируем имя для выходного изображения
            output_filename = self.generate_filename(payload)
            output_path = output_directory / output_filename

            # Скрываем зашифрованное сообщение в изображении
            exifHeader.hide(image_path, output_path, encrypted_payload)
            # Выводим сообщение о успешном выполнении
            print(
                f"\n{config.red_bold}Payload successfully hidden in the image:"
                f"{config.reset}\n{config.bright_blue}{output_path}{config.reset}")
            # Возвращаем путь к выходному файлу, где сообщение было успешно скрыто
            return str(output_path)
        except Exception as e:
            logger.error(f"Error hiding payload: {e}")
            return ""

    def extract_payload(self, image_path: str) -> str:
        """
        Извлекает сообщение из изображения.

        Параметры:
           image_path (str): Путь к изображению, из которого нужно извлечь сообщение.

        Возвращает:
           str: Извлеченное сообщение, или пустую строку в случае ошибки.
        """
        try:
            # Проверяем, существует ли изображение
            if not os.path.exists(image_path):
                logger.error(f"File does not exist: {image_path}")
                return ""

            # Извлекаем зашифрованное сообщение из изображения
            encrypted_secret = exifHeader.reveal(image_path)
            # Расшифровываем сообщение
            decrypted_secret = self.fernet.decrypt(encrypted_secret).decode()
            # Выводим извлеченное сообщение
            print(
                f"\n{config.red_bold}Extracted Payload:"
                f"{config.reset}\n{config.bright_blue}{decrypted_secret}{config.reset}")
            # Возвращаем расшифрованное сообщение, извлеченное из изображения
            return decrypted_secret
        except Exception as e:
            logger.error(f"Error extracting or decrypting payload: {e}")
            return ""

    def process_file(self, file_path: str, action: str) -> None:
        """
        Обрабатывает одно изображение, выполняя указанное действие (скрытие или извлечение сообщений).

        Параметры:
           file_path (str): Путь к изображению, которое нужно обработать.
           action (str): Действие для выполнения, может быть 'hide' или 'extract'.

        Возвращает:
           None
        """
        # Проверяем, существует ли файл
        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {file_path}")
            return

        # Проверяем, имеет ли файл допустимое расширение
        if any(file_path.lower().endswith(ext) for ext in config.allowed_extensions):
            # Выполняем действие в зависимости от аргумента
            if action == 'hide':
                self.hide_payload(file_path, config.default_payload)
            elif action == 'extract':
                self.extract_payload(file_path)
        else:
            # Логируем предупреждение, если расширение файла не поддерживается
            logger.warning(f"Skipped file with unsupported extension: {file_path}")
