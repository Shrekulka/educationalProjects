# inter_exchange_arbitrage_bot/src/bot/logic/__init__.py
"""
Пакет бизнес-логики бота.

Этот __init__.py определяет публичный API пакета, предоставляя
удобный доступ к основным функциям, которые вызываются из обработчиков (handlers).
"""

from .balance_logic import process_and_send_balance
from .menu_logic import show_main_menu
from .settings_logic import show_settings_menu

# __all__ определяет, что будет импортировано при `from src.bot.logic import *`
__all__ = [
    # Функции для отображения основных меню
    'show_main_menu',
    'show_settings_menu',

    # Функции, связанные с отображением данных пользователя
    'process_and_send_balance',
]