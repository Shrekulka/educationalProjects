# fast_api_blog/models/models.py
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для всех моделей с поддержкой асинхронности"""
    __abstract__ = True

    def __repr__(self):
        """Строковое представление модели"""
        columns = list(self.__table__.columns.keys())
        values = [getattr(self, c) for c in columns]
        return f"<{self.__class__.__name__} {dict(zip(columns, values))}>"
