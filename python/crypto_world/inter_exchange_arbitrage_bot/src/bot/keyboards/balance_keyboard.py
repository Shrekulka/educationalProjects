# inter_exchange_arbitrage_bot/src/bot/keyboards/balance_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_balance_menu_keyboard(mode: str = 'tracked') -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для меню баланса с улучшенным UX.

    Args:
        mode (str): Текущий режим отображения ('tracked' или 'all').
    """
    builder = InlineKeyboardBuilder()

    # Кнопка "Обновить" всегда есть, но с разной callback_data
    builder.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh_balance:{mode}")
    )

    # Кнопки для переключения режимов с более понятными названиями
    if mode == 'tracked':
        builder.row(
            InlineKeyboardButton(text="📊 Все активы", callback_data="show_balance:all")
        )
    else:
        builder.row(
            InlineKeyboardButton(text="⭐ Избранные", callback_data="show_balance:tracked")
        )

    builder.row(
        InlineKeyboardButton(text="⚙️ Настройки", callback_data="show_settings"),
        InlineKeyboardButton(text="🏠 Главное", callback_data="back_to_main_menu")
    )

    return builder.as_markup()
