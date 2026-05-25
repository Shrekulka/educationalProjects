# inter_exchange_arbitrage_bot/src/bot/handlers/admin_handlers.py

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.filters import AdminFilter
from src.bot.keyboards.admin_keyboards import (
    get_admin_panel_keyboard,
    get_back_to_admin_panel_keyboard,
    get_exchange_selection_keyboard,
    get_excluded_pairs_keyboard, get_cache_stats_keyboard
)
from src.bot.keyboards.pagination_keyboard import get_pagination_keyboard
from src.bot.logic.admin_logic import format_cache_stats_report
from src.bot.states.user_states import AdminState
from src.constants.telegram_constants import (
    CALLBACK_PAGE_SWITCH, CALLBACK_SHOW_FULL_LIST, CALLBACK_ANSWER_CACHE_TIME,
    PAGINATION_CALLBACK_PARTS_COUNT, DEFAULT_PAGE_SIZE
)
from src.constants.trading_constants import TRADING_PAIR_PATTERN, MAX_SYMBOL_LENGTH
from src.lexicon.lexicon_ru import LEXICON_RU
from src.services.scanner_api_service import (
    get_cache_stats_from_api,
    exclude_pair_via_api,
    include_pair_via_api,
    get_excluded_pairs_from_api
)
from src.utils import get_configured_exchanges
from src.utils.api_error_handler import handle_api_errors
from src.utils.chat_actions import safe_edit_text
from src.utils.logger import logger

router = Router()


@router.callback_query(F.data == "show_admin_panel", AdminFilter())
async def show_admin_panel(callback: CallbackQuery, state: FSMContext):
    """Точка входа в административную панель."""
    await state.clear()
    await safe_edit_text(
        message=callback.message,
        text=LEXICON_RU['admin_panel_header'],
        reply_markup=get_admin_panel_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "admin:pair_status", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_admin_panel_keyboard)
async def get_cache_statistics(callback: CallbackQuery, state: FSMContext):
    """Показывает статистику кэша, делегируя форматирование отчета."""
    await state.clear()
    await callback.answer(cache_time=CALLBACK_ANSWER_CACHE_TIME)
    stats = await get_cache_stats_from_api()
    if not stats: return
    if "message" in stats:
        await safe_edit_text(callback.message, stats["message"], get_admin_panel_keyboard())
        return

    report_text = format_cache_stats_report(stats)

    await safe_edit_text(
        message=callback.message,
        text=report_text,
        reply_markup=get_cache_stats_keyboard(stats),
        log_text=LEXICON_RU['log_cache_stats_updated']
    )


