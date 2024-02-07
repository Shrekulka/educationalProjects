import json
import string
from aiogram import types, Dispatcher


# фильтр мата


# @dp.message_handler()
# будут попадать все сообщения для бота, которые отправляют пользователи в чат
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}.intersection(
            set(json.load(open('cenz.json')))) != set():
        await message.reply('Маты запрещены!')
        await message.delete()


# if message.text == 'Привет':
# await message.answer('И тебе привет!')  # из события получаем текст
# await message.reply(message.text)  # упоминает сообщение на которое отвечает бот
# await bot.send_message(message.from_user.id, message.text) # сработает только в том случае если пользователь когда-либо писал боту

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
