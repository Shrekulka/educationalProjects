# telegram_bot/keyboards/client_kb.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # , ReplyKeyboardRemove

# записываем то, что будет отображаться на кнопке, эту же строку эта кнопка отправляет нашему боту
b1 = KeyboardButton('/Режим_работы')  # в скобки передаем команды с хендлера клиента
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Меню')
# кнопки исключения, которые отправляют не то, что на них написано
b4 = KeyboardButton('Поделиться номером', request_contact=True)
b5 = KeyboardButton('Отправить где я', request_location=True)

# этот класс замещает обычную клавиатуру на ту которую мы создаем
# кнопки меняются под размер того, что написано (resize_keyboard=True)
# спрятать клавиатуру после того как пользователь сделал выбор - (one_time_keyboard=True)
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# в эту клавиатуру добавляем наши кнопки.
# kb_client.add(b1).add(b2).add(b3) - добавляет каждый раз кнопку с новой строки
# kb_client.add(b1).add(b2).insert(b3) - добавляет кнопку в струку с правой стороны
# kb_client.row(b1,b2,b3) - добавляет кнопки в одну строку подряд

kb_client.add(b1).add(b2).add(b3).row(b4, b5)
