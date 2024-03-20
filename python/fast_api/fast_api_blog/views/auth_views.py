# fast_api_blog/views/auth_views.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from controllers.auth_controller import signup_handler, login_handler, refresh_token_handler
from database.session import get_session
from schemas.auth import UserCreate, LoginRequest

# Создаем экземпляр маршрутизатора API для авторизации.
auth_router = APIRouter()


@auth_router.post("/signup")
def signup(request: UserCreate, session: Session = Depends(get_session)) -> JSONResponse:
    """
        Endpoint for user registration.

        Args:
            request (UserCreate): Data schema for creating a new user, containing email and password.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).

        Returns:
            JSONResponse: Response in JSON format containing success status and generated access tokens (access_token
            and refresh_token).

        Raises:
            HTTPException: If there is an error performing database operations during registration.
    """
    # Возвращаем результат выполнения функции обработчика регистрации.
    # Передаем в функцию обработчика запрос на регистрацию пользователя (request) и сеанс базы данных (session).
    return signup_handler(request, session=session)


@auth_router.post("/login")
def login(request: LoginRequest, session: Session = Depends(get_session)) -> JSONResponse:
    """
        Endpoint for user login.

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
    # Вызываем функцию обработчика входа пользователя, передавая ей запрос на вход и сеанс базы данных в качестве
    # параметров
    return login_handler(request, session=session)


@auth_router.post("/refreshToken")
def refresh_token(request: LoginRequest, session: Session = Depends(get_session)) -> JSONResponse:
    """
        Endpoint for refreshing access tokens (access_token and refresh_token) for the user.

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
    # Вызываем функцию обработчика обновления токенов.
    # Передаем в функцию запрос на обновление токенов и сессию базы данных.
    return refresh_token_handler(request, session=session)
