# fast_api_post_manager/routers/user_router.py

import uuid
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from fastapi.security import APIKeyHeader
from sqlmodel import Session
from starlette import status

from controllers.token_controller import verify_user_and_generate_token
from controllers.user_controller import register
from database.database import get_db
from schemas.token_schema import TokenResponse
from schemas.user_schema import UserResponse, UserWithPosts, UserCreate, UserLogin
from utils.logger_config import logger
from utils.password_utils import apikey_scheme
from views.user_view import get_users, get_user_basic, get_user_detailed, get_user_by_token

# Создание роутера для пользователей
user_router = APIRouter()
api_key_header = APIKeyHeader(name="Authorization")



@user_router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return get_users(db, skip=skip, limit=limit)

@user_router.get("/self", response_model=UserResponse)
def read_user_by_id(access_token: Annotated[str, Depends(apikey_scheme)] ,db: Session = Depends(get_db)):
    return get_user_by_token(access_token=access_token, db=db)


@user_router.get("/{user_id}", response_model=UserResponse)
def read_user_basic(user_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
       logger.info(f"Запрос пользователя с ID: {user_id}")
       user = get_user_basic(db=db, user_id=user_id)
       if user is None:
           raise HTTPException(status_code=404, detail="Пользователь не найден")
       return user
    except Exception as e:
        logger.error(f"Ошибка при получении пользователя: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@user_router.get("/{user_id}/full", response_model=UserWithPosts)
def read_user_detailed(user_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
       logger.info(f"Запрос пользователя с ID: {user_id}")
       user = get_user_detailed(db=db, user_id=user_id)
       if user is None:
           raise HTTPException(status_code=404, detail="Пользователь не найден")
       return user
    except Exception as e:
        logger.error(f"Ошибка при получении пользователя: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@user_router.post("", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return register(db=db, user_data=user_data)


@user_router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Вход пользователя в систему и получение токена.

    Args:
        user_data: Данные для входа (email, password)
        db: Сессия БД

    Returns:
        TokenResponse: Токен доступа
    """
    return verify_user_and_generate_token(db, user_data)


@user_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(token: Annotated[str, Depends(api_key_header)], db: Session = Depends(get_db)):
    """
    Выход пользователя из системы (отзыв токена).

    Args:
        token: Токен для отзыва
        db: Сессия БД
    """
    from controllers.token_controller import revoke_access_token
    revoke_access_token(db, token)
    return None