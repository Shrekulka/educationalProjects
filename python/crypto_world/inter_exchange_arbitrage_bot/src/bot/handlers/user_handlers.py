# inter_exchange_arbitrage_bot/src/bot/handlers/user_handlers.py

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.bot.filters.admin_filter import AdminFilter
from src.bot.keyboards.main_menu_keyboard import get_main_menu_inline_keyboard
from src.bot.keyboards.density_screener_keyboards import get_density_coin_selection_keyboard
from src.bot.keyboards.report_keyboards import get_report_menu_keyboard
from src.bot.logic.balance_logic import process_and_send_balance
from src.bot.logic.density_logic import show_density_screener_menu, start_density_scan
from src.bot.logic.menu_logic import show_main_menu
from src.bot.states.user_states import DensityScreenerState, ReportState
from src.constants.system_constants import SYSTEM_STATE_MAIN_MENU_MESSAGE_ID
from src.constants.telegram_constants import ALLOWED_REPORT_HOURS, CALLBACK_GET_REPORT
from src.constants.trading_constants import DENSITY_SCREENER_CONFIG, STABLE_COINS, PRIMARY_QUOTE_CURRENCY
from src.core.database import async_session_factory
from src.lexicon.lexicon_ru import LEXICON_RU
from src.models.system_models import SystemState
from src.models.user_models import UserCoin
from src.services.service_manager import service_manager
from src.services.arbitrage_report_service import ArbitrageReportService
from src.services.data_enricher_service import data_enricher
from src.services.report_formatter import ReportFormatter
from src.utils.chat_actions import show_typing_status, safe_edit_text
from src.utils.api_error_handler import handle_api_errors
from src.utils.logger import logger

router = Router()


@router.message(CommandStart(), AdminFilter())
async def handle_start_admin(message: Message):
    """
    Отправляет приветствие и главное меню, а также сохраняет ID этого
    сообщения для последующего редактирования.
    """
    logger.info(f"Администратор {message.from_user.id} запустил бота.")

    # 1. Получаем текст и клавиатуру
    from src.bot.logic.greeting_logic import get_dynamic_greeting
    from src.lexicon.lexicon_ru import LEXICON_RU
    dynamic_greeting = get_dynamic_greeting(message.from_user.id)
    greeting_part = f"👋 {dynamic_greeting}, {message.from_user.first_name}!\n\n"
    main_text_part = LEXICON_RU['main_menu_greeting']
    text = greeting_part + main_text_part
    keyboard = get_main_menu_inline_keyboard()

    # 2. Отправляем сообщение и получаем его объект
    sent_message = await message.answer(text, reply_markup=keyboard)

    # 3. Сохраняем ID сообщения в базу данных
    admin_id = message.from_user.id
    message_id_key = SYSTEM_STATE_MAIN_MENU_MESSAGE_ID.format(admin_id=admin_id)

    try:
        async with async_session_factory() as session:
            # Используем "upsert" для атомарного создания или обновления записи
            stmt = insert(SystemState).values(key=message_id_key, value=str(sent_message.message_id))
            stmt = stmt.on_conflict_do_update(
                index_elements=['key'],
                set_={'value': stmt.excluded.value}
            )
            await session.execute(stmt)
            await session.commit()
            logger.info(f"Сохранен/обновлен message_id ({sent_message.message_id}) для админа {admin_id}")
    except Exception as e:
        logger.error(f"Не удалось сохранить message_id для админа {admin_id}: {e}")


@router.message(CommandStart())
async def handle_start_unknown(message: Message):
    logger.warning(
        f"Неавторизованный пользователь {message.from_user.id} ({message.from_user.username}) запустил бота.")
    await message.answer("❌ Доступ запрещен. Этот бот предназначен для личного использования.")


@router.callback_query(F.data.startswith("show_balance"), AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)
async def balance_mode_handler(callback: CallbackQuery, bot: Bot):
    """Точка входа в меню баланса и переключатель режимов."""
    await callback.answer()
    mode = callback.data.split(":")[-1] if ":" in callback.data else "tracked"
    await process_and_send_balance(callback, mode, bot)


@router.callback_query(F.data.startswith("refresh_balance"), AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)
async def refresh_balance_handler(callback: CallbackQuery, bot: Bot):
    """Обновляет баланс в текущем режиме."""
    await callback.answer(text=LEXICON_RU['refresh_button'], cache_time=1)
    mode = callback.data.split(":")[-1]
    await process_and_send_balance(callback, mode, bot)


