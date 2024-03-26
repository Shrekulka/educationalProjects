# fastapi_project_skeleton/src/main.py
import uvicorn
from fastapi import FastAPI

from src.auth.utils import generate_users, find_user_by_id
from src.logger_config import logger


def create_app() -> FastAPI:
    """
        Создает экземпляр FastAPI с заголовком "my_second_startup_option" и определяет обработчик маршрута для HTTP GET
        запросов на корневой URL "/".

        Возвращает созданный экземпляр FastAPI.
    """
    # Создаем экземпляр FastAPI с заголовком "my_user_information_lesson"
    app: FastAPI = FastAPI(title="my_user_information_lesson")

    # Количество создаваемых пользователей
    num_users = 100

    # Генерация списка пользователей
    users_list = generate_users(num_users)

    # Конечная точка для получения информации о пользователе по ID
    @app.get("/users/{user_id}")
    async def read_user(user_id: int):
        return find_user_by_id(user_id, users_list)

    @app.get("/users")
    async def read_users(limit: int = 5):
        return users_list[:limit]

    # Возвращаем созданный экземпляр FastAPI
    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("second_startup_option:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
