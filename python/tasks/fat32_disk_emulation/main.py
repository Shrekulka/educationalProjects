import logging
import sys

from exceptions import DiskNotFoundError, UnknownDiskFormatError
from fat32 import Fat32


def main() -> None:
    """
    Главная функция программы для работы с эмулированным диском FAT32.

    Пользователь может выполнять команды для работы с файловой системой:
    - ls: Просмотр содержимого текущего каталога.
    - mkdir <name>: Создание новой директории с заданным именем.
    - touch <name>: Создание нового файла с заданным именем.
    - cd <path>: Перемещение по директориям по указанному пути.
    - quit: Завершение работы программы и размонтирование диска.

    Returns:
        None
    """
    try:
        # Попытка создать экземпляр класса Fat32 и монтировать диск
        disk = Fat32('disk.img')
        disk.mount()  # Монтируем диск
    except (DiskNotFoundError, UnknownDiskFormatError) as e:
        print(e)
        sys.exit(1)

    while True:
        current_dir = disk.get_current_dir()
        cmd = input(f"{current_dir} $ ").strip()  # Получаем введенную команду
        cmd_parts = cmd.split()  # Разделяем команду на части

        if not cmd_parts:
            print("Empty command. Please enter a valid command.")
            continue

        cmd_name = cmd_parts[0]

        if cmd_name == 'quit':
            disk.unmount()  # Перед выходом размонтируем диск
            sys.exit(0)

        elif cmd_name == 'ls':
            logging.info("Command: ls")
            disk.ls()  # Выводим содержимое текущей директории

        elif cmd_name == 'mkdir':
            if len(cmd_parts) < 2:
                print("Usage: mkdir <name>")
                continue
            directory_name = cmd_parts[1]
            logging.info(f"Command: mkdir {directory_name}")
            disk.mkdir(directory_name)  # Создаем новую директорию

        elif cmd_name == 'touch':
            if len(cmd_parts) < 2:
                print("Usage: touch <name>")
                continue
            file_name = cmd_parts[1]
            logging.info(f"Command: touch {file_name}")
            disk.touch(file_name)  # Создаем новый файл

        elif cmd_name == 'cd':
            if len(cmd_parts) < 2:
                print("Usage: cd <path>")
                continue
            path = cmd_parts[1]
            logging.info(f"Command: cd {path}")
            disk.cd(path)  # Переходим в указанную директорию

        else:
            print("Unknown command")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
