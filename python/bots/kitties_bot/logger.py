# kitties_bot/logger.py
import logging
import traceback

from colorama import Style, Fore, Back, init


def configure_logging() -> None:
    """
        Configures the logging system.

        Details:
          - Sets the logging level (level: int).
          - Defines the log format using colorama for color highlighting (log_format: str).
          - Configures the base logger to write to the 'val.log' file.
          - Creates a handler for logging to the console (console_handler: logging.StreamHandler)
            and adds it to the base logger.

        In case of logging configuration error, records the error and terminates the program.
        Return type: None
    """

    try:
        # Инициализируем цвета в консоли
        init(autoreset=True)

        # Устанавливаем уровень логирования
        level = logging.DEBUG

        # Формат логов
        log_format = (
            f'{Fore.MAGENTA}%(asctime)s{Style.RESET_ALL} | '
            f'{Back.GREEN + Style.BRIGHT + Fore.BLACK}%(lineno)04d-%(levelname)-7s{Style.RESET_ALL} | - | '
            f'{Fore.BLUE}%(name)s{Style.RESET_ALL} | - | '
            f'{Fore.GREEN}%(funcName)s{Style.RESET_ALL} | - | '
            f'{Style.BRIGHT + Fore.CYAN}%(message)s{Style.RESET_ALL} |'
        )

        # Конфигурируем базовый логгер
        logging.basicConfig(filename='val.log', format=log_format, filemode='a', level=level)

        # Создаем обработчик для вывода логов в консоль
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(log_format))

        # Добавляем обработчик к базовому логгеру
        logging.getLogger().addHandler(console_handler)
    except Exception as e:
        # В случае ошибки настройки логирования, логируем ошибку и завершаем программу
        detailed_error_traceback = traceback.format_exc()
        logging.error(f"Error configuring logging: {e}\n{detailed_error_traceback}")
        raise SystemExit(1)


# Вызываем функцию настройки логирования
configure_logging()

# Создаем глобальный объект логгера
logger = logging.getLogger(__name__)

# Логгируем приветственное сообщение
logger.info(f"{Back.BLUE + Style.BRIGHT + Fore.BLACK}HI! HI! HI!!!{Style.RESET_ALL}")
