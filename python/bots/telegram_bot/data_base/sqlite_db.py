# telegram_bot/data_base/sqlite_db.py

import sqlite3 as sq
from create_bot import bot


# определяем функцию, в которой пишем создание БД или подключение, если она создана
def sql_start():
    global base, cur
    # метод connect позволяет подключиться к файлу БД, если такого файла не будет, он создастся
    base = sq.connect('pizza_cool.db')
    # создаем cursor - это та чать БД, которая осуществляет поиск, встраивание и выборку данных из БД
    cur = base.cursor()
    # когда бот подключается к БД, выводит в терминал сообщение
    if base:
        print('Data base connected OK!')
    # создаем таблицу, в которую будем вносить данные
    # CREATE TABLE IF NOT EXISTS - позволяет создать таблицу, если такой не существует, если есть игнорируем эту строку
    # menu(img TEXT, name TEXT PIMARY KEY, description TEXT, price TEXT) - создаем таблицу меню в которой будет 4-ре
    # столбца 1) кртинка; почему TEXT - здесь ID картинки; 2) название пиццы; PIMARY KEY - это первичны ключ
    # (повторяться названия не будут); 3) описание; 4) цена - тоже текстовая
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PIMARY KEY, description TEXT, price TEXT)')
    # и сохраняем эти изменения
    base.commit()


# вторая ф-ция, в которой будем записывать изменения в нашу БД
async def sql_add_command(state):  # state - параметр, куда попадает наше Машина состояние бота
    # здесь открываем наш словарь
    async with state.proxy() as data:
        # используя наш cursor командой execute(исполнить) вставляем в таблицу меню значения (подставляем безопастно
        # (?, ?, ?, ?) для избежания sql инъекций) и переводим в кортеж значения data.values
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        # и сохраняем эти изменения
        base.commit()


# получаем сюда событие сообщения, когда срабатывет хендлер на кнопку Меню
async def sql_read(message):
    # в цыкле for делаем sql команду SELECT * FROM Menu - выбрать все из таблицы меню, fetchall() выгружаем все в виде
    # списка и помещаем это все в переменную ret
    for ret in cur.execute('SELECT * FROM Menu').fetchall():
        # отправляем каждую строку этой таблицы  пользователю в личку разбирая ее
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')


# предназначена для того, что бы сделать выборку с нашей таблицы базы данных
async def sql_read2():
    return cur.execute('SELECT * FROM Menu').fetchall()


# сюда передается название пиццы
async def sql_delete_command(data):
    # из БД посылаем sql запрос удалить по названию конкретную запись
    cur.execute('DELETE FROM menu WHERE name ==?', (data,))
    base.commit()
