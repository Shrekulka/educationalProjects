import struct

from config import PARTITION_FORMAT
from logger import logging
from partition import Partition


class PartitionTable:
    def __init__(self):
        self.partitions = []  # Инициализируем список разделов

    def add(self, partition: Partition) -> None:
        """
        Добавляет раздел к таблице разделов.

        Args:
            partition (Partition): Раздел для добавления.

        Returns:
            None: Этот метод не возвращает значения.
        """
        if isinstance(partition, Partition):  # Проверка типа partition
            self.partitions.append(partition)  # Добавляем раздел к таблице
        else:
            logging.error("Invalid partition type. Unable to add partition.")  # Логируем ошибку

    def remove(self, partition: Partition) -> None:
        """
        Удаляет раздел из таблицы разделов.

        Args:
            partition (Partition): Раздел для удаления.

        Returns:
            None: Этот метод не возвращает значения.
        """
        if partition in self.partitions:  # Проверяем, есть ли раздел в таблице
            self.partitions.remove(partition)  # Удаляем раздел из таблицы
        else:
            logging.error("Partition not found. Unable to remove partition.")

    def list_partitions(self) -> list[Partition]:
        """
        Возвращает список разделов в таблице разделов.

        Returns:
            list[Partition]: Список разделов.
        """
        return self.partitions  # Возвращаем список разделов

    def save(self) -> bytes:
        """
        Сериализует данные таблицы разделов в байты.

        Returns:
            bytes: Байты, представляющие данные таблицы разделов.
        """
        partition_data = b''  # Инициализируем байтовую строку для данных разделов
        for partition in self.partitions:
            partition_data += partition.save()  # Сериализуем каждый раздел и добавляем его данные
        return partition_data  # Возвращаем байтовую строку данных

    def load(self, data: bytes) -> None:
        """
        Десериализует данные таблицы разделов из байтов и обновляет таблицу разделов.

        Args:
            data (bytes): Байты, содержащие данные таблицы разделов.

        Returns:
            None: Этот метод не возвращает значения.
        """
        partition_size = struct.calcsize(PARTITION_FORMAT)  # Вычисляем размер структуры раздела
        for i in range(0, len(data), partition_size):
            # Извлекаем данные для одного раздела
            partition_data = data[i:i + partition_size]
            # Создаем временный раздел
            partition = Partition(name="MyPartition", size=1024, start_sector=1, type="FAT32")
            # Десериализуем данные раздела из байтов
            partition.load(partition_data)
            # Добавляем раздел к таблице разделов
            self.partitions.append(partition)
