# fast_api_blog/database/session.py

import traceback
from typing import Generator
from utils.logger_config import logger


def get_session() -> Generator:
    """
        Function to get the database session.

        Returns:
            Generator: Generator yielding the database session.

        Raises:
            Exception: If there is an error obtaining the session.
    """
    from database.database import SessionLocal
    # Получение сессии из локального источника
    session = SessionLocal()
    try:
        # Возвращаем сессию как генератор
        yield session
    except Exception as error:
        # В случае ошибки логируем её и поднимаем исключение дальше
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"An error occurred while getting a session: {error}\n{detailed_error_traceback}")
        raise
    finally:
        # Всегда закрываем сессию после использования
        session.close()
