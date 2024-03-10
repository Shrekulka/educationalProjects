# improved_echo_bot/handlers/other_handlers.py

from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU
from logger_config import logger

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер будет срабатывать на любые ваши сообщения, кроме команд "/start" и "/help"
async def send_echo(message: Message) -> None:
    """
        Sends a copy of the received message back to the user, excluding the commands "/start" and "/help".

        Args:
        message (Message): The message object.

        Returns:
        None
    """
    # Выводим апдейт в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))
    try:
        # Пытаемся отправить копию полученного сообщения обратно пользователю
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # Если не удается отправить копию, отправляем пользователю текст об ошибке из словаря
        await message.reply(text=LEXICON_RU['no_echo'])
