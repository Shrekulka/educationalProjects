# integration_telegram_planfix_in_progress/logger.py

import logging
import sys
import traceback

from colorama import Style, Fore, Back


def configure_logging() -> None:
    """
       Configures the logging system.

       Sets the logging level, log format, and adds a handler for console output.
       In case of configuration error, logs a detailed message and exits the program.

       Returns:
           None
    """
    try:
        # Устанавливаем уровень логирования (DEBUG позволяет логировать все уровни сообщений)
        level = logging.DEBUG

        # Формат для записи логов с использованием цветов (colorama) и различных параметров
        log_format = (
            f'{Fore.MAGENTA}%(asctime)s{Style.RESET_ALL} | '
            f'{Back.GREEN + Style.BRIGHT + Fore.BLACK}%(lineno)04d-%(levelname)-7s{Style.RESET_ALL} | - | '
            f'{Fore.BLUE}%(name)s{Style.RESET_ALL} | - | '
            f'{Fore.GREEN}%(funcName)s{Style.RESET_ALL} | - | '
            f'{Style.BRIGHT + Fore.CYAN}%(message)s{Style.RESET_ALL} |'
        )

        # Настройка основных параметров логирования, таких как файл, формат, режим записи и уровень
        logging.basicConfig(filename='val.log', format=log_format, filemode='a', level=level)

        # Создаем обработчик для вывода логов в консоль
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(log_format))

        # Добавляем обработчик в логгер
        logging.getLogger().addHandler(console_handler)
    except Exception as e:
        # В случае ошибки настройки логирования выводим подробное сообщение и завершаем программу
        detailed_send_message_error = traceback.format_exc()
        logging.error(f"Error configuring logging: {e}\n{detailed_send_message_error}")
        sys.exit(1)  # Завершить программу в случае ошибки настройки логирования


# Вызываем функцию для настройки логирования
configure_logging()

# Получаем логгер с именем текущего модуля
logger = logging.getLogger(__name__)

# Выводим информационное сообщение в лог
logger.info(f"{Back.BLUE + Style.BRIGHT + Fore.BLACK}HI! HI! HI!!!{Style.RESET_ALL}")
