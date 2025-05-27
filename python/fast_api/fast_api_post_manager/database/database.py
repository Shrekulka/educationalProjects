# fast_api_post_manager/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
from utils.logger_config import logger
from config_data.config import config

MYSQL_USER = config.mysql_user
MYSQL_PASSWORD = config.mysql_password.get_secret_value()
MYSQL_HOST = config.mysql_host
MYSQL_DB = config.mysql_db
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={'charset': 'utf8mb4'},
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