# fast_api_post_manager/routers/user_router.py

import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.database import get_db
from schemas.user_schema import UserResponse, UserWithPosts, UserCreate
from controllers.user_controller import register as register_user
from controllers.user_controller import get_user_basic as get_basic_user
from controllers.user_controller import get_user_detailed as get_detailed_user
from controllers.user_controller import get_users as fetch_users

# Создание роутера для пользователей
user_router = APIRouter()

# Исправьте функции:
@user_router.get("/", response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   return fetch_users(db, skip=skip, limit=limit)

@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_basic(user_id: uuid.UUID, db: Session = Depends(get_db)):
   return get_basic_user(db, user_id)

@user_router.get("/{user_id}/full", response_model=UserWithPosts)
def get_user_detailed(user_id: uuid.UUID, db: Session = Depends(get_db)):
   return get_detailed_user(db, user_id)

@user_router.post("", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db=db, user_data=user_data)