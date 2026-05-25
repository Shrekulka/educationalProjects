# inter_exchange_arbitrage_bot/src/bot/handlers/settings_handlers.py
import asyncio
import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, delete, and_
from sqlalchemy.dialects.postgresql import insert

import src.core.state as app_state
from src.bot.handlers.user_handlers import AdminFilter
from src.bot.keyboards import get_coin_selection_keyboard, get_coin_removal_keyboard
from src.bot.keyboards.settings_keyboard import (get_scanner_settings_keyboard, get_settings_keyboard,
                                                 get_back_to_settings_keyboard)
from src.bot.logic.settings_logic import show_settings_menu
from src.bot.states.user_states import SettingsState
from src.constants.telegram_constants import (
    COIN_SELECTION_TOGGLE_PREFIX, COIN_SELECTION_PAGE_PREFIX,  # Импорт новых констант
    COIN_SELECTION_CLEAR_SEARCH_PREFIX, COIN_SELECTION_CONFIRM_PREFIX,  # Импорт новых констант
    # Импорт новой константы
)
from src.constants.trading_constants import (DEFAULT_TRADE_AMOUNT_USD, DEFAULT_PROFIT_THRESHOLD,
                                             MIN_PROFIT_THRESHOLD_PERCENT, MAX_PROFIT_THRESHOLD_PERCENT,
                                             MIN_EXCHANGES_FOR_ARBITRAGE)
from src.core.database import async_session_factory
from src.models.user_models import UserCoin
from src.models.user_settings import UserSetting
from src.services import scanner_api_service
from src.utils import logger
from src.utils.api_error_handler import handle_api_errors
from src.utils.chat_actions import safe_edit_text
from src.utils.helpers import validate_trade_amount, safe_get_numeric

router = Router()


@router.callback_query(F.data == "show_settings", AdminFilter())
async def show_settings_menu_handler(callback: CallbackQuery, state: FSMContext):
    await show_settings_menu(message=callback.message, state=state)
    await callback.answer()


@router.callback_query(F.data == "back_to_settings", AdminFilter())
async def back_to_settings_handler(callback: CallbackQuery, state: FSMContext):
    await show_settings_menu(message=callback.message, state=state)
    await callback.answer()


@router.callback_query(F.data == "show_my_coins", AdminFilter())
async def show_my_coins_handler(callback: CallbackQuery):
    """Показывает список отслеживаемых монет по нажатию кнопки."""
    async with async_session_factory() as session:
        stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == callback.from_user.id).order_by(
            UserCoin.coin_ticker)
        result = await session.execute(stmt)
        coins = result.scalars().all()

    if not coins:
        text = "У вас пока нет отслеживаемых монет. 😕"
    else:
        coin_list = "\n".join([f"• <code>{coin}</code>" for coin in coins])
        text = f"<b>✨ Ваши отслеживаемые монеты:</b>\n{coin_list}"

    await safe_edit_text(
        message=callback.message,
        text=text,
        reply_markup=get_back_to_settings_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "add_coin_start", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_settings_keyboard)
async def start_coin_selection(callback: CallbackQuery, state: FSMContext):
    """
    Получает список монет через API для добавления.
    Защищен от "холодного старта" декоратором @handle_api_errors.
    """
    await safe_edit_text(
        message=callback.message,
        text="⏳ Загружаю список всех доступных монет через API..."
    )
    await callback.answer()

    # 1. Получаем монеты, которые УЖЕ есть у пользователя (из БД, это правильно)
    async with async_session_factory() as session:
        stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == callback.from_user.id)
        user_coins_set = set((await session.execute(stmt)).scalars().all())

    # 2. Получаем ВСЕ доступные монеты через новый API-вызов
    # Декоратор @handle_api_errors уже проверил, что API готово
    api_response = await scanner_api_service.get_all_assets_from_api()

    # 3. Проверяем ответ от API
    if api_response is None:
        await safe_edit_text(
            message=callback.message,
            text="❌ Не удалось загрузить список монет с сервера API.",
            reply_markup=get_back_to_settings_keyboard()
        )
        return

    all_coins_set = set(api_response.get("assets", []))
    successful_exchanges = api_response.get("sources", [])

    if not all_coins_set or not successful_exchanges:
        await safe_edit_text(
            message=callback.message,
            text="❌ API не вернуло список монет.\nВозможно, нет активных бирж. Проверьте логи API.",
            reply_markup=get_back_to_settings_keyboard()
        )
        return

    # 4. Фильтруем монеты, которые уже добавлены у пользователя
    coins_to_display = sorted([coin for coin in all_coins_set if coin not in user_coins_set])

    logger.info(f"✅ Загружено {len(all_coins_set)} уникальных монет с {len(successful_exchanges)} бирж через API.")

    # 5. Обновляем состояние FSM и показываем клавиатуру (логика без изменений)
    await state.set_state(SettingsState.selecting_coins_to_add)
    await state.update_data(
        all_coins=coins_to_display,
        selected_coins=[],
        current_page=0,
        search_query=None,
        menu_message_id=callback.message.message_id,
        source_exchanges=successful_exchanges
    )

    # ИСПОЛЬЗУЕМ НОВЫЕ ПАРАМЕТРЫ для get_coin_selection_keyboard
    keyboard = get_coin_selection_keyboard(
        all_coins=coins_to_display,
        selected_coins=[],
        toggle_prefix=COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data="back_to_settings"  # Back to settings
    )
    exchanges_text = ", ".join([ex.capitalize() for ex in successful_exchanges])
    await safe_edit_text(
        message=callback.message,
        text="<b>Выберите монеты для добавления.</b>\n\n"
             f"<i>Данные загружены с бирж: {exchanges_text}</i>\n\n"
             "Вы можете переключать страницы или просто <b>отправить сообщение с названием монеты (тикер), чтобы найти её.</b>",
        reply_markup=keyboard
    )


@router.message(SettingsState.selecting_coins_to_add, F.text, AdminFilter())
async def handle_coin_search(message: Message, state: FSMContext):
    """
    ФИНАЛЬНАЯ ВЕРСИЯ: Ловит текстовое сообщение, разделяет его на несколько
    тикеров (по пробелам или запятым) и ищет их все.
    """
    await message.delete()

    # ✅ ИСПРАВЛЕНИЕ: Разбиваем ввод пользователя на отдельные тикеры
    search_terms = [term for term in re.split(r'[\s,]+', message.text.strip()) if term]

    if not search_terms:
        return

    # Сохраняем и оригинальную строку, и список для FSM
    original_query_str = ", ".join(term.upper() for term in search_terms)
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
        toggle_prefix=COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data="back_to_settings"
    )

    # Используем оригинальную строку для отображения пользователю
    await message.bot.edit_message_text(
        text=f"🔎 <b>Результаты поиска по запросу «{original_query_str}»:</b>\n\nВыберите монеты или введите новый запрос.",
        chat_id=message.chat.id,
        message_id=menu_message_id,
        reply_markup=keyboard
    )


