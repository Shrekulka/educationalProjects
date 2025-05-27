# fast_api_post_manager/routers/user_router.py

import uuid
from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPBearer

from schemas.user_schema import UserResponse, UserWithPosts

# Создание роутера для пользователей
user_router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
    dependencies=[Depends(HTTPBearer())]
)

@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_basic(user_id: uuid.UUID):
    """Базовая информация о пользователе"""
    return user_service.get_user(user_id)

@user_router.get("/{user_id}/full", response_model=UserWithPosts)
def get_user_detailed(user_id: uuid.UUID):
    """Полная информация о пользователе с постами"""
    return user_service.get_user_with_posts(user_id)