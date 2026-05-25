# inter_exchange_arbitrage_bot/src/bot/filters/admin_filter.py

from aiogram.filters import BaseFilter
from aiogram.types import Message
from src.core.config import config

class AdminFilter(BaseFilter):
    """
    Фильтр для проверки, является ли пользователь администратором бота.
    """
    async def __call__(self, message: Message) -> bool:
        # Проверяем как для Message, так и для CallbackQuery
        user_id = message.from_user.id
        return user_id in config.tg_bot.admin_ids