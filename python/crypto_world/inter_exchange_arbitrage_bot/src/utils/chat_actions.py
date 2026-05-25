# inter_exchange_arbitrage_bot/src/utils/chat_actions.py

import asyncio
import contextlib
from typing import Optional

from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InlineKeyboardMarkup
from src.utils.logger import logger


async def send_typing_action(chat_id: int, bot: Bot):
    """
    Отправляет индикатор 'печатает' каждые N секунд, пока работает фоновая задача.
    """
    while True:
        try:
            from src.constants import TYPING_INDICATOR_INTERVAL
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            await asyncio.sleep(TYPING_INDICATOR_INTERVAL)
        except asyncio.CancelledError:
            # Задача была отменена, это нормальное завершение
            break
        except Exception:
            # В случае других ошибок, просто прекращаем цикл
            break


@contextlib.asynccontextmanager
async def show_typing_status(chat_id: int, bot: Bot):
    """
    Асинхронный менеджер контекста, который показывает статус 'печатает'
    на время выполнения кода внутри блока 'async with'.
    """
    typing_task = asyncio.create_task(send_typing_action(chat_id, bot))
    try:
        yield
    finally:
        typing_task.cancel()


async def safe_edit_text(
        message: Message,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        log_text: str = "Message not modified"
):
    """
    Безопасно редактирует текст сообщения, перехватывая ошибку "message is not modified".
    """
    try:
        await message.edit_text(text=text, reply_markup=reply_markup)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            logger.debug(log_text)
        else:
            # Перевыбрасываем ошибку, если она не связана с отсутствием изменений
            raise
