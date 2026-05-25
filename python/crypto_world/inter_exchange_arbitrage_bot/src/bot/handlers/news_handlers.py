# inter_exchange_arbitrage_bot/src/bot/handlers/news_handlers.py
import re
from typing import List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards.coin_keyboards import get_coin_selection_keyboard
from src.bot.keyboards.news_keyboards import get_news_menu_keyboard, get_back_to_news_menu_keyboard
from src.bot.logic.news_logic import (get_user_favorite_coins, process_news_response,
                                      send_error_and_return_to_menu)
from src.bot.states.user_states import NewsState
from src.constants.telegram_constants import (
    NEWS_COIN_SELECTION_TOGGLE_PREFIX, NEWS_COIN_SELECTION_PAGE_PREFIX,
    NEWS_COIN_SELECTION_CLEAR_SEARCH_PREFIX, NEWS_COIN_SELECTION_CONFIRM_PREFIX,
    NEWS_COIN_SELECTION_CANCEL_PREFIX
)
from src.lexicon import LEXICON_RU
from src.services import scanner_api_service
from src.utils.api_error_handler import handle_api_errors
from src.utils.chat_actions import safe_edit_text
from src.utils.logger import logger

router = Router()


@router.callback_query(F.data == "news_menu")
async def process_news_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit_text(callback.message, LEXICON_RU['news_menu_header'], reply_markup=get_news_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("news_fetch:"))
async def process_fetch_news_request(callback: CallbackQuery):
    # Отправляем сообщение о процессе загрузки. Это сообщение будет редактироваться или удаляться.
    progress_message = await safe_edit_text(callback.message, LEXICON_RU['getting_news_progress'], reply_markup=None)
    await callback.answer()

    try:
        selection = callback.data.split(":", 1)[1]
    except IndexError:
        logger.error(f"Некорректный формат callback_data: {callback.data}")
        await send_error_and_return_to_menu(progress_message,
                                            "⚠️ Ошибка обработки запроса.")  # Передаем progress_message
        return

    api_response = None
    coins_for_report = []

    try:
        if selection == 'mode_favorites':
            coins_for_report = await get_user_favorite_coins(callback.from_user.id)
            if not coins_for_report:
                await send_error_and_return_to_menu(progress_message,
                                                    LEXICON_RU['news_no_favorites'])  # Передаем progress_message
                return
            api_response = await scanner_api_service.get_news_from_api(coins_for_report)

        elif selection == 'mode_top10':
            api_response = await scanner_api_service.get_news_top10_from_api()
            if api_response:
                coins_for_report = api_response.get("processed_coins",
                                                    ["Топ-10"])
            else:
                coins_for_report = ["Топ-10"]

        else:
            logger.warning(f"Неизвестный режим выбора новостей: {selection}")
            await send_error_and_return_to_menu(progress_message, "⚠️ Неизвестный режим.")  # Передаем progress_message
            return

        # Удаляем сообщение о прогрессе перед выводом новостей
        try:
            await progress_message.delete()
        except Exception:
            pass

        await process_news_response(callback.message, api_response)

    except Exception as e:
        logger.error(f"Критическая ошибка в хендлере новостей ({selection}): {e}", exc_info=True)
        try:
            await progress_message.delete()
        except Exception:
            pass
        await send_error_and_return_to_menu(callback.message,
                                            LEXICON_RU['news_api_error'])  # Используем original_message для ответов


# НОВЫЙ ХЕНДЛЕР для кнопки "Выбрать монеты вручную"
@router.callback_query(F.data == "news_select_manual")
@handle_api_errors(fallback_keyboard_func=get_news_menu_keyboard)  # Декоратор для обработки ошибок API
async def start_news_coin_selection(callback: CallbackQuery, state: FSMContext):
    """
    Инициирует процесс выбора монет для получения новостей,
    используя общий UI для выбора монет.
    """
    # Сначала редактируем сообщение пользователя, чтобы показать прогресс
    await safe_edit_text(
        callback.message,
        LEXICON_RU['getting_news_progress']
    )
    await callback.answer()

    # Получаем все доступные монеты через API
    api_response = await scanner_api_service.get_all_assets_from_api()

    if api_response is None:
        await safe_edit_text(
            callback.message,
            "❌ Не удалось загрузить список монет с сервера API.",
            reply_markup=get_back_to_news_menu_keyboard()
        )
        return

    all_coins = sorted(list(set(api_response.get("assets", []))))  # Уникальные и отсортированные
    successful_exchanges = api_response.get("sources", [])

    if not all_coins or not successful_exchanges:
        await safe_edit_text(
            callback.message,
            "❌ API не вернуло список монет.\nВозможно, нет активных бирж для загрузки данных.",
            reply_markup=get_back_to_news_menu_keyboard()
        )
        return

    logger.info(
        f"✅ Загружено {len(all_coins)} уникальных монет с {len(successful_exchanges)} бирж для выбора новостей.")

    await state.set_state(NewsState.selecting_coins_for_news)  # <-- ИСПОЛЬЗУЕМ НОВОЕ НАЗВАНИЕ
    await state.update_data(
        all_coins=all_coins,
        selected_coins=[],
        current_page=0,
        search_query=None,
        menu_message_id=callback.message.message_id,  # Сохраняем ID сообщения для редактирования
        source_exchanges=successful_exchanges
    )

    # Используем универсальную клавиатуру выбора монет
    keyboard = get_coin_selection_keyboard(
        all_coins=all_coins,
        selected_coins=[],
        toggle_prefix=NEWS_COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=NEWS_COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=NEWS_COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=NEWS_COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data=NEWS_COIN_SELECTION_CANCEL_PREFIX,
        confirm_button_text=LEXICON_RU['select_button']
    )

    exchanges_text = ", ".join([ex.capitalize() for ex in successful_exchanges])
    await safe_edit_text(
        callback.message,
        LEXICON_RU['select_coins_for_news_header'].format(exchanges_text=exchanges_text),
        reply_markup=keyboard
    )


