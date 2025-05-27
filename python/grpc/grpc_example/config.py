# restful_text_processing_with_nltk/src/config.py

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    """
        Класс настроек для приложения RESTful Text Processing с использованием NLTK.

        Attributes:
            app_name (str): Наименование приложения. По умолчанию "restful_text_processing_with_nltk".
            host (str): Хост, на котором будет запущено приложение. По умолчанию "127.0.0.1".
            port (int): Порт, на котором будет запущено приложение. По умолчанию 8000.
            log_level (str): Уровень логирования приложения. По умолчанию "INFO".
    """
    # Поле app_name типа str, значение по умолчанию "restful_text_processing_with_nltk"
    app_name: str = "restful_text_processing_with_nltk"

    # Поле host типа str, значение по умолчанию "127.0.0.1"
    host: str = "127.0.0.1"

    # Поле port типа int, значение по умолчанию 8000
    port: int = 8000

    # Поле log_level типа str, значение по умолчанию "INFO"
    log_level: str = "INFO"


# Создание экземпляра класса Settings, который будет использоваться для доступа к настройкам
settings: Settings = Settings()
