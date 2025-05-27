# telegram_bot_project_skeleton/config_data/config.py

from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class DatabaseConfig:
    """
        Class representing the database configuration.

        Attributes:
            db_name (str): The name of the database.
            db_host (str): The URL address of the database.
            db_user (str): The username of the database user.
            db_password (str): The password for the database.
    """
    db_name: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Имя пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TgBot:
    """
       Class representing the Telegram bot configuration.

       Attributes:
           token (str): The token for accessing the Telegram bot.
           admin_ids (list[int]): The list of bot administrator IDs.
    """
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    """
        Class representing the overall configuration.

        Attributes:
            tg_bot (TgBot): The configuration of the Telegram bot.
            db (DatabaseConfig): The configuration of the database.
            _env (Env): An instance of the Env class for working with environment variables.
    """
    # Переменная tg_bot представляет конфигурацию телеграм-бота. Ожидается, что это будет объект типа TgBot.
    tg_bot: TgBot

    # Переменная db представляет конфигурацию базы данных. Ожидается, что это будет объект типа DatabaseConfig.
    db: DatabaseConfig

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
        self.tg_bot = TgBot(token=self._env('BOT_TOKEN'), admin_ids=list(map(int, self._env.list('ADMIN_IDS'))))
        # Создание экземпляра DatabaseConfig с данными из переменных окружения
        self.db = DatabaseConfig(
            db_name=self._env('DB_NAME'),
            db_host=self._env('DB_HOST'),
            db_user=self._env('DB_USER'),
            db_password=self._env('DB_PASSWORD'))

    def __str__(self) -> str:
        """
            Returns a string representation of the Config object.

            Returns:
                str: A string representation of the Config object.
        """
        # Возвращает строку с данными о конфигурации телеграм-бота и базы данных
        return f'TgBot: {self.tg_bot}\nDatabaseConfig: {self.db}'

# Загружаем конфиг в переменную config
config: Config = Config()

########################################################################################################################
# 2) или такой подход вариант №2
# from pydantic.v1 import BaseSettings, SecretStr
# from typing import List
#
#
# class TgBotSettings(BaseSettings):
#     """
#     Settings for the Telegram bot.
#
#     Attributes:
#         bot_token (SecretStr): The token for accessing the Telegram bot.
#         admin_ids (List[int]): The list of bot administrator IDs.
#     """
#     bot_token: SecretStr  # Токен для доступа к боту Telegram, используется SecretStr для безопасного хранения
#     admin_ids: List[int]  # Список идентификаторов администраторов бота
#
#
# class DatabaseSettings(BaseSettings):
#     """
#     Settings for the database connection.
#
#     Attributes:
#         db_name (str): The name of the database.
#         db_host (str): The URL address of the database.
#         db_user (str): The username of the database user.
#         db_password (SecretStr): The password for the database.
#     """
#     db_name: str  # Название базы данных
#     db_host: str  # URL-адрес базы данных
#     db_user: str  # Имя пользователя базы данных
#     db_password: SecretStr  # Пароль к базе данных, используется SecretStr для безопасного хранения
#
#
# class Settings(BaseSettings):
#     """
#     General application settings.
#
#     Attributes:
#         tg_bot (TgBotSettings): The configuration settings for the Telegram bot.
#         db (DatabaseSettings): The configuration settings for the database connection.
#     """
#     tg_bot: TgBotSettings  # Настройки бота Telegram
#     db: DatabaseSettings  # Настройки соединения с базой данных
#
#     class Config:
#         env_file = ".env"  # Указание файла .env для загрузки переменных окружения
#         env_file_encoding = "utf-8"  # Указание кодировки файла .env
#
#
# config = Settings()  # Создание экземпляра класса Settings для хранения конфигурационных данных
########################################################################################################################
# 3) или простой вариант №1

# from dataclasses import dataclass
# from typing import Optional
#
# from environs import Env
#
#
# @dataclass
# class TgBot:
#     """
#        Class representing the Telegram bot configuration.
#
#        Attributes:
#            token (str): The token for accessing the Telegram bot.
#     """
#     token: str  # Токен для доступа к телеграм-боту
#
#
# @dataclass
# class Config:
#     """
#         Class representing the overall configuration.
#
#         Attributes:
#             tg_bot (TgBot): The configuration of the Telegram bot.
#             _env (Env): An instance of the Env class for working with environment variables.
#     """
#     # Переменная tg_bot представляет конфигурацию телеграм-бота. Ожидается, что это будет объект типа TgBot.
#     tg_bot: TgBot
#
#     # Экземпляр _env класса Env используется для работы с переменными окружения.
#     # Если не указан явно, он будет создан с помощью фабричного метода Env.
#     _env: Env = Env()
#
#     def __init__(self, env_path: Optional[str] = None) -> None:
#         """
#            Initializes an instance of the Config class.
#
#            Args:
#                env_path (Optional[str]): The path to the file containing environment variables. Defaults to None.
#         """
#         # Инициализация экземпляра Env для работы с переменными окружения
#         self._env.read_env(env_path)
#         # Создание экземпляра TgBot с данными из переменных окружения
#         self.tg_bot = TgBot(token=self._env('BOT_TOKEN'))
#
#     def __str__(self) -> str:
#         """
#             Returns a string representation of the Config object.
#
#             Returns:
#                 str: A string representation of the Config object.
#         """
#         # Возвращает строку с данными о конфигурации телеграм-бота и базы данных
#         return f"TgBot: {self.tg_bot}"
########################################################################################################################
# 4) или простой вариант №2
# from pydantic.v1 import BaseSettings, SecretStr
#
#
# # Определение класса Settings, наследующегося от BaseModel, для хранения конфигурационных данных
# class Settings(BaseSettings):
#     """
#         A class representing the configuration of the bot.
#
#         This class defines settings for the bot, including the token for accessing the Telegram Bot API.
#
#         Attributes:
#             bot_token (SecretStr): A secret string containing the token for accessing the Telegram Bot API.
#     """
#
#     # Определение переменной bot_token типа SecretStr для хранения токена бота
#     bot_token: SecretStr
#
#     # Вложенный класс Config для определения настроек Pydantic
#     class Config:
#         """
#             Settings for working with Pydantic.
#
#             This nested class defines parameters for loading environment variables from the `.env` file.
#
#             Attributes:
#                 env_file (str): The name of the file containing environment variables.
#                 env_file_encoding (str): The encoding of the file containing environment variables.
#         """
#         # Указание файла .env для загрузки переменных окружения
#         env_file = ".env"
#         # Указание кодировки файла .env
#         env_file_encoding = "utf-8"
#
#
# # Создание экземпляра класса Settings для хранения конфигурационных данных
# config: Settings = Settings()
