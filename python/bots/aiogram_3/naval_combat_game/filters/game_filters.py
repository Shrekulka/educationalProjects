# naval_combat_game/filters/game_filters.py

from aiogram.filters.callback_data import CallbackData


# Определяем свой класс FieldCallbackFactory, который является фабрикой коллбэков для поля игры
# Указываем префикс "user_field" для коллбэков, создаваемых этим классом
class FieldCallbackFactory(CallbackData, prefix="user_field"):
    """
        Factory class for creating callback data related to the user's field.

        This class extends the CallbackData class from aiogram.filters.callback_data module
        and is used to generate callback data for interacting with the user's game field.

        Attributes:
            x (int): The x-coordinate of the cell on the game field.
            y (int): The y-coordinate of the cell on the game field.
    """
    # Определяем атрибуты x и y для координаты клетки поля
    x: int  # Координата x
    y: int  # Координата y
