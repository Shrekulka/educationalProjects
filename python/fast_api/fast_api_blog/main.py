# fast_blog/main.py

from fastapi import FastAPI

from utils.logger_config import logger
from views import auth_views, post_views

# Создание экземпляра FastAPI с указанием названия приложения
app = FastAPI(title="FastAPI-Blog")

# Включение маршрутов для аутентификации
app.include_router(auth_views.auth_router, prefix="/api/auth")

# Включение маршрутов для постов
app.include_router(post_views.posts_router, prefix="/api/posts")

# Логгирование запуска сервера
logger.info("Server started successfully")
