# inter_exchange_arbitrage_bot/src/bot/keyboards/settings_keyboard.py

from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants.trading_constants import DEFAULT_TRADE_AMOUNT_USD, DEFAULT_PROFIT_THRESHOLD


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для меню настроек."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✨ Мои монеты", callback_data="show_my_coins")
    )
    builder.row(
        InlineKeyboardButton(text="➕ Добавить монеты", callback_data="add_coin_start"),
        InlineKeyboardButton(text="🗑️ Удалить монету", callback_data="remove_coin_start")
    )
    builder.row(
        InlineKeyboardButton(text="📈 Настройки сканера", callback_data="show_scanner_settings")
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main_menu")
    )
    return builder.as_markup()


def get_scanner_settings_keyboard(current_amount: Optional[float],
                                  current_threshold: Optional[float]) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для меню настроек сканера."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="✍️ Изменить сумму сделки", callback_data="set_trade_amount")
    )
    builder.row(
        InlineKeyboardButton(text="✍️ Изменить порог прибыльности", callback_data="set_profit_threshold")
    )

    # Кнопки сброса, которые появляются только при кастомных значениях
    if current_amount is not None:
        reset_amount_text = f"🔄 Сбросить сумму к значению по умолчанию (${DEFAULT_TRADE_AMOUNT_USD:.2f})"
        builder.row(
            InlineKeyboardButton(text=reset_amount_text, callback_data="reset_trade_amount")
        )

    if current_threshold is not None:
        reset_threshold_text = f"🔄 Сбросить порог к значению по умолчанию ({DEFAULT_PROFIT_THRESHOLD * 100:.2f}%)"
        builder.row(
            InlineKeyboardButton(text=reset_threshold_text, callback_data="reset_profit_threshold")
        )

    builder.row(
        InlineKeyboardButton(text="⬅️ Назад в Настройки", callback_data="back_to_settings")
    )
    return builder.as_markup()


def get_back_to_settings_keyboard() -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с кнопкой 'Назад' в меню настроек."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад в Настройки", callback_data="back_to_settings")
    )
    return builder.as_markup()
