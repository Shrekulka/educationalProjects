# inter_exchange_arbitrage_bot/src/utils/logger.py
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from colorama import Fore, Style, init

from src.core.config import config

# Инициализируем colorama для поддержки цветов в Windows
init(autoreset=True)

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# --- Форматтеры ---
file_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)-8s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"
)


# Цветной формат для консоли
class ColoredFormatter(logging.Formatter):
    """
    Кастомный форматтер для добавления цветов в лог-сообщения в консоли.
    """
    LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Форматирует запись, добавляя цвета. Этот метод более явный и безопасный.
        """
        # Получаем цвет для текущего уровня логирования
        color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE)

        # Создаем цветную версию имени уровня
        levelname_colored = f"{color}{record.levelname:<8}{Style.RESET_ALL}"

        # Создаем цветную версию имени логгера
        name_colored = f"{Fore.BLUE}{record.name}{Style.RESET_ALL}"

        # Копируем запись, чтобы не изменять оригинал (хорошая практика)
        formatted_record = logging.makeLogRecord(record.__dict__)

        # Подменяем атрибуты в копии
        formatted_record.levelname = levelname_colored
        formatted_record.name = name_colored

        # Используем родительский format для безопасной подстановки в строку формата
        # Этот вызов теперь абсолютно безопасен и понятен
        return super().format(formatted_record)


# Создаем экземпляр нашего нового форматтера
console_formatter = ColoredFormatter(
    # Формат теперь включает цветные плейсхолдеры
    "%(levelname)s - %(name)s - %(message)s"
)

# --- Обработчики ---
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(console_formatter)

file_handler = TimedRotatingFileHandler(
    filename=LOGS_DIR / "bot.log",
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8"
)
file_handler.setFormatter(file_formatter)


def setup_logger():
    """Настраивает и возвращает корневой логгер."""
    log_level = logging.DEBUG if config.debug else logging.INFO

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Уменьшаем "шум" от сторонних библиотек
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("ccxt").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.").setLevel(logging.WARNING)
    logging.getLogger("apscheduler.").setLevel(logging.WARNING)


    return root_logger


# Настраиваем логгер при импорте модуля
logger = setup_logger()

# Эти сообщения будут выведены при первом импорте логгера
logger.info("Система логирования успешно настроена.")
logger.info(f"Уровень логирования: {logging.getLevelName(logger.level)}")
logger.info(f"Логи сохраняются в директорию: {LOGS_DIR.resolve()}")
