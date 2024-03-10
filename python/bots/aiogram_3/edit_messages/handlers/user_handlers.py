# edit_messages/handlers/user_handlers.py

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.more_button_keyboard import keyboard
from lexicon.lexicon import jokes, LEXICON_RU
from logger_config import logger
from services.services import random_joke

# Инициализируем роутер уровня модуля
user_router: Router = Router()


# Этот хэндлер будет срабатывать на команды "/start" и "/joke"
@user_router.message(Command(commands=['start', 'joke']))
async def process_start_command(message: Message) -> None:
    """
        Handles commands "/start" and "/joke" by sending a random joke as a response.

        This function processes messages that contain the commands "/start" or "/joke". It extracts a random joke from
        the 'jokes' dictionary using the 'random_joke' function from the services module and sends it as a response to
        the incoming message. Additionally, it logs information about the incoming message.

        Args:
            message (Message): The incoming message.

        Returns:
            None
    """
    # Вывод информации о сообщении в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))
    # Отправляем случайную шутку в ответ на сообщение. Текст шутки берется из словаря 'jokes' по случайному ключу,
    # полученному с помощью функции random_joke()
    await message.answer(text=jokes[random_joke()], reply_markup=keyboard)


# Этот хэндлер будет срабатывать при нажатии кнопки "Еще, без удаления!" и отправлять в чат новое сообщение с шуткой,
# не удаляя старое.
@user_router.callback_query(F.data == 'WITHOUT')
async def process_more_press(callback: CallbackQuery) -> None:
    """
        Handles the "More, without deletion!" button press by sending a new message with the next joke without deleting
        the old one.

        This function handles a callback query triggered by pressing the "MORE_BUTTON_TEXT_WITHOUT" button with the
        callback_data parameter equal to "WITHOUT". It sends a new joke in response to the original message without
        deleting it. Additionally, it acknowledges the callback query.

        Arguments:
            callback (CallbackQuery): The callback query triggered by pressing the "MORE_BUTTON_TEXT_WITHOUT" button.

        Returns:
            None
    """
    # Отвечаем на callback, чтобы убрать часики ожидания ответа.
    await callback.answer()
    # Отправляем случайную шутку в ответ на сообщение. Текст шутки берется из словаря 'jokes' по случайному ключу,
    # полученному с помощью функции random_joke()
    await callback.message.answer(text=jokes[random_joke()], reply_markup=keyboard)


# Этот хэндлер будет срабатывать при нажатии кнопки "Еще, с удалением!" и отправлять в чат новое сообщение с шуткой,
# при этом, удаляя старое.
@user_router.callback_query(F.data == 'WITH')
async def process_more_press(callback: CallbackQuery) -> None:
    """
        Handles the "More, with deletion!" button press by sending a new message with the next joke and deleting the
        old one.

        This function handles a callback query triggered by pressing the "MORE_BUTTON_TEXT_WITH" button with the
        callback_data parameter equal to "WITH". It sends a new joke in response to the original message and deletes
        the original message. Additionally, it acknowledges the callback query.

        Arguments:
            callback (CallbackQuery): The callback query triggered by pressing the "MORE_BUTTON_TEXT_WITH" button.

        Returns:
            None
    """
    # Удаляем сообщение, в котором была нажата кнопка
    await callback.message.delete()
    # Отправляем случайную шутку в ответ на сообщение. Текст шутки берется из словаря 'jokes' по случайному ключу,
    # полученному с помощью функции random_joke()
    await callback.message.answer(text=jokes[random_joke()], reply_markup=keyboard)


# Этот хэндлер будет срабатывать при нажатии кнопки "Еще, с редактированием!" и будет редактировать исходное сообщение.
@user_router.callback_query(F.data == 'EDIT')
async def process_more_press(callback: CallbackQuery) -> None:
    """
        Processes the command "More with editing!" click the button after editing the original message.

        This function handles a callback query triggered by pressing the "MORE_BUTTON_TEXT_EDIT" button with the
        callback_data parameter equal to "EDIT". It sends a new joke in response to the original message and edits the
        original message, replacing it with the new joke. Additionally, it acknowledges the callback query.

        Arguments:
            callback (CallbackQuery): The callback query triggered by pressing the "MORE_BUTTON_TEXT_EDIT" button.

        Returns:
            None
    """
    # Редактируем сообщение
    await callback.message.edit_text(text=jokes[random_joke()], reply_markup=keyboard)


# Этот хэндлер будет срабатывать на любые сообщения, кроме команд.
@user_router.message()
async def send_echo(message: Message) -> None:
    """
        Sends a response message with the text specified in the lexicon under the key "UNKNOWN_MESSAGE".

        This function handles any incoming message that does not contain a command. It sends a response message with
        the text specified in the lexicon under the key "UNKNOWN_MESSAGE".

        Args:
            message (Message): The incoming message.

        Returns:
            None
    """
    # Отправляем ответное сообщение с текстом, который находится в словаре LEXICON_RU под ключом "UNKNOWN_MESSAGE".
    await message.answer(text=LEXICON_RU["UNKNOWN_MESSAGE"])
