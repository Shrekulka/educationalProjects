# telegram_bot_book/handlers/other_handlers.py

import random

from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_CHOICE_ANSWER

# Создание объекта маршрутизатора для обработки запросов в боте
router = Router()


@router.message()
async def send_random_response(message: Message) -> None:
    """
        Sends a random response to the user.

        Args:
        message (Message): The user's message object.

        Returns:
        None

        This function selects a random response from the LEXICON_CHOICE_ANSWER dictionary,
        substitutes the user's name into the random response, and sends it to the user.
    """
    # Выбираем случайный ключ из словаря LEXICON_CHOICE_ANSWER
    random_key = random.choice(list(LEXICON_CHOICE_ANSWER.keys()))
    # Получаем случайный ответ по выбранному ключу
    random_response = LEXICON_CHOICE_ANSWER[random_key]
    # Подставляем имя пользователя в случайный ответ
    response = random_response.format(first_name=message.from_user.first_name)
    # Отправляем ответ пользователю
    await message.answer(response)
