# regular_buttons_telegram_bot/creation_and_placement_of_buttons.py

import asyncio
import traceback

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from config_data.config import Config
from logger_config import logger


# Функция конфигурирования и запуска бота
async def main() -> None:
    # Загружаем конфиг в переменную config
    config: Config = Config()

    logger.info("Initializing bot...")
    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()
    logger.info("Bot initialized successfully.")
    ####################################################################################################################
    # 1) Создаем клавиатуру из 3-х рядов кнопок по 3 кнопки в каждом ряду.
    # Создаем объекты кнопок
    button_1 = KeyboardButton(text='Кнопка 1')
    button_2 = KeyboardButton(text='Кнопка 2')
    button_3 = KeyboardButton(text='Кнопка 3')
    button_4 = KeyboardButton(text='Кнопка 4')
    button_5 = KeyboardButton(text='Кнопка 5')
    button_6 = KeyboardButton(text='Кнопка 6')
    button_7 = KeyboardButton(text='Кнопка 7')
    button_8 = KeyboardButton(text='Кнопка 8')
    button_9 = KeyboardButton(text='Кнопка 9')

    # Создаем объект клавиатуры, добавляя в него кнопки
    my_keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1, button_2, button_3],
                  [button_4, button_5, button_6],
                  [button_7, button_8, button_9]],
        resize_keyboard=True)

    # #############################################################
    # # 2) Сократив количество строк кода через генераторы коллекций
    # keyboard: list[list[KeyboardButton]] = [[KeyboardButton(
    #     text=f'Кнопка {j * 3 + i}') for i in range(1, 4)] for j in range(3)]
    #
    # # Создаем объект клавиатуры, добавляя в него кнопки
    # my_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    # #############################################################
    # # 3) Клавиатура из 9 кнопок в 5 рядах
    # # Генерируем список с кнопками
    # buttons: list[KeyboardButton] = [KeyboardButton(text=f'Кнопка {i}') for i in range(1, 10)]
    #
    # # Составляем список списков для будущей клавиатуры
    # keyboard: list[list[KeyboardButton]] = [
    #     [buttons[0]],
    #     buttons[1:3],
    #     buttons[3:6],
    #     buttons[6:8],
    #     [buttons[8]]]
    #
    # # Создаем объект клавиатуры, добавляя в него список списков с кнопками
    # my_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    # #############################################################
    # # 4) 2 ряда кнопок по 30 кнопок в каждом ряду.
    # # Генерируем список с кнопками
    # buttons_1: list[KeyboardButton] = [KeyboardButton(text=f'{i}') for i in range(1, 31)]
    #
    # # Генерируем список с кнопками
    # buttons_2: list[KeyboardButton] = [KeyboardButton(text=f'{i}') for i in range(31, 61)]
    #
    # # Составляем список списков для будущей клавиатуры
    # keyboard: list[list[KeyboardButton]] = [buttons_1, buttons_2]
    #
    # # Создаем объект клавиатуры, добавляя в него список списков с кнопками
    # my_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    ####################################################################################################################
    # Этот хэндлер будет срабатывать на команду "/start" и отправлять в чат клавиатуру
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text='Вот такая получается клавиатура', reply_markup=my_keyboard)

    ####################################################################################################################
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    # Обработка прерывания пользователем
    except KeyboardInterrupt:
        logger.warning("Application terminated by the user")
    # Обработка неожиданных ошибок
    except Exception as error:
        # Получение подробной информации об ошибке
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Unexpected error in the application: {error}\n{detailed_send_message_error}")