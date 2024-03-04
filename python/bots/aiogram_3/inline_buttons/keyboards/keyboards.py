# inline_buttons/keyboards/keyboards.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON_RU
from lexicon.urls import URLS

# Создаем объекты для каждой инлайн-кнопки, указывая текст кнопки из словаря лексикона и URL из словаря URLS
url_button_1 = InlineKeyboardButton(text=LEXICON_RU["course_button"], url=URLS["course"])
url_button_2 = InlineKeyboardButton(text=LEXICON_RU["docs_button"], url=URLS["docs"])
url_button_3 = InlineKeyboardButton(text=LEXICON_RU["group_button"], url=URLS["course_group"])
url_button_4 = InlineKeyboardButton(text=LEXICON_RU["author_button"], url=URLS["course_author"])
url_button_5 = InlineKeyboardButton(text=LEXICON_RU["channel_button"], url=URLS["ml_channel"])

# Формируем список списков кнопок, чтобы каждая кнопка была в отдельном списке
buttons = [[url_button_1], [url_button_2], [url_button_3], [url_button_4], [url_button_5]]

# Создаем клавиатуру инлайн-кнопок с указанием списка кнопок и row_width=1 для установки полной ширины кнопок
keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)

