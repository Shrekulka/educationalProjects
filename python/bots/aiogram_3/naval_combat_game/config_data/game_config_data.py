# naval_combat_game/config_data/game_config_data.py
from typing import Union

from pydantic.v1 import BaseSettings, SecretStr


# Определение класса Settings, наследующегося от BaseModel, для хранения конфигурационных данных
class Settings(BaseSettings):
    """
        Class representing the configuration of the Telegram bot.

        Attributes:
            bot_token (SecretStr): A secret string containing the token for accessing the Telegram Bot API.
            admin_ids (Union[list[int], int]): The list of bot administrator IDs or a single administrator ID.
    """
    bot_token: SecretStr  # Определение переменной BOT_TOKEN типа SecretStr для хранения токена бота
    admin_ids: Union[list[int], int]  # Список id администраторов бота

    # Вложенный класс Config для определения настроек Pydantic
    class Config:
        """
            Settings for working with Pydantic.

            This nested class defines parameters for loading environment variables from the `.env` file.

            Attributes:
                env_file (str): The name of the file containing environment variables.
                env_file_encoding (str): The encoding of the file containing environment variables.
        """
        # Указание файла .env для загрузки переменных окружения
        env_file = ".env"
        # Указание кодировки файла .env
        env_file_encoding = "utf-8"


# Создание экземпляра класса Settings для хранения конфигурационных данных
config: Settings = Settings()

# Инициализируем константу размера игрового поля
FIELD_SIZE = 8
