# fast_api_post_manager/views/user_view.py

import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from models.models import User, Token


def get_users(db:Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_basic(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_user_detailed(db: Session, user_id: uuid.UUID):
    # Используйте joinedload для жадной загрузки связанных постов
    from sqlalchemy.orm import joinedload
    return db.query(User).options(joinedload(User.posts)).filter(User.id == user_id).first()

def get_user_by_token(access_token: str, db: Session):
    token = db.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        # Возвращаем полный объект пользователя, а не словарь
        return token.user
    else:
        raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")