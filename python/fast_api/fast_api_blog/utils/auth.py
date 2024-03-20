# fast_blog/utils/auth.py

import traceback
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.session import get_session
from config_data.config import config

from models.models import User
from utils.logger_config import logger

# Создание экземпляра OAuth2PasswordBearer для проверки токенов доступа
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Создаем экземпляр CryptContext для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
        Hashes the password using bcrypt.

        Args:
            password (str): The user's password.

        Returns:
            str: The hashed password.
    """
    # Возвращает хешированный пароль с использованием bcrypt
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
        Checks if the entered password matches the hashed password.

        Args:
            plain_password (str): The password entered by the user.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if the passwords match, False otherwise.
    """
    # Использует метод verify для проверки пароля
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
        Generates a JWT token.

        Args:
            data (dict): Data to include in the token.
            expires_delta (Optional[timedelta], optional): Expiry time of the token. Default is None.

        Returns:
            str: The generated JWT token.

        Note:
            The generate_token function performs the common logic of token generation, while the create_access_token
            and create_refresh_token functions use it by passing appropriate values for expires_delta.
    """
    # Копирует данные для включения в токен
    to_encode = data.copy()
    # Если задано время истечения токена (expires_delta не равен None), вычисляет время истечения токена
    if expires_delta:
        # Вычисляет время истечения токена
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Устанавливает срок действия токена по умолчанию
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # Добавляет время истечения токена к данным для кодирования
    to_encode.update({"exp": expire})

    # Пытается закодировать токен с использованием секретного ключа и указанного алгоритма
    try:
        encoded_jwt = jwt.encode(to_encode, config.secret_key.get_secret_value(), algorithm=config.algorithm)
    # Если происходит ошибка в процессе кодирования токена, записывает подробное сообщение об ошибке
    except Exception as e:
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"Error encoding token: {e}\n{detailed_error_traceback}")
        # Возбуждает исключение HTTPException с кодом состояния 500 (внутренняя ошибка сервера)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error encoding token")
    # Возвращает сгенерированный JWT токен
    return encoded_jwt


def create_access_token(data: dict) -> str:
    """
        Creates an access token.

        Args:
            data (dict): Data to include in the token.

        Returns:
            str: The access token.
    """
    # Использует функцию generate_token для создания токена доступа с сроком действия 15 минут
    return generate_token(data, expires_delta=timedelta(minutes=15))


def create_refresh_token(data: dict) -> str:
    """
        Creates a refresh token.

        Args:
            data (dict): Data to include in the token.

        Returns:
            str: The refresh token.
    """
    # Использует функцию generate_token для создания токена обновления с сроком действия 30 дней
    return generate_token(data, expires_delta=timedelta(days=30))


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> Optional[User]:
    """
        Extracts the current user from the access token.

        Args:
            token (str): The access token obtained from the Authorization header.
            session (Session): An instance of Session for working with the database.

        Returns:
            Optional[User]: The current user object or None if the user is not found.

        Raises:
            HTTPException: If the access token is invalid or expired.
    """
    try:
        # Декодирование токена доступа
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        # Получение адреса электронной почты пользователя из токена
        email = payload.get("sub")
        # Если адрес электронной почты отсутствует в токене, вызывается исключение
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    # Если произошла ошибка при декодировании токена, вызывается исключение
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    # Если произошла другая ошибка, записывается подробное сообщение об ошибке в журнал и вызывается исключение
    except Exception as e:
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"Error decoding access token: {e}\n{detailed_error_traceback}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error decoding access token")

    # Поиск пользователя в базе данных по email
    user = session.query(User).filter(User.email == email).first()
    # Если пользователь не найден, вызывается исключение
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Возвращается объект пользователя или None, если пользователь не найден
    return user if isinstance(user, User) else None
