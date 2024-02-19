# regular_buttons_telegram_bot/special_regular_buttons.py

import asyncio
import traceback

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import KeyboardButton, Message, KeyboardButtonPollType, ReplyKeyboardMarkup, WebAppInfo
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
    # Существует 6 типов специальных обычных кнопок:
    # Для отправки своего телефона (параметр request_contact)
    # Для отправки своей геопозиции (параметр request_location)
    # Для создания опроса/викторины (параметр request_poll)
    # Для запуска Web-приложений прямо в Телеграм (параметр web_app)
    # (параметр request_user)
    # (параметр request_chat)

    # 1) Создадим клавиатуру, отправки телефона - request_contact=True, для отправки геопозиции - request_location=True,
    # для создания викторины - request_poll=KeyboardButtonPollType()

    # Инициализируем билдер
    kb_builder = ReplyKeyboardBuilder()

    # Создаем кнопки
    contact_btn = KeyboardButton(text='Отправить телефон', request_contact=True)

    geo_btn = KeyboardButton(text='Отправить геолокацию', request_location=True)

    poll_btn = KeyboardButton(text='Создать опрос/викторину', request_poll=KeyboardButtonPollType())

    # Добавляем кнопки в билдер
    kb_builder.row(contact_btn, geo_btn, poll_btn, width=1)

    # Создаем объект клавиатуры
    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    # #############################################################
    # # 2) Можно конкретизировать, что именно (опрос или викторина) будет создаваться по кнопке, если в
    # # KeyboardButtonPollType передать соответствующий тип:

    # Создаем кнопки
    poll_btn_2 = KeyboardButton(text='Создать опрос', request_poll=KeyboardButtonPollType(type='regular'))

    quiz_btn = KeyboardButton(text='Создать викторину', request_poll=KeyboardButtonPollType(type='quiz'))

    # Инициализируем билдер
    poll_kb_builder = ReplyKeyboardBuilder()

    # Добавляем кнопки в билдер
    poll_kb_builder.row(poll_btn_2, quiz_btn, width=1)

    # Создаем объект клавиатуры
    poll_keyboard: ReplyKeyboardMarkup = poll_kb_builder.as_markup(resize_keyboard=True)

    # #############################################################
    # # 3) Запускаем веб-приложения прямо внутри самого Телеграм. Web-приложения открываются только по защищенному
    # # протоколу (https).

    # Создаем кнопку
    web_app_btn = KeyboardButton(text='Start Web App', web_app=WebAppInfo(url="https://stepik.org/"))
    # Создаем объект клавиатуры
    web_app_keyboard = ReplyKeyboardMarkup(keyboard=[[web_app_btn]], resize_keyboard=True)

    ####################################################################################################################
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text='Экспериментируем со специальными кнопками', reply_markup=keyboard)

    # Этот хэндлер будет срабатывать на команду "/poll"
    @dp.message(Command(commands='poll'))
    async def process_poll_command(message: Message):
        await message.answer(text='Экспериментируем с кнопками опрос/викторина', reply_markup=poll_keyboard)

    # Этот хэндлер будет срабатывать на команду "/web_app"
    @dp.message(Command(commands='web_app'))
    async def process_web_app_command(message: Message):
        await message.answer(text='Экспериментируем со специальными кнопками', reply_markup=web_app_keyboard)

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