# fast_api_post_manager/schemas/user_schema.py


from pydantic import BaseModel, EmailStr, validator
import uuid
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

    @validator('email')
    def validate_email_format(cls, value):
        return validate_email(value)

    @validator('name')
    def validate_name(cls, value):
        return validate_name(value)

    @validator('surname')
    def validate_surname(cls, value):
        return validate_name(value)

class UserCreate(UserBase):
    """Схема для регистрации пользователя."""
    password: str

    @validator('password')
    def validate_password(cls, value):
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

class TokenResponse(TunedModel):
    """Ответ API с токеном доступа (JWT)."""
    access_token: str
    token_type: str = "bearer"
