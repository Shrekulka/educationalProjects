# auto_ria_tracker/bot.py

import asyncio
import traceback

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config_data.config import config
from handlers import user_handlers
from services.car_service import CarService
from services.telegram_service import TelegramService
from database.database import Database
from logger_config import logger


async def main() -> None:
    """
    Main entry point for the bot. Initializes the bot, sets up necessary services,
    and starts polling for updates.

    This function performs the following steps:
    1. Initializes the bot and dispatcher.
    2. Initializes the services needed for the bot, including the database,
       Telegram service, and car service.
    3. Registers the user handler routers.
    4. Deletes any pending updates from the bot's webhook.
    5. Starts polling for incoming messages and commands.
    6. Handles errors that occur during polling and ensures that necessary
       shutdown tasks are performed, including cleaning up the car service
       and closing the bot's session.

    Raises:
        Exception: If a critical error occurs during the bot initialization or polling.
    """
    try:
        logger.info("Initializing bot...")

        # Инициализируем бот и диспетчер
        bot = Bot(token=config.tg_bot.token,
                  default=DefaultBotProperties(parse_mode='HTML'))
        dp = Dispatcher()

        # Инициализируем сервисы
        database = Database()
        telegram_service = TelegramService(bot, config.tg_bot.channel_id)
        car_service = CarService(database, telegram_service)

        # Сохраняем сервисы в хранилище данных диспетчера
        dp["bot"] = bot
        dp["car_service"] = car_service

        # Регистрация роутеров (обработчиков) для пользователей
        dp.include_router(user_handlers.router)

        # Удаляем накопившиеся обновления, если таковые имеются
        await bot.delete_webhook(drop_pending_updates=True)

        try:
            # Запуск процесса опроса новых сообщений и команд
            await dp.start_polling(bot)
        except Exception as e:
            logger.error(f"Error during polling: {e}")
        finally:
            logger.info("Starting cleanup...")
            try:
                # Завершаем работу с сервисом автомобилей
                await car_service.shutdown()
            except Exception as e:
                logger.error(f"Error during car service shutdown: {e}")
            finally:
                # Закрываем сессию бота
                await bot.session.close()

    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        raise


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Application terminated by the user")
    except Exception as error:
        logger.error(f"Unexpected error: {error}\n{traceback.format_exc()}")