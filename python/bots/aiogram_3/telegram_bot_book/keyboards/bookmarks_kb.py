# telegram_bot_book/keyboards/bookmarks_kb.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON
from services.file_handling import book


# Функция создания клавиатуры с закладками
def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    """
        Creates a keyboard with bookmarks for the book.

        Args:
        *args (int): Page numbers that are bookmarks for the user.

        Returns:
        InlineKeyboardMarkup: A keyboard object with bookmark buttons.

        Each bookmark button represents a page number of the book and the beginning of the page text
        (up to 100 characters).
        When a button is pressed, the corresponding page number is passed as the callback_data.

        At the end of the keyboard, two buttons are added: "Edit" and "Cancel".
    """
    # Создаем объект-строитель клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки-закладки в порядке возрастания
    for button in sorted(args):
        # Создаем кнопку с текстом, содержащим номер страницы и начальный текст страницы (до 100 символов)
        kb_builder.row(InlineKeyboardButton(
            text=f'{button} - {book[button][:100]}',
            callback_data=str(button)
        ))
    # Добавляем две кнопки в конец клавиатуры: "Редактировать" и "Отменить"
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit_bookmarks_button'],
            callback_data='edit_bookmarks'
        ),
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        ),
        width=2  # Установка ширины двух кнопок на одну строку
    )

    # Возвращаем объект клавиатуры
    return kb_builder.as_markup()


# Функция создания клавиатуры для редактирования закладок
def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    """
        Creates a keyboard for editing bookmarks in a book.

        Args:
        *args (int): Page numbers that are bookmarks for the user.

        Returns:
        InlineKeyboardMarkup: A keyboard object with buttons for editing bookmarks.

        Each bookmark button represents a page number of the book and the beginning of the page text (up to 100 characters),
        and also has the option to delete the bookmark.
        When a button is pressed, the corresponding page number is passed with 'del' appended as the callback_data.

        At the end of the keyboard, a "Cancel" button is added so that the user can cancel the editing.
    """
    # Создаем объект-строитель клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки-закладки в порядке возрастания
    for button in sorted(args):
        # Создаем кнопку с текстом для удаления закладки и ее номером (до 100 символов)
        kb_builder.row(InlineKeyboardButton(
            text=f"{LEXICON['del']} {button} - {book[button][:100]}",
            callback_data=f"{button}del"))
    # Добавляем кнопку "Отменить" в конец клавиатуры
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'))

    # Возвращаем объект клавиатуры
    return kb_builder.as_markup()
