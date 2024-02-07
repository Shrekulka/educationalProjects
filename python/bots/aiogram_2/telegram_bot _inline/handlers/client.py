from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


# перечисляем комманды на которые будет реагировать при помощи этого события

# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита!', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через Л/С напишите ему:\nhttps://t.me/My_telegram_For_MeBot')


# @dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пн-Чт с 9.00 до 20.00, Пт-Сб с 10.00 до 23.00')


# @dp.message_handler(commands=['Расположение'])
# reply_markup=ReplyKeyboardRemove() - удаляет нашу клавиатуру после сработки хендлера 'Расположение' и вернуть ее нельзя
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Рабочая, 115', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


# регистрируем все хедлеры и передаем их в файл bot_telegram
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_работы'])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])
