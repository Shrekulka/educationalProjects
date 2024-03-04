# middleware_example_bot/handlers/user_handlers.py

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from filters.filters import MyTrueFilter, MyFalseFilter
from lexicon.lexicon import LEXICON_RU
from logger_config import logger

# Инициализируем роутер уровня модуля
user_router: Router = Router()


# Этот хэндлер срабатывает на команду /start
@user_router.message(CommandStart(), MyTrueFilter())
async def process_start_command(message: Message) -> None:
    """
        Handles the /start command, greeting the user by name and sending them a message with a button.

        Args:
            message (Message): The incoming message from the user.

        Returns:
            None
    """
    # Записываем отладочное сообщение о входе в хэндлер команды /start
    logger.debug("Вошли в хэндлер, обрабатывающий команду /start")
    # Создаем кнопку для инлайн-клавиатуры
    button = InlineKeyboardButton(
        text='Кнопка',
        callback_data='button_pressed')
    # Создаем инлайн-клавиатуру с этой кнопкой
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    # Отправляем пользователю сообщение с инлайн-клавиатурой, приветствуя его по имени
    await message.answer(text=LEXICON_RU['/start'].format(first_name=message.from_user.first_name), reply_markup=markup)
    # Записываем отладочное сообщение о выходе из хэндлера команды /start
    logger.debug("Выходим из хэндлера, обрабатывающего команду /start")


# Этот хэндлер срабатывает на нажатие инлайн-кнопки
@user_router.callback_query(F.data, MyTrueFilter())
async def process_button_click(callback: CallbackQuery) -> None:
    """
        Handles the press of an inline button, sending the user a response about the button press.

        Args:
            callback (CallbackQuery): The callback query object containing information about the pressed button.

        Returns:
            None
    """
    # Записываем отладочное сообщение о входе в хэндлер нажатия на инлайн-кнопку
    logger.debug("Вошли в хэндлер, обрабатывающий нажатие на инлайн-кнопку")
    # Отправляем ответ о нажатии на кнопку
    await callback.answer(text=LEXICON_RU['button_pressed'])
    # Записываем отладочное сообщение о выходе из хэндлера нажатия на инлайн-кнопку
    logger.debug("Выходим из хэндлера, обрабатывающего нажатие на инлайн-кнопку")


# Этот хэндлер обрабатывает входящие текстовые сообщения, но фильтр MyFalseFilter блокирует его выполнение
@user_router.message(F.text, MyFalseFilter())
async def process_text(message: Message) -> None:
    """
        Handles incoming text messages, but the MyFalseFilter filter blocks the execution of the handler.

        Args:
            message (Message): The incoming text message from the user.

        Returns:
            None
    """
    # Записываем отладочное сообщение о входе в хэндлер обработки текста
    logger.debug("Вошли в хэндлер, обрабатывающий текст")
    # Записываем отладочное сообщение о выходе из хэндлера обработки текста
    logger.debug("Выходим из хэндлера, обрабатывающего текст")
