# simple_echo_bot/handlers/client.py
import traceback

from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from create_bot import bot, dp


# Регистрация всех хэндлеров и передача их в файл bot_telegram
# @dp.message()
def register_handlers_client(dp: Dispatcher) -> None:
    """
        Register all handlers for the client part of the bot.

        Args:
            dp: The Dispatcher instance.
    """
    # Регистрируем хэндлеры
    dp.message.register(process_start_command, Command(commands='start'))
    dp.message.register(process_help_command, Command(commands='help'))

