# regular_buttons_telegram_bot/the_input_field_showed_a_hint_line.py

import asyncio
import traceback

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
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
    # # 1) В поле ввода чтобы показывалась нужная строка-подсказка, когда клавиатура активна. в поле ввода блеклым серым
    # # цветом написано "Ничего вводить не нужно, нажимаем кнопки..."
    # Создаем кнопки
    button_1 = KeyboardButton(text='Кнопка 1')

    button_2 = KeyboardButton(text='Кнопка 2')

    # Создаем объект клавиатуры
    placeholder_exmpl_kb = ReplyKeyboardMarkup(
        keyboard=[[button_1, button_2]], resize_keyboard=True,
        input_field_placeholder="Ничего вводить не нужно, нажимаем кнопки...")

    ####################################################################################################################
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text='Экспериментируем с полем placeholder', reply_markup=placeholder_exmpl_kb)

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