import io
import unittest
from typing import List
from unittest.mock import patch, mock_open

from config import (
    FAT_SIZE, BOOT_SECTOR_SIZE, ROOT_DIR_ENTRY_SIZE, ENTRY_SIZE, NULL_BYTE
)
from exceptions import FatLoadError
from fat32 import Fat32


class TestFat32Loading(unittest.TestCase):
    """
    Класс для тестирования загрузки диска FAT32.
    """

    def setUp(self) -> None:
        """
        Настройка тестовой среды.

        Создает пустой файл системы FAT32 и настраивает мок для открытия файлов.
        """
        empty_fat32 = NULL_BYTE * (BOOT_SECTOR_SIZE + FAT_SIZE)
        self.mock_open = mock_open(read_data=empty_fat32)
        patcher = patch('fat32.open', self.mock_open)
        patcher.start()
        self.addCleanup(patcher.stop)

    def _create_disk_with_data(self, root_dir_entries: int = 2) -> Fat32:
        """
        Вспомогательная функция для создания диска с данными.

        Args:
            root_dir_entries (int): Количество записей в корневом каталоге.

        Returns:
            Fat32: Экземпляр класса Fat32 с данными.
        """
        bootloader = NULL_BYTE * BOOT_SECTOR_SIZE
        fat_data = NULL_BYTE * FAT_SIZE
        root_dir_data = NULL_BYTE * (ROOT_DIR_ENTRY_SIZE * root_dir_entries)

        # Открываем файл для записи данных на диск
        with open('disk.img', 'wb') as f:
            f.write(bootloader + fat_data + root_dir_data)

        # Создаем экземпляр класса Fat32 и загружаем данные с диска
        disk = Fat32('disk.img')
        disk.load()

        # Здесь можете добавить другие необходимые операции для заполнения диска данными
        return disk

    def test_load_valid_disk(self) -> None:
        """
        Тестирование загрузки допустимого диска FAT32.
        """
        disk = self._create_disk_with_data(root_dir_entries=0)

        # Проверяем, что размеры таблицы FAT и корневого каталога соответствуют ожидаемым
        self.assertEqual(len(disk.fat.table), FAT_SIZE)
        self.assertEqual(len(disk.root_dir.entries), 0)

    def test_load_invalid_fat(self) -> None:
        """
        Тестирование загрузки диска с недопустимыми данными FAT.
        """
        invalid_fat_data = NULL_BYTE * (FAT_SIZE - 1)
        self.mock_open.return_value = io.BytesIO(invalid_fat_data)

        disk = Fat32('disk.img')

        # Проверяем, что при загрузке диска с неверными данными FAT выбрасывается ожидаемое исключение
        with self.assertRaises(FatLoadError):
            disk.load()

    def test_load_disk_with_files(self) -> None:
        """
        Тестирование загрузки диска с файлами.
        """
        disk = self._create_disk_with_data(root_dir_entries=2)

        # Проверяем, что размеры таблицы FAT и корневого каталога соответствуют ожидаемым
        self.assertEqual(len(disk.fat.table), FAT_SIZE)
        self.assertEqual(len(disk.root_dir.entries), 2)

    def test_format_disk(self) -> None:
        """
        Тестирование форматирования диска FAT32.
        """
        disk = Fat32('empty_disk.img')
        disk.format()

        # Проверяем, что после форматирования размеры таблицы FAT и корневого каталога соответствуют ожидаемым
        self.assertEqual(len(disk.fat.table), FAT_SIZE)
        self.assertEqual(len(disk.root_dir.entries), 0)

    def test_ls_command(self) -> None:
        """
        Тестирование команды 'ls'.
        """
        disk = self._create_disk_with_data(root_dir_entries=2)

        result: List[str] = disk.ls()

        # Проверяем, что команда 'ls' возвращает ожидаемый список элементов
        self.assertEqual(result, ['File\t.file1\t100\t2023-09-14 12:00:00',
                                  'File\t.file2\t200\t2023-09-14 13:00:00',
                                  'Directory\t..\tN/A\tN/A', 'Directory\t.\tN/A\tN/A'])

    def test_ls_command_with_absolute_path(self) -> None:
        """
        Тестирование команды 'ls' с абсолютным путем.
        """
        disk = self._create_disk_with_data(root_dir_entries=2)

        disk.mkdir('folder1')
        disk.cd('/folder1')
        disk.touch('file_in_folder')
        disk.cd('/')

        result: List[str] = disk.ls()

        # Проверяем, что команда 'ls' с абсолютным путем возвращает ожидаемый список элементов
        self.assertEqual(result, ['file_in_folder', '..', '.'])

    def test_cd_command(self) -> None:
        """
        Тестирование команды 'cd'.
        """
        disk = self._create_disk_with_data(root_dir_entries=2)

        disk.cd('/')
        current_dir: str = disk.current_directory

        # Проверяем, что команда 'cd' переходит в корневой каталог
        self.assertEqual(current_dir, '/')

        disk.cd('/')
        current_dir = disk.current_directory

        # Проверяем, что команда 'cd' остается в корневом каталоге
        self.assertEqual(current_dir, '/')

        # Проверяем, что команда 'cd' выбрасывает исключение при попытке перейти в несуществующий каталог
        with self.assertRaisesRegex(Exception, 'Directory not found'):
            disk.cd('/non_existent_folder')

        disk.mkdir('folder1')
        disk.cd('/folder1')
        current_dir = disk.current_directory

        # Проверяем, что команда 'cd' переходит в существующий каталог
        self.assertEqual(current_dir, '/folder1')

    def test_mkdir_command(self) -> None:
        """
        Тестирование команды 'mkdir'.
        """
        disk = self._create_disk_with_data(root_dir_entries=2)

        disk.mkdir('new_folder')
        result: List[str] = disk.ls()

        # Проверяем, что команда 'mkdir' создает новый каталог
        self.assertIn('new_folder', result)

        disk.cd('new_folder')
        disk.mkdir('sub_folder')
        result = disk.ls()

        # Проверяем, что команда 'mkdir' создает вложенный каталог
        self.assertIn('sub_folder', result)

    def test_touch_command(self) -> None:
        """
        Тестирование команды 'touch'.
        """
        disk = self._create_disk_with_data(root_dir_entries=2)

        disk.touch('new_file')
        result: List[str] = disk.ls()

        # Проверяем, что команда 'touch' создает новый файл
        self.assertIn('new_file', result)

    def test_invalid_disk_format(self) -> None:
        """
        Тестирование загрузки диска с недопустимым форматом.
        """
        invalid_bootloader = NULL_BYTE * BOOT_SECTOR_SIZE
        invalid_fat_data = NULL_BYTE * (FAT_SIZE - 1)
        self.mock_open.return_value = io.BytesIO(invalid_bootloader + invalid_fat_data)

        disk = Fat32('invalid_disk.img')

        # Проверяем, что загрузка диска с недопустимым форматом выбрасывает ожидаемое исключение
        with self.assertRaisesRegex(Exception, 'Unknown disk format'):
            disk.load()

    def test_disk_overflow(self) -> None:
        """
        Тестирование переполнения диска.
        """
        max_disk_size = BOOT_SECTOR_SIZE + FAT_SIZE
        max_entries = max_disk_size // ENTRY_SIZE
        root_dir_data = NULL_BYTE * (max_entries * ENTRY_SIZE)

        self.mock_open.return_value = io.BytesIO(root_dir_data)

        disk = Fat32('max_disk.img')
        disk.load()

        # Проверяем, что при попытке создания нового файла на переполненном диске выбрасывается ожидаемое исключение
        with self.assertRaisesRegex(Exception, 'Disk is full'):
            disk.touch('new_file.txt')


if __name__ == '__main__':
    unittest.main()
