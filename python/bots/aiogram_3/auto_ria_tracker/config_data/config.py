# telegram_bot_project_skeleton/config_data/config.py
import os
from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class DatabaseConfig:
    """
        Class representing the database configuration.

        Attributes:
            db_path (str): Путь к файлу базы данных
    """
    db_path: str  # Путь к файлу базы данных.


@dataclass
class TgBot:
    """
       Class representing the Telegram bot configuration.

       Attributes:
           token (str): The token for accessing the Telegram bot.
           channel_id (str): ID канала для отправки уведомлений
    """
    token: str        # Токен для доступа к телеграм-боту
    channel_id: str   # ID канала для отправки уведомлений.


@dataclass
class Config:
    """
        Class representing the overall configuration.

        Attributes:
            tg_bot (TgBot): The configuration of the Telegram bot.
            db (DatabaseConfig): The configuration of the database.
            _env (Env): An instance of the Env class for working with environment variables.
    """
    tg_bot: TgBot       # Конфигурация телеграм-бота.
    db: DatabaseConfig  # Конфигурация базы данных.
    _env: Env = Env()   # Экземпляр Env для работы с переменными окружения.

    def __init__(self, env_path: Optional[str] = None) -> None:
        """
           Initializes an instance of the Config class.

           Args:
               env_path (Optional[str]): The path to the file containing environment variables. Defaults to None.
        """
        # Инициализация экземпляра Env для работы с переменными окружения
        self._env.read_env(env_path)

        # Создание экземпляра TgBot с данными из переменных окружения
        self.tg_bot = TgBot(token=self._env('BOT_TOKEN'), channel_id=self._env('CHANNEL_ID'))

        # Определяем корневую директорию проекта.
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Устанавливаем путь к базе данных по умолчанию (в корне проекта).
        default_db_path = os.path.join(project_root, 'cars.db')

        # Создание экземпляра DatabaseConfig с данными из переменных окружения
        self.db = DatabaseConfig(db_path=self._env('DB_NAME', default_db_path))

    def __str__(self) -> str:
        """
            Returns a string representation of the Config object.

            Returns:
                str: A string representation of the Config object.
        """
        # Возвращает строку с данными о конфигурации телеграм-бота и базы данных
        return f'TgBot: {self.tg_bot}\nDatabaseConfig: {self.db}'

# Загружаем конфигурацию в переменную config при инициализации модуля.
config: Config = Config()