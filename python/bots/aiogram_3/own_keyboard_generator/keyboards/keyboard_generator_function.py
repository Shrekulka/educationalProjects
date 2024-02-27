# own_keyboard_generator/keyboards/keyboard_generator_function.py

from typing import Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON


def create_inline_kb(width: int, *args: Union[str, list], last_btn: Union[str, None] = None,
                     **kwargs: str) -> InlineKeyboardMarkup:
    """
        Generates an inline keyboard based on the provided arguments.

        Parameters:
        - width (int): The width of the keyboard, determining the number of buttons in each row.
        - args (Union[str, list]): A string or list of arguments to create buttons. If a string is passed, each
          character in the string will be interpreted as one button. If a list is passed, each element of the list will
          be interpreted as one button.
        - last_btn (Union[str, None], optional): The text for the last button. Default is None.
        - kwargs (str): Additional keyword arguments for creating buttons. Each key-value pair will be
          interpreted as the text of the button and its callback_data, respectively.

        Returns:
        - InlineKeyboardMarkup: An inline keyboard object ready to be sent to the user.
    """
    # Инициализируем билдер для инлайн-клавиатуры
    kb_builder = InlineKeyboardBuilder()

    # Инициализируем список для хранения кнопок
    buttons: list[InlineKeyboardButton] = []

    # Создаем кнопки из аргументов args

    # Если есть аргументы для кнопок
    if args:
        # Проходимся по переданным аргументам
        for arg in args:
            # Если аргумент является строкой, преобразуем его в список
            if isinstance(arg, str):
                arg = [arg]
            # Для каждой кнопки из аргументов
            for button in arg:
                # Проверяем наличие соответствующего текста кнопки в лексиконе на русском языке
                # Если текст кнопки есть в лексиконе, используем его, иначе используем переданный текст кнопки
                button_text = LEXICON.get(button, button)
                buttons.append(InlineKeyboardButton(
                    text=button_text,
                    # Устанавливаем callback_data для кнопки, который будет отправлен при нажатии на кнопку
                    callback_data=button))

    # Создаем кнопки из именованных аргументов kwargs

    # Если есть ключевые аргументы для кнопок
    if kwargs:
        # Для каждой кнопки и соответствующего текста из ключевых аргументов
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                # Устанавливаем callback_data для кнопки, который будет отправлен при нажатии на кнопку
                callback_data=button))

    # Распаковываем список кнопок в билдер с указанной шириной
    kb_builder.row(*buttons, width=width)

    # Добавляем последнюю кнопку, если она передана в функцию
    if last_btn:
        # Проверяем наличие соответствующего текста последней кнопки в лексиконе
        last_button_text = LEXICON.get(last_btn, last_btn)
        kb_builder.row(InlineKeyboardButton(
            # Устанавливаем текст для последней кнопки
            text=last_button_text,
            # Устанавливаем callback_data для последней кнопки, который будет отправлен при нажатии на кнопку
            callback_data='last_btn'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
