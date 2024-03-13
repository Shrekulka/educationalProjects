# form_filling_bot_fsm/keyboards/keyboard.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import LEXICON_BUTTONS

########################################################################################################################
# 1) gender клавиатура
########################################################################################################################
# Создание объектов кнопок для выбора пола

# Создание кнопки для мужского пола
male_button = InlineKeyboardButton(text=LEXICON_BUTTONS["male_button"], callback_data="male")
# Создание кнопки для женского пола
female_button = InlineKeyboardButton(text=LEXICON_BUTTONS["female_button"], callback_data="female")
# Создание кнопки для неопределенного пола
undefined_button = InlineKeyboardButton(text=LEXICON_BUTTONS["undefined_button"], callback_data="undefined_gender")

# Добавление кнопок в клавиатуру (две кнопки в одном ряду и одна в другом)
keyboard_gender: list[list[InlineKeyboardButton]] = [[male_button, female_button], [undefined_button]]

# Создание объекта инлайн-клавиатуры для выбора пола
markup_gender = InlineKeyboardMarkup(inline_keyboard=keyboard_gender)

########################################################################################################################
# 2) education клавиатура
########################################################################################################################
# Создание объектов кнопок для выбора образования

# Кнопка для выбора среднего образования
secondary_education_button = InlineKeyboardButton(text=LEXICON_BUTTONS["secondary_education_button"],
                                                  callback_data='secondary')
# Кнопка для выбора высшего образования
higher_education_button = InlineKeyboardButton(text=LEXICON_BUTTONS["higher_education_button"],
                                               callback_data='higher')
# Кнопка для выбора отсутствия образования
without_education_button = InlineKeyboardButton(text=LEXICON_BUTTONS["without_education_button"],
                                                callback_data='no_edu')

# Добавление кнопок в клавиатуру (две кнопки в одном ряду и одна в другом)
keyboard_education: list[list[InlineKeyboardButton]] = [[secondary_education_button, higher_education_button],
                                                        [without_education_button]]

# Создание объекта инлайн-клавиатуры для выбора образования
markup_education = InlineKeyboardMarkup(inline_keyboard=keyboard_education)

########################################################################################################################
# 3) news клавиатура
########################################################################################################################
# Создание объектов кнопок для выбора наличия новостей

# Кнопка для подписки на новости
yes_news_button = InlineKeyboardButton(text=LEXICON_BUTTONS["yes_news_button"], callback_data='yes_news')
# Кнопка для отказа от новостей
no_news_button = InlineKeyboardButton(text=LEXICON_BUTTONS["no_news_button"], callback_data='no_news')

# Добавление кнопок в клавиатуру в один ряд
keyboard_news: list[list[InlineKeyboardButton]] = [[yes_news_button, no_news_button]]

# Создание объекта инлайн-клавиатуры для выбора наличия новостей
markup_news = InlineKeyboardMarkup(inline_keyboard=keyboard_news)