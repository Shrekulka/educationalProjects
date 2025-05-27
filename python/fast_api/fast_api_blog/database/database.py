# fast_api_post_manager/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
from utils.logger_config import logger
from config_data.config import config

# Используем метод get_db_url() вместо ручного формирования строки подключения
SQLALCHEMY_DATABASE_URL = config.get_db_url()

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,  # Проверка соединения перед использованием
        pool_recycle=3600    # Пересоздавать соединения каждый час
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database connection established successfully")
except sqlalchemy.exc.SQLAlchemyError as e:
    logger.error(f"Database error occurred: {str(e)}")
    raise RuntimeError("Database error occurred")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()