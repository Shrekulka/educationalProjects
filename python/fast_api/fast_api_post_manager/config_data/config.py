# fast_api_post_manager/config_data/config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    """
    Класс для хранения конфигурационных данных.
    """
    # Используем те же имена переменных, как в .env
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    SECRET_KEY: SecretStr
    ALGORITHM: str

    # Настройка конфигурации через SettingsConfigDict
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        env_file_encoding="utf-8"
    )

    def get_db_url(self):
        """
        Генерирует URL для подключения к базе данных PostgreSQL.
        """
        return (f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@"
                f"{self.POSTGRES_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}")

    def get_async_db_url(self):
        """
        Генерирует URL для асинхронного подключения к базе данных PostgreSQL.
        """
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@"
                f"{self.POSTGRES_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}")


# Создание экземпляра класса Settings
config = Settings()