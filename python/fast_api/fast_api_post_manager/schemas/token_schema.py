# fast_api_post_manager/schemas/token_schema.py

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid
from typing import Optional
from pydantic_core.core_schema import ValidationInfo


class TokenBase(BaseModel):
    """
    Базовая модель токена с общими полями.

    Attributes:
        access_token: Строка токена доступа
        token_type: Тип токена (обычно "bearer")
        expires_at: Дата и время истечения срока действия
    """
    access_token: str = Field(..., description="Token string used for authorization")
    token_type: str = Field("bearer", description="Token type (usually 'bearer')")
    expires_at: datetime = Field(..., description="Token expiration timestamp")


class TokenCreate(TokenBase):
    """
    Модель для создания токена.

    Расширяет TokenBase и добавляет user_id для связи с пользователем.
    """
    user_id: uuid.UUID = Field(..., description="ID of the user this token belongs to")
    is_jwt: bool = Field(False, description="Is this token a JWT")


class TokenResponse(TokenBase):
    """
    Модель для ответа API с токеном.
    """

    class Config:
        from_attributes = True


class TokenInDB(TokenBase):
    """
    Модель токена как он хранится в базе данных.

    Attributes:
        id: Уникальный идентификатор токена
        user_id: Идентификатор пользователя-владельца токена
        created_at: Дата и время создания токена
        is_jwt: Является ли токен JWT
    """
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    is_jwt: bool

    class Config:
        from_attributes = True