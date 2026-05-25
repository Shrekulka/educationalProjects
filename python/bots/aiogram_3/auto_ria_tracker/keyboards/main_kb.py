# auto_ria_tracker/keyboards/main_kb.py


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_ru import LEXICON_BUTTONS

# Создание объектов кнопок для главного меню

# Кнопка для запуска мониторинга
start_monitoring_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["start_monitoring"], callback_data="start_monitoring"
)

# Кнопка для остановки мониторинга
stop_monitoring_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["stop_monitoring"],
    callback_data="stop_monitoring"
)

# Кнопка для просмотра настроек
view_settings_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["view_settings"], callback_data="view_settings"
)

# Кнопка для помощи
help_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["help"], callback_data="help"
)

# Добавление кнопок в клавиатуру главного меню
keyboard_main: list[list[InlineKeyboardButton]] = [
    [start_monitoring_button, stop_monitoring_button],
    [view_settings_button, help_button]
]

# Создание объекта инлайн-клавиатуры для главного меню
markup_main = InlineKeyboardMarkup(inline_keyboard=keyboard_main)

# Создание кнопок для меню настроек
set_model_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["set_model"], callback_data="set_model"
)

# Кнопка для выбора "Импортированные"
import_yes_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["import_yes"], callback_data="set_import:yes"
)

# Кнопка для выбора "Не импортированные"
import_no_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["import_no"], callback_data="set_import:no"
)

# Кнопка для выбора "С ДТП"
accident_yes_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["accident_yes"], callback_data="set_accident:yes"
)

# Кнопка для выбора "Без ДТП"
accident_no_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["accident_no"], callback_data="set_accident:no"
)

# Кнопка для возврата в главное меню
back_button = InlineKeyboardButton(
    text=LEXICON_BUTTONS["back"], callback_data="back_to_main"
)

# Создание клавиатуры настроек
keyboard_settings: list[list[InlineKeyboardButton]] = [
    [set_model_button],
    [import_yes_button, import_no_button],
    [accident_yes_button, accident_no_button],
    [back_button]
]

# Создаем объект клавиатуры с кнопками для настроек
markup_settings = InlineKeyboardMarkup(inline_keyboard=keyboard_settings)