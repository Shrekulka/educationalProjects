# fast_api_post_manager/database/init_db.py

from database.database import async_engine
from utils.logger_config import logger

async def initialize_database():
    try:
        from models.models import Base
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise SystemExit(f"Database initialization failed: {e}")