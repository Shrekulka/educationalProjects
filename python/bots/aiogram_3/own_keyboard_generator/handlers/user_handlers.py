# own_keyboard_generator/handlers/user_handlers.py

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.keyboard_generator_function import create_inline_kb
from lexicon.lexicon_ru import BUTTONS
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
    ####################################################################################################################
    # 1) Создаем инлайн-клавиатуру с шириной 2 кнопки, задавая список кнопок ['but_1', 'but_3'] и текст последней
    # кнопки 'but_7'
    keyboard = create_inline_kb(2, ['but_1', 'but_3'], 'but_7')
    # Отправляем ответное сообщение с текстом и созданной клавиатурой
    await message.answer(text="№1 Это инлайн-клавиатура, сформированная из списка кнопок",
                         reply_markup=keyboard)
    ####################################################################################################################
    # 2) Создаем инлайн-клавиатуру с шириной 4 кнопки, используя все кнопки из словаря BUTTONS
    keyboard = create_inline_kb(4, **BUTTONS)
    # Отправляем ответное сообщение с текстом и созданной клавиатурой
    await message.answer(text="№2 Это инлайн-клавиатура, сформированная из словаря BUTTONS",
                         reply_markup=keyboard)
    ####################################################################################################################
    # 3) Создаем инлайн-клавиатуру с шириной 4 кнопки, используя все кнопки из словаря BUTTONS и добавляем последнюю
    # кнопку 'Последняя кнопка'
    keyboard_with_last_btn = create_inline_kb(4, last_btn='Последняя кнопка', **BUTTONS)
    # Отправляем ответное сообщение с текстом и созданной клавиатурой
    await message.answer(text="№3 Это инлайн-клавиатура с последней кнопкой 'Последняя кнопка'",
                         reply_markup=keyboard_with_last_btn)
    ####################################################################################################################
    # 4) Создаем инлайн-клавиатуру с шириной 2 кнопки и именованными аргументами для кнопок
    keyboard_with_named_args = create_inline_kb(
        2,
        btn_tel='Телефон',
        btn_email='email',
        btn_website='Web-сайт',
        btn_vk='VK',
        btn_tgbot='Наш телеграм-бот')
    # Отправляем ответное сообщение с текстом и созданной клавиатурой
    await message.answer(text="№4 Это инлайн-клавиатура с именованными аргументами для кнопок",
                         reply_markup=keyboard_with_named_args)
    ####################################################################################################################

