# fast_api_post_manager/controllers/user_controller.py

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from models.models import User
from schemas.user_schema import UserCreate
from utils.password_utils import hash_password


def register(db: Session, user_data: UserCreate):
    if db.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!"
        )

    # Создаём пользователя со всеми полями
    user = User(
        email=str(user_data.email),
        name=user_data.name,
        surname=user_data.surname,
        hashed_password=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)  # обновляем из БД, чтобы получить все поля
    return user       # возвращаем объект пользователя, Pydantic автоматически преобразует
