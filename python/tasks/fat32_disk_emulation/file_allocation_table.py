import struct

from config import MAX_TABLE_SIZE, FAT_FORMAT, UNPACK_FORMAT, SECTORS_PER_CLUSTER, FAT_SIZE, SEC_SIZE, FAT_ENTRY_SIZE
from exceptions import FatLoadError
from logger import logging


class FileAllocationTable:
    def __init__(self):
        # Инициализация таблицы FAT с нулевыми значениями размером, определенным в MAX_TABLE_SIZE
        self.table = [0] * MAX_TABLE_SIZE

    def allocate_clusters(self, start: int, count: int) -> bool:
        """
        Выделение кластеров

        Args:
            start (int): Начальный кластер для выделения.
            count (int): Количество кластеров для выделения.

        Returns:
            bool: True, если выделение прошло успешно, иначе False.
        """
        # Проверяем, что start и count находятся в допустимых границах
        if start < 0 or start >= MAX_TABLE_SIZE or count <= 0:
            logging.error("Invalid parameters for allocate_clusters.")
            return False

        # Проверяем, что кластеры доступны для выделения
        for cluster in range(start, min(start + count, MAX_TABLE_SIZE)):
            if self.table[cluster] != 0:
                logging.error(f"Cluster {cluster} is already allocated.")
                return False

        # Если проверки прошли успешно, выделяем кластеры
        for cluster in range(start, min(start + count, MAX_TABLE_SIZE)):
            self.table[cluster] = 1

        logging.info(f"Allocated {count} clusters starting from cluster {start}.")
        return True

    def free_clusters(self, start: int, count: int) -> bool:
        """
        Освобождение кластеров

        Args:
            start (int): Начальный кластер для освобождения.
            count (int): Количество кластеров для освобождения.

        Returns:
            bool: True, если освобождение прошло успешно, иначе False.
        """
        # Проверяем, что start и count находятся в допустимых границах
        if start < 0 or start >= MAX_TABLE_SIZE or count <= 0:
            logging.error("Invalid parameters for free_clusters.")
            return False

        # Проверяем, что кластеры доступны для освобождения
        for cluster in range(start, min(start + count, MAX_TABLE_SIZE)):
            if self.table[cluster] != 1:
                logging.error(f"Cluster {cluster} is not allocated.")
                return False

        # Если проверки прошли успешно, освобождаем кластеры
        for cluster in range(start, min(start + count, MAX_TABLE_SIZE)):
            self.table[cluster] = 0

        logging.info(f"Freed {count} clusters starting from cluster {start}.")
        return True

    def read_cluster_chain(self, start_cluster: int) -> list:
        """
        Чтение цепочки кластеров, начиная с указанного начального кластера.

        Args:
            start_cluster (int): Начальный кластер для чтения цепочки.

        Returns:
            list: Список кластеров цепочки.
        """
        cluster_chain = []

        # Проверяем, что start_cluster находится в допустимых границах
        if start_cluster < 0 or start_cluster >= MAX_TABLE_SIZE:
            logging.error("Invalid start_cluster for read_cluster_chain.")
            return cluster_chain

        # Начинаем с указанного начального кластера и читаем цепочку
        current_cluster = start_cluster
        while current_cluster != -1:
            cluster_chain.append(current_cluster)
            if current_cluster < 0 or current_cluster >= MAX_TABLE_SIZE:
                break
            current_cluster = self.table[current_cluster]

        return cluster_chain

    def save(self) -> bytes:
        """
        Сохранение данных структуры FAT в виде байтов.

        Returns:
            bytes: Байтовое представление структуры FAT.
        """
        # Проверка, что структура не пуста
        if not any(self.table):
            logging.warning("Trying to save an empty FAT structure.")
            return b''

        # Формируем данные структуры FAT в виде байтов
        fat_data = struct.pack(UNPACK_FORMAT, *self.table)
        return fat_data

    def load(self, data: bytes) -> None:
        """
        Загрузка данных структуры FAT из байтового представления.

        Args:
            data (bytes): Байтовое представление структуры FAT.

        Raises:
            FatLoadError: Если загрузка не удалась из-за неправильного формата данных.
        """
        # Проверка, что данные не пусты
        if not data:
            logging.warning("Trying to load an empty FAT structure.")
            return

        # Распаковываем данные и заполняем поля структуры
        try:
            self.table = list(struct.unpack(FAT_FORMAT, data))
        except struct.error:
            logging.error("Failed to unpack FAT data. Data format may be incorrect.")
            raise FatLoadError()  # Генерируем ошибку при неудачной загрузке

        # Проверяем размер данных FAT
        expected_size = SECTORS_PER_CLUSTER * FAT_SIZE * SEC_SIZE  # Ожидаемый размер данных FAT (4 КБайта)

        if len(data) != expected_size:
            logging.error(f"Invalid FAT data size: {len(data)} bytes")
            raise FatLoadError()

    def get_table_size(self) -> int:
        """
        Возвращает размер таблицы размещения файлов (FAT) в байтах.

        Returns:
            int: Размер таблицы FAT в байтах, или 0, если размер элементов FAT некорректен.
        """
        logging.info("Getting FAT table size.")

        # Размер одного элемента FAT в байтах
        fat_entry_size = struct.calcsize('I')

        # Проверяем, что размер одного элемента FAT корректен
        if fat_entry_size != FAT_ENTRY_SIZE:
            logging.error(f"Invalid FAT entry size: {fat_entry_size} bytes")
            return 0

        # Вычисляем размер всей таблицы FAT в байтах
        table_size_bytes = len(self.table) * fat_entry_size

        logging.info(f"FAT table size: {table_size_bytes} bytes")
        return table_size_bytes

    def get_next_free_sector(self) -> int:
        """
        Получение следующего доступного сектора в таблице FAT.

        Returns:
            int: Номер следующего доступного сектора или -1, если нет свободных секторов.
        """
        logging.info("Getting next free sector from FAT.")

        # Проверяем, что структура FAT не пуста
        if not any(self.table):
            logging.error("File Allocation Table is empty. No free sectors available.")
            return -1

        # Ищем первый свободный сектор
        for sector, status in enumerate(self.table):
            if status == 0:
                # Метка 0 указывает на свободный сектор
                logging.info(f"Found free sector: {sector}")
                return sector

        # Если не найдено свободных секторов
        logging.error("No free sectors available in File Allocation Table.")
        return -1
