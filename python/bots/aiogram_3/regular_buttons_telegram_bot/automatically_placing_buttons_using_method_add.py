# regular_buttons_telegram_bot/automatically_placing_buttons_using_method_add.py

import asyncio
import traceback

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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
    # В отличие от метода row() метод add() добавляет кнопки с нового ряда только если в предыдущем ряду для новых
    # кнопок уже нет места. Причем, методу add все равно какой там у вас был параметр width до этого. Кнопки будут
    # добавляться в ряд пока их там не станет 8 и только потом начнут заполнять новый ряд. Тоже до 8 штук.

    # 1) Создадим клавиатуру, в которую добавим 5 кнопок методом row с параметром width=4, а затем добавим еще 10
    # кнопок методом add.
    # Инициализируем билдер
    kb_builder = ReplyKeyboardBuilder()

    # Создаем первый список с кнопками
    buttons_1: list[KeyboardButton] = [KeyboardButton(text=f'Кн. {i + 1}') for i in range(5)]

    # Создаем второй список с кнопками
    buttons_2: list[KeyboardButton] = [KeyboardButton(text=f'Кн. {i + 6}') for i in range(10)]

    # Распаковываем список с кнопками в билдер методом row, указываем, что в одном ряду должно быть 4 кнопки
    kb_builder.row(*buttons_1, width=4)

    # Распаковываем второй список с кнопками методом add
    kb_builder.add(*buttons_2)

    ####################################################################################################################
    # Этот хэндлер будет срабатывать на команду "/start" и отправлять в чат клавиатуру
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(
            text='Вот такая получается клавиатура',
            # Устанавливает клавиатуру в качестве ответа на сообщение с возможностью изменения размера клавиатуры.
            reply_markup=kb_builder.as_markup(resize_keyboard=True))

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