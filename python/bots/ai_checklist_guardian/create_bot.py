# ai_checklist_guardian/create_bot.py
# Библиотека aiogram (версия 2.25)
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from logger import logger

# Инициализация логгера с информацией о запуске бота
logger.info("Initializing bot...")
logger.debug("Bot token: %s", BOT_TOKEN)

# Инициализация хранилища состояний в памяти
storage = MemoryStorage()

# Создание экземпляров бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Логирование успешной инициализации бота
logger.info("Bot initialized successfully.")
