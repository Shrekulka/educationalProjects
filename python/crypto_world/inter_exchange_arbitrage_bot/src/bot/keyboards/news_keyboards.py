# inter_exchange_arbitrage_bot/src/bot/keyboards/news_keyboards.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicon.lexicon_ru import LEXICON_RU


def get_news_menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['top_10_coins_button'],
            callback_data='news_fetch:mode_top10'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['my_favorite_coins_button'],
            callback_data='news_fetch:mode_favorites'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['select_coins_manually_button'],
            callback_data='news_select_manual'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back_to_main_menu_button'],
            callback_data='back_to_main_menu'
        )
    )
    return builder.as_markup()


# НОВАЯ функция клавиатуры "Назад в Новости"
def get_back_to_news_menu_keyboard() -> InlineKeyboardMarkup:  # Указан тип возврата
    """Возвращает клавиатуру с кнопкой 'Назад' в меню новостей."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=LEXICON_RU['back_to_news_menu_button'], callback_data='news_menu')
    )
    return builder.as_markup()
