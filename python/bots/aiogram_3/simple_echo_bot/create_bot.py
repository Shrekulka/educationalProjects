# simple_echo_bot/create_bot.py

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode

from config_data.config import Config
from logger import logger
# Инициализация диспетчера
dp = Dispatcher()

# Создание экземпляра конфигурации
config = Config()

# Получение токена бота из конфигурации
BOT_TOKEN = config.tg_bot.token

# Инициализация логгера с информацией о запуске бота
logger.info("Initializing bot...")
logger.debug(f"Bot token: {BOT_TOKEN}")

# Создание экземпляров бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

# Логирование успешной инициализации бота
logger.info("Bot initialized successfully.")
