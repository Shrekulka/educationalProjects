# fast_api_post_manager/utils/token_utils.py

import secrets
import uuid
from datetime import UTC, datetime, timezone, timedelta
from typing import Optional
import jwt


def create_access_token() -> str:
    """
    Генерация криптографически стойкого токена для доступа
    """
    return str(uuid.uuid4())


def create_token_expiration_time(hours: int = 2) -> datetime:
    """
    Генерация времени истечения токена
    """
    return datetime.now(UTC) + timedelta(hours=hours)

def compare_tokens_safely(stored_token: str, provided_token: str) -> bool:
    """
    Безопасное сравнение токенов
    """
    return secrets.compare_digest(stored_token, provided_token)


def create_user_token(user_id: uuid.UUID, token_lifetime_minutes: int = 30,
                      use_jwt: bool = False, secret_key: Optional[str] = None):
    """
    Создает новый токен для указанного пользователя.
    """
    from models.models import Token

    expiration = datetime.now(timezone.utc) + timedelta(minutes=token_lifetime_minutes)

    if use_jwt:
        if not secret_key:
            raise ValueError("Secret key is required for JWT token")

        # Создаем JWT токен
        payload = {
            "sub": str(user_id),
            "exp": expiration.timestamp(),
            "iat": datetime.now(timezone.utc).timestamp()
        }
        access_token = jwt.encode(payload, secret_key, algorithm="HS256")
    else:
        # Создаем случайный токен
        access_token = secrets.token_urlsafe(32)

    return Token(
        user_id=user_id,
        access_token=access_token,
        expires_at=expiration,
        is_jwt=use_jwt
    )


def verify_token(token_string: str, is_jwt: bool = False,
                 user_id: Optional[uuid.UUID] = None,
                 secret_key: Optional[str] = None,
                 expires_at: Optional[datetime] = None) -> bool:
    """
    Проверяет, действителен ли предоставленный токен.
    """
    if is_jwt and secret_key:
        try:
            payload = jwt.decode(token_string, secret_key, algorithms=["HS256"])
            # Проверяем, что токен принадлежит правильному пользователю, если указан user_id
            if user_id and str(user_id) != payload.get("sub"):
                return False
            # Проверяем срок действия
            return datetime.fromtimestamp(payload.get("exp"), timezone.utc) > datetime.now(timezone.utc)
        except jwt.PyJWTError:
            return False
    else:
        # Для не-JWT токенов просто проверяем срок действия
        if expires_at:
            return datetime.now(timezone.utc) < expires_at
        return False


def is_token_valid(expires_at: datetime) -> bool:
    """
    Проверяет, действителен ли токен по времени истечения.
    """
    return datetime.now(timezone.utc) < expires_at
