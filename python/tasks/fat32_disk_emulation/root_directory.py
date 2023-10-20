from config import ENTRY_SIZE, NULL_TERMINATOR  # Импорт констант ENTRY_SIZE и NULL_TERMINATOR из модуля config
from directory import Directory  # Импорт класса Directory из модуля directory
from file import File  # Импорт класса File из модуля file
from logger import logging  # Импорт логирования из модуля logger


# Класс RootDirectory представляет корневой каталог файловой системы.
class RootDirectory:
    def __init__(self):
        self.entries: dict[str, Directory or File] = {}  # Словарь для хранения записей в корневом каталоге

    def create_entry(self, name: str, entry: Directory or File) -> bool:
        """
        Создает запись (файл или директорию) в корневом каталоге.

        Args:
            name (str): Имя записи.
            entry (Directory or File): Объект записи.

        Returns:
            bool: True, если запись успешно создана, иначе False.
        """
        if name in self.entries:  # Проверка наличия записи с таким именем
            logging.error(f"Entry with name '{name}' already exists.")
            return False

        self.entries[name] = entry  # Добавление записи в корневой каталог
        logging.info(f"Created entry '{name}' successfully.")
        return True

    def remove_entry(self, name: str) -> bool:
        """
        Удаляет запись (файл или директорию) из корневого каталога.

        Args:
            name (str): Имя записи.

        Returns:
            bool: True, если запись успешно удалена, иначе False.
        """
        if name not in self.entries:  # Проверка наличия записи с таким именем
            logging.error(f"Entry with name '{name}' not found.")
            return False

        del self.entries[name]  # Удаление записи из корневого каталога
        logging.info(f"Removed entry '{name}' successfully.")
        return True

    def get_entry(self, name: str) -> Directory or File or None:
        """
        Получает запись (файл или директорию) из корневого каталога.

        Args:
            name (str): Имя записи.

        Returns:
            Directory or File or None: Объект записи, если найден, иначе None.
        """
        if name not in self.entries:  # Проверка наличия записи с таким именем
            logging.error(f"Entry with name '{name}' not found.")
            return None

        return self.entries[name]  # Возвращение объекта записи

    def load(self, data: bytes) -> None:
        """
        Загружает записи из байтовых данных и обновляет корневой каталог.

        Args:
            data (bytes): Байтовые данные, представляющие записи.

        Returns:
            None: Этот метод не возвращает значения.
        """
        # Проверка, что длина данных корректная
        if len(data) % ENTRY_SIZE != 0:
            logging.error("Invalid data length for RootDirectory.")
            return

        # Разбор данных на записи:
        entries = []
        for i in range(0, len(data), ENTRY_SIZE):
            entry = data[i:i + ENTRY_SIZE]
            name = entry[:11].decode('utf-8').strip(NULL_TERMINATOR)  # Декодируем имя и убираем нулевые байты
            attr = entry[11]
            entries.append((name, attr))

        self.entries = {name: entry for name, entry in entries}  # Обновление корневого каталога
        logging.info(f"Loaded {len(self.entries)} entries from RootDirectory.")

    def save(self) -> bytes:
        """
        Сохраняет записи корневого каталога в виде байтов.

        Returns:
            bytes: Байтовые данные, представляющие записи корневого каталога.
        """
        data = b''
        for name, entry in self.entries.items():
            # Проверка, что имя записи не превышает 11 символов
            if len(name) > 11:
                logging.warning(f"Truncated name in RootDirectory: {name}")
                name = name[:11]

            # Заполняем нулевыми байтами, если имя короче 11 символов
            name = name.encode('utf-8').ljust(11, NULL_TERMINATOR.encode('utf-8'))

            # Проверка, что атрибут записи корректный
            if not 0 <= entry <= 255:
                logging.warning(f"Invalid attribute in RootDirectory: {entry}")
                entry = 0

            data += name + bytes([entry])  # Конвертируем имя в байты и добавляем атрибут в данные

        return data

    def add_entry(self, name: str, entry: Directory or File) -> None:
        """
        Добавляет запись (файл или директорию) в корневой каталог.

        Args:
            name (str): Имя записи.
            entry (Directory or File): Объект записи.

        Returns:
            None: Этот метод не возвращает значения.
        """
        if not isinstance(entry, (Directory, File)):  # Проверка типа записи
            logging.error("Invalid entry type. Only Directory and File instances can be added.")
            return

        # Проверка наличия записи с таким именем
        if name in self.entries:
            logging.error(f"Entry with name {name} already exists in the root directory.")
            return

        self.entries[name] = entry  # Добавление записи в корневой каталог
