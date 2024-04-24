# cookie_authentication_service/src/main.py

from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Response, Cookie

from src.database import dbuser
from src.logger_config import logger
from src.models import User
from src.utils import generate_session_token


def create_app() -> FastAPI:
    """
    Создает экземпляр FastAPI приложения для обработки запросов, связанных с аутентификацией.

    Returns:
        FastAPI: Экземпляр FastAPI приложения.
    """
    # Создаем экземпляр FastAPI с заголовком "Cookie Authentication Service"
    app: FastAPI = FastAPI(title="Cookie Authentication Service")

    @app.post("/login")
    async def login(user: User, response: Response) -> dict:
        """
            Маршрут для входа пользователя в систему.

            Args:
                user (User): Модель пользователя, содержащая имя пользователя и пароль.
                response (Response): Объект ответа FastAPI для установки cookie.

            Returns:
                dict: Словарь с сессионным токеном, если аутентификация прошла успешно.

            Raises:
                HTTPException: Ошибка 401, если учетные данные неверны.
        """
        # Ищем пользователя в базе данных по имени пользователя
        user_data = next((i for i in dbuser if i["username"] == user.username), None)
        # Если пользователь найден и пароль совпадает
        if user_data and user_data["password"] == user.password:
            # Генерируем новый сессионный токен
            session_token = generate_session_token()
            # Добавляем сессионный токен в данные пользователя
            user_data["session_token"] = session_token
            # Устанавливаем cookie с сессионным токеном в ответ
            response.set_cookie(key="session_token", value=session_token, httponly=True, samesite="strict")
            # Возвращаем сессионный токен в ответе
            return {"session_token": session_token}
        # Если пользователь не найден или пароль неверный, возвращаем ошибку 401
        raise HTTPException(status_code=401, detail="Invalid credentials")

    @app.get("/user")
    async def get_user_profile(session_token: Optional[str] = Cookie(None)) -> dict:
        """
            Маршрут для получения профиля пользователя.

            Args:
                session_token (Optional[str], optional): Сессионный токен пользователя, переданный через cookie.
                    По умолчанию None.

            Returns:
                dict: Словарь с данными пользователя.

            Raises:
                HTTPException: Ошибка 401, если сессионный токен отсутствует или недействителен.
        """
        # Если сессионный токен не передан, возвращаем ошибку 401
        if not session_token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Ищем пользователя в базе данных по сессионному токену
        user_data = next((i for i in dbuser if "session_token" in i and i["session_token"] == session_token), None)
        # Если пользователь найден, возвращаем его данные
        if user_data:
            return {"user": user_data}

        # Если пользователь не найден, возвращаем ошибку 401
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Возвращаем созданный экземпляр FastAPI
    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("main:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        # Логируем прерывание программы пользователем
        logger.info("Program interrupted by user")
    except Exception as e:
        # Логируем непредвиденную ошибку
        logger.error(f"An unexpected error occurred: {e}")
