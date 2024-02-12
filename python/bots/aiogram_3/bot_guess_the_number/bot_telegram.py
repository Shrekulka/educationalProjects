# bot_guess_the_number/bot_telegram.py
import asyncio
import traceback

from create_bot import dp, bot
from data_base import sqlite_db
from handlers import client
from logger import logger


async def main() -> None:
    """
        Main function to start the bot.

        Returns:
            None
    """
    logger.info("The bot is online")
    try:
        # подключимся к нашей БД или создадим нашу БД
        await sqlite_db.sql_start()
        # Регистрируем обработчики клиента
        client.register_handlers_client(dp)
        logger.info('Connected to the database')
        # Запускаем опрос бота
        await dp.start_polling(bot)  # dp.run_polling(bot)
    except Exception as e:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error connecting to the database: {e}\n{detailed_send_message_error}")


if __name__ == "__main__":
    asyncio.run(main())
