# inter_exchange_arbitrage_bot/src/bot/keyboards/admin_keyboards.py

from typing import List, Dict, Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants.telegram_constants import CALLBACK_SHOW_FULL_LIST, CACHE_STATS_PREVIEW_LIMIT, ADMIN_KEYBOARD_WIDTH
from src.lexicon.lexicon_ru import LEXICON_RU


def get_admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для главной административной панели."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['pair_status_button'],
            callback_data="admin:pair_status"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['exclude_pair_button'],
            callback_data="admin:exclude_pair_start"
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['include_pair_button'],
            callback_data="admin:include_pair_start"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back_to_main_menu'],
            callback_data="back_to_main_menu"
        )
    )
    return builder.as_markup()


def get_cache_stats_keyboard(stats: Dict[str, Any]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для статистики кэша, включая динамические кнопки "Показать все".
    """
    builder = InlineKeyboardBuilder.from_markup(get_admin_panel_keyboard())
    dynamic_buttons = []

    # Используем константу для лимита предпросмотра
    preview_limit = CACHE_STATS_PREVIEW_LIMIT

    for exchange, data in stats.items():
        # Кнопка для временно недоступных пар
        temp_list = data.get('temp_unavailable_list', [])
        if len(temp_list) > preview_limit:
            dynamic_buttons.append(InlineKeyboardButton(
                text=LEXICON_RU['show_all_unavailable_button'].format(exchange=exchange.capitalize(),
                                                                      count=len(temp_list)),
                callback_data=f"{CALLBACK_SHOW_FULL_LIST}:{exchange}:temp_unavailable:0"
            ))

        # Кнопка для исключенных администратором пар
        excluded_list = data.get('admin_excluded_list', [])
        if len(excluded_list) > preview_limit:
            dynamic_buttons.append(InlineKeyboardButton(
                text=LEXICON_RU['show_all_excluded_button'].format(exchange=exchange.capitalize(),
                                                                   count=len(excluded_list)),
                callback_data=f"{CALLBACK_SHOW_FULL_LIST}:{exchange}:admin_excluded:0"
            ))

    for button in dynamic_buttons:
        builder.row(button)

    return builder.as_markup()

def get_exchange_selection_keyboard(exchanges: List[str], action: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора биржи."""
    builder = InlineKeyboardBuilder()
    for exchange in exchanges:
        builder.add(
            InlineKeyboardButton(
                text=exchange.capitalize(),
                callback_data=f"admin:{action}_exchange:{exchange}"
            )
        )
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back_to_admin_panel'],
            callback_data="show_admin_panel"
        )
    )
    return builder.as_markup()


def get_excluded_pairs_keyboard(excluded_pairs: Dict[str, List[str]]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопками для включения исключенных пар.
    В тексте каждой кнопки указана биржа.
    """
    builder = InlineKeyboardBuilder()

    if not excluded_pairs or not any(excluded_pairs.values()):
        builder.row(
            InlineKeyboardButton(
                text=LEXICON_RU['no_excluded_pairs_button'],
                callback_data="admin:no_excluded_pairs"
            )
        )
    else:
        # Убираем заголовки, добавляем биржу в текст кнопки
        # Проходим по всем биржам
        for exchange, pairs in excluded_pairs.items():
            if not pairs:
                continue

            # Для каждой пары на этой бирже создаем отдельную кнопку
            for symbol in pairs:
                builder.add(
                    InlineKeyboardButton(
                        # Формируем текст кнопки: "Биржа Символ"
                        text=f"✅ {exchange.capitalize()} {symbol}",
                        callback_data=f"admin:include_pair:{exchange}:{symbol}"
                    )
                )

        # Расставляем кнопки по 2 в ряд для компактности
        builder.adjust(ADMIN_KEYBOARD_WIDTH)

    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back_to_admin_panel_button'],
            callback_data="show_admin_panel"
        )
    )
    return builder.as_markup()

def get_back_to_admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой "Назад в админ-панель"."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back_to_admin_panel'],
            callback_data="show_admin_panel"
        )
    )
    return builder.as_markup()