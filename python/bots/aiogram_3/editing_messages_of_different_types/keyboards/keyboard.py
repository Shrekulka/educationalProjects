# editing_messages_of_different_types/keyboards/keyboard.py

from typing import Union, Dict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


# Функция для генерации инлайн-клавиатуры с заданным шириной и кнопками
def get_markup(width: int, *args: Union[str, Dict[str, str]], **kwargs: str) -> InlineKeyboardMarkup:
    """
        Generates an inline keyboard with the specified width and buttons.

        Args:
            width (int): The width of the keyboard (number of buttons in a row).
            *args (Union[str, Dict[str, str]]): Positional arguments. Can be strings (button texts) or dictionaries,
                where keys are callback_data of the buttons, and values are button texts. If the button text from the
                LEXICON dictionary is specified, it will be used instead of the key.
            **kwargs (str): Keyword arguments. Keys are callback_data of the buttons, values are button texts.

        Returns:
            InlineKeyboardMarkup: The inline keyboard object.

        Examples:
            Usage example:
            >>> keyboard = get_markup(2, 'button1', 'button2', button3='Button 3', button4='Button 4')
    """
    # Создаем экземпляр билдера инлайн-клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для хранения кнопок
    buttons: list[InlineKeyboardButton] = []
    # Добавляем кнопки из аргументов args
    if args:
        # Перебираем кнопки из аргументов args
        for button in args:
            # Если кнопка присутствует в словаре LEXICON, используем соответствующий текст,
            # иначе используем текст кнопки напрямую
            buttons.append(InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button,
                                                callback_data=button))
    # Добавляем кнопки из аргументов kwargs
    if kwargs:
        # Перебираем пары ключ-значение из аргументов kwargs
        for button, text in kwargs.items():
            # Создаем кнопку с указанным текстом и callback_data
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))
    # Добавляем кнопки в инлайн-клавиатуру с заданной шириной
    kb_builder.row(*buttons, width=width)
    # Возвращаем созданную инлайн-клавиатуру
    return kb_builder.as_markup()
