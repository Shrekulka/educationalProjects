# fast_api_blog/database/database.py

import sqlalchemy.exc
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from config_data.config import config
from utils.logger_config import logger

# Извлечение данных подключения к MySQL из переменных окружения
MYSQL_USER = config.mysql_user
MYSQL_PASSWORD = config.mysql_password.get_secret_value()
MYSQL_HOST = config.mysql_host
MYSQL_DB = config.mysql_db

# Строка подключения к MySQL
SQLALCHEMY_DATABASE_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

try:
    # Создание экземпляра SQLAlchemy Engine для управления соединениями с базой данных
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # Создание базового класса для моделей, определенных в базе данных
    Base = sqlalchemy.orm.declarative_base()

    # Создание экземпляра Session для взаимодействия с базой данных
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Base)

    # Определение моделей и создание соответствующих таблиц в базе данных
    from models import models

    # Создаем таблицы в базе данных
    Base.metadata.create_all(engine)

except sqlalchemy.exc.SQLAlchemyError as e:
    logger.error(f"Database error occurred: {str(e)}")
    # Бросаем исключение HTTPException в случае ошибки базы данных
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
