# improved_echo_bot/bot.py

import asyncio
import traceback

from aiogram import Bot, Dispatcher

from config_data.config import config
from handlers import user_handlers, other_handlers
from logger_config import logger


# Функция конфигурирования и запуска бота
class DefaultBotProperties:
    pass


async def main() -> None:
    logger.info("Initializing bot...")
    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    logger.info("Bot initialized successfully.")

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

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
