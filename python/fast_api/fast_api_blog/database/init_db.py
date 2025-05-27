# fast_api_post_manager/database/init_db.py

from database.database import engine

from utils.logger_config import logger

def initialize_database():
    try:
        from models.models import Base, User, Post
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise