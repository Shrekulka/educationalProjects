# inline_сallback_buttons/keyboards/keyboards.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup  # Импорт необходимых классов из модуля aiogram.types
from lexicon.lexicon_ru import LEXICON_RU  # Импорт словаря лексикона для русского языка

# Создание объектов кнопок с текстом из словаря и соответствующими callback_data
button_1 = InlineKeyboardButton(text=LEXICON_RU["name_button_1"], callback_data="callback_button_1")
button_2 = InlineKeyboardButton(text=LEXICON_RU["name_button_2"], callback_data="callback_button_2")

# Формирование списка списков кнопок, чтобы каждая кнопка была в отдельном списке
buttons = [[button_1], [button_2]]

# Создание клавиатуры инлайн-кнопок с указанием списка кнопок
keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

