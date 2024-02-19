# bot_rock_paper_scissors/handlers/other_handlers.py

from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_RU

# Создание объекта маршрутизатора для обработки запросов в боте
router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message) -> None:
    """
        Handles messages that did not match any other handlers.

        Replies to the user with a predefined message from the lexicon.

        Args:
            message (Message): The incoming message.

        Returns:
            None
    """
    await message.answer(text=LEXICON_RU['other_answer'])
