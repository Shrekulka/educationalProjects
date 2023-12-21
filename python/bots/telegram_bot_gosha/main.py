import telebot
from telebot import types

# подключаем к нашему боту
bot = telebot.TeleBot('your_token')


# все методы и параметры - https://pypi.org/project/pyTelegramBotAPI/
# https://pytba.readthedocs.io/ru/latest/index.html

# Для отслеживания команд нужно прописать декоратор
@bot.message_handler(commands=['start'])
# в параметр message помещается все: что ввел пользователь (команду: сообщение)
def start(message):
    # создаем переменную, куда получаем имя и фамилию пользователя
    mess = f'Привет <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
    # для ответа пользователю нам нужно обратиться к нашему боту и к методу send(в этом методе указываем два параметра)
    # 1) в какой чат будем отсылать ответ - message.chat.id - в тот чат с которого пришло сообщение
    # 2) mess
    # 3) режим в котором отправляется текст
    bot.send_message(message.chat.id, mess, parse_mode='html')


# для отслеживания любого текста, который пользователь будет вводить; пустые скобки означают любой текс -
# @bot.message_handler() или (content_types=['text'])
# @bot.message_handler(content_types=['text'])
# def get_user_text(message):
#     # будем выводить всю информацию, которая содержится в message
#     # bot.send_message(message.chat.id, message, parse_mode='html')
#
#     # проверка на совпадение
#     if message.text == "Hello":
#         bot.send_message(message.chat.id, "И тебе привет!", parse_mode='html')
#     elif message.text == "id":
#         bot.send_message(message.chat.id, f"Твой ID: {message.from_user.id}", parse_mode='html')
#     elif message.text == "photo":
#         photo = open('1649982839_5-kartinkof-club-p-yaitsa-prikolnie-kartinki-6.jpg', 'rb')
#         bot.send_photo(message.chat.id, photo)
#
#     else:
#         bot.send_message(message.chat.id, "Я тебя не понимаю!", parse_mode='html')


# Обрабатываем отправленные боту документы в [] - указываем какой контент мы отслеживаем
@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Вау, какое крутое фото!!!')


# Создание кнопок
@bot.message_handler(commands=['website'])
# если пользователь введет команду 'website' то мы вместе с текстом будем показывать набор различных кнопок
def website(message):
    markup = types.InlineKeyboardMarkup()  # создание обычной кнопки встроенной в сообщение
    # скомпановываем в одну единую структуру. Первый параметр - текст написанный на кнопке, второй - url адрес
    markup.add(types.InlineKeyboardButton("Посетить веб сайт", url="https://www.google.ru/"))
    # reply_markup=markup - прикрепляем кнопку
    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)


# Создание кнопок
@bot.message_handler(commands=['help'])
def website(message):
    # создание отдельных кнопок, там где и ввод сообщений. resize_keyboard=True - чтоб кнопки корректно выглядили
    # row_width=1 - ширина ряда, т.е. в ряд одна кнпка 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    website = types.KeyboardButton('Веб сайт')  # создание непосредственно кнопоки
    start = types.KeyboardButton('Старт')  # создание непосредственно кнопоки
    # скомпановываем в одну единую структуру.
    markup.add(website, start)
    # reply_markup=markup - прикрепляем кнопку
    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)


# запускаем наш бот на постоянное выполнение
bot.polling(none_stop=True)
