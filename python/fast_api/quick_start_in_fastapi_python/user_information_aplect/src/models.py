# user_information_aplect/src/models.py

from pydantic import BaseModel


class User(BaseModel):
    """
        Pydantic модель "Пользователь" с полями name и id.

        Атрибуты:
            name (str): Имя пользователя.
            id (int): Идентификатор пользователя.
    """
    name: str  # Имя пользователя типа str
    id: int    # Идентификатор пользователя типа int
