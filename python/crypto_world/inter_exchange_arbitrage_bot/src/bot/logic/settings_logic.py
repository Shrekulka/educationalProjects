# inter_exchange_arbitrage_bot/src/bot/logic/settings_logic.py

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select, and_

from src.bot.keyboards.settings_keyboard import get_settings_keyboard
from src.constants.trading_constants import DEFAULT_TRADE_AMOUNT_USD, DEFAULT_PROFIT_THRESHOLD
from src.core.database import async_session_factory
from src.models.user_settings import UserSetting


async def show_settings_menu(message: Message, state: FSMContext):
    """
    Отображает меню настроек, редактируя существующее сообщение.
    """
    await state.clear()
    await message.edit_text(
        "⚙️ <b>Меню настроек</b>\n\nЗдесь вы можете управлять списком отслеживаемых монет.",
        reply_markup=get_settings_keyboard()
    )


async def get_user_settings(user_id: int) -> tuple[float, float]:
    """
    Получает торговую сумму и порог прибыльности для указанного пользователя из БД.
    Возвращает значения по умолчанию, если настройки не найдены.
    """
    trade_amount = DEFAULT_TRADE_AMOUNT_USD
    profit_threshold = DEFAULT_PROFIT_THRESHOLD

    async with async_session_factory() as session:
        # Получаем торговую сумму
        stmt_amount = select(UserSetting.value).where(
            and_(UserSetting.user_id == user_id, UserSetting.key == 'trade_amount')
        )
        saved_amount = (await session.execute(stmt_amount)).scalar_one_or_none()
        if saved_amount:
            try:
                trade_amount = float(saved_amount)
            except (ValueError, TypeError):
                pass  # Используем значение по умолчанию

        # Получаем порог прибыли
        stmt_threshold = select(UserSetting.value).where(
            and_(UserSetting.user_id == user_id, UserSetting.key == 'profit_threshold')
        )
        saved_threshold = (await session.execute(stmt_threshold)).scalar_one_or_none()
        if saved_threshold:
            try:
                # Порог в БД хранится в %, а в коде используется как доля (e.g., 0.5% -> 0.005)
                profit_threshold = float(saved_threshold) / 100.0
            except (ValueError, TypeError):
                pass  # Используем значение по умолчанию

    return trade_amount, profit_threshold
