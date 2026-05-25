# grpc_example/config.py

from pydantic.v1 import BaseSettings

from model.todo_model import Todo


class Settings(BaseSettings):

    # Поле host типа str, значение по умолчанию "0.0.0.0"
    host: str = "0.0.0.0"

    # Поле port типа int, значение по умолчанию 8000
    port: int = 5080


# Создание экземпляра класса Settings, который будет использоваться для доступа к настройкам
settings: Settings = Settings()

