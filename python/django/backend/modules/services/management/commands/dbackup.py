# backend/modules/services/management/commands/dbackup.py

from django.core.management import BaseCommand, call_command
from datetime import datetime


class Command(BaseCommand):
    """
        Команда для создания резервной копии базы данных.

        Эта команда создает резервную копию базы данных в формате JSON,
        исключая таблицы `contenttypes` и `admin.logentry`. Файл резервной
        копии сохраняется в текущей директории с именем, включающим текущую
        дату и время.
    """
    def handle(self, *args: tuple, **options: dict) -> None:
        """
            Основной метод команды, который выполняется при запуске.

            :param args: Позиционные аргументы команды.
            :param options: Именованные аргументы команды.
            :return: None
        """
        # Выводим сообщение о начале процесса создания резервной копии
        self.stdout.write('Waiting for database dump...')

        # Формируем имя файла с текущей датой и временем
        output_filename = f'database-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.json'

        # Выполняем команду dumpdata для создания резервной копии базы данных
        call_command(
            'dumpdata',  # Команда для экспорта данных из базы данных
            '--natural-foreign',  # Включаем натуральные внешние ключи
            '--natural-primary',  # Включаем натуральные первичные ключи
            '--exclude=contenttypes',  # Исключаем таблицу contenttypes
            '--exclude=admin.logentry',  # Исключаем таблицу admin.logentry
            '--indent=4',  # Форматируем JSON с отступом в 4 пробела
            f'--output={output_filename}'  # Указываем файл для сохранения данных
        )

        # Выводим сообщение об успешном завершении процесса создания резервной копии
        self.stdout.write(self.style.SUCCESS('Database successfully backed up'))
