# inter_exchange_arbitrage_bot/src/core/resilience.py

import asyncio
import random
import time
from enum import Enum
from functools import wraps
from typing import Callable, Coroutine, Any

from src.utils.logger import logger


class CircuitBreakerState(Enum):
    """Состояния автоматического выключателя."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerException(Exception):
    """Исключение, выбрасываемое когда CircuitBreaker находится в состоянии OPEN."""

    def __init__(self, service_name: str, timeout_remaining: float):
        self.service_name = service_name
        self.timeout_remaining = timeout_remaining
        super().__init__(f"CircuitBreaker is OPEN for [{service_name}]. "
                         f"Retry in {timeout_remaining:.1f} seconds")


class APICircuitBreaker:
    """
    Реализует паттерн "Автоматический выключатель" для изоляции сбоящих внешних сервисов.
    """

    def __init__(self, service_name: str, failure_threshold: int = 3, timeout: int = 120):
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = CircuitBreakerState.CLOSED

    def _should_attempt_request(self) -> bool:
        """Определяет, следует ли пытаться выполнить запрос."""
        if self.state == CircuitBreakerState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                logger.warning(f"CircuitBreaker для [{self.service_name}]: "
                               f"перехожу в состояние {self.state.value.upper()}.")
                return True
            return False
        return True

    def _get_timeout_remaining(self) -> float:
        """Возвращает оставшееся время до возможности повторного запроса."""
        if self.state == CircuitBreakerState.OPEN:
            return max(0.0, self.timeout - (time.time() - self.last_failure_time))
        return 0.0

    def _handle_success(self):
        """Обрабатывает успешный запрос."""
        if self.state == CircuitBreakerState.HALF_OPEN:
            logger.info(f"CircuitBreaker для [{self.service_name}]: "
                        f"успешный вызов, перехожу в {CircuitBreakerState.CLOSED.value.upper()}.")
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED

    def _handle_failure(self):
        """Обрабатывает неуспешный запрос."""
        self.failure_count += 1
        should_open = (self.state == CircuitBreakerState.HALF_OPEN or
                       self.failure_count >= self.failure_threshold)

        if should_open:
            self.state = CircuitBreakerState.OPEN
            self.last_failure_time = time.time()
            logger.error(f"CircuitBreaker для [{self.service_name}]: "
                         f"{self.state.value.upper()} после {self.failure_count} неудач подряд.")

    async def call(self, func: Callable[..., Coroutine], *args, **kwargs) -> Any:
        """Выполняет функцию с защитой через Circuit Breaker."""
        if not self._should_attempt_request():
            timeout_remaining = self._get_timeout_remaining()
            raise CircuitBreakerException(self.service_name, timeout_remaining)

        try:
            result = await func(*args, **kwargs)
            self._handle_success()
            return result
        except Exception as e:
            self._handle_failure()
            # Пробрасываем оригинальное исключение для retry_with_backoff
            raise e

    def get_status(self) -> dict:
        """Возвращает текущий статус Circuit Breaker."""
        return {
            'service_name': self.service_name,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'timeout_remaining': self._get_timeout_remaining() if self.state == CircuitBreakerState.OPEN else 0,
            'failure_threshold': self.failure_threshold
        }


def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """
    Декоратор, реализующий повторные попытки с экспоненциальной задержкой.
    """

    def decorator(func: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except CircuitBreakerException:
                    # Не ретраим, если Circuit Breaker открыт
                    raise
                except Exception as e:
                    last_exception = e

                    if attempt < max_retries - 1:
                        wait_time = (base_delay * (2 ** attempt)) + random.uniform(0, 0.5)
                        logger.warning(
                            f"Попытка {attempt + 1}/{max_retries} для {func.__qualname__} провалена. "
                            f"Ошибка: {type(e).__name__}: {str(e)}. Повтор через {wait_time:.2f} сек."
                        )
                        await asyncio.sleep(wait_time)

            logger.error(f"Функция {func.__qualname__} не выполнилась после {max_retries} попыток.")
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


# # inter_exchange_arbitrage_bot/src/core/resilience.py
#
# import asyncio
# import random
# import time
# from functools import wraps
# from typing import Callable, Coroutine, Any
#
# from src.utils.logger import logger
#
#
# class APICircuitBreaker:
#     """
#     Реализует паттерн "Автоматический выключатель" для изоляции сбоящих внешних сервисов.
#     """
#
#     def __init__(self, service_name: str, failure_threshold: int = 3, timeout: int = 120):
#         self.service_name = service_name
#         self.failure_threshold = failure_threshold
#         self.timeout = timeout
#         self.failure_count = 0
#         self.last_failure_time = 0
#         self.state = "CLOSED"  # Состояния: CLOSED, OPEN, HALF_OPEN
#
#     async def call(self, func: Callable[..., Coroutine], *args, **kwargs) -> Any:
#         if self.state == "OPEN":
#             if time.time() - self.last_failure_time > self.timeout:
#                 self.state = "HALF_OPEN"
#                 logger.warning(f"CircuitBreaker для [{self.service_name}]: перехожу в состояние HALF_OPEN.")
#             else:
#                 raise Exception(f"CircuitBreaker is OPEN for [{self.service_name}]")
#
#         try:
#             result = await func(*args, **kwargs)
#             if self.state == "HALF_OPEN":
#                 logger.info(f"CircuitBreaker для [{self.service_name}]: успешный вызов, перехожу в CLOSED.")
#             self.failure_count = 0
#             self.state = "CLOSED"
#             return result
#         except Exception as e:
#             self.failure_count += 1
#             if self.state == "HALF_OPEN" or self.failure_count >= self.failure_threshold:
#                 self.state = "OPEN"
#                 self.last_failure_time = time.time()
#                 logger.error(
#                     f"CircuitBreaker для [{self.service_name}]: ОТКРЫТ после {self.failure_count} неудач подряд.")
#
#             # Пробрасываем оригинальное исключение, чтобы сработал retry_with_backoff
#             raise e
#
#
# def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
#     """
#     Декоратор, реализующий повторные попытки с экспоненциальной задержкой.
#     """
#
#     def decorator(func: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             for attempt in range(max_retries):
#                 try:
#                     return await func(*args, **kwargs)
#                 except Exception as e:
#                     # Логируем только если это не последняя попытка
#                     if attempt < max_retries - 1:
#                         wait_time = (base_delay * (2 ** attempt)) + random.uniform(0, 0.5)
#                         logger.warning(
#                             f"Попытка {attempt + 1}/{max_retries} для {func.__qualname__} провалена. "
#                             f"Ошибка: {type(e).__name__}. Повтор через {wait_time:.2f} сек."
#                         )
#                         await asyncio.sleep(wait_time)
#                     else:
#                         logger.error(f"Функция {func.__qualname__} не выполнилась после {max_retries} попыток.")
#                         raise e  # Пробрасываем оригинальную ошибку
#
#         return wrapper
#
#     return decorator
