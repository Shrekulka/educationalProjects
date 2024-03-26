# user_age_verification_service/src/main.py
import os

import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse

from src.logger_config import logger
from src.models import User


def create_app() -> FastAPI:
    """
    Функция для создания экземпляра FastAPI с определением обработчика маршрута для POST запросов на маршрут "/user",
    который принимает данные JSON, содержащие информацию о пользователе, и возвращает те же данные с дополнительным
    полем is_adult, указывающим, является ли пользователь взрослым.

    Returns:
        FastAPI: Созданный экземпляр FastAPI.
    """
    app: FastAPI = FastAPI(title="user_age_verification_service")

    @app.get("/user")
    async def get_user_form() -> FileResponse:
        """
        Функция для отображения HTML-формы для ввода данных пользователя.

        Возвращает:
            FileResponse: Файловый объект, представляющий HTML-форму для ввода данных пользователя.
        """
        # Получение пути к текущему файлу
        current_dir: str = os.path.dirname(os.path.abspath(__file__))

        # Составление пути к файлу HTML-шаблону
        template_path: str = os.path.join(current_dir, "..", "templates", "user_input_form.html")

        # Проверка наличия файла
        if not os.path.exists(template_path):
            raise RuntimeError(f"Файл {template_path} не существует.")

        # Возврат файла в виде объекта FileResponse
        return FileResponse(template_path)

    @app.post("/user")
    async def create_user(user_data: User) -> User:
        """
        Функция для обработки POST-запросов на маршрут /user.

        Args:
            user_data (User): Данные пользователя, предоставленные в формате JSON.

        Returns:
            User: Данные пользователя в формате JSON с дополнительным полем is_adult, указывающим, является ли
            пользователь взрослым.
        """
        # Определяем, является ли возраст пользователя 18 и больше
        is_adult: bool = user_data.age >= 18

        # Присваиваем полученное значение is_adult новому полю объекта user_data с именем is_adult
        user_data.is_adult = is_adult

        # Возвращаем объект user_data в качестве результата функции
        return user_data

    # Возвращаем созданный экземпляр FastAPI
    return app


if __name__ == '__main__':
    try:
        # Запуск приложения с помощью uvicorn
        uvicorn.run("src.main:create_app", host='127.0.0.1', port=5080)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
