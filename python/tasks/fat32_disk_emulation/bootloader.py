from config import BOOT_SECTOR_SIZE
from logger import logging


class BootLoader:
    def __init__(self):
        self.data = None

    def load(self, boot_data: bytes) -> bool:
        """
        Загружает данные загрузочного сектора.

        Args:
            boot_data (bytes): Данные загрузочного сектора. Ожидается тип данных bytes.

        Returns:
            bool: True, если загрузка успешна, иначе False.
        """
        if not isinstance(boot_data, bytes):  # Проверка типа данных boot_data - должен быть bytes
            logging.error("Invalid boot data type.")
            return False

        if len(boot_data) != BOOT_SECTOR_SIZE:  # Проверка размера данных
            logging.error("Invalid boot data size.")
            return False

        self.data = boot_data  # Присвоение атрибуту data загруженных данных
        return True

    def save(self) -> bytes:
        """
        Сохраняет данные загрузочного сектора.

        Returns:
            bytes: Сохраненные данные загрузочного сектора.
        """
        return self.data
