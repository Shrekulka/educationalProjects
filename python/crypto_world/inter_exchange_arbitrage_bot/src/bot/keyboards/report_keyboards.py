# inter_exchange_arbitrage_bot/src/bot/keyboards/report_keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicon import LEXICON_RU
from src.constants.telegram_constants import CALLBACK_GET_REPORT


def get_report_menu_keyboard(hours: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для меню выбора отчетов.

    Args:
        hours (int): Период отчета в часах, для формирования callback_data.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['report_summary_button'],
            callback_data=f"{CALLBACK_GET_REPORT}:summary:{hours}"
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['report_detailed_button'],
            callback_data=f"{CALLBACK_GET_REPORT}:detailed:{hours}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back_to_main_menu'],
            callback_data="back_to_main_menu"
        )
    )
    return builder.as_markup()