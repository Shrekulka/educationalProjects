from bootloader import BootLoader
from config import BOOT_SECTOR_SIZE
from logger import logging
from partition_table import PartitionTable


class MasterBootRecord:
    """
    Класс для работы с записью мастер-загрузочного регистра (MBR).
    MBR содержит загрузчик и таблицу разделов.

    Attributes:
        bootloader (BootLoader): Объект загрузочного сектора.
        partition_table (PartitionTable): Объект таблицы разделов.
    """

    def __init__(self):
        """
        Инициализация MBR с пустым загрузочным сектором и таблицей разделов.
        """
        self.bootloader = BootLoader()  # Создаем объект загрузочного сектора
        self.partition_table = PartitionTable()  # Создаем объект таблицы разделов

    def load(self, data: bytes) -> None:
        """
        Загрузка данных MBR из байтового представления.

        Args:
            data (bytes): Байтовое представление MBR.
        """
        # Проверка, что данные не пусты
        if not data:
            logging.warning("Trying to load an empty MBR.")
            return

        # Проверка, что данные достаточной длины
        if len(data) < BOOT_SECTOR_SIZE:
            logging.error("MBR data is too short. Data format may be incorrect.")
            return

        # Извлекаем данные загрузчика и таблицы разделов
        bootloader = data[:BOOT_SECTOR_SIZE]
        partition_table = data[BOOT_SECTOR_SIZE:]

        # Загружаем данные в структуры
        self.bootloader.load(bootloader)
        self.partition_table.load(partition_table)

    def save(self) -> bytes:
        """
        Сохранение данных MBR в виде байтов.

        Returns:
            bytes: Байтовое представление MBR.
        """
        # Получение данных из структур
        bootloader = self.bootloader.save()
        partition_table = self.partition_table.save()

        # Объединяем данные
        return bootloader + partition_table
