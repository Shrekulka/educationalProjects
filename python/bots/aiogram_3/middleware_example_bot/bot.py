# middleware_example_bot/bot.py

import asyncio
import traceback

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config_data.config_data import config
from handlers import user_handlers, other_handlers
from handlers.other_handlers import other_router
from handlers.user_handlers import user_router
from logger_config import logger
from middlewares.inner import FirstInnerMiddleware, SecondInnerMiddleware, ThirdInnerMiddleware
from middlewares.outer import FirstOuterMiddleware, SecondOuterMiddleware, ThirdOuterMiddleware


# Функция конфигурирования и запуска бота
async def main() -> None:
    """
        Function to configure and run the bot.

        Initializes the bot and dispatcher, registers routers, skips accumulated updates,
        and starts polling.

        Returns:
            None
    """
    logger.info("Initializing bot...")
    # Инициализируем бот и диспетчер
    # Указывая parse_mod, мы даем понять боту, что некоторые HTML-теги, поддерживаемые API Telegram, нужно воспринимать
    # именно как HTML-теги.
    bot: Bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
    dp: Dispatcher = Dispatcher()
    logger.info("Bot initialized successfully.")

    # Регистрируем роутеры в диспетчере
    ####################################################################################################################
    dp.include_router(user_handlers.user_router)
    dp.include_router(other_handlers.other_router)
    ####################################################################################################################

    # Здесь будем регистрировать миддлвари
    ####################################################################################################################
    # Отвечает за то, чтобы через FirstOuterMiddleware проходили любые типы апдейтов (она подключена к корневому роутеру
    # на тип событий Update). То есть апдейт с командой /start обязательно попадет в FirstOuterMiddleware
    dp.update.outer_middleware(FirstOuterMiddleware())

    # Она отвечает за то, чтобы через SecondOuterMiddleware проходили апдейты типа CallbackQuery, но только в рамках
    # поиска хэндлеров, зарегистрированных на user_router. Хэндлер на команду /start у нас зарегистрирован на
    # user_router, одно условие выполнено. Но, вот, тип события не совпадает. Нам нужен Message, а данная миддлварь
    # будет работать для CallbackQuery. Значит, апдейт с командой /start не попадет в SecondOuterMiddleware.
    user_router.callback_query.outer_middleware(SecondOuterMiddleware())

    # Теперь для апдейта на команду /start у нас совпадает тип, но не совпадает роутер. Значит, ThirdOuterMiddleware
    # также не будет работать с нашим апдейтом.
    other_router.message.outer_middleware(ThirdOuterMiddleware())

    # Кажется, это то, что нам нужно. Хэндлер на команду /start зарегистрирован в user_router, а тип апдейта как раз
    # Message. То есть в FirstInnerMiddleware, по логике, мы с нашим стартом должны попасть.
    user_router.message.middleware(FirstInnerMiddleware())

    # Роутер совпадает, но тип события нет. То есть в SecondInnerMiddleware наш апдейт не попадет.
    user_router.callback_query.middleware(SecondInnerMiddleware())

    # Тип события совпадает, а, вот, роутер уже нет. Снова апдейт не попадет в миддлварь.
    other_router.message.middleware(ThirdInnerMiddleware())
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


