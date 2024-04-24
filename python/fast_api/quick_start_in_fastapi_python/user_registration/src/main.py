# user_registration/src/main.py
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException

from src.logger_config import logger
from src.models import UserCreate


def create_app() -> FastAPI:
    """
       Создание экземпляра FastAPI и настройка маршрутов.

       Returns:
           FastAPI: Экземпляр веб-приложения FastAPI.
    """
    # Создаем экземпляр FastAPI с заголовком "User Registration"
    app: FastAPI = FastAPI(title="User Registration")

    # Список пользователей, который будет использоваться для хранения данных о созданных пользователях.
    users_db: List[UserCreate] = []

    @app.get("/create_user")
    async def get_feedback(limit: int = 10) -> List[UserCreate]:
        """
        Возвращает список созданных пользователей с ограничением по количеству.

        Args:
            limit (int): Максимальное количество пользователей для возврата (по умолчанию 10).

        Returns:
            List[UserCreate]: Список созданных пользователей.
        """
        try:
            return users_db[:limit]
        except Exception as e:
            # Если произошла ошибка при получении списка пользователей
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/create_user")
    async def add_feedback(user: UserCreate) -> dict:
        """
            Создает нового пользователя на основе переданных данных.

            Args:
                user (UserCreate): Данные нового пользователя.

            Returns:
                dict: Словарь с сообщением об успешном создании пользователя.
        """
        try:
            # Попытка добавить пользователя в базу данных
            users_db.append(user)
            return {"message": f"Thank you, {user.name}!"}
        except Exception as e:
            # Если произошла ошибка при добавлении пользователя
            raise HTTPException(status_code=500, detail=str(e))

    # Возвращаем созданный экземпляр FastAPI
    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("main:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
