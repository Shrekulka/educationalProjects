# cookie_authentication_service/src/models.py

from pydantic import BaseModel, Field

# Паттерн для проверки пароля.
password_pattern = r'^[A-Za-z0-9@$!%*?&]{8,}$'


class User(BaseModel):
    """
       Модель пользователя.

       Attributes:
           username (str): Имя пользователя (от 2 до 50 символов).
           password (str): Пароль пользователя (от 8 до 100 символов) с определенным паттерном.
    """
    username: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Имя пользователя (строка, обязательно)"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        pattern=password_pattern,
        description="Пароль пользователя (секретная строка, обязательно)"
    )
