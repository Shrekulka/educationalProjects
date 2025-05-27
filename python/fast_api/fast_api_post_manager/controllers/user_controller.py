# fast_api_post_manager/controllers/user_controller.py

import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from models.models import User
from schemas.user_schema import UserCreate
from secret import pwd_context

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_basic(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_user_detailed(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.id == user_id).first()


def register(db: Session, user_data: UserCreate):
    if db.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!"
        )

    # Создаём пользователя со всеми полями
    user = User(
        email=user_data.email,
        name=user_data.name,
        surname=user_data.surname,
        hashed_password=pwd_context.hash(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)  # обновляем из БД, чтобы получить все поля
    return user  # возвращаем объект пользователя, Pydantic автоматически преобразует
