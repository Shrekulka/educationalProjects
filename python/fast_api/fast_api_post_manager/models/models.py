# fast_api_post_manager/models/models.py

import uuid
from datetime import datetime, timezone, timedelta
import secrets

from sqlalchemy import Column, String, Boolean, UUID, Text
from sqlalchemy import DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship, DeclarativeBase

from models.base import Base
from utils.cache_utils import is_cache_valid
from utils.password_utils import verify_password
from utils.token_utils import is_token_valid


class User(Base):

    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Связь один-ко-многим с таблицей Post
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")
    # Связь один-ко-многим с таблицей Token
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User: {self.name} {self.surname}, id: {self.id}, email: {self.email}"

    def check_password(self, plain_password: str) -> bool:
        """
        Проверяет пароль пользователя.
        """
        return verify_password(plain_password, self.hashed_password)


class Post(Base):

    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(100), index=True)
    text = Column(Text, nullable=False)  # Text тип будет валидироваться в Pydantic схеме
    status = Column(String(50), default='draft', server_default='draft')
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    # Дата и время создания в UTC
    created_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Дата и время обновления в UTC
    updated_date = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))

    cache_expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5))

    # Связь многие-к-одному с таблицей User
    owner = relationship("User", back_populates="posts")

    __table_args__ = (
        CheckConstraint('LENGTH(text) <= 1048576', name='check_text_length'),  # 1MB максимум
        CheckConstraint("status IN ('draft', 'published')", name='check_status'),
        CheckConstraint('LENGTH(title) >= 3', name='check_title_min_length'),  # Минимум 3 символа для заголовка
    )

    def __repr__(self):
        return f'post_id: {self.id}, title: {self.title}, status: {self.status}, created date: {self.created_date}, author: {self.user_id}'

    def check_cache_valid(self) -> bool:
        """
        Проверяет, действителен ли кэш для данного поста.
        """
        return is_cache_valid(self.cache_expires_at)

    def refresh_cache(self) -> None:
        """
        Обновляет время истечения кэша на 5 минут вперед.
        """
        self.cache_expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)


class Token(Base):

    __tablename__ = 'tokens'
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    access_token = Column(String(255), unique=True, index=True, default=lambda: secrets.token_urlsafe(32))
    token_type = Column(String(50), default='bearer')
    expires_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=30))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    is_jwt = Column(Boolean, default=False)  # Указывает, является ли токен JWT

    # Связь многие-к-одному с таблицей User
    user = relationship("User", back_populates="tokens")

    def __repr__(self):
        return f"Token id: {self.id}, expires_at: {self.expires_at}, user_id: {self.user_id}"

    def check_valid(self) -> bool:
        """
        Проверяет, действителен ли токен в настоящий момент.
        """
        return is_token_valid(self.expires_at)
