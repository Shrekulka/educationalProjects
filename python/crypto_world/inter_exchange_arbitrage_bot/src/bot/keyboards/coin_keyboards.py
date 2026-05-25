# inter_exchange_arbitrage_bot/src/bot/keyboards/coin_keyboards.py

from typing import List, Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants.telegram_constants import (
    PAGINATION_ITEMS_PER_PAGE,
    COIN_SELECTION_TOGGLE_PREFIX,
    COIN_SELECTION_PAGE_PREFIX,
    COIN_SELECTION_CLEAR_SEARCH_PREFIX,
    COIN_SELECTION_CONFIRM_PREFIX,
    COIN_SELECTION_CANCEL_PREFIX
)
from src.lexicon.lexicon_ru import LEXICON_RU
from src.utils.helpers import get_prioritized_search_results


def get_coin_selection_keyboard(
        all_coins: List[str],
        selected_coins: List[str],
        current_page: int = 0,
        search_query: Union[str, List[str]] = None,
        toggle_prefix: str = COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix: str = COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data: str = COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data: str = COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data: str = COIN_SELECTION_CANCEL_PREFIX,
        confirm_button_text: str = LEXICON_RU['confirm_button']
) -> InlineKeyboardMarkup:
    """
    ФИНАЛЬНАЯ ВЕРСИЯ: Создает универсальную клавиатуру для выбора монет
    с настраиваемым текстом кнопки подтверждения и счетчиком.
    """
    builder = InlineKeyboardBuilder()
    items_per_page = PAGINATION_ITEMS_PER_PAGE

    display_coins = get_prioritized_search_results(all_coins, search_query)

    start_index = current_page * items_per_page
    end_index = start_index + items_per_page
    page_coins = display_coins[start_index:end_index]

    for coin in page_coins:
        is_selected = coin in selected_coins
        text = f"✅ {coin}" if is_selected else f"⬜️ {coin}"
        callback_data = f"{toggle_prefix}:{coin}:{current_page}"
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    builder.adjust(3)

    # --- Пагинация ---
    pagination_buttons = []
    total_pages = (len(display_coins) + items_per_page - 1) // items_per_page
    if current_page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(text=LEXICON_RU['pagination_back_button'],
                                 callback_data=f"{page_prefix}:{current_page - 1}")
        )
    if total_pages > 1:
        pagination_buttons.append(
            InlineKeyboardButton(text=f"{current_page + 1}/{total_pages}", callback_data="noop")
        )
    if end_index < len(display_coins):
        pagination_buttons.append(
            InlineKeyboardButton(text=LEXICON_RU['pagination_forward_button'],
                                 callback_data=f"{page_prefix}:{current_page + 1}")
        )
    if pagination_buttons:
        builder.row(*pagination_buttons)

    # --- Кнопки действий ---
    action_buttons = []
    if search_query:
        action_buttons.append(
            InlineKeyboardButton(text=LEXICON_RU['clear_search_button'], callback_data=clear_search_callback_data)
        )

    action_buttons.append(
        InlineKeyboardButton(text=LEXICON_RU['cancel_button'], callback_data=cancel_callback_data)
    )

    if selected_coins:
        # Формируем текст кнопки с количеством выбранных элементов
        button_text = f"{confirm_button_text} ({len(selected_coins)})"

        # Добавляем кнопку в тот же список, чтобы она была в одном ряду
        action_buttons.append(
            InlineKeyboardButton(text=button_text, callback_data=confirm_callback_data)
        )

    # Собираем все кнопки действий в одну строку
    builder.row(*action_buttons)

    return builder.as_markup()


