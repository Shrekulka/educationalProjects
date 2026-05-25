# inter_exchange_arbitrage_bot/src/services/api_health_checker.py

import asyncio
from datetime import datetime, timedelta
from json import JSONDecodeError
from typing import Optional

import httpx

from src.constants.api_constants import (API_BASE_URL, STATUS_CHECK_TIMEOUT, API_SUCCESS_CODES,
                                         TOTAL_STARTUP_TIMEOUT_SECONDS, HEALTH_CHECK_RETRY_COUNT,
                                         HEALTH_CHECK_RETRY_DELAY_SECONDS, API_KEY_READY_FOR_ARBITRAGE)
from src.utils.exceptions import APINotReadyError, APIConnectionError, APIHealthCheckError
from src.utils.logger import logger


class APIHealthChecker:
    _instance: Optional['APIHealthChecker'] = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self._is_ready: bool = False
        self._last_check: Optional[datetime] = None
        self._cache_duration: timedelta = timedelta(seconds=5)
        self._check_in_progress = asyncio.Lock()

    async def check_readiness(self, force_check: bool = False) -> bool:
        """Основной метод проверки с таймаутом на весь процесс."""
        now = datetime.now()
        if not force_check and self._is_ready and self._last_check and (now - self._last_check < self._cache_duration):
            return True

        try:
            # Оборачиваем ожидание в общий таймаут
            async with asyncio.timeout(TOTAL_STARTUP_TIMEOUT_SECONDS):
                async with self._check_in_progress:
                    # Двойная проверка кэша
                    if not force_check and self._is_ready and self._last_check and (
                            datetime.now() - self._last_check < self._cache_duration):
                        return True

                    await self._wait_for_api_readiness()
                    self._last_check = datetime.now()
            return True
        except TimeoutError:
            logger.error(f"❌ API не ответило за {TOTAL_STARTUP_TIMEOUT_SECONDS} секунд. Запуск считается неудачным.")
            self._is_ready = False
            # Выбрасываем ошибку, которую поймет декоратор
            raise APIConnectionError("Таймаут ожидания запуска API.")

    async def _wait_for_api_readiness(self) -> None:
        """
        Терпеливо ждет готовности API, делая несколько попыток,
        но выходит СРАЗУ ЖЕ после получения статуса "готов".
        """
        last_exception = None

        for attempt in range(HEALTH_CHECK_RETRY_COUNT):
            try:
                is_fully_ready = await self._perform_single_health_check()

                # Если проверка вернула True, это означает, что API ПОЛНОСТЬЮ готово.
                if is_fully_ready:
                    self._is_ready = True
                    if attempt > 0:
                        logger.info(f"✅ API готово к работе после {attempt + 1} попыток.")
                    return  # НЕМЕДЛЕННО ВЫХОДИМ ИЗ ФУНКЦИИ И ЦИКЛА

            except (APIConnectionError, APINotReadyError, httpx.TimeoutException) as e:
                # Этот блок остается прежним. Он срабатывает, когда API еще не готово.
                message = getattr(e, 'message', str(e))
                last_exception = e
                logger.info(
                    f"Ожидание API (попытка {attempt + 1}/{HEALTH_CHECK_RETRY_COUNT}): {type(e).__name__} - {message}. "
                    f"Повтор через {HEALTH_CHECK_RETRY_DELAY_SECONDS} сек..."
                )

                # Если это не последняя попытка, ждем и продолжаем.
                if attempt < HEALTH_CHECK_RETRY_COUNT - 1:
                    await asyncio.sleep(HEALTH_CHECK_RETRY_DELAY_SECONDS)
                continue

            except Exception as e:
                logger.error(f"⚠️ Неожиданная ошибка при проверке здоровья API: {e}", exc_info=True)
                self._is_ready = False
                raise APIHealthCheckError(f"Критическая ошибка проверки здоровья: {str(e)}")

        # Этот код выполнится, только если все попытки в цикле провалились
        self._is_ready = False
        logger.error(f"❌ Не удалось дождаться готовности API после {HEALTH_CHECK_RETRY_COUNT} попыток.")
        raise last_exception or APIConnectionError("Не удалось подключиться к серверу API.")

    async def _perform_single_health_check(self) -> bool:
        """
        Выполняет ОДНУ проверку. Возвращает True только если API доступно И готово.
        В противном случае выбрасывает конкретное исключение.
        """
        try:
            async with httpx.AsyncClient(timeout=STATUS_CHECK_TIMEOUT) as client:
                response = await client.get(f"{API_BASE_URL}/health")

            if response.status_code not in API_SUCCESS_CODES:
                raise APIConnectionError("Сервер API вернул код ошибки.")

            health_data = response.json()
            is_ready = health_data.get(API_KEY_READY_FOR_ARBITRAGE, False)

            if not is_ready:
                # API доступно, но его внутренние сервисы еще не готовы.
                raise APINotReadyError("API доступно, но сервисы еще инициализируются.")

            # Если дошли сюда, значит все проверки пройдены
            return True

        except httpx.ConnectError:
            # API еще не начало принимать соединения.
            raise APIConnectionError("Не удалось подключиться к серверу API.")

        except (KeyError, ValueError) as e:
            # Ответ от API пришел, но он некорректный.
            raise APIHealthCheckError(f"Некорректный или пустой ответ от API: {e}")

    def invalidate_cache(self) -> None:
        """Сбрасывает кэш состояния готовности API."""
        self._last_check = None
        self._is_ready = False
        logger.info("Кэш состояния готовности API сброшен.")

    async def _get_progress_details(self) -> Optional[dict]:
        """
        Запрашивает детализированный прогресс с нового эндпоинта,
        обрабатывая только ожидаемые сетевые ошибки.
        """
        try:
            async with httpx.AsyncClient(timeout=STATUS_CHECK_TIMEOUT) as client:
                response = await client.get(f"{API_BASE_URL}/health/progress")

            # Проверяем статус ответа до парсинга JSON
            if response.status_code != 200:
                logger.warning(f"Запрос прогресса вернул статус {response.status_code}")
                return None

            return response.json()

        # Перехватываем конкретные, ожидаемые исключения
        except (httpx.RequestError, JSONDecodeError) as e:
            # httpx.RequestError - базовый класс для всех сетевых ошибок (ConnectError, Timeout, etc.)
            # JSONDecodeError - ошибка, если ответ от сервера - невалидный JSON
            logger.debug(f"Не удалось получить детали прогресса: {type(e).__name__} - {e}")
            return None


# Глобальный экземпляр
api_health_checker = APIHealthChecker()
