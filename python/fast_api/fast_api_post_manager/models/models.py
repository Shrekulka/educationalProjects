# fast_api_post_manager/models/models.py

import uuid
from datetime import datetime, timezone

import sqlalchemy
from sqlalchemy import Column, String, Boolean, UUID
from sqlalchemy import DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    Class representing a table of users in the database.

    Attributes:
        id (UUID): Field for user identifier (primary key).
        name (str): User's first name.
        surname (str): User's last name.
        email (str): Field for user's email address (unique, mandatory).
        hashed_password (str): Field for hashed user's password.
        is_active (bool): Whether the user account is active.
        posts (relationship): One-to-many relationship with the Post table.
    """
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

    # Установка отношения "один ко многим" с таблицей Post и указание атрибута обратного отношения
    posts = relationship("Post", back_populates="owner")

    def __repr__(self):
        return f"User: {self.name} {self.surname}, id: {self.id}, email: {self.email}"


class Post(Base):
    """
        Class representing a table of posts in the database.

        Attributes:
            id (int): Field for post identifier (primary key).
            status (str): Field for post status.
            user_id (int): Foreign key linking the Post table to the User table.
            created_date (DateTime): Field for post creation date and time.
            updated_date (DateTime): Field for post update date and time.
            owner (relationship): Many-to-one relationship with the User table.
    """
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), index=True)
    text = Column(sqlalchemy.Text(1048576), nullable=False)  # 1MB limit
    status = Column(String(50))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Для создания даты и времени в текущем часовом поясе и затем преобразования в UTC
    created_date = Column(DateTime, default=datetime.now(timezone.utc))

    # Для обновления даты и времени при каждом обновлении объекта
    updated_date = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))

    # Установка отношения "многие к одному" с таблицей User и указание атрибута обратного отношения
    owner = relationship("User", back_populates="posts")

    __table_args__ = (
        CheckConstraint('LENGTH(text) <= 1048576', name='check_text_length'),
        CheckConstraint("status IN ('draft', 'published')", name='check_status'),
    )

    def __repr__(self):
        return f'post_id: {self.id}, text: {self.text} with status: {self.status} created date: {self.created_date}. Author: {self.user_id}'
