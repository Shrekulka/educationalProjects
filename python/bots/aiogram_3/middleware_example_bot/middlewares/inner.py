# middleware_example_bot/middlewares/inner.py

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from logger_config import logger


# Первый внутренний миддлварь
class FirstInnerMiddleware(BaseMiddleware):
    """
        The first inner middleware.

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
            f"Вошли в первый внутренний миддлварь {__class__.__name__}, тип события {event.__class__.__name__}")

        # Вызываем переданный обработчик для выполнения определенной логики
        result = await handler(event, data)

        # Записываем отладочное сообщение о выходе из миддлвари
        logger.debug(f"Выходим из первого внутреннего миддлвари {__class__.__name__}")

        # Возвращаем результат выполнения обработчика
        return result


# Второй внутренний миддлварь
class SecondInnerMiddleware(BaseMiddleware):
    """
        The second inner middleware.

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
            f"Вошли во второй внутренний миддлварь {__class__.__name__}, тип события {event.__class__.__name__}")

        # Вызываем переданный обработчик для выполнения определенной логики
        result = await handler(event, data)

        # Записываем отладочное сообщение о выходе из миддлвари
        logger.debug(f"Выходим из второго внутреннего миддлвари {__class__.__name__}")

        # Возвращаем результат выполнения обработчика
        return result


# Третий внутренний миддлварь
class ThirdInnerMiddleware(BaseMiddleware):
    """
        The third inner middleware.

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
            f"Вошли в третий внутренний миддлварь {__class__.__name__}, тип события {event.__class__.__name__}")

        # Вызываем переданный обработчик для выполнения определенной логики
        result = await handler(event, data)

        # Записываем отладочное сообщение о выходе из миддлвари
        logger.debug(f"Выходим из третьего внутреннего миддлвари {__class__.__name__}")

        # Возвращаем результат выполнения обработчика
        return result
