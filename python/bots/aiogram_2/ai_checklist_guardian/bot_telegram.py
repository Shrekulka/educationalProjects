# ai_checklist_guardian/bot_telegram.py
# Библиотека aiogram (версия 2.25)
import traceback

from aiogram.utils import executor

from create_bot import dp
from data_base import sqlite_db
from logger import logger


async def on_startup(_) -> None:
    """
        Asynchronous function called on bot startup.
        - Prints information that the bot is online.
        - Connects or creates SQLite database.

        Parameters:
        - _: Unused parameter.

        Return type: None
    """

    logger.info("The bot is online")
    try:
        # Подключение к базе данных или её создание
        await sqlite_db.sql_start()
        logger.info('Connected to the database')
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error connecting to the database: {e}\n{detailed_send_message_error}")


# Регистрация обработчиков для клиента
from handlers import client
client.register_handlers_client(dp)

# Запуск поллинга (постоянного опроса) бота
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# telegram_bot/bot_telegram.py
# # Библиотека aiogram (версия 3.4.0)
# import asyncio
# import logging
# import sys
# import traceback
#
# from create_bot import dp, bot
# from data_base import sqlite_db
# from handlers import client
# from logger import logger
#
#
# # функция старта - это ф-ция, которая исполняется во время старта полинга нашего бота
# async def on_startup(_):
#     logger.info("The bot is online")
#     try:
#         # подключимся к нашей БД или создадим нашу БД
#         sqlite_db.sql_start()
#         logger.info('Connected to the database')
#     except Exception as e:
#         detailed_send_message_error = traceback.format_exc()
#         logger.error(f"Error connecting to the database: {e}\n{detailed_send_message_error}")
#
#     # Регистрация хэндлеров клиента
#     client.register_handlers_client(dp)
#
#z
# async def main() -> None:
#     # Запуск поллинга с передачей on_startup функции
#     await dp.start_polling(bot, on_startup=on_startup)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
