# inter_exchange_arbitrage_bot/src/bot/keyboards/__init__.py
"""
Пакет для генерации инлайн-клавиатур бота.

Этот __init__.py собирает все функции-генераторы клавиатур из разных модулей
и предоставляет единый, удобный интерфейс для их импорта в обработчиках.
Использование __all__ с группировкой делает API пакета явным и понятным.
"""

from .main_menu_keyboard import get_main_menu_inline_keyboard
from .balance_keyboard import get_balance_menu_keyboard
from .scanner_keyboard import get_scanner_menu_keyboard, get_back_to_scanner_menu_keyboard
from .settings_keyboard import get_settings_keyboard, get_scanner_settings_keyboard, get_back_to_settings_keyboard
from .coin_keyboards import get_coin_selection_keyboard, get_coin_removal_keyboard

# __all__ определяет публичный API пакета 'keyboards'
__all__ = [
    # --- Главное меню ---
    'get_main_menu_inline_keyboard',

    # --- Меню баланса ---
    'get_balance_menu_keyboard',

    # --- Меню сканера ---
    'get_scanner_menu_keyboard',
    'get_back_to_scanner_menu_keyboard',

    # --- Меню настроек и его под-меню ---
    'get_settings_keyboard',            # Основное меню настроек
    'get_scanner_settings_keyboard',    # Настройки суммы и порога для сканера
    'get_back_to_settings_keyboard',    # Простая кнопка "назад" в настройки

    # --- Меню управления монетами ---
    'get_coin_selection_keyboard',      # Клавиатура для добавления монет (с пагинацией)
    'get_coin_removal_keyboard',        # Клавиатура для удаления монет
]