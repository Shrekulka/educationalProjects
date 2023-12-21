# Для анатации типа т.е. указываем в хендлере то, что хендлер используется в Машина состояний
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None


# Создаем клас наших состояний, наследуемся от класа StatesGroup
# У нас будет 4-ре состояний(пункты последовательных вопросов)
# Этот клас необходим, чтобы бот переходил между этими состояниями. Переход напишем в хендлере

class FSMAdmin(StatesGroup):
    # отправка фотографии для нашей пицерии(отправляем фото пицы)
    photo = State()
    # наименование нашей пицы
    name = State()
    # описание нашей пицы
    description = State()
    # цена нашей пицы
    price = State()


# Для проверки является ли пользователь модератором нашей группы и модератором бота
# Получаем ID текущего модератора
# @dp.message_handler(commands=['Moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    # reply_markup=admin_kb.button_case_admin - добавляем клавиатуру админа
    await bot.send_message(message.from_user.id, 'Что хозяину угодно???', reply_markup=admin_kb.button_case_admin)
    await message.delete()  # удалаем сообщение из группового чата


# Хендлер который запускает Машину состояний
# Начало дифлога загрузки нового меню
# @dp.message_handler(commands=['Загрузить'], state=None)
async def cm_start(message: types.Message):  # бот переходит в состояние ожидания загрузки фото
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузите фото')


# Выход из состояний
# @dp.message_handler(state="*", commands='Отмена')  # "*" - обозначает в каком бы бот ненаходился состоянии
# @dp.message_handler(Text(equals='Отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()  # проверяем в каком состоянии находится бот
        if current_state is None:  # Если бот ненаходится ни в каком состоянии команда 'Отмена' не сработает
            return
        await state.finish()  # Если бот ненаходится в каком либо состоянии то закрываем Машину состояния
        await message.reply('OK')  # И выводим какое либо сообщение


# Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Теперь введите название")


# Ловим следующий (второй) ответ пользователя
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите описание")


# Ловим следующий (третий) ответ пользователя
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь укажите цену")


# Ловим последний ответ и использеум полученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        # просто выведем нашим ботом всю информацию в наш чат
        # async with state.proxy() as data:
        #     await message.reply(str(data))

        # запускаем ф-цию, в которой будем записывать изменения в нашу БД и передаем полученный ранее словарь - state
        await sqlite_db.sql_add_command(state)

        # бот выходит из Машина состояния и полностью очищает все что было записано
        await state.finish()


# если событие начинается с 'del ' срабатывет этот хендлер
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    # запускаем ф-цию, которая удалит по названию пиццы конкретную запись из БД
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    # отвечаем телеграмму, что запрос выполнен и отправляем администратору, что такае-то пицца удалена
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")}) удалена.', show_alert=True)


# Добавляем нашему администратору кнопку удалить
# @dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    # Проверяем является ли он модератором
    if message.from_user.id == ID:
        # в переменную read читаем выборку с нашей таблицы базы данных
        read = await sqlite_db.sql_read2()
        # по получившемуся списку меню проходим циклом фор
        for ret in read:
            # отправляем администратору и в личку клиенту фото, описание и цену нашей пицы
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            # к каждому отправлению добавляем одну инлайн кнопку в личку клиенту
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


# Регистрирем наши хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['Moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands='Удалить')
    # dp.callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
