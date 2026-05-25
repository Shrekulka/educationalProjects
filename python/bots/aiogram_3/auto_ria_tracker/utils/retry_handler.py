# auto_ria_tracker/utils/retry_handler.py

import asyncio
from typing import Union, Any


class RetryHandler:
    """
    A flexible retry mechanism for asynchronous operations with exponential backoff.

    Provides robust error handling and retry strategy for async functions,
    implementing exponential backoff to manage transient failures.

    Attributes:
        max_retries (int): Maximum number of retry attempts
        base_delay (int/float): Initial delay between retries
        max_delay (int/float): Maximum delay between retries
    """

    def __init__(self, max_retries=3, base_delay=1, max_delay=60) -> None:
        """
        Initialize the RetryHandler with configurable retry parameters.

        Args:
          max_retries (int, optional): Maximum retry attempts. Defaults to 3.
          base_delay (int/float, optional): Initial delay between retries. Defaults to 1.
          max_delay (int/float, optional): Maximum delay between retries. Defaults to 60.

        Raises:
          ValueError: If max_retries is less than 1
        """
        # Проверяем корректность количества попыток
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1")

        # Сохраняем параметры повторных попыток
        self.max_retries: int = max_retries
        self.base_delay: Union[int, float] = base_delay
        self.max_delay: Union[int, float] = max_delay

    async def execute(self, func, *args, **kwargs)-> Any:
        """
        Execute an async function with retry and exponential backoff.

        Args:
            func (Callable): Async function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Result of the successful function execution

        Raises:
            Exception: If all retry attempts fail
        """
        # Итерируемся по количеству попыток
        for attempt in range(self.max_retries):
            try:
                # Пытаемся выполнить функцию
                return await func(*args, **kwargs)
            except Exception as e:
                # Вычисляем задержку с экспоненциальным возрастанием
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                await asyncio.sleep(delay)

                # В последней попытке перевозбуждаем последнее исключение
                if attempt == self.max_retries - 1:
                    raise e