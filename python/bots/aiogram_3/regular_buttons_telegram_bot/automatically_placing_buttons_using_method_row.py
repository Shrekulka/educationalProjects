# regular_buttons_telegram_bot/automatically_placing_buttons_using_method_row.py

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
    # Метод row у класса ReplyKeyboardBuilder позволяет расположить кнопки клавиатуры автоматически, в зависимости от
    # параметра width - желаемого количества кнопок в ряду. "Лишние" кнопки переносятся на следующий ряд.
    # Не смотря на то, что клиент Телеграм, как мы выяснили на предыдущем шаге, позволяет в одном ряду разместить до 12
    # кнопок, "строитель клавиатур" позволит разместить не больше 8. Попытка указать width больше 8 приведет к ошибке.

    # 1) Автоматическое размещение сначала 6-ти кнопок с параметром width=4, а затем еще 4-х кнопок с параметром width=3
    # Инициализируем билдер
    kb_builder = ReplyKeyboardBuilder()

    # Создаем первый список с кнопками
    buttons_1: list[KeyboardButton] = [KeyboardButton(text=f'Кнопка {i + 1}') for i in range(6)]

    # Создаем второй список с кнопками
    buttons_2: list[KeyboardButton] = [KeyboardButton(text=f'Кнопка {i + 7}') for i in range(4)]

    # Распаковываем список с кнопками в билдер, указываем, что в одном ряду должно быть 4 кнопки
    kb_builder.row(*buttons_1, width=4)

    # Еще раз распаковываем список с кнопками в билдер, указываем, что теперь в одном ряду должно быть 3 кнопки
    kb_builder.row(*buttons_2, width=3)
    # #############################################################
    # # 2) Автоматическое размещение 8 кнопок с параметром width=3
    # # Инициализируем билдер
    # kb_builder = ReplyKeyboardBuilder()
    #
    # # Создаем список с кнопками
    # buttons: list[KeyboardButton] = [KeyboardButton(text=f'Кнопка {i + 1}') for i in range(8)]
    #
    # # Распаковываем список с кнопками в билдер, указываем, что в одном ряду должно быть 3 кнопки
    # kb_builder.row(*buttons, width=3)
    # #############################################################
    # # 3) Автоматическое размещение 10 кнопок с параметром width=4
    # # Инициализируем билдер
    # kb_builder = ReplyKeyboardBuilder()
    #
    # # Создаем список с кнопками
    # buttons: list[KeyboardButton] = [KeyboardButton(text=f'Кнопка {i + 1}') for i in range(10)]
    #
    # # Распаковываем список с кнопками в билдер, указываем, что в одном ряду должно быть 4 кнопки
    # kb_builder.row(*buttons, width=4)

    ####################################################################################################################
    # Этот хэндлер будет срабатывать на команду "/start" и отправлять в чат клавиатуру
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text='Вот такая получается клавиатура',
                             # Отправка клавиатуры с установленным параметром resize_keyboard=True для автоматического
                             # изменения размера клавиатуры на устройствах с разными размерами экрана.
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