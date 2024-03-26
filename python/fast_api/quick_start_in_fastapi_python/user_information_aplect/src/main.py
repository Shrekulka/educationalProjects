# user_information_aplect/src/main.py

import uvicorn
from fastapi import FastAPI

from src.logger_config import logger
from src.models import User


def create_app() -> FastAPI:
    """
        Функция для создания экземпляра FastAPI с определением обработчика маршрута для HTTP GET запросов на корневой
        URL "/".

        Returns:
            FastAPI: Созданный экземпляр FastAPI.
    """
    # Создаем экземпляр FastAPI с заголовком "my_first_user"
    app: FastAPI = FastAPI(title="my_first_user")

    # Инициализация данных первого пользователя
    first_user = {'name': 'John Doe', 'id': 1}

    # Создание экземпляра User из данных первого пользователя
    # Этот синтаксис с ** используется для распаковки пар ключ-значение из словаря first_user в качестве аргументов
    # ключевых слов при создании экземпляра User. Это позволяет нам передавать данные о пользователе в виде именованных
    # аргументов конструктора User, используя ключи из словаря first_user в качестве имен аргументов и их значения в
    # качестве значений аргументов.
    my_user = User(**first_user)

    @app.get("/users")  # Обработчик маршрута для GET-запросов на /users
    async def get_user():
        """
            Функция для обработки GET-запросов на маршрут /users.

            Returns:
                User: Данные о пользователе в виде экземпляра User.
        """
        return my_user  # Возврат данных о пользователе

    return app  # Возвращаем созданный экземпляр FastAPI


if __name__ == '__main__':
    try:
        # Запуск приложения с помощью uvicorn
        uvicorn.run("src.main:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
