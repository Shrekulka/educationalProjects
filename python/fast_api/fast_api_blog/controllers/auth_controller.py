# fast_api_blog/controllers/auth_controller.py

import traceback

from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database.session import get_session
from models.models import User
from schemas.auth import UserCreate, LoginRequest
from utils.auth import hash_password, verify_password, create_access_token, create_refresh_token
from utils.logger_config import logger


def signup_handler(request: UserCreate, session: Session = Depends(get_session)) -> JSONResponse:
    """
        Registers a new user in the system.

        Args:
            request (UserCreate): Data schema for creating a new user, containing email and password.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).

        Returns:
            JSONResponse: Response in JSON format containing success status and generated access tokens (access_token
            and refresh_token).

        Raises:
            HTTPException: If there is an error performing database operations during registration.
    """
    try:
        # Проверка, что пользователь с таким email не существует
        existing_user = session.query(User).filter(and_(User.email == request.email)).first()
        # Если пользователь существует, предлагаем войти в систему вместо регистрации
        if existing_user:
            return login_handler(LoginRequest(email=request.email, password=request.password), session=session)

        # Создание нового пользователя
        new_user = User(email=request.email, password=hash_password(request.password))
        session.add(new_user)      # Добавление нового пользователя в базу данных
        session.commit()           # Сохранение изменений в базе данных
        # Обновление объекта new_user в базе данных, чтобы получить значения, сгенерированные базой данных, такие как id
        session.refresh(new_user)

        # Генерация access_token с данными о новом пользователе
        access_token = create_access_token(data={"sub": new_user.email})
        # Генерация refresh_token с данными о новом пользователе
        new_refresh_token = create_refresh_token(data={"sub": new_user.email})

        # Возвращение успешного ответа с кодом состояния HTTP 200 OK и сгенерированными токенами доступа
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"status": "success", "access_token": access_token,
                                     "refresh_token": new_refresh_token})
    # Обработка ошибок базы данных при регистрации
    except SQLAlchemyError as e:
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"Database error occurred during signup: {str(e)}\n{detailed_error_traceback}")
        # Бросаем исключение HTTPException в случае ошибки базы данных
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred during signup")


def login_handler(request: LoginRequest, session: Session = Depends(get_session)) -> JSONResponse:
    """
        Authenticates a user in the system.

        Args:
            request (LoginRequest): Data schema for user login, containing email and password.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).

        Returns:
            JSONResponse: Response in JSON format containing success status and generated access tokens (access_token
            and refresh_token).

        Raises:
            HTTPException: If there is an error performing database operations during login.
            HTTPException: If an incorrect email address or password is entered.
    """
    try:
        # Поиск пользователя по email
        user = session.query(User).filter(and_(User.email == request.email)).first()
        # Проверка наличия пользователя и совпадения пароля
        if not user or not verify_password(request.password, user.password):
            # Если пользователь не найден или пароль неверен, генерируется исключение HTTP 401 UNAUTHORIZED
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        # Генерация access_token с данными о новом пользователе
        access_token = create_access_token(data={"sub": user.email})
        # Генерация refresh_token с данными о новом пользователе
        new_refresh_token = create_refresh_token(data={"sub": user.email})

        # Возвращение успешного ответа с кодом состояния HTTP 200 OK и сгенерированными токенами доступа
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"status": "success", "access_token": access_token,
                                     "refresh_token": new_refresh_token})
    # Обработка ошибок базы данных при входе
    except SQLAlchemyError as e:
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"Database error occurred during login: {str(e)}\n{detailed_error_traceback}")
        # Генерация исключения HTTP 500 INTERNAL SERVER ERROR с деталями ошибки базы данных
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred during login")


# Обновление токенов
def refresh_token_handler(request: LoginRequest, session: Session = Depends(get_session)) -> JSONResponse:
    """
        Refreshes access tokens (access_token and refresh_token) for the user.

        Args:
            request (LoginRequest): Data schema for token refresh, containing user email and password.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).

        Returns:
            JSONResponse: Response in JSON format containing success status and updated access tokens (access_token and
             refresh_token).

        Raises:
            HTTPException: If there is an error performing database operations during token refresh.
            HTTPException: If the user is not found in the database.
    """
    try:
        # Поиск пользователя по email
        user = session.query(User).filter(and_(User.email == request.email)).first()
        # Проверка наличия пользователя]
        if not user:
            # Если пользователь не найден, генерируется исключение HTTP 401 UNAUTHORIZED
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        # Генерация access_token с данными о новом пользователе
        access_token = create_access_token(data={"sub": user.email})
        # Генерация refresh_token с данными о новом пользователе
        new_refresh_token = create_refresh_token(data={"sub": user.email})

        # Возвращение успешного ответа с кодом состояния HTTP 200 OK и сгенерированными токенами доступа
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"status": "success", "access_token": access_token,
                                     "refresh_token": new_refresh_token})
    # Обработка ошибок базы данных при обновлении токенов
    except SQLAlchemyError as e:
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"Database error occurred during token refresh: {str(e)}\n{detailed_error_traceback}")
        # Генерация исключения HTTP 500 INTERNAL SERVER ERROR с деталями ошибки базы данных
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred during token refresh")
