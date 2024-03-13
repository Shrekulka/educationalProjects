# form_filling_bot_fsm/bot.py

import asyncio
import traceback

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis

from config_data.config_data import config
from handlers import user_handlers
from logger_config import logger

########################################################################################################################
# mode - определяет тип хранилища данных, которое будет использоваться ботом для сохранения состояний пользователей и
# другой информации во время работы.
########################################################################################################################
# mode = 1 (Redis): это отдельный сервис, который можно запустить на удаленном сервере, и сохранять в нем данные как в
# обычный питоновский словарь, то есть пары "ключ-значение". Причем, данные Redis держит в оперативной памяти,
# обеспечивая к ним очень быстрый доступ. Также данные периодически сохраняются на диск - делается снимок текущего
# состояния данных, повышая надежность сервиса.
########################################################################################################################
# mode = 2 (MemoryStorage): вся информация о состояниях хранится в оперативной памяти компьютера и стирается при
# перезапуске бота.
########################################################################################################################

mode: int = 1


# Функция конфигурирования и запуска бота
async def main() -> None:
    if mode == 1:
        # Инициализируем Redis
        redis = Redis(host='localhost')

        # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
        storage = RedisStorage(redis=redis)
        logger.info("Initializing bot...")
        # Инициализируем бот и диспетчер
        # Указывая parse_mod, мы даем понять боту, что некоторые HTML-теги, поддерживаемые API Telegram, нужно
        # воспринимать именно как HTML-теги.
        bot: Bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
        dp: Dispatcher = Dispatcher(storage=storage)
        logger.info("Bot initialized successfully.")

        # Сохраняем объект bot в хранилище workflow_data диспетчера dp. Это позволит использовать один и тот же объект
        # bot во всех обработчиках без необходимости явно передавать его из функции в функцию
        dp.workflow_data['bot'] = bot

        # Регистрируем роутеры в диспетчере
        dp.include_router(user_handlers.user_router)

        # Пропускаем накопившиеся апдейты и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    elif mode == 2:
        # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
        storage = MemoryStorage()

        logger.info("Initializing bot...")
        # Инициализируем бот и диспетчер
        # Указывая parse_mod, мы даем понять боту, что некоторые HTML-теги, поддерживаемые API Telegram, нужно
        # воспринимать именно как HTML-теги.
        bot: Bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
        dp: Dispatcher = Dispatcher(storage=storage)
        logger.info("Bot initialized successfully.")

        # Сохраняем объект bot в хранилище workflow_data диспетчера dp. Это позволит использовать один и тот же объект
        # bot во всех обработчиках без необходимости явно передавать его из функции в функцию
        dp.workflow_data['bot'] = bot

        # Регистрируем роутеры в диспетчере
        dp.include_router(user_handlers.user_router)

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