# @router.message(SettingsState.selecting_coins_to_add, F.text, AdminFilter())
# async def handle_coin_search(message: Message, state: FSMContext):
#     """
#     Ловит текстовое сообщение в состоянии выбора монет и использует его для поиска.
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
#     # ИСПОЛЬЗУЕМ НОВЫЕ ПАРАМЕТРЫ для get_coin_selection_keyboard
#     keyboard = get_coin_selection_keyboard(
#         all_coins=data.get("all_coins", []),
#         selected_coins=data.get("selected_coins", []),
#         current_page=0,
#         search_query=search_query,
#         toggle_prefix=COIN_SELECTION_TOGGLE_PREFIX,
#         page_prefix=COIN_SELECTION_PAGE_PREFIX,
#         clear_search_callback_data=COIN_SELECTION_CLEAR_SEARCH_PREFIX,
#         confirm_callback_data=COIN_SELECTION_CONFIRM_PREFIX,
#         cancel_callback_data="back_to_settings"
#     )
#
#     await message.bot.edit_message_text(
#         text=f"🔎 <b>Результаты поиска по запросу «{search_query}»:</b>\n\nВыберите монеты или введите новый запрос.",
#         chat_id=message.chat.id,
#         message_id=menu_message_id,
#         reply_markup=keyboard
#     )


@router.callback_query(F.data == COIN_SELECTION_CLEAR_SEARCH_PREFIX, SettingsState.selecting_coins_to_add,
                       AdminFilter())
async def clear_coin_search(callback: CallbackQuery, state: FSMContext):
    """Сбрасывает поисковый запрос и показывает полный список монет."""
    await callback.answer()
    data = await state.get_data()

    await state.update_data(search_query=None, current_page=0)

    # ИСПОЛЬЗУЕМ НОВЫЕ ПАРАМЕТРЫ для get_coin_selection_keyboard
    keyboard = get_coin_selection_keyboard(
        all_coins=data.get("all_coins", []),
        selected_coins=data.get("selected_coins", []),
        current_page=0,
        search_query=None,
        toggle_prefix=COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data="back_to_settings"
    )

    await callback.message.edit_text(
        "<b>Выберите монеты для добавления.</b>\n\n"
        "Вы можете переключать страницы или просто <b>отправить сообщение с названием монеты (тикер), чтобы найти её.</b>",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith(f"{COIN_SELECTION_PAGE_PREFIX}:"), SettingsState.selecting_coins_to_add,
                       AdminFilter())
async def handle_coin_page_switch(callback: CallbackQuery, state: FSMContext):
    """Переключает страницы, учитывая текущий поисковый запрос."""
    await callback.answer()
    page = int(callback.data.split(":")[1])
    await state.update_data(current_page=page)
    data = await state.get_data()

    keyboard = get_coin_selection_keyboard(
        all_coins=data.get("all_coins", []),
        selected_coins=data.get("selected_coins", []),
        current_page=page,
        search_query=data.get("search_terms"),
        toggle_prefix=COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data="back_to_settings"
    )

    text = f"🔎 <b>Результаты поиска по запросу «{data.get('search_query')}»:</b>" if data.get(
        'search_query') else "<b>Выберите монеты для добавления.</b>"

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith(f"{COIN_SELECTION_TOGGLE_PREFIX}:"), SettingsState.selecting_coins_to_add,
                       AdminFilter())
async def handle_toggle_coin(callback: CallbackQuery, state: FSMContext):
    """Выбирает/снимает выбор с монеты, сохраняя состояние поиска."""
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

    # ИСПОЛЬЗУЕМ НОВЫЕ ПАРАМЕТРЫ для get_coin_selection_keyboard
    keyboard = get_coin_selection_keyboard(
        all_coins=data.get("all_coins", []),
        selected_coins=selected_coins,
        current_page=page,
        search_query=data.get("search_terms"),
        toggle_prefix=COIN_SELECTION_TOGGLE_PREFIX,
        page_prefix=COIN_SELECTION_PAGE_PREFIX,
        clear_search_callback_data=COIN_SELECTION_CLEAR_SEARCH_PREFIX,
        confirm_callback_data=COIN_SELECTION_CONFIRM_PREFIX,
        cancel_callback_data="back_to_settings"
    )
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == COIN_SELECTION_CONFIRM_PREFIX, AdminFilter())
async def confirm_coin_selection(callback: CallbackQuery, state: FSMContext):
    """Подтверждает выбор монет для добавления в избранное пользователя."""
    await callback.answer()
    data = await state.get_data()
    selected_coins = data.get("selected_coins", [])

    if not selected_coins:
        await callback.answer("Вы ничего не выбрали!", show_alert=True)
        return

    async with async_session_factory() as session:
        coins_to_insert = [
            {"user_id": callback.from_user.id, "coin_ticker": coin}
            for coin in selected_coins
        ]
        stmt = insert(UserCoin).values(coins_to_insert).on_conflict_do_nothing(
            index_elements=['user_id', 'coin_ticker'])
        await session.execute(stmt)
        await session.commit()

    await safe_edit_text(
        message=callback.message,
        text=f"✅ Успешно добавлено {len(selected_coins)} монет!",
        reply_markup=get_back_to_settings_keyboard()
    )
    await state.clear()
    await show_settings_menu(message=callback.message, state=state)
    await callback.answer(f"✅ Успешно добавлено {len(selected_coins)} монет!")


