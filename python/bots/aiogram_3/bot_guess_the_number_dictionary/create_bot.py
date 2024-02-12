# bot_guess_the_number_dictionary/create_bot.py

from aiogram import Bot
from aiogram import Dispatcher

from config import BOT_TOKEN
from logger import logger

# Инициализация логгера с информацией о запуске бота
logger.info("Initializing bot...")
logger.debug("Bot token: %s", BOT_TOKEN)

# Создание экземпляров бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Логирование успешной инициализации бота
logger.info("Bot initialized successfully.")
