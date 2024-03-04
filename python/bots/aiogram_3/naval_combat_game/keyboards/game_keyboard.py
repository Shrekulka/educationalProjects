# naval_combat_game/keyboards/game_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.game_database import users
from filters.game_filters import FieldCallbackFactory
from lexicon.game_lexicon import LEXICON
from services.game_services import FIELD_SIZE


# Функция get_field_keyboard генерирует клавиатуру для игрового поля пользователя.
# Она использует данные из матрицы ходов пользователя для определения состояния каждой клетки поля.
def get_field_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
       Generate an inline keyboard representing the game field for the specified user.

       This function generates an inline keyboard representing the game field for the specified user.
       Each cell in the field is represented by a button with a callback data containing its coordinates.

       Args:
           user_id (int): The ID of the user for whom the game field keyboard is generated.

       Returns:
           InlineKeyboardMarkup: The generated inline keyboard representing the game field.
    """
    # Создаем пустой список кнопок для каждой клетки игрового поля
    array_buttons: list[list[InlineKeyboardButton]] = []

    # Перебираем строки игрового поля
    for i in range(FIELD_SIZE):
        # Для каждой строки создаем внутренний список кнопок
        array_buttons.append([])

        # Перебираем столбцы игрового поля
        for j in range(FIELD_SIZE):
            # Создаем кнопку для каждой клетки игрового поля
            array_buttons[i].append(InlineKeyboardButton(
                # Устанавливаем текст кнопки в соответствии с состоянием клетки (вода, попадание, промах)
                text=LEXICON[users[user_id]['field'][i][j]],
                # Устанавливаем коллбэк-данные кнопки для определения координаты клетки
                callback_data=FieldCallbackFactory(x=i, y=j).pack()))

    # Возвращаем сформированную клавиатуру в виде объекта InlineKeyboardMarkup
    return InlineKeyboardMarkup(inline_keyboard=array_buttons)