@router.callback_query(F.data == "remove_coin_start", AdminFilter())
async def start_coin_removal(callback: CallbackQuery, state: FSMContext):
    """Начинает интерактивный процесс удаления монет."""
    async with async_session_factory() as session:
        stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == callback.from_user.id)
        user_coins = (await session.execute(stmt)).scalars().all()

    if not user_coins:
        await callback.answer("У вас нет монет для удаления.", show_alert=True)
        return

    await state.set_state(SettingsState.selecting_coins_to_remove)
    await state.update_data(user_coins=user_coins, selected_for_removal=[])

    keyboard = get_coin_removal_keyboard(user_coins, [])
    await callback.message.edit_text("Выберите монеты для удаления, их может быть несколько:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("toggle_remove:"), SettingsState.selecting_coins_to_remove, AdminFilter())
async def handle_toggle_removal(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор/снятие выбора монеты для удаления."""
    coin_to_toggle = callback.data.split(":")[1]
    data = await state.get_data()
    user_coins = data.get("user_coins", [])
    selected_for_removal = data.get("selected_for_removal", [])

    if coin_to_toggle in selected_for_removal:
        selected_for_removal.remove(coin_to_toggle)
    else:
        selected_for_removal.append(coin_to_toggle)

    await state.update_data(selected_for_removal=selected_for_removal)

    keyboard = get_coin_removal_keyboard(user_coins, selected_for_removal)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "confirm_remove_coins", SettingsState.selecting_coins_to_remove, AdminFilter())
async def confirm_coin_removal(callback: CallbackQuery, state: FSMContext):
    """Подтверждает и выполняет удаление выбранных монет из БД."""
    data = await state.get_data()
    selected_for_removal = data.get("selected_for_removal", [])

    if not selected_for_removal:
        await callback.answer("Вы ничего не выбрали!", show_alert=True)
        return

    async with async_session_factory() as session:
        stmt = delete(UserCoin).where(
            UserCoin.user_id == callback.from_user.id,
            UserCoin.coin_ticker.in_(selected_for_removal)
        )
        await session.execute(stmt)
        await session.commit()

    await callback.answer(f"Успешно удалено {len(selected_for_removal)} монет.", show_alert=True)
    await show_settings_menu(message=callback.message, state=state)


@router.callback_query(F.data == "show_scanner_settings", AdminFilter())
async def show_scanner_settings_handler(callback: CallbackQuery):
    """
    Показывает меню настроек сканера, получая ВСЕ необходимые данные из БД.
    """
    user_id = callback.from_user.id
    current_amount = None
    current_threshold = None

    async with async_session_factory() as session:
        # Получаем сумму сделки
        stmt_amount = select(UserSetting.value).where(
            and_(UserSetting.user_id == user_id, UserSetting.key == 'trade_amount')
        )
        result_amount = (await session.execute(stmt_amount)).scalar_one_or_none()
        if result_amount:
            current_amount = safe_get_numeric({'value': result_amount}, 'value')

        # Получаем порог прибыльности
        stmt_threshold = select(UserSetting.value).where(
            and_(UserSetting.user_id == user_id, UserSetting.key == 'profit_threshold')
        )
        result_threshold = (await session.execute(stmt_threshold)).scalar_one_or_none()
        if result_threshold:
            current_threshold = safe_get_numeric({'value': result_threshold},
                                                 'value')  # Здесь нам нужно значение как есть (в %, без деления на 100

    # Формируем текст сообщения
    if current_amount:
        amount_status_text = f"**Текущая сумма сделки: <code>${current_amount:,.2f} USDT</code>**"
    else:
        amount_status_text = f"**Текущая сумма сделки: <code>${DEFAULT_TRADE_AMOUNT_USD:,.2f} USDT</code>** (по умолчанию)"

    if current_threshold:
        threshold_status_text = f"**Текущий порог прибыльности: <code>{current_threshold:.2f}%</code>**"
    else:
        # Отображаем порог в процентах
        threshold_status_text = f"**Текущий порог прибыльности: <code>{DEFAULT_PROFIT_THRESHOLD * 100:.2f}%</code>** (по умолчанию)"

    await safe_edit_text(
        message=callback.message,
        text="📈 <b>Настройки сканера</b>\n\n"
             "Здесь вы можете настроить параметры для поиска арбитражных возможностей.\n\n"
             f"{amount_status_text}\n"
             f"{threshold_status_text}\n\n"
             "Выберите действие:",
        reply_markup=get_scanner_settings_keyboard(current_amount, current_threshold)
    )
    await callback.answer()


@router.callback_query(F.data == "set_trade_amount", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_settings_keyboard)
async def set_trade_amount_start(callback: CallbackQuery, state: FSMContext):
    """
    Анализирует лимиты бирж и балансы перед установкой суммы сделки.
    Защищен от "холодного старта" API и других ошибок подключения.
    """
    # Шаг 1: Уведомляем пользователя о начале длительной операции
    # Используем safe_edit_text для предотвращения ошибок "message not modified"
    await safe_edit_text(
        message=callback.message,
        text="⏳ Анализирую лимиты бирж и балансы..."
    )
    # Отвечаем на callback, чтобы убрать "часики" с кнопки
    await callback.answer()

    if not app_state.balance_service:
        logger.error("Критическая ошибка: BalanceService не был инициализирован при запуске.")
        await safe_edit_text(
            message=callback.message,
            text="❌ Внутренняя ошибка: Сервис балансов недоступен.",
            reply_markup=get_back_to_settings_keyboard()
        )
        return

        # ИСПОЛЬЗУЕМ ГЛОБАЛЬНЫЙ СЕРВИС ВМЕСТО СОЗДАНИЯ НОВОГО
    balance_service = app_state.balance_service

    all_balances, min_limits = await asyncio.gather(
        balance_service.get_all_balances(),
        balance_service.get_all_min_order_limits()
    )

    # Шаг 4: Проверяем, удалось ли получить данные хотя бы с двух бирж
    if not all_balances or len(all_balances) < MIN_EXCHANGES_FOR_ARBITRAGE:
        await safe_edit_text(
            message=callback.message,
            text="❌ Не удалось получить балансы как минимум с двух бирж. "
                 "Проверьте API ключи и пополните счета.",
            reply_markup=get_back_to_settings_keyboard()
        )
        return

    # Шаг 5: Выполняем умный анализ полученных данных через BalanceService
    analysis_result = balance_service.calculate_safe_trade_limits(all_balances, min_limits)

    # Распаковываем результаты анализа для удобства
    min_amount = analysis_result['min_trade_amount']
    max_amount = analysis_result['max_trade_amount']
    insufficient_exchanges = analysis_result['insufficient_exchanges']
    sufficient_exchanges = analysis_result['sufficient_exchanges']

    # Шаг 6: Критическая проверка - возможна ли торговля в принципе
    # Проверяем, есть ли хотя бы 2 готовые к торговле биржи и что макс. сумма больше мин.
    if len(sufficient_exchanges) < MIN_EXCHANGES_FOR_ARBITRAGE or max_amount < min_amount:
        # Формируем детальное сообщение об ошибке
        error_message = "Недостаточно средств для торговли. Необходимо как минимум 2 биржи с балансом, превышающим минимальный лимит."
        if insufficient_exchanges:
            problem_details = [
                f"• {p['exchange'].capitalize()}: нехватка ${p['shortage']:.2f}"
                for p in insufficient_exchanges
            ]
            error_message += "\n\n<b>Проблемные биржи:</b>\n" + "\n".join(problem_details)

        # Отправляем пользователю сообщение об ошибке и выходим
        await safe_edit_text(
            message=callback.message,
            text=f"❌ <b>{error_message}</b>",
            reply_markup=get_back_to_settings_keyboard()
        )
        return

    # Шаг 7: Если торговля возможна, переводим пользователя в состояние ожидания ввода суммы
    await state.set_state(SettingsState.waiting_for_trade_amount)
    # Сохраняем рассчитанные лимиты в FSM для последующей валидации
    await state.update_data(min_amount=min_amount, max_amount=max_amount)

    # Шаг 8: Формируем информативное сообщение для пользователя
    message_lines = [
        "💵 <b>Установка суммы сделки</b>",
        "Отправьте сумму в USDT для поиска арбитражных связок.",
        f"📊 <b>Допустимый диапазон (рассчитан по готовым биржам):</b>",
        f"🔹 <b>Минимум:</b> `${min_amount:,.2f}`",
        f"🔸 <b>Максимум:</b> `${max_amount:,.2f}`"
    ]

    # Добавляем информацию о текущих балансах USDT
    balance_breakdown = [f"   • {ex_id.capitalize()}: `${bal.get('USDT', 0.0):,.2f}`" for ex_id, bal in
                         all_balances.items()]
    message_lines.extend(["", "💰 <b>Все балансы USDT:</b>", *balance_breakdown])

    # Если есть биржи с недостаточным балансом, добавляем неблокирующее предупреждение
    if insufficient_exchanges:
        problem_details = [f"   • {p['exchange'].capitalize()} (не хватает ${p['shortage']:.2f})" for p in
                           insufficient_exchanges]
        message_lines.extend(
            ["", "⚠️ <b>Предупреждение:</b>", "Следующие биржи будут проигнорированы из-за нехватки средств:",
             *problem_details])

    # Шаг 9: Отправляем итоговое сообщение пользователю
    await safe_edit_text(
        message=callback.message,
        text="\n".join(message_lines),
        reply_markup=get_back_to_settings_keyboard()
    )


@router.message(SettingsState.waiting_for_trade_amount, F.text, AdminFilter())
async def process_trade_amount(message: Message, state: FSMContext):
    """
    Обрабатывает введенную пользователем сумму для торговли.
    """
    try:
        # Парсим введенную сумму (поддерживаем как точку, так и запятую)
        amount_str = message.text.strip().replace(',', '.')
        amount = float(amount_str)
    except ValueError:
        await message.reply(
            "❌ Пожалуйста, введите корректное числовое значение.\n"
            "Примеры: `15.5`, `20`, `100.75`",
            reply_markup=get_back_to_settings_keyboard()
        )
        return

    # Получаем сохраненные лимиты из состояния
    data = await state.get_data()
    min_amount = data.get('min_amount', DEFAULT_TRADE_AMOUNT_USD)
    max_amount = data.get('max_amount', DEFAULT_TRADE_AMOUNT_USD)

    # Валидируем введенную сумму
    is_valid, error_message = validate_trade_amount(amount, min_amount, max_amount)

    if not is_valid:
        await message.reply(
            f"❌ {error_message}\n\n"
            f"📊 <b>Допустимый диапазон:</b> `${min_amount:,.2f}` - `${max_amount:,.2f}`\n\n"
            "Попробуйте еще раз или отмените операцию.",
            reply_markup=get_back_to_settings_keyboard()
        )
        return

    # Сохраняем валидную сумму в базу данных
    user_id = message.from_user.id
    async with async_session_factory() as session:
        stmt = insert(UserSetting).values(
            user_id=user_id,
            key='trade_amount',
            value=str(amount)
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=['user_id', 'key'],
            set_={'value': stmt.excluded.value}
        )
        await session.execute(stmt)
        await session.commit()

    # Очищаем состояние
    await state.clear()

    # Отправляем подтверждение и возвращаем в меню настроек
    await message.answer(
        f"✅ <b>Сумма сделки успешно установлена:</b> `${amount:,.2f} USDT`\n\n"
        f"Теперь бот будет искать арбитражные возможности для этой суммы.",
        reply_markup=get_settings_keyboard()
    )


@router.callback_query(F.data == "reset_trade_amount", AdminFilter())
async def reset_trade_amount_handler(callback: CallbackQuery):
    """
    Сбрасывает сумму сделки к значению по умолчанию.
    """
    user_id = callback.from_user.id

    # Удаляем настройку из базы данных
    async with async_session_factory() as session:
        stmt = delete(UserSetting).where(
            and_(UserSetting.user_id == user_id, UserSetting.key == 'trade_amount')
        )
        await session.execute(stmt)
        await session.commit()

    # Используем answer вместо попытки редактирования
    await callback.answer("✅ Сумма сделки сброшена к значению по умолчанию.", show_alert=True)

    # Безопасно возвращаемся в меню через новое сообщение
    try:
        await callback.message.edit_text(
            "🔄 Настройки обновлены. Возвращаюсь в главное меню...",
            reply_markup=None
        )
        # Короткая пауза для лучшего UX
        await asyncio.sleep(0.5)
        await show_scanner_settings_handler(callback)
    except Exception as e:
        logger.warning(f"Ошибка при обновлении интерфейса: {e}")
        # Альтернативный путь - отправляем новое сообщение
        await callback.message.answer(
            "✅ Сумма сделки сброшена. Откройте меню настроек заново.",
            reply_markup=get_settings_keyboard()
        )


@router.callback_query(F.data == "set_profit_threshold", AdminFilter())
async def set_profit_threshold_start(callback: CallbackQuery, state: FSMContext):
    """Запускает процесс установки порога прибыльности, информируя о лимитах."""
    await callback.message.edit_text(
        "📈 <b>Установка порога прибыльности</b>\n\n"
        "Отправьте сообщением желаемый процент минимальной чистой прибыли для поиска связок.\n\n"
        # --- НОВОЕ: Информируем пользователя о допустимом диапазоне ---
        f"🔹 <b>Допустимый диапазон: от <code>{MIN_PROFIT_THRESHOLD_PERCENT:.1f}%</code> до <code>{MAX_PROFIT_THRESHOLD_PERCENT:.1f}%</code>.</b>\n\n"
        "Например, если вы введете `0.7`, бот будет искать связки с прибыльностью не менее 0.7%.",
        reply_markup=get_back_to_settings_keyboard()
    )
    await state.set_state(SettingsState.waiting_for_profit_threshold)
    await callback.answer()


@router.message(SettingsState.waiting_for_profit_threshold, F.text, AdminFilter())
async def process_profit_threshold(message: Message, state: FSMContext):
    """Ловит и валидирует введенный пользователем порог с учетом лимитов."""
    try:
        threshold = float(message.text.strip().replace(',', '.'))
    except ValueError:
        await message.reply(
            "❌ Ошибка.\n\nПожалуйста, введите число. Например: `0.7` или `1.5`.",
            reply_markup=get_back_to_settings_keyboard()
        )
        return

    # Используем функцию, передаем в нее лимиты для порога
    is_valid, error_message = validate_trade_amount(
        amount=threshold,
        min_amount=MIN_PROFIT_THRESHOLD_PERCENT,
        max_amount=MAX_PROFIT_THRESHOLD_PERCENT
    )

    if not is_valid:
        # Хелпер вернет сообщение "Сумма ...", заменим его на "Порог" для ясности
        error_text = error_message.replace("Сумма", "Порог").replace("$", "") + "%"

        await message.reply(
            f"❌ Ошибка.\n\n{error_text}.\n\nПопробуйте еще раз или отмените.",
            reply_markup=get_back_to_settings_keyboard()
        )
        return

    # Сохраняем в БД (код без изменений)
    user_id = message.from_user.id
    async with async_session_factory() as session:
        stmt = insert(UserSetting).values(user_id=user_id, key='profit_threshold', value=str(threshold))
        stmt = stmt.on_conflict_do_update(
            index_elements=['user_id', 'key'],
            set_={'value': stmt.excluded.value}
        )
        await session.execute(stmt)
        await session.commit()

    await state.clear()

    await message.answer(
        f"✅ Порог прибыльности успешно установлен: <b>{threshold:.2f}%</b>",
        reply_markup=get_settings_keyboard()
    )


@router.callback_query(F.data == "reset_profit_threshold", AdminFilter())
async def reset_profit_threshold_handler(callback: CallbackQuery):
    """
    Удаляет настройку порога из БД и вызывает главный обработчик для обновления меню.
    """
    user_id = callback.from_user.id

    async with async_session_factory() as session:
        stmt = delete(UserSetting).where(
            and_(UserSetting.user_id == user_id, UserSetting.key == 'profit_threshold')
        )
        await session.execute(stmt)
        await session.commit()

    await callback.answer("✅ Порог прибыльности сброшен к значению по умолчанию.")

    # Просто вызываем "мастер" хендлер ---
    await show_scanner_settings_handler(callback)


# # inter_exchange_arbitrage_bot/src/bot/handlers/settings_handlers.py
# import asyncio
#
# from aiogram import Router, F
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, CallbackQuery
# from sqlalchemy import select, delete, and_
# from sqlalchemy.dialects.postgresql import insert
#
# import src.core.state as app_state
# from src.bot.handlers.user_handlers import AdminFilter
# from src.bot.keyboards import get_coin_selection_keyboard, get_coin_removal_keyboard
# from src.bot.keyboards.settings_keyboard import (get_scanner_settings_keyboard, get_settings_keyboard,
#                                                  get_back_to_settings_keyboard)
# from src.bot.logic.settings_logic import show_settings_menu
# from src.bot.states.user_states import SettingsState
# from src.constants.trading_constants import (DEFAULT_TRADE_AMOUNT_USD, DEFAULT_PROFIT_THRESHOLD,
#                                              MIN_PROFIT_THRESHOLD_PERCENT, MAX_PROFIT_THRESHOLD_PERCENT,
#                                              MIN_EXCHANGES_FOR_ARBITRAGE)
# from src.core.database import async_session_factory
# from src.models.user_models import UserCoin
# from src.models.user_settings import UserSetting
# from src.services import scanner_api_service
# from src.utils import logger
# from src.utils.api_error_handler import handle_api_errors
# from src.utils.chat_actions import safe_edit_text
# from src.utils.helpers import validate_trade_amount, safe_get_numeric
#
# router = Router()
#
#
# @router.callback_query(F.data == "show_settings", AdminFilter())
# async def show_settings_menu_handler(callback: CallbackQuery, state: FSMContext):
#     await show_settings_menu(message=callback.message, state=state)
#     await callback.answer()
#
#
# @router.callback_query(F.data == "back_to_settings", AdminFilter())
# async def back_to_settings_handler(callback: CallbackQuery, state: FSMContext):
#     await show_settings_menu(message=callback.message, state=state)
#     await callback.answer()
#
#
# @router.callback_query(F.data == "show_my_coins", AdminFilter())
# async def show_my_coins_handler(callback: CallbackQuery):
#     """Показывает список отслеживаемых монет по нажатию кнопки."""
#     async with async_session_factory() as session:
#         stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == callback.from_user.id).order_by(
#             UserCoin.coin_ticker)
#         result = await session.execute(stmt)
#         coins = result.scalars().all()
#
#     if not coins:
#         text = "У вас пока нет отслеживаемых монет. 😕"
#     else:
#         coin_list = "\n".join([f"• <code>{coin}</code>" for coin in coins])
#         text = f"<b>✨ Ваши отслеживаемые монеты:</b>\n{coin_list}"
#
#     await safe_edit_text(
#         message=callback.message,
#         text=text,
#         reply_markup=get_back_to_settings_keyboard()
#     )
#     await callback.answer()
#
#
# @router.callback_query(F.data == "add_coin_start", AdminFilter())
# @handle_api_errors(fallback_keyboard_func=get_settings_keyboard)
# async def start_coin_selection(callback: CallbackQuery, state: FSMContext):
#     """
#     ИСПРАВЛЕННАЯ ВЕРСИЯ: Получает список монет через API.
#     Защищен от "холодного старта" декоратором @handle_api_errors.
#     """
#     await safe_edit_text(
#         message=callback.message,
#         text="⏳ Загружаю список всех доступных монет через API..."
#     )
#     await callback.answer()
#
#     # 1. Получаем монеты, которые УЖЕ есть у пользователя (из БД, это правильно)
#     async with async_session_factory() as session:
#         stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == callback.from_user.id)
#         user_coins_set = set((await session.execute(stmt)).scalars().all())
#
#     # 2. Получаем ВСЕ доступные монеты через новый API-вызов
#     # Декоратор @handle_api_errors уже проверил, что API готово
#     api_response = await scanner_api_service.get_all_assets_from_api()
#
#     # 3. Проверяем ответ от API
#     if api_response is None:
#         await safe_edit_text(
#             message=callback.message,
#             text="❌ Не удалось загрузить список монет с сервера API.",
#             reply_markup=get_back_to_settings_keyboard()
#         )
#         return
#
#     all_coins_set = set(api_response.get("assets", []))
#     successful_exchanges = api_response.get("sources", [])
#
#     if not all_coins_set or not successful_exchanges:
#         await safe_edit_text(
#             message=callback.message,
#             text="❌ API не вернуло список монет.\nВозможно, нет активных бирж. Проверьте логи API.",
#             reply_markup=get_back_to_settings_keyboard()
#         )
#         return
#
#     # 4. Фильтруем монеты, которые уже добавлены у пользователя
#     coins_to_display = sorted([coin for coin in all_coins_set if coin not in user_coins_set])
#
#     logger.info(f"✅ Загружено {len(all_coins_set)} уникальных монет с {len(successful_exchanges)} бирж через API.")
#
#     # 5. Обновляем состояние FSM и показываем клавиатуру (логика без изменений)
#     await state.set_state(SettingsState.selecting_coins_to_add)
#     await state.update_data(
#         all_coins=coins_to_display,
#         selected_coins=[],
#         current_page=0,
#         search_query=None,
#         menu_message_id=callback.message.message_id,
#         source_exchanges=successful_exchanges
#     )
#
#     keyboard = get_coin_selection_keyboard(all_coins=coins_to_display, selected_coins=[])
#     exchanges_text = ", ".join([ex.capitalize() for ex in successful_exchanges])
#     await safe_edit_text(
#         message=callback.message,
#         text="<b>Выберите монеты для добавления.</b>\n\n"
#              f"<i>Данные загружены с бирж: {exchanges_text}</i>\n\n"
#              "Вы можете переключать страницы или просто <b>отправить сообщение с названием монеты (тикер), чтобы найти её.</b>",
#         reply_markup=keyboard
#     )
#
#
# @router.message(SettingsState.selecting_coins_to_add, F.text, AdminFilter())
# async def handle_coin_search(message: Message, state: FSMContext):
#     """
#     Ловит текстовое сообщение в состоянии выбора монет и использует его для поиска.
#     """
#     search_query = message.text.strip()
#     await message.delete()
#
#     if not search_query:
#         return
#
#     data = await state.get_data()
#     # --- ИЗМЕНЕНИЕ: Получаем ID сообщения из состояния ---
#     menu_message_id = data.get('menu_message_id')
#     if not menu_message_id:
#         # На случай, если что-то пошло не так
#         return
#
#     await state.update_data(search_query=search_query, current_page=0)
#
#     keyboard = get_coin_selection_keyboard(
#         all_coins=data.get("all_coins", []),
#         selected_coins=data.get("selected_coins", []),
#         current_page=0,
#         search_query=search_query
#     )
#
#     # --- ИЗМЕНЕНИЕ: Используем сохраненный ID для редактирования ---
#     await message.bot.edit_message_text(
#         text=f"🔎 <b>Результаты поиска по запросу «{search_query}»:</b>\n\nВыберите монеты или введите новый запрос.",
#         chat_id=message.chat.id,
#         message_id=menu_message_id,  # <-- ИСПОЛЬЗУЕМ СОХРАНЕННЫЙ ID
#         reply_markup=keyboard
#     )
#
#
# @router.callback_query(F.data == "clear_coin_search", SettingsState.selecting_coins_to_add, AdminFilter())
# async def clear_coin_search(callback: CallbackQuery, state: FSMContext):
#     """Сбрасывает поисковый запрос и показывает полный список монет."""
#     await callback.answer()
#     data = await state.get_data()
#
#     # Сбрасываем поиск и страницу
#     await state.update_data(search_query=None, current_page=0)
#
#     keyboard = get_coin_selection_keyboard(
#         all_coins=data.get("all_coins", []),
#         selected_coins=data.get("selected_coins", []),
#         current_page=0,
#         search_query=None  # Явно передаем None
#     )
#
#     await callback.message.edit_text(
#         "<b>Выберите монеты для добавления.</b>\n\n"
#         "Вы можете переключать страницы или просто <b>отправить сообщение с названием монеты (тикер), чтобы найти её.</b>",
#         reply_markup=keyboard
#     )
#
#
# @router.callback_query(F.data.startswith("select_coin_page:"), SettingsState.selecting_coins_to_add, AdminFilter())
# async def handle_coin_page_switch(callback: CallbackQuery, state: FSMContext):
#     """Переключает страницы, учитывая текущий поисковый запрос."""
#     await callback.answer()
#     page = int(callback.data.split(":")[1])
#     await state.update_data(current_page=page)
#     data = await state.get_data()
#
#     # Передаем в клавиатуру текущий поисковый запрос из состояния
#     keyboard = get_coin_selection_keyboard(
#         all_coins=data.get("all_coins", []),
#         selected_coins=data.get("selected_coins", []),
#         current_page=page,
#         search_query=data.get("search_query")
#     )
#
#     # Текст сообщения зависит от того, активен ли поиск
#     text = f"🔎 <b>Результаты поиска по запросу «{data.get('search_query')}»:</b>" if data.get(
#         'search_query') else "<b>Выберите монеты для добавления.</b>"
#
#     await callback.message.edit_text(text, reply_markup=keyboard)
#
#
# @router.callback_query(F.data.startswith("toggle_coin:"), SettingsState.selecting_coins_to_add, AdminFilter())
# async def handle_toggle_coin(callback: CallbackQuery, state: FSMContext):
#     """Выбирает/снимает выбор с монеты, сохраняя состояние поиска."""
#     await callback.answer()
#     _, coin_to_toggle, page_str = callback.data.split(":")
#     page = int(page_str)
#
#     data = await state.get_data()
#     selected_coins = data.get("selected_coins", [])
#
#     if coin_to_toggle in selected_coins:
#         selected_coins.remove(coin_to_toggle)
#     else:
#         selected_coins.append(coin_to_toggle)
#
#     await state.update_data(selected_coins=selected_coins)
#
#     # Пересобираем клавиатуру с учетом всех данных из состояния
#     keyboard = get_coin_selection_keyboard(
#         all_coins=data.get("all_coins", []),
#         selected_coins=selected_coins,
#         current_page=page,
#         search_query=data.get("search_query")
#     )
#     await callback.message.edit_reply_markup(reply_markup=keyboard)
#
#
# @router.callback_query(F.data == "confirm_add_coins", AdminFilter())
# async def confirm_coin_selection(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()
#     data = await state.get_data()
#     selected_coins = data.get("selected_coins", [])
#
#     if not selected_coins:
#         await callback.answer("Вы ничего не выбрали!", show_alert=True)
#         return
#
#     async with async_session_factory() as session:
#         coins_to_insert = [
#             {"user_id": callback.from_user.id, "coin_ticker": coin}
#             for coin in selected_coins
#         ]
#         stmt = insert(UserCoin).values(coins_to_insert).on_conflict_do_nothing(
#             index_elements=['user_id', 'coin_ticker'])
#         await session.execute(stmt)
#         await session.commit()
#
#     await safe_edit_text(
#         message=callback.message,
#         text=f"✅ Успешно добавлено {len(selected_coins)} монет!",
#         reply_markup=get_back_to_settings_keyboard()
#     )
#     await state.clear()
#     await show_settings_menu(message=callback.message, state=state)
#     await callback.answer(f"✅ Успешно добавлено {len(selected_coins)} монет!")
#
#
# @router.callback_query(F.data == "remove_coin_start", AdminFilter())
# async def start_coin_removal(callback: CallbackQuery, state: FSMContext):
#     """Начинает интерактивный процесс удаления монет."""
#     async with async_session_factory() as session:
#         stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == callback.from_user.id)
#         user_coins = (await session.execute(stmt)).scalars().all()
#
#     if not user_coins:
#         await callback.answer("У вас нет монет для удаления.", show_alert=True)
#         return
#
#     await state.set_state(SettingsState.selecting_coins_to_remove)
#     await state.update_data(user_coins=user_coins, selected_for_removal=[])
#
#     keyboard = get_coin_removal_keyboard(user_coins, [])
#     await callback.message.edit_text("Выберите монеты для удаления, их может быть несколько:", reply_markup=keyboard)
#     await callback.answer()
#
#
# @router.callback_query(F.data.startswith("toggle_remove:"), SettingsState.selecting_coins_to_remove, AdminFilter())
# async def handle_toggle_removal(callback: CallbackQuery, state: FSMContext):
#     """Обрабатывает выбор/снятие выбора монеты для удаления."""
#     coin_to_toggle = callback.data.split(":")[1]
#     data = await state.get_data()
#     user_coins = data.get("user_coins", [])
#     selected_for_removal = data.get("selected_for_removal", [])
#
#     if coin_to_toggle in selected_for_removal:
#         selected_for_removal.remove(coin_to_toggle)
#     else:
#         selected_for_removal.append(coin_to_toggle)
#
#     await state.update_data(selected_for_removal=selected_for_removal)
#
#     keyboard = get_coin_removal_keyboard(user_coins, selected_for_removal)
#     await callback.message.edit_reply_markup(reply_markup=keyboard)
#     await callback.answer()
#
#
# @router.callback_query(F.data == "confirm_remove_coins", SettingsState.selecting_coins_to_remove, AdminFilter())
# async def confirm_coin_removal(callback: CallbackQuery, state: FSMContext):
#     """Подтверждает и выполняет удаление выбранных монет из БД."""
#     data = await state.get_data()
#     selected_for_removal = data.get("selected_for_removal", [])
#
#     if not selected_for_removal:
#         await callback.answer("Вы ничего не выбрали!", show_alert=True)
#         return
#
#     async with async_session_factory() as session:
#         stmt = delete(UserCoin).where(
#             UserCoin.user_id == callback.from_user.id,
#             UserCoin.coin_ticker.in_(selected_for_removal)
#         )
#         await session.execute(stmt)
#         await session.commit()
#
#     await callback.answer(f"Успешно удалено {len(selected_for_removal)} монет.", show_alert=True)
#     await show_settings_menu(message=callback.message, state=state)
#
#
# @router.callback_query(F.data == "show_scanner_settings", AdminFilter())
# async def show_scanner_settings_handler(callback: CallbackQuery):
#     """
#     Показывает меню настроек сканера, получая ВСЕ необходимые данные из БД.
#     """
#     user_id = callback.from_user.id
#     current_amount = None
#     current_threshold = None
#
#     async with async_session_factory() as session:
#         # Получаем сумму сделки
#         stmt_amount = select(UserSetting.value).where(
#             and_(UserSetting.user_id == user_id, UserSetting.key == 'trade_amount')
#         )
#         result_amount = (await session.execute(stmt_amount)).scalar_one_or_none()
#         if result_amount:
#             current_amount = safe_get_numeric({'value': result_amount}, 'value')
#
#         # Получаем порог прибыльности
#         stmt_threshold = select(UserSetting.value).where(
#             and_(UserSetting.user_id == user_id, UserSetting.key == 'profit_threshold')
#         )
#         result_threshold = (await session.execute(stmt_threshold)).scalar_one_or_none()
#         if result_threshold:
#             current_threshold = safe_get_numeric({'value': result_threshold},
#                                                  'value')  # Здесь нам нужно значение как есть (в %), без деления на 100
#
#     # Формируем текст сообщения
#     if current_amount:
#         amount_status_text = f"**Текущая сумма сделки: <code>${current_amount:,.2f} USDT</code>**"
#     else:
#         amount_status_text = f"**Текущая сумма сделки: <code>${DEFAULT_TRADE_AMOUNT_USD:,.2f} USDT</code>** (по умолчанию)"
#
#     if current_threshold:
#         threshold_status_text = f"**Текущий порог прибыльности: <code>{current_threshold:.2f}%</code>**"
#     else:
#         # Отображаем порог в процентах
#         threshold_status_text = f"**Текущий порог прибыльности: <code>{DEFAULT_PROFIT_THRESHOLD * 100:.2f}%</code>** (по умолчанию)"
#
#     await safe_edit_text(
#         message=callback.message,
#         text="📈 <b>Настройки сканера</b>\n\n"
#              "Здесь вы можете настроить параметры для поиска арбитражных возможностей.\n\n"
#              f"{amount_status_text}\n"
#              f"{threshold_status_text}\n\n"
#              "Выберите действие:",
#         reply_markup=get_scanner_settings_keyboard(current_amount, current_threshold)
#     )
#     await callback.answer()
#
#
# @router.callback_query(F.data == "set_trade_amount", AdminFilter())
# @handle_api_errors(fallback_keyboard_func=get_settings_keyboard)
# async def set_trade_amount_start(callback: CallbackQuery, state: FSMContext):
#     """
#     Анализирует лимиты бирж и балансы перед установкой суммы сделки.
#     Защищен от "холодного старта" API и других ошибок подключения.
#     """
#     # Шаг 1: Уведомляем пользователя о начале длительной операции
#     # Используем safe_edit_text для предотвращения ошибок "message not modified"
#     await safe_edit_text(
#         message=callback.message,
#         text="⏳ Анализирую лимиты бирж и балансы..."
#     )
#     # Отвечаем на callback, чтобы убрать "часики" с кнопки
#     await callback.answer()
#
#     if not app_state.balance_service:
#         logger.error("Критическая ошибка: BalanceService не был инициализирован при запуске.")
#         await safe_edit_text(
#             message=callback.message,
#             text="❌ Внутренняя ошибка: Сервис балансов недоступен.",
#             reply_markup=get_back_to_settings_keyboard()
#         )
#         return
#
#         # ИСПОЛЬЗУЕМ ГЛОБАЛЬНЫЙ СЕРВИС ВМЕСТО СОЗДАНИЯ НОВОГО
#     balance_service = app_state.balance_service
#
#     all_balances, min_limits = await asyncio.gather(
#         balance_service.get_all_balances(),
#         balance_service.get_all_min_order_limits()
#     )
#
#     # Шаг 4: Проверяем, удалось ли получить данные хотя бы с двух бирж
#     if not all_balances or len(all_balances) < MIN_EXCHANGES_FOR_ARBITRAGE:
#         await safe_edit_text(
#             message=callback.message,
#             text="❌ Не удалось получить балансы как минимум с двух бирж. "
#                  "Проверьте API ключи и пополните счета.",
#             reply_markup=get_back_to_settings_keyboard()
#         )
#         return
#
#     # Шаг 5: Выполняем умный анализ полученных данных через BalanceService
#     analysis_result = balance_service.calculate_safe_trade_limits(all_balances, min_limits)
#
#     # Распаковываем результаты анализа для удобства
#     min_amount = analysis_result['min_trade_amount']
#     max_amount = analysis_result['max_trade_amount']
#     insufficient_exchanges = analysis_result['insufficient_exchanges']
#     sufficient_exchanges = analysis_result['sufficient_exchanges']
#
#     # Шаг 6: Критическая проверка - возможна ли торговля в принципе
#     # Проверяем, есть ли хотя бы 2 готовые к торговле биржи и что макс. сумма больше мин.
#     if len(sufficient_exchanges) < MIN_EXCHANGES_FOR_ARBITRAGE or max_amount < min_amount:
#         # Формируем детальное сообщение об ошибке
#         error_message = "Недостаточно средств для торговли. Необходимо как минимум 2 биржи с балансом, превышающим минимальный лимит."
#         if insufficient_exchanges:
#             problem_details = [
#                 f"• {p['exchange'].capitalize()}: нехватка ${p['shortage']:.2f}"
#                 for p in insufficient_exchanges
#             ]
#             error_message += "\n\n<b>Проблемные биржи:</b>\n" + "\n".join(problem_details)
#
#         # Отправляем пользователю сообщение об ошибке и выходим
#         await safe_edit_text(
#             message=callback.message,
#             text=f"❌ <b>{error_message}</b>",
#             reply_markup=get_back_to_settings_keyboard()
#         )
#         return
#
#     # Шаг 7: Если торговля возможна, переводим пользователя в состояние ожидания ввода суммы
#     await state.set_state(SettingsState.waiting_for_trade_amount)
#     # Сохраняем рассчитанные лимиты в FSM для последующей валидации
#     await state.update_data(min_amount=min_amount, max_amount=max_amount)
#
#     # Шаг 8: Формируем информативное сообщение для пользователя
#     message_lines = [
#         "💵 <b>Установка суммы сделки</b>",
#         "Отправьте сумму в USDT для поиска арбитражных связок.",
#         f"📊 <b>Допустимый диапазон (рассчитан по готовым биржам):</b>",
#         f"🔹 <b>Минимум:</b> `${min_amount:,.2f}`",
#         f"🔸 <b>Максимум:</b> `${max_amount:,.2f}`"
#     ]
#
#     # Добавляем информацию о текущих балансах USDT
#     balance_breakdown = [f"   • {ex_id.capitalize()}: `${bal.get('USDT', 0.0):,.2f}`" for ex_id, bal in
#                          all_balances.items()]
#     message_lines.extend(["", "💰 <b>Все балансы USDT:</b>", *balance_breakdown])
#
#     # Если есть биржи с недостаточным балансом, добавляем неблокирующее предупреждение
#     if insufficient_exchanges:
#         problem_details = [f"   • {p['exchange'].capitalize()} (не хватает ${p['shortage']:.2f})" for p in
#                            insufficient_exchanges]
#         message_lines.extend(
#             ["", "⚠️ <b>Предупреждение:</b>", "Следующие биржи будут проигнорированы из-за нехватки средств:",
#              *problem_details])
#
#     # Шаг 9: Отправляем итоговое сообщение пользователю
#     await safe_edit_text(
#         message=callback.message,
#         text="\n".join(message_lines),
#         reply_markup=get_back_to_settings_keyboard()
#     )
#
#
# @router.message(SettingsState.waiting_for_trade_amount, F.text, AdminFilter())
# async def process_trade_amount(message: Message, state: FSMContext):
#     """
#     Обрабатывает введенную пользователем сумму для торговли.
#     """
#     try:
#         # Парсим введенную сумму (поддерживаем как точку, так и запятую)
#         amount_str = message.text.strip().replace(',', '.')
#         amount = float(amount_str)
#     except ValueError:
#         await message.reply(
#             "❌ Пожалуйста, введите корректное числовое значение.\n"
#             "Примеры: `15.5`, `20`, `100.75`",
#             reply_markup=get_back_to_settings_keyboard()
#         )
#         return
#
#     # Получаем сохраненные лимиты из состояния
#     data = await state.get_data()
#     min_amount = data.get('min_amount', DEFAULT_TRADE_AMOUNT_USD)
#     max_amount = data.get('max_amount', DEFAULT_TRADE_AMOUNT_USD)
#
#     # Валидируем введенную сумму
#     is_valid, error_message = validate_trade_amount(amount, min_amount, max_amount)
#
#     if not is_valid:
#         await message.reply(
#             f"❌ {error_message}\n\n"
#             f"📊 <b>Допустимый диапазон:</b> `${min_amount:,.2f}` - `${max_amount:,.2f}`\n\n"
#             "Попробуйте еще раз или отмените операцию.",
#             reply_markup=get_back_to_settings_keyboard()
#         )
#         return
#
#     # Сохраняем валидную сумму в базу данных
#     user_id = message.from_user.id
#     async with async_session_factory() as session:
#         stmt = insert(UserSetting).values(
#             user_id=user_id,
#             key='trade_amount',
#             value=str(amount)
#         )
#         stmt = stmt.on_conflict_do_update(
#             index_elements=['user_id', 'key'],
#             set_={'value': stmt.excluded.value}
#         )
#         await session.execute(stmt)
#         await session.commit()
#
#     # Очищаем состояние
#     await state.clear()
#
#     # Отправляем подтверждение и возвращаем в меню настроек
#     await message.answer(
#         f"✅ <b>Сумма сделки успешно установлена:</b> `${amount:,.2f} USDT`\n\n"
#         f"Теперь бот будет искать арбитражные возможности для этой суммы.",
#         reply_markup=get_settings_keyboard()
#     )
#
#
# @router.callback_query(F.data == "reset_trade_amount", AdminFilter())
# async def reset_trade_amount_handler(callback: CallbackQuery):
#     """
#     🔧 ИСПРАВЛЕННАЯ ВЕРСИЯ: Предотвращает ошибку дублирования сообщений.
#     """
#     user_id = callback.from_user.id
#
#     # Удаляем настройку из базы данных
#     async with async_session_factory() as session:
#         stmt = delete(UserSetting).where(
#             and_(UserSetting.user_id == user_id, UserSetting.key == 'trade_amount')
#         )
#         await session.execute(stmt)
#         await session.commit()
#
#     # 🔧 ИСПРАВЛЕНИЕ: Используем answer вместо попытки редактирования
#     await callback.answer("✅ Сумма сделки сброшена к значению по умолчанию.", show_alert=True)
#
#     # Безопасно возвращаемся в меню через новое сообщение
#     try:
#         await callback.message.edit_text(
#             "🔄 Настройки обновлены. Возвращаюсь в главное меню...",
#             reply_markup=None
#         )
#         # Короткая пауза для лучшего UX
#         await asyncio.sleep(0.5)
#         await show_scanner_settings_handler(callback)
#     except Exception as e:
#         logger.warning(f"Ошибка при обновлении интерфейса: {e}")
#         # Альтернативный путь - отправляем новое сообщение
#         await callback.message.answer(
#             "✅ Сумма сделки сброшена. Откройте меню настроек заново.",
#             reply_markup=get_settings_keyboard()
#         )
#
#
# @router.callback_query(F.data == "set_profit_threshold", AdminFilter())
# async def set_profit_threshold_start(callback: CallbackQuery, state: FSMContext):
#     """Запускает процесс установки порога прибыльности, информируя о лимитах."""
#     await callback.message.edit_text(
#         "📈 <b>Установка порога прибыльности</b>\n\n"
#         "Отправьте сообщением желаемый процент минимальной чистой прибыли для поиска связок.\n\n"
#         # --- НОВОЕ: Информируем пользователя о допустимом диапазоне ---
#         f"🔹 <b>Допустимый диапазон: от <code>{MIN_PROFIT_THRESHOLD_PERCENT:.1f}%</code> до <code>{MAX_PROFIT_THRESHOLD_PERCENT:.1f}%</code>.</b>\n\n"
#         "Например, если вы введете `0.7`, бот будет искать связки с прибыльностью не менее 0.7%.",
#         reply_markup=get_back_to_settings_keyboard()
#     )
#     await state.set_state(SettingsState.waiting_for_profit_threshold)
#     await callback.answer()
#
#
# @router.message(SettingsState.waiting_for_profit_threshold, F.text, AdminFilter())
# async def process_profit_threshold(message: Message, state: FSMContext):
#     """Ловит и валидирует введенный пользователем порог с учетом лимитов."""
#     try:
#         threshold = float(message.text.strip().replace(',', '.'))
#     except ValueError:
#         await message.reply(
#             "❌ Ошибка.\n\nПожалуйста, введите число. Например: `0.7` или `1.5`.",
#             reply_markup=get_back_to_settings_keyboard()
#         )
#         return
#
#     # Используем функцию, передаем в нее лимиты для порога
#     is_valid, error_message = validate_trade_amount(
#         amount=threshold,
#         min_amount=MIN_PROFIT_THRESHOLD_PERCENT,
#         max_amount=MAX_PROFIT_THRESHOLD_PERCENT
#     )
#
#     if not is_valid:
#         # Хелпер вернет сообщение "Сумма ...", заменим его на "Порог" для ясности
#         error_text = error_message.replace("Сумма", "Порог").replace("$", "") + "%"
#
#         await message.reply(
#             f"❌ Ошибка.\n\n{error_text}.\n\nПопробуйте еще раз или отмените.",
#             reply_markup=get_back_to_settings_keyboard()
#         )
#         return
#
#     # Сохраняем в БД (код без изменений)
#     user_id = message.from_user.id
#     async with async_session_factory() as session:
#         stmt = insert(UserSetting).values(user_id=user_id, key='profit_threshold', value=str(threshold))
#         stmt = stmt.on_conflict_do_update(
#             index_elements=['user_id', 'key'],
#             set_={'value': stmt.excluded.value}
#         )
#         await session.execute(stmt)
#         await session.commit()
#
#     await state.clear()
#
#     await message.answer(
#         f"✅ Порог прибыльности успешно установлен: <b>{threshold:.2f}%</b>",
#         reply_markup=get_settings_keyboard()
#     )
#
#
# @router.callback_query(F.data == "reset_profit_threshold", AdminFilter())
# async def reset_profit_threshold_handler(callback: CallbackQuery):
#     """
#     Удаляет настройку порога из БД и вызывает главный обработчик для обновления меню.
#     """
#     user_id = callback.from_user.id
#
#     async with async_session_factory() as session:
#         stmt = delete(UserSetting).where(
#             and_(UserSetting.user_id == user_id, UserSetting.key == 'profit_threshold')
#         )
#         await session.execute(stmt)
#         await session.commit()
#
#     await callback.answer("✅ Порог прибыльности сброшен к значению по умолчанию.")
#
#     # Просто вызываем "мастер" хендлер ---
#     await show_scanner_settings_handler(callback)
