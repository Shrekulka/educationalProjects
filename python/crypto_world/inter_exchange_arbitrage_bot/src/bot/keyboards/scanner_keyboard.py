# inter_exchange_arbitrage_bot/src/bot/keyboards/scanner_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_scanner_menu_keyboard(is_running: bool) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для меню управления сканером."""
    builder = InlineKeyboardBuilder()

    status_text = "🟢 Статус: Запущен" if is_running else "🔴 Статус: Остановлен"
    builder.row(InlineKeyboardButton(text=status_text, callback_data="check_scanner_status"))

    if is_running:
        builder.row(InlineKeyboardButton(text="⏹️ Остановить сканер", callback_data="stop_scanner"))
    else:
        builder.row(InlineKeyboardButton(text="▶️ Запустить сканер", callback_data="start_scanner"))

    builder.row(InlineKeyboardButton(text="🛰️ Разведка", callback_data="recon_scanner"))

    builder.row(InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main_menu"))
    return builder.as_markup()


def get_back_to_scanner_menu_keyboard(is_running: bool) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для уведомлений с полным набором кнопок управления."""
    builder = InlineKeyboardBuilder()
    status_text = "🟢 Статус: Запущен" if is_running else "🔴 Статус: Остановлен"
    builder.row(InlineKeyboardButton(text=status_text, callback_data="check_scanner_status"))

    if is_running:
        builder.row(InlineKeyboardButton(text="⏹️ Остановить", callback_data="stop_scanner"))
    else:
        builder.row(InlineKeyboardButton(text="▶️ Запустить", callback_data="start_scanner"))

    builder.row(InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main_menu"))
    return builder.as_markup()

def get_cancel_keyboard(callback_data: str = "cancel_recon") -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру с одной кнопкой 'Отмена'."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❌ Отмена", callback_data=callback_data)
    )
    return builder.as_markup()