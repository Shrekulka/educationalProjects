# improved_echo_bot/config_data/config.py

from pydantic.v1 import BaseSettings, SecretStr


# Определение класса Settings, наследующегося от BaseModel, для хранения конфигурационных данных
class Settings(BaseSettings):
    """
        A class representing the configuration of the bot.

        This class defines settings for the bot, including the token for accessing the Telegram Bot API.

        Attributes:
            bot_token (SecretStr): A secret string containing the token for accessing the Telegram Bot API.
    """

    # Определение переменной bot_token типа SecretStr для хранения токена бота
    bot_token: SecretStr

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
