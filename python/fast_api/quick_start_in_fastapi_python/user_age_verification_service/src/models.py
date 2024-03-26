# user_age_verification_service/src/models.py

from pydantic import BaseModel


class User(BaseModel):
    """
        Pydantic модель "Пользователь" с полями name, age и is_adult.

        Attributes:
            name (str): Имя пользователя.
            age (int): Возраст пользователя.
            is_adult (bool): Флаг, указывающий, является ли пользователь взрослым.
    """
    name: str               # Имя пользователя типа str
    age: int                # Возраст пользователя типа int
    is_adult: bool = False  # Флаг, указывающий, является ли пользователь взрослым
