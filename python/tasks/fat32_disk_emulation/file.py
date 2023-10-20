from datetime import datetime

from logger import logging


class File:
    def __init__(self, name: str):
        """
        Инициализация объекта файла.

        Args:
            name (str): Имя файла.
        """
        self.name = name  # Устанавливаем имя файла
        self.contents = b""  # Инициализируем пустые данные файла
        self.date_created = datetime.now()  # Записываем текущую дату как дату создания файла
        self.size = len(self.contents)  # Вычисляем размер файла (0, так как файл пустой)

    def read(self) -> bytes:
        """
        Чтение содержимого файла.

        Returns:
            bytes: Содержимое файла в виде байтов.
        """
        logging.info(f"Reading file: {self.name}")
        return self.contents

    def write(self, data: bytes) -> None:
        """
        Запись данных в файл.

        Args:
            data (bytes): Данные для записи в файл.

        Raises:
            TypeError: Если переданные данные не являются байтами.
        """
        if not isinstance(data, bytes):
            logging.error(f"Error writing to {self.name}: Data must be of type 'bytes'")
            raise TypeError("Data must be of type 'bytes'")

        logging.info(f"Writing to file: {self.name}")
        self.contents = data

    def append(self, data: bytes) -> None:
        """
        Добавление данных к содержимому файла.

        Args:
            data (bytes): Данные для добавления к содержимому файла.

        Raises:
            TypeError: Если переданные данные не являются байтами.
        """
        if not isinstance(data, bytes):
            logging.error(f"Error appending to {self.name}: Data must be of type 'bytes'")
            raise TypeError("Data must be of type 'bytes'")

        logging.info(f"Appending to file: {self.name}")
        self.contents += data

    def clear(self) -> None:
        """
        Очистка содержимого файла.
        """
        logging.info(f"Clearing file: {self.name}")
        self.contents = b""  # Устанавливаем пустые данные файла

    def is_empty(self) -> bool:
        """
        Проверка, пустой ли файл.

        Returns:
            bool: True, если файл пустой, иначе False.
        """
        return len(self.contents) == 0  # Проверяем длину данных файла

    def get_size(self) -> int:
        """
        Получение размера файла.

        Returns:
            int: Размер файла в байтах.
        """
        size = len(self.contents)  # Вычисляем размер файла
        logging.info(f"Getting size of file {self.name}: {size} bytes")
        return size
