# regular_buttons_telegram_bot/config_data/config.py

from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class TgBot:
    """
       Class representing the Telegram bot configuration.

       Attributes:
           token (str): The token for accessing the Telegram bot.
    """
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Config:
    """
        Class representing the overall configuration.

        Attributes:
            tg_bot (TgBot): The configuration of the Telegram bot.
            _env (Env): An instance of the Env class for working with environment variables.
    """
    # Переменная tg_bot представляет конфигурацию телеграм-бота. Ожидается, что это будет объект типа TgBot.
    tg_bot: TgBot

    # Экземпляр _env класса Env используется для работы с переменными окружения.
    # Если не указан явно, он будет создан с помощью фабричного метода Env.
    _env: Env = Env()

    def __init__(self, env_path: Optional[str] = None) -> None:
        """
           Initializes an instance of the Config class.

           Args:
               env_path (Optional[str]): The path to the file containing environment variables. Defaults to None.
        """
        # Инициализация экземпляра Env для работы с переменными окружения
        self._env.read_env(env_path)
        # Создание экземпляра TgBot с данными из переменных окружения
        self.tg_bot = TgBot(token=self._env('BOT_TOKEN'))

    def __str__(self) -> str:
        """
            Returns a string representation of the Config object.

            Returns:
                str: A string representation of the Config object.
        """
        # Возвращает строку с данными о конфигурации телеграм-бота и базы данных
        return f"TgBot: {self.tg_bot}"
