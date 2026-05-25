# fast_api_post_manager/schemas/user_schema.py


import uuid

from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo

from schemas.post_schema import PostResponse
from utils.validation import validate_password, validate_name, validate_email


class TunedModel(BaseModel):
    """Базовая модель с включенным режимом ORM для работы с SQLAlchemy."""

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """Базовая информация о пользователе (используется в других схемах)."""
    email: EmailStr
    name: str
    surname: str

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, value: str, info: ValidationInfo) -> str:
        return validate_email(value)

    @field_validator('name')
    @classmethod
    def validate_name_format(cls, value: str, info: ValidationInfo) -> str:
        return validate_name(value)

    @field_validator('surname')
    @classmethod
    def validate_surname_format(cls, value: str, info: ValidationInfo) -> str:
        return validate_name(value)


class UserCreate(UserBase):
    """Схема для регистрации пользователя."""
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: str, info: ValidationInfo) -> str:
        return validate_password(value)


class UserLogin(BaseModel):
    """Схема для входа в систему (авторизация)."""
    email: EmailStr
    password: str


class UserResponse(UserBase, TunedModel):
    """Основной ответ API с данными пользователя."""
    id: uuid.UUID
    is_active: bool


class UserWithPosts(UserResponse):
    """Детальная информация о пользователе, включая список его постов."""
    posts: list["PostResponse"] = []

