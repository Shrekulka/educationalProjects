# inter_exchange_arbitrage_bot/src/api/__init__.py
"""
Пакет API, построенный на FastAPI.

Этот пакет определяет все эндпоинты, доступные для внешнего взаимодействия с ботом.
__init__.py служит для агрегации и экспорта основных компонентов API:
роутеров и схем данных, делая их доступными для основного приложения.
"""

# Импорты сгруппированы по модулям для ясности
from .api_router import api_router
from .system_router import system_router
from .schemas import ScannerActionResponse, ScannerStatusResponse

# __all__ определяет публичный API пакета 'api'
__all__ = [
    # --- FastAPI Роутеры ---
    # Эти объекты должны быть подключены в главном приложении FastAPI (`app.include_router(...)`)
    'api_router',
    'system_router',

    # --- Pydantic Схемы ---
    # Используются для валидации данных и генерации документации OpenAPI
    'ScannerActionResponse',
    'ScannerStatusResponse',
]