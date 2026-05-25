# inter_exchange_arbitrage_bot/src/bot/handlers/__init__.py

from .user_handlers import router as user_router
from .settings_handlers import router as settings_router
from .scanner_handlers import router as scanner_router

__all__ = ['user_router', 'settings_router', 'scanner_router']