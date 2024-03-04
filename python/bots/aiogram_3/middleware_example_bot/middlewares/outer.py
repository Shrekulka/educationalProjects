# middleware_example_bot/middlewares/outer.py

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from logger_config import logger


class FirstOuterMiddleware(BaseMiddleware):
    """
    The first outer middleware.

    This middleware logs the entry and exit of it, as well as the type of event it operates with.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        """
        Executes the handler.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): The event handler.
            event (TelegramObject): The event object.
            data (Dict[str, Any]): The event data.

        Returns:
            Any: The result of executing the handler.
        """
        # Записываем отладочное сообщение о входе в миддлварь и типе события
        logger.debug(
            f"Вошли в первый внешний миддлварь {__class__.__name__}, тип события {event.__class__.__name__}")

        # Вызываем переданный обработчик для выполнения определенной логики
        result = await handler(event, data)

        # Записываем отладочное сообщение о выходе из миддлвари
        logger.debug(f"Выходим из первого внешнего миддлвари {__class__.__name__}")

        # Возвращаем результат выполнения обработчика
        return result


class SecondOuterMiddleware(BaseMiddleware):
    """
    The second outer middleware.

    This middleware logs the entry and exit of it, as well as the type of event it operates with.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        """
        Executes the handler.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): The event handler.
            event (TelegramObject): The event object.
            data (Dict[str, Any]): The event data.

        Returns:
            Any: The result of executing the handler.
        """
        # Записываем отладочное сообщение о входе в миддлварь и типе события
        logger.debug(
            f"Вошли во второй внешний миддлварь {__class__.__name__}, тип события {event.__class__.__name__}")

        # Вызываем переданный обработчик для выполнения определенной логики
        result = await handler(event, data)

        # Записываем отладочное сообщение о выходе из миддлвари
        logger.debug(f"Выходим из второго внешнего миддлвари {__class__.__name__}")

        # Возвращаем результат выполнения обработчика
        return result


class ThirdOuterMiddleware(BaseMiddleware):
    """
    The third outer middleware.

    This middleware logs the entry and exit of it, as well as the type of event it operates with.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        """
        Executes the handler.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): The event handler.
            event (TelegramObject): The event object.
            data (Dict[str, Any]): The event data.

        Returns:
            Any: The result of executing the handler.
        """
        # Записываем отладочное сообщение о входе в миддлварь и типе события
        logger.debug(
            f"Вошли в третий внешний миддлварь {__class__.__name__}, тип события {event.__class__.__name__}")

        # Вызываем переданный обработчик для выполнения определенной логики
        result = await handler(event, data)

        # Записываем отладочное сообщение о выходе из миддлвари
        logger.debug(f"Выходим из третьего внешнего миддлвари {__class__.__name__}")

        # Возвращаем результат выполнения обработчика
        return result
