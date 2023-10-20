import struct

from config import MAX_PARTITION_NAME_LENGTH, NULL_TERMINATOR
from logger import logging


class Partition:
    def __init__(self, name: str, start_sector: int, size: int, type: str):
        """
        Инициализирует объект раздела.

        Args:
            name (str): Имя раздела.
            start_sector (int): Номер начального сектора раздела.
            size (int): Размер раздела в секторах.
            type (str): Тип раздела.
        """
        self.name = name
        self.start_sector = start_sector
        self.size = size
        self.type = type

    def save(self) -> bytes:
        """
        Сериализует данные раздела в байты.

        Returns:
            bytes: Байты, представляющие данные раздела.
        """
        try:
            # Упаковываем данные раздела в байты с использованием формата struct.
            partition_data = struct.pack(
                f'<{MAX_PARTITION_NAME_LENGTH}sII{MAX_PARTITION_NAME_LENGTH}s',
                self.name.encode('utf-8'), self.start_sector, self.size,
                self.type.encode('utf-8')
            )
            return partition_data
        except struct.error as e:
            logging.error(f"Error packing partition data: {e}")
            return b''

    def load(self, data: bytes) -> None:
        """
        Десериализует данные раздела из байтов.

        Args:
            data (bytes): Байты, содержащие данные раздела.

        Returns:
            None: Этот метод не возвращает значения.
        """
        try:
            # Распаковываем данные раздела из байтов, используя формат struct.
            unpacked_data = struct.unpack(
                f'<{MAX_PARTITION_NAME_LENGTH}sII{MAX_PARTITION_NAME_LENGTH}s',
                data
            )
            # Присваиваем распакованные данные атрибутам объекта раздела.
            self.name = unpacked_data[0].decode('utf-8').strip(NULL_TERMINATOR)
            self.start_sector = unpacked_data[1]
            self.size = unpacked_data[2]
            self.type = unpacked_data[3].decode('utf-8').strip(NULL_TERMINATOR)
        except struct.error as e:
            logging.error(f"Error unpacking partition data: {e}")

    def __str__(self) -> str:
        """
        Возвращает строковое представление раздела.

        Returns:
            str: Строковое представление раздела.
        """
        return f"Name: {self.name}, Type: {self.type}, Start Sector: {self.start_sector}, Size: {self.size}"
