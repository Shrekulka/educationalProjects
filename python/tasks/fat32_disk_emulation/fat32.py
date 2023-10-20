import os
import shutil
import sys
import time
import uuid
from typing import Dict, Union, Optional, List

from config import (SEC_PER_CLUS, NUM_FATS, NUM_ROOT_ENTRIES, DISK_SIZE, MAX_DISK_SIZE, SEC_SIZE, BOOT_SECTOR_SIZE,
                    FAT_SIZE, ROOT_DIR_SIZE, DISK_FORMAT, UNPACK_FORMAT, SECTORS_PER_CLUSTER, NULL_BYTE, )
from directory import Directory
from exceptions import FatLoadError, FileAllocationError
from file import File
from file_allocation_table import FileAllocationTable
from logger import logging
from master_boot_record import MasterBootRecord
from root_directory import RootDirectory


class Fat32:
    """
    Класс для работы с эмулированным диском в формате FAT32.

    Args:
        filename (str, optional): Путь к файлу диска. По умолчанию '/my_disk.img'.
        disk_size_bytes (int, optional): Размер эмулированного диска в байтах. По умолчанию DISK_SIZE.

    Attributes:
    filename (str): Путь к файлу диска.
    current_directory (str): Текущая директория на диске.
    disk_size_bytes (int): Размер диска в байтах.
    mbr (MasterBootRecord): Экземпляр класса MasterBootRecord, представляющий загрузочный сектор.
    fat (FileAllocationTable): Экземпляр класса FileAllocationTable, представляющий таблицу размещения файлов (FAT).
    root_dir (RootDirectory): Экземпляр класса RootDirectory, представляющий корневой каталог.
    is_mounted (bool): Флаг, указывающий, смонтирован ли диск.
    previous_directory (str): Предыдущий каталог.
    sec_per_clus (int): Количество секторов на кластер.
    num_fats (int): Количество таблиц размещения файлов (FAT).
    num_root_entries (int): Количество записей в корневом каталоге.
    is_new_disk (bool): Флаг, указывающий, что диск новый.
    fat_sec (int): Сектор, где находится таблица размещения файлов (FAT).
    root_dir_sec (int): Сектор, где находится корневой каталог.
    disk_size (int): Размер диска.
    sectors_per_cluster (int): Количество секторов на кластер.
    fat_size (int): Размер таблицы размещения файлов (FAT).
    allocated_sectors (Dict[int, int]): Словарь для отслеживания выделенных секторов на диске.


    Methods:
        1. Инициализация и основные операции:

        __init__: Инициализация объекта класса.
        create_disk: Создание нового диска.
        load_or_create_disk: Загрузка существующего диска или создание нового.
        format: Форматирование диска.
        mount: Смонтировать диск.
        unmount: Размонтировать диск.
        check_disk_size: Проверка размера диска.
        initialize_disk_structures: Инициализация структур данных на диске.
        initialize_root_directory: Инициализация корневого каталога диска.
        clear_disk_structures: Очистка структур данных на диске.

        2. Операции с каталогами и файлами:

        ls: Вывод списка файлов и каталогов.
        cd: Изменение текущей директории.
        mkdir: Создание каталога в текущей директории.
        touch: Создание файла в текущей директории.
        get_entry: Получение записи из каталога по имени.
        dir_exists: Проверка существования каталога.
        get_dir_listing: Получение списка файлов и каталогов в директории.

        3. Операции с таблицей размещения файлов (FAT):

        write_fat_data: Запись данных таблицы размещения файлов (FAT) на диск.
        is_valid_disk_format: Проверка формата диска.
        has_allocated_sectors: Проверка наличия выделенных секторов на диске.
        is_disk_structures_empty: Проверка, пусты ли структуры данных на диске.

        4. Операции сохранения и загрузки данных:

        save: Сохранение диска.
        load: Загрузка диска.

        5. Обработка ошибок и логирование:

        handle_disk_creation_error: Обработка ошибки создания диска.
        handle_disk_not_found: Обработка ошибки отсутствия файла диска.

    Raises:
        FileNotFoundError: Возникает, если файл диска не существует и не удалось создать новый.
        ValueError: Возникает при нарушении ограничений размера диска или других значениях.
        FatLoadError: Возникает, если произошла ошибка при загрузке данных из таблицы размещения файлов (FAT).
        OSError: Возникает при общих ошибках ввода/вывода, таких как отсутствие доступа к файлу и другие системные ошибки.
    """

    def __init__(self, filename: str = '/my_disk.img', disk_size_bytes: int = DISK_SIZE) -> None:
        """
        Инициализирует диск из указанного файла или создает новый диск.

        Args:
            filename (str, optional): Путь к файлу диска. По умолчанию - '/my_disk.img'.
            disk_size_bytes (int, optional): Размер эмулированного диска в байтах. По умолчанию - DISK_SIZE.

        Raises:
            FileNotFoundError: Если файл диска не существует и не удалось создать новый.
        """
        # Инициализация класса Fat32.
        logging.info("Fat32 class initialization.")
        self.filename = filename  # Имя файла диска
        self.disk_size_bytes = disk_size_bytes  # Размер диска в байтах
        self.is_mounted = False  # Флаг, указывающий, смонтирован ли диск (изначально не смонтирован)
        self.previous_directory = '/'  # Предыдущий каталог (изначально корневой каталог)
        self.sec_per_clus = SEC_PER_CLUS  # Количество секторов на кластер
        self.num_fats = NUM_FATS  # Количество таблиц размещения файлов (FAT)
        self.num_root_entries = NUM_ROOT_ENTRIES  # Количество записей в корневом каталоге
        self.is_new_disk = False  # Флаг, указывающий, что диск новый (изначально False)
        self.fat_sec = None  # Сектор, где находится таблица размещения файлов (FAT)
        self.root_dir_sec = None  # Сектор, где находится корневой каталог
        self.disk_size = None  # Размер диска
        self.sectors_per_cluster = None  # Количество секторов на кластер
        self.fat_size = None  # Размер таблицы размещения файлов (FAT)
        self.root_dir = RootDirectory()  # Инициализация корневого каталога
        self.current_directory = self.root_dir  # Инициализируем текущий каталог как корневой каталог
        self.allocated_sectors: Dict[int, int] = {}  # Словарь для отслеживания выделенных секторов на диске
        self.mbr = MasterBootRecord()  # Инициализация загрузочного сектора (MBR)
        self.fat = FileAllocationTable()  # Инициализация таблицы размещения файлов (FAT)
        self.print_loading_message()  # Вывод сообщения о загрузке диска
        self.check_disk_size()  # Проверка размера диска
        self.load_or_create_disk()  # Загрузка существующего диска или создание нового

    def print_loading_message(self) -> None:
        """
        Вывод сообщения о загрузке диска.
        """
        logging.info("Disk loading message.")
        print(f"Loading disk from file: {self.filename}")

    def check_disk_size(self) -> None:
        """
        Проверка размера диска.

        Эта функция выполняет проверку размера диска на соответствие определенным ограничениям:
        1. Проверяет, что размер диска (self.disk_size_bytes) больше или равен размеру загрузочного сектора.
        2. Проверяет, что размер диска не превышает максимально допустимый размер (MAX_DISK_SIZE).

        Если одно из условий не выполняется, функция выбрасывает исключение ValueError с соответствующим сообщением.

        Returns:
            None
        """
        logging.info("Checking disk size.")

        # Шаг 1: Проверка минимального размера диска
        if self.disk_size_bytes < BOOT_SECTOR_SIZE:
            raise ValueError("Disk size is too small. It must be at least equal to or greater than BOOT_SECTOR_SIZE.")

        # Шаг 2: Проверка максимального размера диска
        if self.disk_size_bytes > MAX_DISK_SIZE:
            raise ValueError("Disk size exceeds the maximum allowed size.")

    def load(self) -> None:
        """
        Загрузка диска.

        Эта функция загружает данные диска из файла, имя которого указано в self.filename. Она выполняет следующие шаги:
        1. Открывает файл диска для чтения в бинарном режиме.
        2. Загружает загрузочный сектор (MBR) с помощью метода self.mbr.load().
        3. Загружает данные таблицы размещения файлов (FAT) с помощью метода self.fat.load().
        4. Загружает данные корневого каталога с помощью метода self.root_dir.load().
        5. Закрывает файл диска после загрузки данных.

        Если произойдет ошибка при загрузке данных, она будет зарегистрирована с помощью модуля logging.

        Returns:
            None
        """
        with open(self.filename, 'rb') as f:
            # Шаг 1: Загрузка загрузочного сектора (MBR)
            bootloader = f.read(BOOT_SECTOR_SIZE)
            self.mbr.load(bootloader)

            # Шаг 2: Загрузка данных таблицы размещения файлов (FAT)
            fat_data = f.read(FAT_SIZE)
            logging.debug("FAT raw data: %s", fat_data)
            if len(fat_data) != FAT_SIZE:
                logging.error("Invalid FAT size: %d", len(fat_data))
                raise FatLoadError
            self.fat.load(fat_data)

            # Шаг 3: Загрузка данных корневого каталога
            root_dir_data = f.read(ROOT_DIR_SIZE)
            self.root_dir.load(root_dir_data)

        # Шаг 4: Загрузка оставшихся данных таблицы размещения файлов (FAT)
        fat_data = f.read(FAT_SIZE)
        self.fat.load(fat_data)
        logging.debug(f"Unpacking {len(fat_data)} bytes of FAT data with format {UNPACK_FORMAT}")

    def save(self) -> None:
        """
        Сохранение диска.

        Эта функция сохраняет данные диска в файл с именем, указанным в self.filename. Она выполняет следующие шаги:
        1. Открывает файл диска для записи в бинарном режиме.
        2. Сохраняет загрузочный сектор (MBR) с помощью метода self.mbr.save().
        3. Сохраняет данные таблицы размещения файлов (FAT) с помощью метода self.fat.save().
        4. Сохраняет данные корневого каталога с помощью метода self.root_dir.save().
        5. Закрывает файл диска после сохранения данных.

        Если произойдет ошибка при сохранении данных, она будет зарегистрирована с помощью модуля logging.

        Returns:
            None
        """
        try:
            logging.info(f"Saving disk data to '{os.path.abspath(self.filename)}'...")

            with open(self.filename, 'wb') as f:
                # Сохраняем загрузочный сектор (MBR)
                bootloader = self.mbr.save()
                f.write(bootloader)
                logging.info("Bootloader saved successfully.")

                # Сохраняем данные таблицы размещения файлов (FAT)
                fat_data = self.fat.save()
                f.write(fat_data)
                logging.info("FAT data saved successfully.")

                # Сохраняем данные корневого каталога
                root_dir_data = self.root_dir.save()
                f.write(root_dir_data)
                logging.info("Root directory data saved successfully.")

            logging.info(f"Disk data successfully saved to '{os.path.abspath(self.filename)}'!")

        except Exception as save_error:
            logging.error(f'Error saving disk data to "{os.path.abspath(self.filename)}": {save_error}')

    def load_or_create_disk(self) -> None:
        """
        Загрузка существующего диска или создание нового.

        Returns:
            None
        """
        logging.info("Loading or creating a disc.")

        if os.path.exists(self.filename):
            self.load()
        else:
            self.handle_disk_not_found()  # Обработка ошибки отсутствия файла диска

    def handle_disk_not_found(self) -> None:
        """
        Обработка ошибки отсутствия файла диска.

        Returns:
            None
        """
        logging.info(f"Disk file '{self.filename}' not found. Attempting to create a new {DISK_SIZE} MB disk.")
        try:
            self.create_new_disk()  # Попытка создания нового диска
        except Exception as creation_error:
            self.handle_disk_creation_error(creation_error)  # Обработка ошибки создания диска

    @staticmethod
    def handle_disk_creation_error(error: Exception) -> None:
        """
        Обработка ошибки создания диска.

        Args:
            error (Exception): Исключение, связанное с созданием диска.

        Returns:
            None
        """
        logging.error(f'Error creating a new disk: {error}')
        sys.exit(1)

    def create_new_disk(self) -> None:
        """
        Создает новый файл диска.

        Returns:
            None
        """
        # Указываем путь к временному каталогу для сохранения файла диска
        tmp_dir = "/Users/shrekulka/educationalProjects/python/tasks/fat32_disk_emulation/tmp"

        # Генерируем уникальное имя файла на основе текущего времени и случайного UUID
        timestamp = int(time.time() * 1000)  # Получаем текущее время в миллисекундах
        unique_id = uuid.uuid4()  # Генерируем случайный UUID
        filename = f"{tmp_dir}/disk_{timestamp}_{unique_id}.disk"  # Составляем имя файла

        # Проверяем, существует ли файл по указанному пути
        if os.path.exists(filename):
            logging.error(f"Disk file '{filename}' already exists.")
            return

        # Получаем свободное место на диске, где будет создан файл диска
        free_space = shutil.disk_usage(tmp_dir).free

        # Проверяем, достаточно ли свободного места для создания файла диска
        if free_space < self.disk_size_bytes:
            logging.error("Not enough free disk space to create disk file")
            return

        logging.info(f"Creating new disk file: {os.path.abspath(filename)}")

        try:
            # Создаем новый файл диска и заполняем его нулевыми байтами до указанного размера
            with open(filename, 'xb') as f:
                f.write(NULL_BYTE * self.disk_size_bytes)

            # Сохраняем информацию о новом диске
            self.filename = filename  # Сохраняем имя файла
            self.disk_size = self.disk_size_bytes  # Сохраняем размер диска в байтах
            self.sectors_per_cluster = SECTORS_PER_CLUSTER  # Устанавливаем количество секторов на кластер
            self.num_fats = NUM_FATS  # Устанавливаем количество таблиц FAT
            self.fat_size = FAT_SIZE  # Устанавливаем размер таблицы FAT

            # Инициализируем структуры данных для нового диска
            self.initialize_disk_structures()
            self.mbr = MasterBootRecord()  # Создаем новую запись MBR
            self.fat = FileAllocationTable()  # Создаем новую таблицу FAT
            self.root_dir = RootDirectory()  # Создаем новый корневой каталог

            logging.info("New disk successfully created!!!")
            logging.info(f"Disk size: {self.disk_size} bytes")
            logging.info(f"Sectors per cluster: {self.sectors_per_cluster}")
            logging.info(f"Number of FATs: {self.num_fats}")
            logging.info(f"FAT size: {self.fat_size} bytes")

        except OSError as e:
            logging.error(f"Error creating disk file: {e}")
            return
        except Exception as creation_error:
            logging.error("Error writing to disk file. Disk was not created.")
            logging.error(f"Error creating disk file: {creation_error}")
            print("Error creating disk file. Please check logs for details.")
            return

    def initialize_disk_structures(self) -> None:
        """
        Инициализирует структуры данных диска.

        Returns:
            None
        """
        logging.info("Инициализация структур данных диска.")

        # Создаем MBR
        self.mbr = MasterBootRecord()

        # Создаем таблицу файловой выделенной памяти (FAT)
        self.fat = FileAllocationTable()

        # Создаем корневой каталог
        self.root_dir = RootDirectory()

        logging.info("Структуры данных диска инициализированы.")

    @staticmethod
    def create_disk_file(filename: str, size_mb: int) -> None:
        """
        Создает файл диска заданного размера.

        Args:
            filename (str): Имя файла диска.
            size_mb (int): Размер диска в мегабайтах.

        Returns:
            None
        """
        with open(filename, 'wb') as f:
            f.seek(size_mb * SEC_SIZE)  # Используем SEC_SIZE для вычисления размера в байтах
            f.write(b'\0')

    def check_disk_file(self) -> None:
        """
        Проверяет наличие файла диска и создает новый, если его нет.

        Returns:
            None
        """
        if not os.path.exists(self.filename):
            logging.warning(f"Disk file {self.filename} not found.")
            logging.info(f"Creating a new disk of size {DISK_SIZE} MB.")
            self.create_new_disk()
        else:
            logging.info(f"Disk file {self.filename} found")

    def format(self) -> bool:
        """
        Форматирует диск.

        Returns:
            bool: True, если форматирование успешно, в противном случае - False.
        """
        logging.info(f"Start formatting the disk: {self.filename}")

        # Проверяем, смонтирован ли диск
        if not self.is_mounted:
            logging.error("Disk is not mounted. Cannot format.")
            return False

        # Проверяем, занято ли диск (есть выделенные сектора)
        if self.has_allocated_sectors():
            logging.error("Unable to format a busy disk.")
            return False

        # Проверяем, соответствует ли формат диска ожидаемому формату
        if not self.is_valid_disk_format():
            logging.error(f"Unknown disk format. Expected format: {DISK_FORMAT}")
            return False

        logging.debug(f"Formatting disk structures for disk: {self.filename}")

        # Очищаем структуры данных диска
        if not self.clear_disk_structures():
            logging.error("Failed to clear disk structures.")
            return False

        logging.debug(f"Generating new FAT data for disk: {self.filename}...")

        # Генерируем новые данные FAT
        fat_data = self.fat.save()

        # Выводим данные FAT (первые 16 байт)
        logging.debug(f"FAT data (first 16 bytes) for disk: {self.filename}: {fat_data[:16]}")

        # Проверяем размер данных FAT
        expected_size = self.num_fats * self.fat.get_table_size()
        if len(fat_data) != expected_size:
            logging.error(
                f"Invalid FAT data size for disk: {self.filename}. Expected {expected_size} bytes, got {len(fat_data)} bytes.")
            return False

        logging.debug(f"Writing FAT data to disk: {self.filename}...")

        # Записываем данные FAT на диск
        if not self.write_fat_data(fat_data):
            logging.error(f"Failed to write FAT data to disk: {self.filename}.")
            return False

        logging.debug(f"Initializing root directory for disk: {self.filename}...")

        # Инициализируем корневой каталог
        if not self.initialize_root_directory():
            logging.error(f"Failed to initialize root directory for disk: {self.filename}.")
            return False

        # Сохраняем изменения на диск
        try:
            self.save()
            logging.info(f"Disk successfully formatted: {self.filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to save changes to disk: {e}")
            return False

    def initialize_root_directory(self) -> bool:
        """
        Инициализирует корневой каталог диска.

        Returns:
            bool: True, если инициализация успешна, в противном случае - False.
        """
        logging.info("Initializing root directory.")

        # Проверяем, смонтирован ли диск
        if not self.is_mounted:
            logging.error("Disk is not mounted. Cannot initialize root directory.")
            return False

        try:
            # Создаем корневой каталог
            root_dir = Directory("")

            # Добавляем ссылку на текущий каталог (".")
            root_dir.add_entry(".", root_dir)

            # Добавляем ссылку на родительский каталог ("..")
            root_dir.add_entry("..", root_dir)

            # Добавляем корневой каталог в структуры данных диска
            self.root_dir = root_dir
            self.root_dir_sec = self.fat.get_next_free_sector()

            # Вычисляем размер корневого каталога
            root_dir_size = self.root_dir.calculate_size()

            # Выводим информацию о корневом каталоге
            logging.info("Root directory successfully initialized.")
            logging.info(f"Root directory sector: {self.root_dir_sec}")
            logging.info(f"Root directory size: {root_dir_size} bytes")

            return True

        except FileAllocationError as e:
            logging.error(f"Failed to allocate a sector for the root directory: {e}")
            return False

        except Exception as e:
            logging.error(f"An unexpected error occurred while initializing root directory: {e}")
            return False

    def write_fat_data(self, fat_data) -> bool:
        """
        Записывает данные таблицы файловой выделенной памяти (FAT) на диск.

        Args:
            fat_data (bytes): Байтовое представление данных FAT.

        Returns:
            bool: True, если запись успешна, в противном случае - False.
        """
        logging.info("Writing FAT data to disk.")

        # Проверяем, смонтирован ли диск
        if not self.is_mounted:
            logging.error("Disk is not mounted. Cannot write FAT data.")
            return False

        # Проверяем, не пусты ли данные FAT
        if not fat_data:
            logging.error("FAT data is empty. Nothing to write.")
            return False

        try:
            with open(self.filename, 'rb+') as f:
                # Переходим к сектору с данными FAT
                f.seek(self.fat_sec * SEC_SIZE)

                # Записываем данные FAT на диск
                f.write(fat_data)

            logging.info("FAT data successfully written to disk.")
            return True

        except Exception as e:
            logging.error(f"Failed to write FAT data to disk: {e}")
            return False

    def is_disk_structures_empty(self) -> bool:
        """
        Проверяет, пусты ли структуры данных диска.

        Returns:
            bool: True, если структуры данных диска пусты, False в противном случае.
        """
        logging.info("Checking if disk structures are empty.")

        # Проверяем, не содержит ли allocated_sectors выделенных секторов
        if self.allocated_sectors:
            logging.error("Disk structures are not empty. Allocated sectors found.")
            return False

        # Добавьте другие проверки для пустоты других структур данных, если необходимо
        if self.root_dir.entries:
            logging.error("Root directory is not empty.")
            return False

        # Если ни одна из проверок не вернула False, это означает, что структуры данных диска пусты
        logging.info("Disk structures are empty.")
        return True

    def mount(self) -> bool:
        """
        Монтирует диск.

        Returns:
            bool: True, если диск успешно смонтирован, False в противном случае.
        """
        logging.info("Mounting the disk.")

        if not os.path.exists(self.filename):
            logging.error("Disk file does not exist.")
            return False

        try:
            self.load()
        except Exception as e:
            logging.error(f"Failed to load disk data: {e}")
            return False

        if not self.is_valid_disk_format():
            logging.error("Unknown disk format.")
            return False

        self.is_mounted = True
        logging.info("Disk successfully mounted.")
        return True

    def unmount(self) -> None:
        """
        Отмонтирует диск.

        Returns:
            None
        """
        logging.info("Unmounting the disk.")

        # Добавьте проверку, был ли диск смонтирован перед отмонтированием
        if not self.is_mounted:
            logging.error("Disk is not mounted. Cannot unmount.")
            return

        self.save()

        # Сбрасываем флаг монтирования
        self.is_mounted = False

        logging.info("Disk successfully unmounted.")

    def is_valid_disk_format(self) -> bool:
        """Проверяет формат диска."""
        with open(self.filename, 'rb') as f:
            boot_sector = f.read(BOOT_SECTOR_SIZE)

        # Проверяем, содержит ли байты 82-89 в загрузочном секторе формат "FAT32"
        if boot_sector[82:90] == DISK_FORMAT:
            return True
        else:
            return False

    def has_allocated_sectors(self) -> bool:

        """
        Проверяет, занят ли диск (есть выделенные секторы).

        Returns:
            bool: True, если есть выделенные секторы, и False в противном случае.
        """

        logging.info("Checking for allocated sectors.")
        return len(self.allocated_sectors) > 0

    def clear_disk_structures(self) -> None:
        """
        Очищает структуры данных диска.

        Returns:
            None: Этот метод не возвращает значения.
        """
        logging.info("Clean up disk data structures.")
        self.allocated_sectors = {}

    def get_current_dir(self) -> Union[Directory, RootDirectory]:
        """
        Возвращает текущий каталог.

        Returns:
            Union[Directory, RootDirectory]: Текущий каталог.
        """
        logging.debug(f"Current directory: {self.current_directory}")
        return self.current_directory

    @staticmethod
    def dir_exists(path: str) -> bool:
        """
        Проверяет существование каталога.

        Args:
            path (str): Путь к каталогу.

        Returns:
            bool: True, если каталог существует, и False в противном случае.
        """
        logging.debug(f"Checking if a directory exists {path}.")

        try:
            # Используем функцию os.path.isdir() для проверки существования каталога
            return os.path.isdir(path)
        except Exception as e:
            logging.error(f"Error checking directory existence: {e}")
            return False

    @staticmethod
    def get_dir_listing(path: str) -> List[str]:
        """
        Получает список файлов и каталогов в каталоге.

        Аргументы:
            path (str): Путь к каталогу.

        Возвращает:
            List[str]: Список имен файлов и каталогов в указанном каталоге.
        """
        logging.debug(f"Getting a list for {path}.")

        try:
            # Используем функцию os.listdir() для получения списка элементов в указанной директории
            dir_listing = os.listdir(path)
            return dir_listing
        except FileNotFoundError:
            logging.error(f"Directory {path} not found.")
            return []

    def create_dir(self, name: str) -> Optional[Directory]:
        """
        Создает каталог в текущем каталоге.

        Args:
            name (str): Имя нового каталога.

        Returns:
            Optional[Directory]: Созданный каталог, или None, если что-то пошло не так.
        """
        logging.info(f"Creating directory {name}.")

        # Проверяем, смонтирован ли диск
        if not self.is_mounted:
            logging.error("Disk is not mounted. Cannot create a directory.")
            return None

        # Проверяем, существует ли уже каталог или файл с таким же именем в текущем каталоге
        if self.current_directory.get_entry(name) is not None:
            logging.error(f"Directory or file with name {name} already exists in the current directory.")
            return None

        # Создаем новый каталог
        new_directory = Directory(name)

        # Добавляем новый каталог в текущий каталог
        self.current_directory.create_entry(name, new_directory)

        logging.info(f"Directory {name} created successfully!")
        return new_directory  # Возвращаем созданный каталог

    def ls(self) -> List[str]:
        """
        Список файлов и каталогов.

        Returns:
            List[str]: Список имен файлов и каталогов в текущем каталоге.
        """
        logging.info(f"Список файлов и каталогов в {self.current_directory}:")

        # Проверяем, смонтирован ли диск
        if not self.is_mounted:
            logging.error("Диск не смонтирован. Невозможно получить список файлов и каталогов.")
            return []

        # Получаем список записей (файлов и каталогов) в текущем каталоге (корневом каталоге)
        entries = list(self.current_directory.entries.keys())

        # Проверяем, пуст ли текущий каталог
        if not entries:
            return ["Текущий каталог пуст."]

        result = []
        for entry_name in entries:
            entry = self.current_directory.entries[entry_name]
            # Определяем тип записи (файл или каталог)
            entry_type = "Файл" if isinstance(entry, File) else "Каталог"
            # Определяем размер записи (если это файл)
            entry_size = entry.size if isinstance(entry, File) else "N/A"
            # Определяем дату создания записи (если у нее есть атрибут 'date_created')
            entry_date_created = entry.date_created.strftime("%Y-%m-%d %H:%M:%S") if hasattr(entry,
                                                                                             'date_created') else "N/A"

            result.append(f"{entry_type}\t{entry_name}\t{entry_size}\t{entry_date_created}")

        return result

    def cd(self, path: str) -> bool:
        """
        Изменяет текущий каталог на указанный путь (абсолютный путь).

        Args:
            path (str): Абсолютный путь к каталогу, на который нужно изменить текущий каталог.

        Returns:
            bool: True, если текущий каталог был успешно изменен, False в противном случае.
        """
        logging.info(f"Changing current directory to {path}.")

        # Проверяем, смонтирован ли диск
        if not self.is_mounted:
            logging.error("Disk is not mounted. Cannot change directory.")
            return False

        # Проверяем, существует ли указанный каталог
        if not self.dir_exists(path):
            logging.error(f"Directory {path} does not exist.")
            return False

        # Устанавливаем новый текущий каталог
        self.current_directory = path

        logging.info(f"Current directory changed to {path}.")
        return True

    def get_entry(self, name: str) -> Union[Directory, File, None]:
        """Получает запись из каталога по имени.

        Args:
            name (str): Имя записи, которую нужно найти.

        Returns:
            entry (Union[Directory, File, None]): Найденная запись (каталог или файл) или None, если запись не найдена.
        """
        for entry in self.root_dir.entries:
            # Проверяем, что entry является объектом типа Directory или File
            if isinstance(entry, (Directory, File)):
                # Проверяем, совпадает ли имя entry с заданным именем
                if entry.name == name:
                    # Возвращаем найденную запись
                    return entry

        logging.error(f"Entry {name} not found in the directory {self.current_directory}.")
        return None

    def mkdir(self, name: str) -> Union[Directory, None]:
        """
        Создает каталог в текущем каталоге.

        Args:
            name (str): Имя каталога, который нужно создать.

        Returns:
            directory (Union[Directory, None]): Созданный каталог или None, если каталог с таким именем уже существует.
        """
        logging.info(f"Creating directory {name}.")

        # Проверяем, смонтирован ли диск
        if not self.is_mounted:
            logging.error("Disk is not mounted. Cannot create a directory.")
            return None

        # Проверяем, существует ли каталог или файл с таким же именем в текущем каталоге
        existing_entry = self.get_entry(name)
        if existing_entry is not None:
            logging.error(f"Directory or file with name {name} already exists in the current directory.")
            return None

        # Создаем новый каталог
        new_directory = Directory(name)

        # Добавляем новый каталог в текущий каталог
        self.current_directory.create_entry(name, new_directory)

        logging.info(f"Directory {name} created successfully!")
        return new_directory

    def touch(self, name: str) -> Union[File, None]:
        """
        Создает файл в текущем каталоге.

        Args:
            name (str): Имя файла, который нужно создать.

        Returns:
            file (Union[File, None]): Созданный файл или None, если файл с таким именем уже существует.
        """
        logging.info(f"Creating file {name}.")

        # Проверяем, смонтирован ли диск
        if not self.is_mounted:
            logging.error("Disk is not mounted. Cannot create a file.")
            return None

        # Проверяем, существует ли каталог или файл с таким же именем в текущем каталоге
        existing_entry = self.get_entry(name)
        if existing_entry is not None:
            logging.error(f"Directory or file with name {name} already exists in the current directory.")
            return None

        # Создаем новый файл
        new_file = File(name)

        # Добавляем новый файл в текущий каталог (root_dir)
        self.root_dir.create_entry(name, new_file)

        logging.info(f"File {name} created successfully!")
        return new_file
