# fast_api_blog/config_data/config.py


from pydantic.v1 import BaseSettings, SecretStr


# Определение класса Settings, наследующегося от BaseModel, для хранения конфигурационных данных
class Settings(BaseSettings):
    """
        Class for storing configuration data.

        Attributes:
            mysql_host (str): MySQL database host.
            mysql_user (str): MySQL database user.
            mysql_password (SecretStr): Password for accessing the MySQL database.
            mysql_db (str): MySQL database name.
            secret_key (SecretStr): Secret key for data encryption.
            algorithm (str): Encryption algorithm.
    """
    mysql_host: str            # Хост базы данных MySQL.
    mysql_user: str            # Пользователь базы данных MySQL.
    mysql_password: SecretStr  # Пароль для доступа к базе данных MySQL. (Скрытый)
    mysql_db: str              # Имя базы данных MySQL.
    secret_key: SecretStr      # Секретный ключ для шифрования данных. (Скрытый)
    algorithm: str             # Алгоритм шифрования.

    # Вложенный класс Config для определения настроек Pydantic
    class Config:
        """
            Nested class for defining Pydantic settings.

            Attributes:
                env_file (str): File to load environment variables from.
                env_file_encoding (str): Encoding of the file to load environment variables from.
        """
        env_file = ".env"             # Указание файла .env для загрузки переменных окружения
        env_file_encoding = "utf-8"   # Указание кодировки файла .env


# Создание экземпляра класса Settings для хранения конфигурационных данных
config: Settings = Settings()

