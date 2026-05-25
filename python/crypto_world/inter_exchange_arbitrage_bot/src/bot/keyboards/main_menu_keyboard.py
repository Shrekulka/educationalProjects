# inter_exchange_arbitrage_bot/src/bot/keyboards/main_menu_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicon import LEXICON_RU


def get_main_menu_inline_keyboard() -> InlineKeyboardMarkup:
    """Возвращает ГЛАВНУЮ инлайн-клавиатуру с кнопкой возврата."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_to_main_menu")
    )
    builder.row(
        InlineKeyboardButton(text="💰 Баланс", callback_data="show_balance"),
        InlineKeyboardButton(text="📈 Сканер", callback_data="show_scanner_menu")
    )
    builder.row(
        InlineKeyboardButton(text="🛡️ Скринер плотностей", callback_data="show_density_screener"),
        InlineKeyboardButton(text="📊 Отчет по сделкам", callback_data="show_report_menu")
    )
    builder.row(
        InlineKeyboardButton(text=LEXICON_RU.get('news_button',''), callback_data="news_menu")
    )
    builder.row(
        InlineKeyboardButton(text="⚙️ Настройки", callback_data="show_settings")
    )
    builder.row(
        InlineKeyboardButton(text=LEXICON_RU['admin_panel_button'], callback_data="show_admin_panel")
    )
    return builder.as_markup()
