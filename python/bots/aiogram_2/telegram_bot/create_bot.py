# telegram_bot/create_bot.py

from config import TOKEN
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

# Машина состояний -позволяет задать пользователю ряд взаимосвязанных вопросов и запомнить ряд ответов от пользователей
# необходимо указать хранилище, в котором бот будет хранить эти данные. Для этого есть несколько хранилищ.
# from aiogram.contrib.fsm_storage.memory import MemoryStorage - данные хранятся в оперативной памяти. Если бот вылетит
# (выйдет в офлайн) данные потеряются
# from aiogram.contrib.fsm_storage.mongo import MongoStorage - база данных Mongo - используют для важной информации
# from aiogram.contrib.fsm_storage.redis import RedisStorage - база данных Redis - используют для важной информации
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# в этом файле создаем экземпляры нашего бота
bot = Bot(token=TOKEN)
# (storage = storage) - место, где будем хранить ответы от пользователя
dp = Dispatcher(bot, storage=storage)