@router.callback_query(F.data == "show_report_menu", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)
async def show_report_menu_handler(callback: CallbackQuery, state: FSMContext):
    """Показывает меню выбора отчетов с динамическим заголовком."""
    await state.clear()
    report_period_hours = next(iter(ALLOWED_REPORT_HOURS))
    text = LEXICON_RU['report_menu_header'].format(hours=report_period_hours)
    reply_markup = get_report_menu_keyboard(hours=report_period_hours)
    await safe_edit_text(message=callback.message, text=text, reply_markup=reply_markup)
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_GET_REPORT), AdminFilter())
async def get_report_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Генерирует отчет с валидацией и очисткой старых сообщений."""
    await callback.answer("⏳ Формирую отчет...")
    user_id = callback.from_user.id

    try:
        _, report_type, hours_str = callback.data.split(":")
        hours_back = int(hours_str)
        if hours_back not in ALLOWED_REPORT_HOURS:
            raise ValueError(f"Disallowed hours value: {hours_back}")
    except ValueError as e:
        logger.warning(f"Некорректный callback для отчета: {callback.data}. Ошибка: {e}")
        await callback.answer("❌ Ошибка: Некорректный запрос.", show_alert=True)
        return

    try:
        current_data = await state.get_data()
        old_message_ids = current_data.get('report_message_ids', [])
        if old_message_ids:
            await callback.message.edit_text("⏳ Обновляю отчет...")
            for msg_id in old_message_ids:
                if msg_id != callback.message.message_id:
                    try:
                        await bot.delete_message(user_id, msg_id)
                    except Exception:
                        pass
    finally:
        await state.clear()

    async with show_typing_status(chat_id=user_id, bot=bot):
        report_service = ArbitrageReportService()
        if report_type == "summary":
            report_data = await report_service.get_summary_report(user_id, hours_back)
            report_text = ReportFormatter.format_summary_report(report_data)
            await safe_edit_text(callback.message, report_text, get_report_menu_keyboard(hours_back))
        elif report_type == "detailed":
            report_data = await report_service.get_detailed_attempts_report(user_id, hours_back)
            report_messages = ReportFormatter.format_detailed_arbitrage_report(report_data)
            message_ids_to_track = []
            for i, msg_text in enumerate(report_messages):
                is_last = (i == len(report_messages) - 1)
                reply_markup = get_report_menu_keyboard(hours_back) if is_last else None
                if i == 0:
                    msg = await callback.message.edit_text(text=msg_text, reply_markup=reply_markup)
                else:
                    msg = await callback.message.answer(text=msg_text, reply_markup=reply_markup)
                message_ids_to_track.append(msg.message_id)
            if message_ids_to_track:
                await state.set_state(ReportState.viewing)
                await state.update_data(report_message_ids=message_ids_to_track)


# =======================================================
# === 🛡️ ЛОГИКА ДЛЯ СКРИНЕРА ПЛОТНОСТЕЙ 🛡️ ========
# =======================================================

@router.callback_query(F.data == "show_density_screener", AdminFilter())
async def show_density_screener_menu_handler(callback: CallbackQuery, state: FSMContext):
    """Показывает подменю скринера плотностей."""
    await callback.answer()
    await show_density_screener_menu(callback.message, state)


@router.callback_query(F.data == "density:scan_top_100", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)
async def handle_scan_top_100(callback: CallbackQuery):
    """Запускает сканирование для топ-N монет из конфига."""
    limit = DENSITY_SCREENER_CONFIG['TOP_COINS_BY_CAP_LIMIT']
    await safe_edit_text(message=callback.message,
                         text=LEXICON_RU['density_screener_loading_top_100'].replace("100", str(limit)))
    await callback.answer()

    top_coins = await data_enricher.get_top_coins_by_market_cap(limit=limit)
    if not top_coins:
        await safe_edit_text(callback.message, LEXICON_RU['density_screener_scan_failed_assets'],
                             get_main_menu_inline_keyboard())
        return

    symbols_to_scan = [f"{coin}/{PRIMARY_QUOTE_CURRENCY}" for coin in top_coins if coin.upper() not in STABLE_COINS]
    await start_density_scan(callback.message, symbols_to_scan)


@router.callback_query(F.data == "density:scan_favorites", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)
async def handle_scan_favorites(callback: CallbackQuery):
    """Запускает сканирование для избранных монет."""
    await safe_edit_text(message=callback.message, text=LEXICON_RU['density_screener_loading_favorites'])
    await callback.answer()

    async with async_session_factory() as session:
        stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == callback.from_user.id)
        fav_coins = (await session.execute(stmt)).scalars().all()

    if not fav_coins:
        await safe_edit_text(callback.message, LEXICON_RU['density_screener_no_favorites'],
                             get_main_menu_inline_keyboard())
        return

    symbols_to_scan = [f"{coin}/USDT" for coin in fav_coins if coin.upper() not in STABLE_COINS]
    await start_density_scan(callback.message, symbols_to_scan)


@router.callback_query(F.data == "density:select_custom", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)
async def handle_select_custom(callback: CallbackQuery, state: FSMContext):
    """Запускает процесс ручного выбора монет."""
    await safe_edit_text(callback.message, LEXICON_RU['density_screener_loading_all_assets'])
    await callback.answer()

    all_assets = service_manager.get_all_spot_assets_from_cache()
    if not all_assets:
        await safe_edit_text(callback.message, LEXICON_RU['density_screener_scan_failed_assets'],
                             get_main_menu_inline_keyboard())
        return

    coins_to_display = sorted([c for c in all_assets if c.upper() not in STABLE_COINS])

    await state.set_state(DensityScreenerState.selecting_coins)
    await state.update_data(all_coins=coins_to_display, selected_coins=[], current_page=0, search_query=None,
                            menu_message_id=callback.message.message_id)

    keyboard = get_density_coin_selection_keyboard(all_coins=coins_to_display, selected_coins=[])
    await safe_edit_text(callback.message, LEXICON_RU['density_screener_select_custom_header'], reply_markup=keyboard)


# --- Обработчики для меню ручного выбора монет СКРИНЕРА ---

@router.message(DensityScreenerState.selecting_coins, F.text, AdminFilter())
async def handle_density_coin_search(message: Message, state: FSMContext):
    search_query = message.text.strip()
    await message.delete()
    if not search_query: return
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if not menu_message_id: return
    await state.update_data(search_query=search_query, current_page=0)
    keyboard = get_density_coin_selection_keyboard(all_coins=data.get("all_coins", []),
                                                   selected_coins=data.get("selected_coins", []), current_page=0,
                                                   search_query=search_query)
    await message.bot.edit_message_text(text=f"🔎 <b>Результаты поиска по запросу монетки 🪙 «{search_query}»:</b>",
                                        chat_id=message.chat.id, message_id=menu_message_id, reply_markup=keyboard)


@router.callback_query(F.data.startswith("density:page:"), DensityScreenerState.selecting_coins, AdminFilter())
async def handle_density_page_switch(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    page = int(callback.data.split(":")[2])
    await state.update_data(current_page=page)
    data = await state.get_data()
    keyboard = get_density_coin_selection_keyboard(all_coins=data.get("all_coins", []),
                                                   selected_coins=data.get("selected_coins", []), current_page=page,
                                                   search_query=data.get("search_query"))
    text = f"🔎 <b>Результаты поиска по запросу монетки 🪙 «{data.get('search_query')}»:</b>" if data.get('search_query') else LEXICON_RU[
        'density_screener_select_custom_header']
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("density:toggle:"), DensityScreenerState.selecting_coins, AdminFilter())
async def handle_density_toggle_coin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    _, _, coin_to_toggle, page_str = callback.data.split(":")
    page = int(page_str)
    data = await state.get_data()
    selected_coins = data.get("selected_coins", [])
    if coin_to_toggle in selected_coins:
        selected_coins.remove(coin_to_toggle)
    else:
        selected_coins.append(coin_to_toggle)
    await state.update_data(selected_coins=selected_coins)
    keyboard = get_density_coin_selection_keyboard(all_coins=data.get("all_coins", []), selected_coins=selected_coins,
                                                   current_page=page, search_query=data.get("search_query"))
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == "density:confirm", DensityScreenerState.selecting_coins, AdminFilter())
async def handle_density_confirm_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    selected_coins = data.get("selected_coins", [])
    if not selected_coins:
        await callback.answer("Вы ничего не выбрали!", show_alert=True)
        return
    await state.clear()
    await safe_edit_text(callback.message, LEXICON_RU['density_screener_starting_scan'])
    symbols_to_scan = [f"{coin}/USDT" for coin in selected_coins]
    await start_density_scan(callback.message, symbols_to_scan)


@router.callback_query(F.data == "density:clear_search", DensityScreenerState.selecting_coins, AdminFilter())
async def handle_density_clear_search(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await state.update_data(search_query=None, current_page=0)
    keyboard = get_density_coin_selection_keyboard(all_coins=data.get("all_coins", []),
                                                   selected_coins=data.get("selected_coins", []), current_page=0,
                                                   search_query=None)
    await callback.message.edit_text(LEXICON_RU['density_screener_select_custom_header'], reply_markup=keyboard)


@router.callback_query(F.data == "show_density_screener", DensityScreenerState.selecting_coins, AdminFilter())
async def handle_density_cancel_selection(callback: CallbackQuery, state: FSMContext):
    """Возвращает в меню скринера из режима выбора."""
    await callback.answer()
    await show_density_screener_menu(callback.message, state)


@router.callback_query(F.data == "back_to_main_menu", AdminFilter())
async def back_to_main_menu_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await show_main_menu(callback.message, callback.from_user, edit=True)
    await callback.answer()
