# regular_buttons_telegram_bot/automatically_placing_buttons_using_method_adjust.py

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
    # Чтобы указать какое количество кнопок должно быть в каждом ряду - нужно передать в метод adjust целые числа (от 1
    # до 8), начиная с первого ряда. Причем данный метод будет игнорировать параметр width, если кнопки были добавлены
    # в билдер методом row.
    # Можно указывать количество кнопок не для всех рядов. Тогда последующие ряды будут заполняться кнопками по значению
    # последнего переданного аргумента. То есть, если у нас 7 кнопок, а мы в adjust добавили 2 и 1, то в первом ряду
    # будет 2 кнопки, а во втором и последующих по одной.

    # 1) Создадим клавиатуру, добавив 8 кнопок методом add и расставим их так, чтобы в 1-м ряду была одна кнопка, во
    # втором - 3, а остальные расставились бы автоматически.
    # Инициализируем билдер
    kb_builder = ReplyKeyboardBuilder()

    # Создаем первый список с кнопками
    buttons_1: list[KeyboardButton] = [KeyboardButton(text=f'Кнопка {i + 1}') for i in range(8)]

    # Распаковываем список с кнопками методом add
    kb_builder.add(*buttons_1)

    # Явно сообщаем билдеру сколько хотим видеть кнопок в 1-м и 2-м рядах
    kb_builder.adjust(1, 3)

    # #############################################################
    # # 2) Создадим клавиатуру с 10 кнопками, переданными в билдер методом add и методом adjust разместим их по две в
    # # каждом нечетном ряду и по 1 в каждом четном.
    # # Инициализируем билдер
    # kb_builder = ReplyKeyboardBuilder()
    #
    # # Создаем первый список с кнопками
    # buttons_1: list[KeyboardButton] = [KeyboardButton(text=f'Кнопка {i + 1}') for i in range(10)]
    # 
    # # Распаковываем список с кнопками методом add
    # kb_builder.add(*buttons_1)
    #
    # # Явно сообщаем билдеру сколько хотим видеть кнопок в 1-м и 2-м рядах, а также говорим методу повторять такое
    # # размещение для остальных рядов
    # kb_builder.adjust(2, 1, repeat=True)

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