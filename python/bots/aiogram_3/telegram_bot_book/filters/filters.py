# telegram_bot_book/filters/filters.py

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDigitCallbackData(BaseFilter):
    """
    Filter to check if callback data is a digit.

    This filter is used to determine if the callback data contains only digits.
    Returns True if the callback data represents a number, False otherwise.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        Checks if the callback data is a digit.

        Args:
            callback (CallbackQuery): The callback object.

        Returns:
            bool: True if the callback data is a digit, False otherwise.
        """
        # Проверяем, состоит ли строка данных коллбэка только из цифр.
        return callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    """
    Filter to check if callback data is a bookmark deletion command.

    This filter is used to determine if the callback data is a bookmark deletion command.
    Returns True if the callback data ends with 'del' and the preceding part is a digit,
    False otherwise.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        Checks if the callback data is a bookmark deletion command.

        Args:
            callback (CallbackQuery): The callback object.

        Returns:
            bool: True if the callback data is a bookmark deletion command, False otherwise.
        """
        # Проверяем, оканчивается ли строка данных коллбэка на 'del' и является ли оставшаяся часть строки числом.
        return callback.data.endswith('del') and callback.data[:-3].isdigit()
