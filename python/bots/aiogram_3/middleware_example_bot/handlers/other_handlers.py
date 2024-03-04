# middleware_example_bot/handlers/other_handlers.py
from aiogram import Router
from aiogram.types import Message

from filters.filters import MyTrueFilter
from lexicon.lexicon import LEXICON_RU
from logger_config import logger

# Инициализируем роутер уровня модуля
other_router: Router = Router()


# Этот хэндлер будет обрабатывать все входящие сообщения, которые не попадают под другие специфические хэндлеры
@other_router.message(MyTrueFilter())
async def send_echo(message: Message):
    # Записываем отладочное сообщение о входе в хэндлер
    logger.debug('Вошли в хэндлер эхо-сообщений')
    try:
        # Пытаемся отправить пользователю копию его собственного сообщения
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # Если возникает ошибка при отправке копии (например, из-за ограничений Телеграма),
        # отправляем пользователю сообщение о невозможности выполнить операцию эхо
        await message.reply(text=LEXICON_RU['no_echo'])
    # Записываем отладочное сообщение о выходе из хэндлера
    logger.debug('Выходим из хэндлера эхо-сообщений')