@router.message(NewsState.selecting_coins_for_news, F.text)
async def handle_news_coin_search(message: Message, state: FSMContext):
    """
    ФИНАЛЬНАЯ ВЕРСИЯ: Ловит текстовое сообщение, разделяет его на несколько
    тикеров (по пробелам или запятым) и ищет их все.
    """
    await message.delete()

    # ✅ ИСПРАВЛЕНИЕ: Разбиваем ввод пользователя на отдельные тикеры
    # re.split() отлично справляется с запятыми, пробелами и их комбинациями
    search_terms = [term for term in re.split(r'[\s,]+', message.text.strip()) if term]

    if not search_terms:
        return

    # Сохраняем и оригинальную строку, и список для FSM
    original_query_str = ", ".join(search_terms)
    await state.update_data(search_query=original_query_str, search_terms=search_terms, current_page=0)

    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if not menu_message_id:
        return

    # ✅ ИСПРАВЛЕНИЕ: Передаем в клавиатуру СПИСОК тикеров
    keyboard = get_coin_selection_keyboard(
        all_coins=data.get("all_coins", []),
        selected_coins=data.get("selected_coins", []),
        current_page=0,
        search_query=data.get("search_terms"),  # Передаем список
        toggle_prefix=NEWS_COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=NEWS_COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=NEWS_COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=NEWS_COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data=NEWS_COIN_SELECTION_CANCEL_PREFIX,
        confirm_button_text=LEXICON_RU['select_button']
    )

    # Используем оригинальную строку для отображения пользователю
    await message.bot.edit_message_text(
        text=LEXICON_RU['news_manual_selection_search_results'].format(original_query_str),
        chat_id=message.chat.id,
        message_id=menu_message_id,
        reply_markup=keyboard
    )


# @router.message(NewsState.selecting_coins_for_news, F.text)
# async def handle_news_coin_search(message: Message, state: FSMContext):
#     """
#     Ловит текстовое сообщение в состоянии выбора монет для новостей и использует его для поиска.
#     """
#     search_query = message.text.strip()
#     await message.delete()
#
#     if not search_query:
#         return
#
#     data = await state.get_data()
#     menu_message_id = data.get('menu_message_id')
#     if not menu_message_id:
#         return
#
#     await state.update_data(search_query=search_query, current_page=0)
#
#     keyboard = get_coin_selection_keyboard(
#         all_coins=data.get("all_coins", []),
#         selected_coins=data.get("selected_coins", []),
#         current_page=0,
#         search_query=search_query,
#         toggle_prefix=NEWS_COIN_SELECTION_TOGGLE_PREFIX,
#         page_prefix=NEWS_COIN_SELECTION_PAGE_PREFIX,
#         clear_search_callback_data=NEWS_COIN_SELECTION_CLEAR_SEARCH_PREFIX,
#         confirm_callback_data=NEWS_COIN_SELECTION_CONFIRM_PREFIX,
#         cancel_callback_data=NEWS_COIN_SELECTION_CANCEL_PREFIX
#     )
#
#     await message.bot.edit_message_text(
#         text=LEXICON_RU['news_manual_selection_search_results'].format(search_query),
#         chat_id=message.chat.id,
#         message_id=menu_message_id,
#         reply_markup=keyboard
#     )


@router.callback_query(F.data == NEWS_COIN_SELECTION_CLEAR_SEARCH_PREFIX,
                       NewsState.selecting_coins_for_news)
async def clear_news_coin_search(callback: CallbackQuery, state: FSMContext):
    """Сбрасывает поисковый запрос и показывает полный список монет для новостей."""
    await callback.answer()
    data = await state.get_data()

    await state.update_data(search_query=None, current_page=0)

    keyboard = get_coin_selection_keyboard(
        all_coins=data.get("all_coins", []),
        selected_coins=data.get("selected_coins", []),
        current_page=0,
        search_query=None,
        toggle_prefix=NEWS_COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=NEWS_COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=NEWS_COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=NEWS_COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data=NEWS_COIN_SELECTION_CANCEL_PREFIX,
        confirm_button_text=LEXICON_RU['select_button']
    )

    exchanges_text = ", ".join([ex.capitalize() for ex in data.get("source_exchanges", [])])
    await callback.message.edit_text(
        LEXICON_RU['select_coins_for_news_header'].format(exchanges_text=exchanges_text),
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith(f"{NEWS_COIN_SELECTION_PAGE_PREFIX}:"),
                       NewsState.selecting_coins_for_news)