@router.callback_query(F.data.startswith(CALLBACK_SHOW_FULL_LIST), AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_admin_panel_keyboard)
async def show_full_pair_list(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик для отображения полного списка пар с пагинацией.
    """
    await callback.answer()

    try:
        parts = callback.data.split(":")
        if len(parts) != PAGINATION_CALLBACK_PARTS_COUNT: raise ValueError("Invalid callback format")
        _, exchange, status_type, page_str = parts
        page = int(page_str)
        if page < 0: raise ValueError("Invalid page number")
    except ValueError as e:
        logger.warning(LEXICON_RU['log_invalid_callback_data'].format(callback_data=callback.data, error=e))
        await safe_edit_text(callback.message, LEXICON_RU['error_invalid_callback_format'], get_admin_panel_keyboard())
        return

    stats = await get_cache_stats_from_api()
    if not stats or exchange not in stats:
        await safe_edit_text(callback.message, LEXICON_RU['error_data_outdated'], get_admin_panel_keyboard())
        return

    list_key = f"{status_type}_list"
    full_list = stats[exchange].get(list_key, [])

    if not full_list:
        # Динамическое получение текста статуса из лексикона
        status_text_key = f'status_type_{status_type}'  # Например, 'status_type_temp_unavailable'
        status_text = LEXICON_RU.get(status_text_key, "неизвестных")
        await safe_edit_text(
            callback.message,
            LEXICON_RU['info_list_is_empty'].format(status_text=status_text, exchange=exchange.capitalize()),
            get_admin_panel_keyboard()
        )
        return

    total_pages = (len(full_list) + DEFAULT_PAGE_SIZE - 1) // DEFAULT_PAGE_SIZE
    if page >= total_pages:
        page = total_pages - 1

    start = page * DEFAULT_PAGE_SIZE
    end = start + DEFAULT_PAGE_SIZE
    page_items = full_list[start:end]

    # Динамическое получение заголовка из лексикона
    header_key = f'header_{status_type}'  # Например, 'header_temp_unavailable'
    status_rus = LEXICON_RU.get(header_key, "Список пар")
    header = LEXICON_RU['pair_list_header'].format(
        status_rus=status_rus, exchange=exchange.capitalize(),
        page=page + 1, total_pages=total_pages, total_items=len(full_list)
    )

    page_text = "\n".join([f"• <code>{item}</code>" for item in page_items])
    builder = InlineKeyboardBuilder()

    if total_pages > 1:
        pagination_kb = get_pagination_keyboard(
            current_page=page, total_pages=total_pages,
            callback_prefix=f"{CALLBACK_PAGE_SWITCH}:{exchange}:{status_type}"
        )
        builder.attach(InlineKeyboardBuilder.from_markup(pagination_kb))

    builder.row(
        InlineKeyboardButton(text=LEXICON_RU['back_to_statistics_button'], callback_data="admin:pair_status"))

    await state.set_state(AdminState.viewing_pair_list)
    await safe_edit_text(callback.message, header + page_text, builder.as_markup())


@router.callback_query(F.data.startswith(CALLBACK_PAGE_SWITCH), AdminState.viewing_pair_list, AdminFilter())
async def switch_pair_list_page(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик переключения страниц в списке пар.
    Перенаправляет на основной обработчик для избежания дублирования кода.
    """
    # Заменяем префикс callback_data и перенаправляем
    original_callback_data = callback.data.replace(CALLBACK_PAGE_SWITCH, CALLBACK_SHOW_FULL_LIST, 1)
    callback.data = original_callback_data
    await show_full_pair_list(callback, state)


# =======================================================
# === ИСКЛЮЧЕНИЕ ПАРЫ (МНОГОШАГОВЫЙ СЦЕНАРИЙ) ===
# =======================================================

@router.callback_query(F.data == "admin:exclude_pair_start", AdminFilter())
async def start_excluding_pair(callback: CallbackQuery, state: FSMContext):
    """Начинает процесс исключения пары - выбор биржи."""
    exchanges = get_configured_exchanges()
    await state.set_state(AdminState.choosing_exchange_for_exclude)
    await safe_edit_text(
        message=callback.message,
        text=LEXICON_RU['prompt_exclude_pair'],
        reply_markup=get_exchange_selection_keyboard(exchanges, action='exclude')
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:exclude_exchange:"), AdminFilter())
async def choose_exchange_to_exclude(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор биржи для исключения пары."""
    exchange = callback.data.split(":")[2]
    await state.update_data(selected_exchange=exchange)
    await state.set_state(AdminState.waiting_for_symbol_to_exclude)
    await safe_edit_text(
        message=callback.message,
        text=LEXICON_RU['prompt_enter_symbol_exclude'],
        reply_markup=get_back_to_admin_panel_keyboard()
    )
    await callback.answer()


@router.message(AdminState.waiting_for_symbol_to_exclude, F.text, AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_admin_panel_keyboard)
async def process_pair_to_exclude(message: Message, state: FSMContext):
    """
    Обрабатывает ввод символа пары для исключения с предварительной
    проверкой, не исключена ли пара уже.
    """
    data = await state.get_data()
    exchange = data.get('selected_exchange')
    symbol = message.text.strip().upper()

    # Блок валидации остается без изменений
    if not exchange:
        await message.answer(LEXICON_RU['error_no_exchange_selected'], reply_markup=get_admin_panel_keyboard())
        await state.clear()
        return
    if not symbol:
        await message.answer(LEXICON_RU['error_empty_symbol'], reply_markup=get_back_to_admin_panel_keyboard())
        return
    if not TRADING_PAIR_PATTERN.match(symbol):
        await message.answer(LEXICON_RU['error_invalid_symbol_format'], reply_markup=get_back_to_admin_panel_keyboard())
        return
    if len(symbol) > MAX_SYMBOL_LENGTH:
        await message.answer(LEXICON_RU['error_symbol_too_long'].format(max_length=MAX_SYMBOL_LENGTH),
                             reply_markup=get_back_to_admin_panel_keyboard())
        return

    # 1. Сначала получаем текущий список исключенных пар
    excluded_pairs = await get_excluded_pairs_from_api()
    if excluded_pairs is not None:
        # 2. Проверяем, есть ли наша биржа в списке и есть ли наша пара для этой биржи
        if exchange in excluded_pairs and symbol in excluded_pairs[exchange]:
            # 3. Если пара уже исключена, сообщаем об этом пользователю и выходим
            await message.answer(
                text=LEXICON_RU['info_pair_already_excluded'].format(symbol=symbol, exchange=exchange),
                reply_markup=get_admin_panel_keyboard()
            )
            await state.clear()
            return

    # Если проверки пройдены, отправляем запрос на исключение
    success = await exclude_pair_via_api(exchange, symbol)
    if success:
        response_text = LEXICON_RU['exclude_success'].format(symbol=symbol, exchange=exchange)
        logger.info(f"Пара {symbol} исключена администратором на {exchange}")
    else:
        response_text = LEXICON_RU['error_api_negative_response'].format(action="исключить пару")
        logger.warning(f"Ошибка исключения пары {symbol} на {exchange}")

    await message.answer(text=response_text, reply_markup=get_admin_panel_keyboard())
    await state.clear()


# =======================================================
# === ВКЛЮЧЕНИЕ ПАРЫ - НОВАЯ КНОПОЧНАЯ ЛОГИКА ===
# =======================================================

@router.callback_query(F.data == "admin:include_pair_start", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_admin_panel_keyboard)
async def start_including_pair(callback: CallbackQuery):
    await callback.answer()
    excluded_pairs = await get_excluded_pairs_from_api()
    if not excluded_pairs or not any(excluded_pairs.values()):
        text, reply_markup = LEXICON_RU['info_no_excluded_pairs'], get_admin_panel_keyboard()
    else:
        text, reply_markup = LEXICON_RU['include_pair_header'], get_excluded_pairs_keyboard(excluded_pairs)
    await safe_edit_text(message=callback.message, text=text, reply_markup=reply_markup)


@router.callback_query(F.data.startswith("admin:include_pair:"), AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_admin_panel_keyboard)
async def include_pair_from_button(callback: CallbackQuery):
    await callback.answer()
    try:
        _, _, exchange, symbol = callback.data.split(":")
        success = await include_pair_via_api(exchange, symbol)
        if success:
            text = LEXICON_RU['include_success_formatted'].format(symbol=symbol, exchange=exchange.capitalize())
        else:
            action_text = LEXICON_RU['action_exclude_pair']
            text = LEXICON_RU['error_api_negative_response'].format(action=action_text)
    except ValueError as e:
        logger.error(LEXICON_RU['log_callback_parse_error'].format(error=e, callback_data=callback.data))
        text = LEXICON_RU['error_internal']

    await safe_edit_text(message=callback.message, text=text, reply_markup=get_admin_panel_keyboard())


# =======================================================
# === ОБРАБОТЧИКИ DUMMY CALLBACKS ===
# =======================================================

@router.callback_query(F.data.in_({"admin:no_excluded_pairs", "admin:exchange_header"}), AdminFilter())
async def handle_dummy_callbacks(callback: CallbackQuery):
    await callback.answer(LEXICON_RU['info_informational_button'], show_alert=False)
