# inline_сallback_buttons/handlers/user_handlers.py

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards.keyboards import keyboard
from lexicon.lexicon_ru import LEXICON_RU
from logger_config import logger

# Создание объекта маршрутизатора для обработки сообщений
router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
        Handler for the "/start" command.

        Sends a response message with text and a keyboard.

        Parameters:
            message (Message): The message object.

        Returns:
            None
    """
    # Вывод информации о сообщении в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))
    # Отправка ответного сообщения с текстом и клавиатурой
    await message.answer(text=LEXICON_RU["/start"], reply_markup=keyboard)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery с data 'big_button_1_pressed'
@router.callback_query(F.data == "callback_button_1")
async def process_button_1_press(callback: CallbackQuery) -> None:
    """
        Handler for pressing the "callback_button_1" button.

        Checks the current message text and edits it if it does not match the expected text.
        Sends a response message with text and action confirmation.

        Parameters:
            callback (CallbackQuery): The callback query object.

        Returns:
            None
    """
    # Вывод информации о сообщении в терминал
    logger.info(callback.message.model_dump_json(indent=4, exclude_none=True))
    # Проверяем текст текущего сообщения и сравниваем его с текстом, который должен быть отображен на кнопке
    # "callback_button_1"
    if callback.message.text != LEXICON_RU["text_button_1"]:
        # Редактируем текст текущего сообщения, заменяя его на текст, указанный в словаре LEXICON_RU для кнопки
        # "callback_button_1", и сохраняем текущую клавиатуру сообщения
        await callback.message.edit_text(text=LEXICON_RU["text_button_1"], reply_markup=callback.message.reply_markup)
    # Отправляем ответное сообщение пользователю с указанным текстом и подтверждаем выполнение действия с показом
    # алерта, который автоматически закроется
    await callback.answer(text=LEXICON_RU["text_answer_1"])


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery с data 'big_button_2_pressed'
@router.callback_query(F.data == "callback_button_2")
async def process_button_2_press(callback: CallbackQuery) -> None:
    """
        Handler for pressing the "callback_button_2" button.

        Checks the current message text and edits it if it does not match the expected text.
        Sends a response message with text and action confirmation, and also shows an alert.

        Parameters:
            callback (CallbackQuery): The callback query object.

        Returns:
            None
    """
    # Вывод информации о сообщении в терминал
    logger.info(callback.message.model_dump_json(indent=4, exclude_none=True))
    # Проверяем текст текущего сообщения и сравниваем его с текстом, который должен быть отображен на кнопке
    # "callback_button_2"
    if callback.message.text != LEXICON_RU["text_button_2"]:
        # Редактируем текст текущего сообщения, заменяя его на текст, указанный в словаре LEXICON_RU для кнопки
        # "callback_button_2", и сохраняем текущую клавиатуру сообщения
        await callback.message.edit_text(text=LEXICON_RU["text_button_2"], reply_markup=callback.message.reply_markup)
    # Отправляем ответное сообщение пользователю с указанным текстом и подтверждаем выполнение действия с показом
    # алерта, который нужно закрыть нажатием на клавише OK
    await callback.answer(text=LEXICON_RU["text_answer_2"], show_alert=True)
