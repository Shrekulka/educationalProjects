# restful_text_processing_with_nltk/src/main.py

import ssl
import traceback

from src.logger_config import logger

# Пытаемся создать неподтвержденный HTTPS-контекст
try:
    # Сохраняем ссылку на функцию создания неподтвержденного контекста
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Если возникает исключение AttributeError (например, если функция отсутствует в текущей версии библиотеки),
    # ничего не делаем (пропускаем блок)
    pass
else:
    # Если исключения не произошло, заменяем функцию создания стандартного HTTPS-контекста
    # на функцию создания неподтвержденного HTTPS-контекста
    ssl._create_default_https_context = _create_unverified_https_context

import uvicorn
from fastapi import FastAPI

from src.config import settings
from src.nlp.router import router as nlp_router
from src.nlp.utils import download_nltk_resources


def create_app() -> FastAPI:
    """
        Создает и конфигурирует экземпляр приложения FastAPI для обработки запросов NLP.
        Загружает необходимые ресурсы NLTK, подключает роутеры и задает корневой маршрут.
        Returns:
            FastAPI: Настроенное приложение FastAPI.
    """
    # Создаем экземпляр FastAPI с указанием названия приложения
    app = FastAPI(title=settings.app_name)

    # Загрузка необходимых ресурсов NLTK при запуске приложения
    download_nltk_resources()

    # Подключение роутера NLP без префикса
    app.include_router(nlp_router, tags=["NLP"])

    @app.get("/")
    async def root() -> dict:
        """
            Корневой маршрут API.

            Returns:
                dict: Сообщение приветствия.
        """
        # Возвращаем приветственное сообщение в формате JSON
        return {"message": "Welcome to the NLP API"}

    # Возвращаем настроенное приложение FastAPI
    return app


# Запуск приложения с помощью Uvicorn
if __name__ == '__main__':
    try:
        # Запуск сервера Uvicorn с указанным хостом и портом из настроек
        uvicorn.run("main:create_app", host=settings.host, port=settings.port)
    except KeyboardInterrupt:
        logger.warning("Приложение завершено пользователем")
    except Exception as error:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Неожиданная ошибка в приложении: {error}\n{detailed_error_message}")
