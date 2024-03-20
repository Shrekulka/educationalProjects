# fast_api_blog/models/models.py

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    """
        Class representing a table of users in the database.

        Attributes:
            id (int): Field for user identifier (primary key).
            email (str): Field for user's email address (unique, mandatory).
            password (str): Field for user's password (mandatory).
            hashed_password (str): Field for hashed user's password.
            posts (relationship): One-to-many relationship with the Post table.
    """
    __tablename__ = 'users'                                   # Название таблицы в базе данных
    id = Column(Integer, primary_key=True)                    # Поле идентификатора пользователя
    email = Column(String(100), unique=True, nullable=False)  # Поле адреса электронной почты пользователя
    password = Column(String(100), nullable=False)            # Поле пароля пользователя
    hashed_password = Column(String(100))                     # Поле хешированного пароля пользователя

    # Установка отношения "один ко многим" с таблицей Post и указание атрибута обратного отношения
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    """
        Class representing a table of posts in the database.

        Attributes:
            id (int): Field for post identifier (primary key).
            title (str): Field for post title (index).
            content (str): Field for post content (index).
            status (str): Field for post status.
            user_id (int): Foreign key linking the Post table to the User table.
            created_date (DateTime): Field for post creation date and time.
            updated_date (DateTime): Field for post update date and time.
            owner (relationship): Many-to-one relationship with the User table.
    """
    __tablename__ = "posts"                             # Название таблицы в базе данных
    id = Column(Integer, primary_key=True, index=True)  # Поле идентификатора поста
    title = Column(String(255), index=True)             # Поле заголовка поста
    content = Column(String(1000), index=True)          # Поле содержания поста
    status = Column(String(50))                         # Поле статуса поста
    user_id = Column(Integer, ForeignKey("users.id"))   # Внешний ключ, связывающий таблицу Post с таблицей User

    # Для создания даты и времени в текущем часовом поясе и затем преобразования в UTC
    created_date = Column(DateTime, default=datetime.now(timezone.utc))

    # Для обновления даты и времени при каждом обновлении объекта
    updated_date = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))

    # Установка отношения "многие к одному" с таблицей User и указание атрибута обратного отношения
    owner = relationship("User", back_populates="posts")


class TokenTable(Base):
    """
        Class representing a table of tokens in the database.

        Attributes:
            user_id (int): Foreign key linking the TokenTable to the User table.
            access_token (str): Field for access token (primary key).
            refresh_token (str): Field for refresh token (mandatory).
            status (bool): Field for token status.
            created_date (DateTime): Field for record creation date.
            owner (relationship): Many-to-one relationship with the User table.
    """
    __tablename__ = "token"                               # Название таблицы в базе данных
    user_id = Column(Integer, ForeignKey("users.id"))     # Внешний ключ, связывающий таблицу TokenTable с таблицей User
    access_token = Column(String(450), primary_key=True)  # Поле токена доступа
    refresh_token = Column(String(450), nullable=False)   # Поле токена обновления
    status = Column(Boolean)                              # Поле статуса токена
    created_date = Column(DateTime, default=datetime.now)  # Поле даты создания записи

    # Установка отношения "многие к одному" с таблицей User
    owner = relationship("User")
