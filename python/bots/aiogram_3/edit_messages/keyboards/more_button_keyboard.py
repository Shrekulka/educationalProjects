# edit_messages/keyboards/more_button_keyboard.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import LEXICON_BUTTONS

# Инициализируем пустой список для хранения объектов InlineKeyboardButton
buttons: list[InlineKeyboardButton] = []

# Итерируемся по элементам словаря LEXICON_BUTTONS
# Каждый элемент содержит ключ (строку) и значение (кортеж из двух строк: текст кнопки и callback_data)
for button_key, (button_text, callback_data) in LEXICON_BUTTONS.items():
    # Создаем объект InlineKeyboardButton с указанным текстом и callback_data. И добавляем его в список buttons
    buttons.append(InlineKeyboardButton(text=button_text, callback_data=callback_data))

# Создаем объект InlineKeyboardMarkup, который представляет собой разметку клавиатуры
# Передаем в конструктор inline_keyboard список со списком buttons
# Таким образом, все кнопки из списка buttons будут расположены в одной строке клавиатуры
keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
