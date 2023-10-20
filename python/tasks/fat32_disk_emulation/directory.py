from __future__ import annotations
from typing import Union

from file import File
from logger import logging


class Directory:
    def __init__(self, name: str):
        """
        Инициализация объекта директории.

        Args:
            name (str): Имя директории.
        """
        self.name = name  # Установка имени директории
        self.entries = []  # Инициализация списка записей в директории

    def add_entry(self, entry_name: str, entry: Directory | File) -> None:
        """
        Добавление записи в директорию.

        Args:
            entry_name (str): Имя записи.
            entry: Объект записи (Directory или File).

        Returns:
            None: Этот метод не возвращает значения.
        """
        if not isinstance(entry, (Directory, File)):
            logging.error("Invalid entry type. Only Directory and File instances can be added.")
            return

        # Проверка наличия записи с таким именем
        if any(e.name == entry_name for e in self.entries):
            logging.error(f"Entry with name {entry_name} already exists in the directory {self.name}.")
            return

        entry.name = entry_name  # Устанавливаем имя записи
        self.entries.append(entry)

    def remove_entry(self, name: str) -> None:
        """
        Метод для удаления записи из директории по имени.

        Args:
            name (str): Имя записи, которую необходимо удалить.

        Returns:
            None: Этот метод не возвращает значения.
        """
        entry_to_remove = None
        # Проходим по всем записям в директории и ищем запись с заданным именем.
        for entry in self.entries:
            if entry.name == name:
                entry_to_remove = entry
                break

        if entry_to_remove:
            # Если запись найдена, удаляем её из списка записей.
            self.entries.remove(entry_to_remove)
            logging.info(f"Запись {name} успешно удалена из директории {self.name}.")
        else:
            logging.error(f"Запись {name} не найдена в директории {self.name}.")

    def get_entry(self, name: str) -> Directory | File | None:
        """
        Получение записи из директории по имени.

        Args:
            name (str): Имя записи.

        Returns:
            Union[Directory, File, None]: Объект записи (Directory или File) или None, если запись не найдена.
        """
        for entry in self.entries:
            # Если имя текущей записи совпадает с искомым именем, возвращаем эту запись (файл или подкаталог).
            if entry.name == name:
                return entry

        # Если запись с указанным именем не найдена, генерируется сообщение об ошибке.
        logging.error(f"Entry {name} not found in the directory {self.name}.")

        # Возвращается None, чтобы указать отсутствие найденной записи.
        return None

    def calculate_size(self) -> int:
        """
        Вычисление размера каталога на основе его записей.

        Returns:
            int: Размер каталога в байтах.
        """
        size = 0
        for entry in self.entries:
            if isinstance(entry, File):  # Если текущая запись является экземпляром класса File (файл)
                size += entry.size  # Увеличиваем значение size на размер текущего файла.
            elif isinstance(entry, Directory):
                # Вызываем метод calculate_size() для вычисления размера текущего подкаталога.
                # Рекурсивно вычисляем размер подкаталогов, так как подкаталоги могут содержать файлы и другие подкаталоги.
                size += entry.calculate_size()
        return size  # Возвращаем общий размер каталога, включая файлы и подкаталоги.
