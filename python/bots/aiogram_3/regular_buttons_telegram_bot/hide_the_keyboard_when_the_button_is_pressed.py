# regular_buttons_telegram_bot/hide_the_keyboard_when_the_button_is_pressed.py

import asyncio
import traceback

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message

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
    # Создаем объекты кнопок
    button_1: KeyboardButton = KeyboardButton(text='Собак 🦮')
    button_2: KeyboardButton = KeyboardButton(text='Огурцов 🥒')
    button_3 = KeyboardButton(text='Мышей 🐁')
    button_4 = KeyboardButton(text='Ежей 🦔')

    # Создаем объект клавиатуры, добавляя в него кнопки
    keyboard = ReplyKeyboardMarkup(
        # Кнопки располагаются в единственном ряду.
        keyboard=[[button_1, button_2, button_3, button_4]],
        # Параметр resize_keyboard установлен в True для обеспечения нормального размера кнопок.
        resize_keyboard=True,
        # Параметр one_time_keyboard установлен в True, чтобы клавиатура скрывалась после использования, но оставалась
        # доступной для повторного вызова.
        one_time_keyboard=True)

    ####################################################################################################################
    # Этот хэндлер будет срабатывать на команду "/start" и отправлять в чат клавиатуру
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(
            text="Чего кошки боятся больше?",
            # Отправляем сообщение с текстом "Чего кошки боятся больше?" и прикрепляем к нему клавиатуру `keyboard`.
            reply_markup=keyboard)

    # Этот хэндлер будет срабатывать на ответ "Собак 🦮"
    @dp.message(F.text == 'Собак 🦮')
    async def process_dog_answer(message: Message):
        await message.answer(text="Да, несомненно, кошки боятся собак. Но вы видели как они боятся огурцов?")

    # Этот хэндлер будет срабатывать на ответ "Огурцов 🥒"
    @dp.message(F.text == 'Огурцов 🥒')
    async def process_cucumber_answer(message: Message):
        await message.answer(text="Да, иногда кажется, что огурцов кошки боятся больше")

    # Этот хэндлер будет срабатывать на ответ "Мышей 🐁"
    @dp.message(F.text == 'Мышей 🐁')
    async def process_cucumber_answer(message: Message):
        await message.answer(text="Да, иногда кажется, что мышей собаки боятся больше")

    # Этот хэндлер будет срабатывать на ответ "Ежей 🦔"
    @dp.message(F.text == 'Ежей 🦔')
    async def process_cucumber_answer(message: Message):
        await message.answer(text="Да, иногда кажется, что ежей собаки боятся больше")

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