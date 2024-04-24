# user_registration/src/models.py

from pydantic import BaseModel, Field
from pydantic import EmailStr


class UserCreate(BaseModel):
    """
       Модель данных для обратной связи пользователя.

       Attributes:
           name (str): Имя пользователя, который оставил отзыв. Обязательное поле. Должно содержать от 2 до 20
                       символов.
           email (EmailStr): Адрес электронной почты пользователя. Обязательное поле. Должен иметь допустимый формат и
                             содержать от 5 до 50 символов.
           age (int, optional): Возраст пользователя в годах. Если указан, должен быть целым числом от 11 до 120.
           is_subscribed (bool): Флажок, указывающий, подписан ли пользователь на новостную рассылку. Необязательное
                                 поле.
   """
    name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="Имя пользователя, который оставил отзыв"
    )
    email: EmailStr = Field(
        ...,
        description="Адрес электронной почты пользователя",
        min_length=5,
        max_length=50
    )
    age: int = Field(
        None,
        gt=10,
        le=120,
        description="Возраст пользователя в годах"
    )
    is_subscribed: bool = Field(
        False,
        description="Флажок, указывающий, подписан ли пользователь на новостную рассылку"
    )
