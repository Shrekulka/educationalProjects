# middleware_example_bot/filters/filters.py

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from logger_config import logger


# Класс пользовательского фильтра, который всегда возвращает True
class MyTrueFilter(BaseFilter):
    """
        A filter that always returns True.

        This filter allows executing the command or handler it is applied to always,
        as its logic always returns True.
    """
    # Метод, который вызывается при проверке фильтра
    async def __call__(self, event: TelegramObject) -> bool:
        """
            Checks the condition of the filter and returns the result.

            Args:
                event (TelegramObject): The object to which the filter is applied.

            Returns:
                bool: The result of the filter condition check (always True).
        """

        # Логируем информацию о том, что фильтр был применен
        logger.debug(f"Применен фильтр, всегда возвращающий True: {__class__.__name__}")
        # Всегда возвращаем True, чтобы позволить выполнение команды или обработчика
        return True


# Класс пользовательского фильтра, который всегда возвращает False
class MyFalseFilter(BaseFilter):
    """
        A filter that always returns False.

        This filter always prevents the execution of the command or handler it is applied to,
        as its logic always returns False.
    """
    # Метод, который вызывается при проверке фильтра
    async def __call__(self, event: TelegramObject) -> bool:
        """
            Checks the condition of the filter and returns the result.

            Args:
                event (TelegramObject): The object to which the filter is applied.

            Returns:
                bool: The result of the filter condition check (always False).
        """

        # Логируем информацию о том, что фильтр был применен
        logger.debug(f"Применен фильтр, всегда возвращающий False: {__class__.__name__}")
        # Всегда возвращаем False, чтобы предотвратить выполнение команды или обработчика
        return False
