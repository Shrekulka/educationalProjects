# feedback_service/src/main.py
from typing import List

import uvicorn
from fastapi import FastAPI

from src.logger_config import logger
from src.models import Feedback


def create_app() -> FastAPI:
    """
       Создание экземпляра FastAPI и настройка маршрутов.

       Returns:
           FastAPI: Экземпляр веб-приложения FastAPI.
    """
    # Создаем экземпляр FastAPI с заголовком "Feedback Service"
    app: FastAPI = FastAPI(title="Feedback Service")

    # Создание списка для хранения отзывов (наша BD)
    feedback_db: List[Feedback] = []

    @app.get("/feedback")
    async def get_feedback(limit: int = 10) -> List[Feedback]:
        """
            Получает список отзывов.

            Args:
                limit (int): Ограничение на количество возвращаемых отзывов. По умолчанию 10.

            Returns:
                List[Feedback]: Список отзывов.
        """
        # Возвращаем список отзывов с ограничением по количеству
        return feedback_db[:limit]

    @app.post("/feedback")
    async def add_feedback(feedback: Feedback) -> dict:
        """
            Добавляет отзыв в список обратной связи.

            Args:
                feedback (Feedback): Объект отзыва для добавления.

            Returns:
                dict: Сообщение об успешном добавлении отзыва.
        """
        # Добавляем полученный отзыв в список отзывов
        feedback_db.append(feedback)
        return {"message": f"Feedback received. Thank you, {feedback.name}!"}

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