def get_coin_removal_keyboard(
        user_coins: List[str],
        selected_for_removal: List[str]
) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для интерактивного выбора монет для удаления.
    """
    builder = InlineKeyboardBuilder()

    for coin in sorted(user_coins):
        is_selected = coin in selected_for_removal
        text = f"✅ {coin}" if is_selected else f"⬜️ {coin}"
        callback_data = f"toggle_remove:{coin}"
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    builder.adjust(3)

    builder.row(
        InlineKeyboardButton(text=LEXICON_RU['cancel_button'], callback_data="back_to_settings")
    )
    if selected_for_removal:
        builder.add(
            InlineKeyboardButton(text=LEXICON_RU['remove_selected_button'], callback_data="confirm_remove_coins"))

    return builder.as_markup()

# # inter_exchange_arbitrage_bot/src/bot/keyboards/coin_keyboards.py
#
# from typing import List
#
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
#
# from src.constants.telegram_constants import PAGINATION_ITEMS_PER_PAGE
# from src.utils.helpers import get_prioritized_search_results
#
#
# def get_coin_selection_keyboard(
#         all_coins: List[str],
#         selected_coins: List[str],
#         current_page: int = 0,
#         search_query: str = None
# ) -> InlineKeyboardMarkup:
#     """
#     Создает клавиатуру для интерактивного выбора монет с пагинацией и поиском.
#     """
#     builder = InlineKeyboardBuilder()
#     items_per_page = PAGINATION_ITEMS_PER_PAGE
#
#     if search_query:
#         # Используем новую функцию для получения отсортированного списка
#         display_coins = get_prioritized_search_results(all_coins, search_query)
#     else:
#         display_coins = all_coins
#
#     start_index = current_page * items_per_page
#     end_index = start_index + items_per_page
#     page_coins = display_coins[start_index:end_index]
#
#     for coin in page_coins:
#         is_selected = coin in selected_coins
#         text = f"✅ {coin}" if is_selected else f"⬜️ {coin}"
#         callback_data = f"toggle_coin:{coin}:{current_page}"
#         builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
#
#     builder.adjust(3)
#
#     # --- Пагинация и кнопки действий остаются без изменений ---
#     pagination_buttons = []
#     total_pages = (len(display_coins) + items_per_page - 1) // items_per_page
#     if current_page > 0:
#         pagination_buttons.append(
#             InlineKeyboardButton(text="⬅️ Назад", callback_data=f"select_coin_page:{current_page - 1}")
#         )
#     if total_pages > 1:
#         pagination_buttons.append(
#             InlineKeyboardButton(text=f"{current_page + 1}/{total_pages}", callback_data="noop")
#         )
#     if end_index < len(display_coins):
#         pagination_buttons.append(
#             InlineKeyboardButton(text="Вперед ➡️", callback_data=f"select_coin_page:{current_page + 1}")
#         )
#     if pagination_buttons:
#         builder.row(*pagination_buttons)
#
#     action_buttons = []
#     if search_query:
#         action_buttons.append(
#             InlineKeyboardButton(text="🔄 Сбросить поиск", callback_data="clear_coin_search")
#         )
#     action_buttons.append(
#         InlineKeyboardButton(text="🚫 Отмена", callback_data="back_to_settings")
#     )
#     if selected_coins:
#         action_buttons.append(
#             InlineKeyboardButton(text="✅ Сохранить", callback_data="confirm_add_coins")
#         )
#     builder.row(*action_buttons)
#
#     return builder.as_markup()
#
#
# def get_coin_removal_keyboard(
#         user_coins: List[str],
#         selected_for_removal: List[str]
# ) -> InlineKeyboardMarkup:
#     """
#     Создает клавиатуру для интерактивного выбора монет для удаления.
#     """
#     builder = InlineKeyboardBuilder()
#
#     # Создаем кнопки для монет пользователя
#     for coin in sorted(user_coins):
#         is_selected = coin in selected_for_removal
#         text = f"✅ {coin}" if is_selected else f"⬜️ {coin}"
#         # Используем другой префикс, чтобы не было конфликтов с добавлением
#         callback_data = f"toggle_remove:{coin}"
#         builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
#
#     builder.adjust(3)  # Расставляем по 3 в ряд
#
#     builder.row(
#         InlineKeyboardButton(text="🚫 Отмена", callback_data="back_to_settings")
#     )
#     if selected_for_removal:
#         builder.add(InlineKeyboardButton(text="🗑️ Удалить выбранные", callback_data="confirm_remove_coins"))
#
#     return builder.as_markup()
