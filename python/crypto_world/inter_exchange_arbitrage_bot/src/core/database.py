# inter_exchange_arbitrage_bot/src/core/database.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.core.config import config
from src.utils.logger import logger

# Проверяем, что конфиг для БД существует
if not config.db:
    logger.error("Конфигурация базы данных отсутствует в .env! Невозможно продолжить.")
    raise ValueError("Database configuration is missing.")

# Формируем URL для подключения из конфига
DB_URL = (
    f"{config.db.engine}://{config.db.user}:{config.db.password}"
    f"@{config.db.host}:{config.db.port}/{config.db.name}"
)

# Создаем "движок" для асинхронной работы с БД
# echo=config.debug выводит все SQL-запросы в консоль, если включен режим DEBUG
engine = create_async_engine(DB_URL, echo=config.debug)

# Создаем фабрику сессий, через которую будем делать запросы
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для всех наших будущих моделей (таблиц)
class Base(DeclarativeBase):
    pass