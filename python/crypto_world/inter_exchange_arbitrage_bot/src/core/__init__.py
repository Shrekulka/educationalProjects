# inter_exchange_arbitrage_bot/src/core/__init__.py

from .config import config
from .database import async_session_factory, Base
from .scheduler import scheduler

__all__ = [
    # Глобальный экземпляр конфигурации
    'config',

    # Компоненты для работы с базой данных
    'async_session_factory',
    'Base',

    # Глобальный экземпляр планировщика задач
    'scheduler',
]