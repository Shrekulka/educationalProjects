import struct

# Размер эмулированного диска в байтах (20 МБ)
DISK_SIZE = 20 * 1024 * 1024

# Максимальный размер диска для FAT32 с размером кластера 4 КБ (16 TB)
MAX_DISK_SIZE = (2 ** 32) * (4 * 1024)

# Максимальный размер таблицы файловой системы.
MAX_TABLE_SIZE = 1024

# Описывает структуру таблицы FAT для FAT32 - как последовательность 1024 элементов uint32_t
FAT_FORMAT = '<' + 'I' * MAX_TABLE_SIZE

# Устанавливается равной 1, что означает, что каждый кластер на диске FAT32 будет состоять из одного сектора.
SECTORS_PER_CLUSTER = 1

# Размер FAT
FAT_SIZE = 1024

# Переменная, которая должна содержать формат для распаковки данных FAT
UNPACK_FORMAT = '<' + 'I' * FAT_SIZE

# Размер загрузочного сектора
BOOT_SECTOR_SIZE = 512

# Список поддерживаемых команд оболочки
COMMANDS = ['format', 'ls', 'cd', 'mkdir', 'touch']

# Значение свободной записи FAT32
FAT_ENTRY_FREE = 0x0FFFFFF8

# Строка, представляющая нулевой символ ASCII
NULL_TERMINATOR = '\x00'

# Константа для нулевого байта
NULL_BYTE = b'\x00'

# Смещение в заголовке FAT32
HEADER_OFFSET = 0x0B

# Формат заголовка диска FAT32:
HEADER_FORMAT_STRUCT = '<11sBBHBB'

# Формат заголовка диска FAT32 (значения):
HEADER_FORMAT_VALUES = '<11sBBHHB'

PARTITION_FORMAT = '<32sII32s'

# Размер заголовка без магического числа
HEADER_SIZE_WITHOUT_MAGIC = struct.calcsize(HEADER_FORMAT_VALUES)

# Максимальная длина имени раздела (32 символа)
MAX_PARTITION_NAME_LENGTH = 32

# Размер записи FAT32 в байтах
FAT_ENTRY_SIZE = 4

# Размер записи в корневом каталоге в байтах
ROOT_DIR_ENTRY_SIZE = 32

# Флаг, указывающий на директорию
ATTR_DIRECTORY = 16

# Размер записи в корневом каталоге (32 байта).
ENTRY_SIZE = 32

# ATTR_FILE: Флаг, указывающий на файл
ATTR_FILE = 32

# Формат диска (в байтах) - строка "FAT32"
DISK_FORMAT = b'FAT32'

# Количество секторов в кластере
SEC_PER_CLUS = 1

# Количество FAT32
NUM_FATS = 2

# Количество записей в корневом каталоге
NUM_ROOT_ENTRIES = 512

# Размер сектора в байтах
SEC_SIZE = 512

# Размер корневого каталога
ROOT_DIR_SIZE = 2048

# Размер заголовка, включая FAT32 и корневой каталог
HEADER_SIZE = 32 + (NUM_FATS * (SEC_PER_CLUS * SEC_SIZE))
