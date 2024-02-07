# telegram_bot/bot_telegram.py

from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db


# функция старта - это ф-ция, которая исполняется во время старта полинга нашего бота
async def on_startup(_):
    print('Бот вошел в онлайн')
    # подключимся к нашей БД или создадим нашу БД
    sqlite_db.sql_start()

from handlers import client, admin, other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

# старт нашего поллинга (старт входа)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
