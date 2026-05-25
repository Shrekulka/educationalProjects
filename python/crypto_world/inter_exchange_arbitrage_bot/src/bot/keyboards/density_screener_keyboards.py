# inter_exchange_arbitrage_bot/src/bot/keyboards/density_screener_keyboards.py

from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants.telegram_constants import PAGINATION_ITEMS_PER_PAGE
from src.lexicon.lexicon_ru import LEXICON_RU
from src.utils.helpers import get_prioritized_search_results


def get_density_screener_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для подменю скринера плотностей, используя тексты из лексикона.
    """
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=LEXICON_RU['scan_top_100_button'], callback_data="density:scan_top_100"))
    builder.row(InlineKeyboardButton(text=LEXICON_RU['scan_favorites_button'], callback_data="density:scan_favorites"))
    builder.row(InlineKeyboardButton(text=LEXICON_RU['select_custom_button'], callback_data="density:select_custom"))
    builder.row(InlineKeyboardButton(text=LEXICON_RU['back_to_main_menu_button'], callback_data="back_to_main_menu"))

    return builder.as_markup()


def get_density_coin_selection_keyboard(
        all_coins: List[str],
        selected_coins: List[str],
        current_page: int = 0,
        search_query: str = None
) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора монет для скринера, используя тексты из лексикона.
    """
    builder = InlineKeyboardBuilder()
    items_per_page = PAGINATION_ITEMS_PER_PAGE

    if search_query:
        # Используем новую функцию для получения отсортированного списка
        display_coins = get_prioritized_search_results(all_coins, search_query)
    else:
        display_coins = all_coins

    start_index = current_page * items_per_page
    page_coins = display_coins[start_index: start_index + items_per_page]

    for coin in page_coins:
        text = f"✅ {coin}" if coin in selected_coins else f"⬜️ {coin}"
        builder.add(InlineKeyboardButton(text=text, callback_data=f"density:toggle:{coin}:{current_page}"))

    builder.adjust(3)

    # --- Пагинация и кнопки действий остаются без изменений ---
    pagination_buttons = []
    total_pages = (len(display_coins) + items_per_page - 1) // items_per_page
    if current_page > 0:
        pagination_buttons.append(InlineKeyboardButton(text=LEXICON_RU['pagination_back_button'],
                                                       callback_data=f"density:page:{current_page - 1}"))
    if total_pages > 1:
        pagination_buttons.append(InlineKeyboardButton(text=f"{current_page + 1}/{total_pages}", callback_data="noop"))
    if start_index + items_per_page < len(display_coins):
        pagination_buttons.append(InlineKeyboardButton(text=LEXICON_RU['pagination_forward_button'],
                                                       callback_data=f"density:page:{current_page + 1}"))
    if pagination_buttons:
        builder.row(*pagination_buttons)

    action_buttons = []
    if search_query:
        action_buttons.append(
            InlineKeyboardButton(text=LEXICON_RU['clear_search_button'], callback_data="density:clear_search"))

    action_buttons.append(InlineKeyboardButton(text=LEXICON_RU['cancel_button'], callback_data="show_density_screener"))

    if selected_coins:
        action_buttons.append(
            InlineKeyboardButton(text=LEXICON_RU['scan_selected_button'], callback_data="density:confirm"))

    builder.row(*action_buttons)
    return builder.as_markup()