async def handle_news_coin_page_switch(callback: CallbackQuery, state: FSMContext):
    """Переключает страницы выбора монет для новостей, учитывая текущий поисковый запрос."""
    await callback.answer()
    page = int(callback.data.split(":")[1])
    await state.update_data(current_page=page)
    data = await state.get_data()

    keyboard = get_coin_selection_keyboard(
        all_coins=data.get("all_coins", []),
        selected_coins=data.get("selected_coins", []),
        current_page=page,
        search_query=data.get("search_terms"),
        toggle_prefix=NEWS_COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=NEWS_COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=NEWS_COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=NEWS_COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data=NEWS_COIN_SELECTION_CANCEL_PREFIX,
        confirm_button_text=LEXICON_RU['select_button']
    )

    text_to_send = LEXICON_RU['news_manual_selection_search_results'].format(data['search_query']) if data.get(
        'search_query') \
        else LEXICON_RU['select_coins_for_news_header'].format(
        exchanges_text=", ".join([ex.capitalize() for ex in data.get("source_exchanges", [])]))

    await callback.message.edit_text(text_to_send, reply_markup=keyboard)


@router.callback_query(F.data.startswith(f"{NEWS_COIN_SELECTION_TOGGLE_PREFIX}:"),
                       NewsState.selecting_coins_for_news)
async def handle_news_toggle_coin(callback: CallbackQuery, state: FSMContext):
    """Выбирает/снимает выбор с монеты для новостей, сохраняя состояние поиска."""
    await callback.answer()
    _, coin_to_toggle, page_str = callback.data.split(":")
    page = int(page_str)

    data = await state.get_data()
    selected_coins = data.get("selected_coins", [])

    if coin_to_toggle in selected_coins:
        selected_coins.remove(coin_to_toggle)
    else:
        selected_coins.append(coin_to_toggle)

    await state.update_data(selected_coins=selected_coins)

    keyboard = get_coin_selection_keyboard(
        all_coins=data.get("all_coins", []),
        selected_coins=selected_coins,
        current_page=page,
        search_query=data.get("search_terms"),
        toggle_prefix=NEWS_COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=NEWS_COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=NEWS_COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=NEWS_COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data=NEWS_COIN_SELECTION_CANCEL_PREFIX,
        confirm_button_text=LEXICON_RU['select_button']
    )
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == NEWS_COIN_SELECTION_CONFIRM_PREFIX,
                       NewsState.selecting_coins_for_news)
async def confirm_news_coin_selection(callback: CallbackQuery, state: FSMContext):
    """
    Подтверждает выбор монет для новостей, получает новости и отображает их.
    """
    await callback.answer()
    data = await state.get_data()
    selected_coins: List[str] = data.get("selected_coins", [])

    if not selected_coins:
        await callback.answer("Вы ничего не выбрали!", show_alert=True)
        return

    await state.clear()

    # УЛУЧШЕНИЕ 1: Работаем с одним и тем же объектом сообщения для статуса/ошибок.
    message_to_process = callback.message

    # Редактируем исходное сообщение, чтобы показать прогресс.
    await safe_edit_text(message_to_process, LEXICON_RU['getting_news_progress'], reply_markup=None)

    try:
        api_response = await scanner_api_service.get_news_from_api(selected_coins)

        # УЛУЧШЕНИЕ 2: Явная и безопасная проверка ответа от API.
        if api_response is None or not isinstance(api_response, dict):
            logger.error("scanner_api_service.get_news_from_api вернул None или некорректный тип, обработка прервана.")
            await send_error_and_return_to_menu(message_to_process, LEXICON_RU['news_api_error'])
            return

        # УЛУЧШЕНИЕ 3: Удаляем сообщение о прогрессе перед отправкой новостей для лучшего UX.
        try:
            await message_to_process.delete()
        except Exception:
            pass  # Игнорируем ошибку, если сообщение уже удалено

        # Передаем оригинальное сообщение для отправки НОВЫХ сообщений с результатами
        await process_news_response(callback.message, api_response)

    except Exception as e:
        logger.error(f"Ошибка при получении новостей вручную (выбор): {e}", exc_info=True)
        # УЛУЧШЕНИЕ 4: Гарантируем обработку ошибок через тот же объект сообщения.
        await send_error_and_return_to_menu(message_to_process, LEXICON_RU['news_api_error'])


@router.callback_query(F.data == NEWS_COIN_SELECTION_CANCEL_PREFIX,
                       NewsState.selecting_coins_for_news)
async def cancel_news_coin_selection(callback: CallbackQuery, state: FSMContext):
    """
    Отмена выбора монет для новостей, возвращает в основное меню новостей.
    """
    await state.clear()
    await safe_edit_text(callback.message, LEXICON_RU['news_menu_header'], reply_markup=get_news_menu_keyboard())
    await callback.answer(LEXICON_RU['cancel_button_pressed'])
