# ai_checklist_guardian/keyboards/client_kb.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Список локаций
locations = ["Location 1", "Location 2", "Location 3", "Location 4", "Location 5"]

# Список вариантов чек-листа
checklist_options = ["All clear", "Leave comment"]

# InlineKeyboardMarkup для выбора локации
kb_client_locations = ReplyKeyboardMarkup().add(*[KeyboardButton(location) for location in locations])

# ReplyKeyboardMarkup для общего выбора локации
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    *[KeyboardButton(location) for location in locations])

# Клавиатура с вариантами чек-листа
kb_checklist = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_checklist.row("All clear", "Leave comment")

# Клавиатура для отправки фото
kb_send_photo = ReplyKeyboardMarkup(resize_keyboard=True)
kb_send_photo.add(KeyboardButton('Send photo'))
