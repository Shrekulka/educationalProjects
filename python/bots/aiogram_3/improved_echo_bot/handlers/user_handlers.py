# improved_echo_bot/handlers/user_handlers.py

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU
from logger_config import logger

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    # Выводим апдейт в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer(text=LEXICON_RU['/start'].format(first_name=message.from_user.first_name))


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    # Выводим апдейт в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer(text=LEXICON_RU['/help'])
