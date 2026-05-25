# fast_api_post_manager/controllers/token_controller.py

import secrets
from datetime import datetime, UTC

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from models.models import User, Token
from schemas.user_schema import UserLogin
from utils.password_utils import verify_password
from utils.token_utils import create_access_token, create_token_expiration_time


def verify_user_and_generate_token(db: Session, user_data: UserLogin):
    user: User = db.scalar(select(User).where(User.email == user_data.email))
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    # Отладочный вывод - добавьте это
    print(f"Тип хеша: {type(user.hashed_password)}")
    print(f"Значение хеша: {user.hashed_password}")

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Используем TokenService для генерации
    token = Token(
        user_id=user.id,
        access_token=create_access_token(),
        token_type= "bearer",
        expires_at=create_token_expiration_time()
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return Token(
        access_token=token.access_token,
        expires_at=token.expires_at
    )


def revoke_access_token(db: Session, token: str):
    """Аннулирование токена"""
    # Находим токен с безопасным сравнением
    db_token = db.scalar(
        select(Token).where(
            # Используем безопасное сравнение токенов
            Token.access_token.op('=')(token)  # SQLAlchemy безопасное сравнение
        )
    )

    if not db_token:
        raise HTTPException(status_code=404, detail="Token not found")

    db.delete(db_token)
    db.commit()
    return {"message": "Token successfully revoked"}


def get_user_by_token(db: Session, token: str) -> User:
    """Получение пользователя по токену"""
    # Находим токен с проверкой срока действия
    db_tokens = db.scalars(
        select(Token)
        .where(Token.access_token.op('=')(token))
        .where(Token.expires_at > datetime.now(UTC))
    ).all()

    # Дополнительная проверка с использованием compare_digest
    matching_tokens = [
        t for t in db_tokens
        if secrets.compare_digest(t.access_token, token)
    ]

    if not matching_tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return matching_tokens[0].user