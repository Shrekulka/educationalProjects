# formatting_text_in_messages/handlers/user_handlers.py

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU
from logger_config import logger

# Инициализируем роутер уровня модуля
user_router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@user_router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
        Processes the /start command by sending a welcome message to the user.

        Args:
        message (Message): The incoming message object.

        Returns:
        None
    """
    # Выводим апдейт в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))
    # Отправляем ответное сообщение пользователю с текстом из словаря LEXICON_RU, подставляя имя пользователя
    await message.answer(text=LEXICON_RU['/start'].format(first_name=message.from_user.first_name))


# Этот хэндлер будет срабатывать на команду "/help"
@user_router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    """
        Processes the /help command by sending informational help to the user.

        Args:
        message (Message): The incoming message object.

        Returns:
        None
    """
    # Отправляем ответное сообщение пользователю с текстом из словаря LEXICON_RU по ключу '/help'
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на команду "/html"
@user_router.message(Command(commands='html'))
async def process_html_command(message: Message) -> None:
    """
        Processes the /html command by sending a message to the user with HTML markup.

        Args:
        message (Message): The incoming message object.

        Returns:
        None
    """
    # Отправляем ответное сообщение пользователю с текстом из словаря LEXICON_RU и указываем парсеру, что текст
    # содержит разметку HTML
    await message.answer(text=LEXICON_RU['/html'], parse_mode='HTML')


# Этот хэндлер будет срабатывать на команду "/markdownv2"
@user_router.message(Command(commands='markdownv2'))
async def process_markdownv2_command(message: Message) -> None:
    """
        Processes the /markdownv2 command by sending a message to the user with MarkdownV2 markup.

        Args:
        message (Message): The incoming message object.

        Returns:
        None
    """
    # Отправляем ответное сообщение пользователю с текстом из словаря LEXICON_RU и указываем парсеру, что текст
    # содержит разметку MarkdownV2
    await message.answer(text=LEXICON_RU['/markdownv2'], parse_mode='MarkdownV2')


# Этот хэндлер будет срабатывать на команду "/noformat"
@user_router.message(Command(commands='noformat'))
async def process_noformat_command(message: Message) -> None:
    """
        Processes the /noformat command by sending a message to the user without any additional formatting.

        Args:
        message (Message): The incoming message object.

        Returns:
        None
    """
    # Отправляем ответное сообщение пользователю с текстом из словаря LEXICON_RU без указания парсера, чтобы текст
    # отображался без какой-либо дополнительной разметки
    await message.answer(text=LEXICON_RU['/noformat'])


# Этот хэндлер будет срабатывать на любые сообщения, кроме команд, отлавливаемых хэндлерами выше
@user_router.message()
async def send_echo(message: Message) -> None:
    """
        Handles any messages other than commands caught by other handlers.

        Args:
        message (Message): The incoming message object.

        Returns:
        None
    """
    # Отправляем ответное сообщение пользователю с текстом из словаря LEXICON_RU для отображения сообщения о
    # непонимании введенной команды
    await message.answer(text=LEXICON_RU['/echo'])
