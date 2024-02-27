# telegram_bot_book/keyboards/pagination_kb.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON


# Функция, генерирующая клавиатуру для страницы книги
def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    """
        Creates an inline keyboard with pagination buttons for the book page.

        Parameters:
            buttons (tuple[str]): A tuple of strings representing the button names.

        Returns:
            InlineKeyboardMarkup: A keyboard object with pagination buttons.

        Example usage:
            ```
                pagination_kb = create_pagination_keyboard('backward', '1/10', 'forward')
            ```

        Each button is generated using values from the LEXICON dictionary if these values are present in the dictionary.
        If not, the button text remains unchanged.

        A button is created with callback_data corresponding to the button text. For example, the button 'backward'
        corresponds to callback_data='backward'.

        If the arguments passed to the function are not keys in the LEXICON dictionary, they are used as button text
        without changes.

        Pagination buttons are arranged in a single row for clarity and compactness.
    """
    # Добавляем в билдер ряд с кнопками пагинации
    kb_builder = InlineKeyboardBuilder()

    # Создаем ряд кнопок пагинации. Каждая кнопка получает текст из словаря LEXICON, если соответствующий ключ
    # присутствует в словаре. Если ключа в словаре нет, то используется исходный текст кнопки без изменений.
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons])

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
