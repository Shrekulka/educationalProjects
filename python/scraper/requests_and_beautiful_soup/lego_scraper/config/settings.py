# selenium/config.py

from pydantic.v1 import BaseSettings, SecretStr


class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения.
    """
    CUSTOM_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"

    BASE_URL = "https://lego.com/"
    THEME_URL = BASE_URL + "en-us/themes/"

    # Значения по умолчанию
    DEFAULT_PAGE = 1
    DEFAULT_OFFSET = 0

    # Путь к CSV-файлу для записи данных
    CSV_FILE_PATH_SIMPLE = "../data/all_toy_data_simple.csv"
    CSV_FILE_PATH_THREADS = "../data/all_toy_data_threads.csv"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Создаем экземпляр класса Settings для хранения конфигурационных данных
config: Settings = Settings()