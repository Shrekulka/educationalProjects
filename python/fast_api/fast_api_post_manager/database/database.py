# fast_api_post_manager/database/database.py
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config_data.config import config
from utils.logger_config import logger

# Асинхронный движок
async_engine = create_async_engine(
    config.get_async_db_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,  # Размер пула
    max_overflow=20,  # Дополнительные соединения при нагрузке
    echo=False
)

# Асинхронная фабрика сессий
async_session_maker = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database error: {type(e).__name__} - {e}")
            raise
        finally:
            await session.close()
