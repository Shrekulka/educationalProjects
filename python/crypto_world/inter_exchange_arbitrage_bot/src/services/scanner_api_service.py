# inter_exchange_arbitrage_bot/src/services/scanner_api_service.py

import asyncio
from functools import wraps
from math import ceil
from typing import Callable, Coroutine, Any, Optional, Dict, List

import httpx

import src.core.state as app_state
from src.constants.api_constants import (
    API_BASE_URL, SCANNER_OPERATION_TIMEOUT, DEFAULT_API_TIMEOUT, STATUS_CHECK_TIMEOUT, API_SUCCESS_CODES,
    API_CLIENT_ERROR_CODES, MAX_RETRIES, RETRY_INTERVALS, HEADER_INTERNAL_API_KEY, API_ENDPOINT_SCANNER_STATUS,
    API_KEY_STATUS, API_STATUS_VALUE_RUNNING, API_STATUS_VALUE_STOPPED, API_ENDPOINT_SCANNER_START,
    API_ENDPOINT_SCANNER_STOP, API_ENDPOINT_ADMIN_CACHE_STATS, API_ENDPOINT_ADMIN_EXCLUDE_PAIR, API_KEY_EXCHANGE,
    API_KEY_SYMBOL, API_ENDPOINT_ADMIN_INCLUDE_PAIR, API_ENDPOINT_ADMIN_EXCLUDED_PAIRS, API_STATUS_VALUE_SUCCESS,
    API_KEY_EXCLUDED_PAIRS, GET_BALANCE_TIMEOUT_SECONDS, GET_ALL_ASSETS_TIMEOUT_SECONDS, RECONNAISSANCE_TIMEOUT_SECONDS,
    API_PREFIX_NEWS, AI_REQUEST_TIMEOUT, NEWS_HTTP_TIMEOUT, AI_SINGLE_REQUEST_TIMEOUT
)
from src.constants.api_constants import (TIMEOUT_COIN_WAVE_SIZE, TIMEOUT_PER_WAVE_ADDITION_SECONDS)
from src.core.config import config
from src.services.api_health_checker import api_health_checker
from src.utils.logger import logger


def _get_internal_http_client() -> httpx.AsyncClient:
    """
    Возвращает HTTP-клиент для внутренних запросов (бот -> свой API).
    Гарантирует, что сессия была инициализирована.
    """
    if not app_state.internal_httpx_session:
        # Эта ошибка не должна происходить в нормальном цикле работы,
        # но она важна для отладки, если что-то пойдет не так при старте.
        raise RuntimeError("Внутренний HTTP-клиент (internal_httpx_session) не был инициализирован.")
    return app_state.internal_httpx_session


def _get_auth_headers() -> Dict[str, str]:
    """Создает словарь с HTTP-заголовками для авторизации."""
    if not config.internal_api_key:
        logger.warning("INTERNAL_API_KEY не настроен, административные запросы могут не работать.")
        return {}
    return {HEADER_INTERNAL_API_KEY: config.internal_api_key}


def _calculate_dynamic_timeout(coin_count: int) -> float:
    """
    Рассчитывает динамический таймаут для запроса новостей в зависимости от количества монет.
    """
    if coin_count <= 0:
        return AI_SINGLE_REQUEST_TIMEOUT

    # Считаем, сколько "волн" обработки потребуется
    waves = ceil(coin_count / TIMEOUT_COIN_WAVE_SIZE)

    # Добавляем дополнительное время за каждую волну, кроме первой
    additional_time = (waves - 1) * TIMEOUT_PER_WAVE_ADDITION_SECONDS

    # Итоговый таймаут = базовый + дополнительное время, но не больше максимального
    calculated_timeout = AI_SINGLE_REQUEST_TIMEOUT + additional_time

    return min(calculated_timeout, AI_REQUEST_TIMEOUT)


def api_ready_check(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await api_health_checker.check_readiness()
        return await func(*args, **kwargs)

    return wrapper


@api_ready_check
async def get_scanner_status() -> bool:
    """
    Запрашивает статус сканера у API, возвращая True, если он запущен.

    Использует механизм повторных попыток для устойчивости к временным сбоям сети или API.

    Returns:
        True, если сканер активен ('running'), иначе False.
    """
    # Повторяем запрос до MAX_RETRIES раз в случае временных ошибок.
    for attempt in range(MAX_RETRIES):
        try:
            # Используем короткий таймаут, так как этот эндпоинт должен отвечать быстро.
            timeout = httpx.Timeout(STATUS_CHECK_TIMEOUT)
            async with httpx.AsyncClient(timeout=timeout) as client:
                # Формируем URL из базового адреса и эндпоинта из констант.
                response = await client.get(f"{API_BASE_URL}{API_ENDPOINT_SCANNER_STATUS}")

            # Если код ответа успешный (например, 200 OK), обрабатываем данные.
            if response.status_code in API_SUCCESS_CODES:
                # Безопасно извлекаем значение по ключу 'status' из JSON-ответа.
                status = response.json().get(API_KEY_STATUS)
                # Проверяем, что полученный статус соответствует ожидаемым значениям.
                if status in [API_STATUS_VALUE_RUNNING, API_STATUS_VALUE_STOPPED]:
                    # Возвращаем True только если статус 'running'.
                    return status == API_STATUS_VALUE_RUNNING
                else:
                    # Если API вернуло что-то неожиданное, логируем и прекращаем попытки.
                    logger.warning(f"Некорректный статус в ответе API: {status}")
                    return False

            # Если это ошибка клиента (4xx), нет смысла повторять запрос.
            if response.status_code in API_CLIENT_ERROR_CODES:
                logger.error(
                    f"Ошибка клиента при запросе статуса (попытка #{attempt + 1}): {response.status_code}. Отмена.")
                return False

            # Для ошибок сервера (5xx) или других проблем, делаем паузу и повторяем.
            logger.warning(
                f"Попытка #{attempt + 1} не удалась (код: {response.status_code}). Повтор через {RETRY_INTERVALS[attempt]} сек...")

        except (httpx.TimeoutException, httpx.RequestError) as e:
            # Ловим ошибки сети или таймаута и готовимся к повторной попытке.
            logger.warning(
                f"Попытка #{attempt + 1} не удалась (ошибка соединения: {e}). Повтор через {RETRY_INTERVALS[attempt]} сек...")
        except ValueError:
            # Ловим ошибку, если ответ от API - невалидный JSON. Повторять бессмысленно.
            logger.error("Не удалось декодировать JSON-ответ от API. Отмена.")
            return False

        # Если это не последняя попытка, ждем перед следующей.
        if attempt < MAX_RETRIES - 1:
            await asyncio.sleep(RETRY_INTERVALS[attempt])

    # Если все попытки провалились, логируем критическую ошибку.
    logger.critical(f"Не удалось получить статус сканера после {MAX_RETRIES} попыток.")
    return False


@api_ready_check
async def start_scanner() -> bool:
    """Отправляет API команду на запуск сканера."""
    try:
        client = _get_internal_http_client()
        response = await client.post(
            f"{API_BASE_URL}{API_ENDPOINT_SCANNER_START}",
            headers=_get_auth_headers(),
            timeout=SCANNER_OPERATION_TIMEOUT
        )
        response.raise_for_status()
        logger.info("Команда запуска сканера успешно отправлена.")
        return True
    except httpx.HTTPError as e:
        logger.error(f"Ошибка API при запуске сканера: {e}")
        return False


@api_ready_check
async def stop_scanner() -> bool:
    """Отправляет API команду на остановку сканера."""
    try:
        client = _get_internal_http_client()
        response = await client.post(
            f"{API_BASE_URL}{API_ENDPOINT_SCANNER_STOP}",
            headers=_get_auth_headers(),
            timeout=SCANNER_OPERATION_TIMEOUT
        )
        response.raise_for_status()
        logger.info("Команда остановки сканера успешно отправлена.")
        return True
    except httpx.HTTPError as e:
        logger.error(f"Ошибка API при остановке сканера: {e}")
        return False


@api_ready_check
async def get_cache_stats_from_api() -> Optional[dict]:
    """Запрашивает у API статистику кэша торговых пар."""
    try:
        timeout = httpx.Timeout(DEFAULT_API_TIMEOUT)
        headers = _get_auth_headers()

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"{API_BASE_URL}{API_ENDPOINT_ADMIN_CACHE_STATS}", headers=headers)

        if response.status_code in API_SUCCESS_CODES:
            return response.json()
        else:
            logger.error(f"Ошибка API при получении статистики кэша: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Не удалось подключиться к API для получения статистики кэша: {e}")
        return None


@api_ready_check
async def exclude_pair_via_api(exchange: str, symbol: str) -> bool:
    """Отправляет API команду на добавление торговой пары в список исключений."""
    try:
        # Формируем тело запроса, используя ключи из констант.
        payload = {API_KEY_EXCHANGE: exchange, API_KEY_SYMBOL: symbol}
        headers = _get_auth_headers()

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE_URL}{API_ENDPOINT_ADMIN_EXCLUDE_PAIR}", json=payload,
                                         headers=headers)

        if response.status_code in API_SUCCESS_CODES:
            logger.info(f"API успешно обработало исключение пары {symbol} на {exchange}.")
            return True

        logger.error(f"Ошибка API при исключении пары: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        logger.error(f"Не удалось подключиться к API для исключения пары: {e}")
        return False


@api_ready_check
async def include_pair_via_api(exchange: str, symbol: str) -> bool:
    """Отправляет API команду на удаление торговой пары из списка исключений."""
    try:
        payload = {API_KEY_EXCHANGE: exchange, API_KEY_SYMBOL: symbol}
        headers = _get_auth_headers()

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE_URL}{API_ENDPOINT_ADMIN_INCLUDE_PAIR}", json=payload,
                                         headers=headers)

        if response.status_code in API_SUCCESS_CODES:
            logger.info(f"API успешно обработало включение пары {symbol} на {exchange}.")
            return True

        logger.error(f"Ошибка API при включении пары: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        logger.error(f"Не удалось подключиться к API для включения пары: {e}")
        return False


@api_ready_check
async def get_excluded_pairs_from_api() -> Optional[Dict[str, List[str]]]:
    """Запрашивает у API текущий список пар, исключенных администратором."""
    try:
        timeout = httpx.Timeout(DEFAULT_API_TIMEOUT)
        headers = _get_auth_headers()

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"{API_BASE_URL}{API_ENDPOINT_ADMIN_EXCLUDED_PAIRS}", headers=headers)

        if response.status_code in API_SUCCESS_CODES:
            data = response.json()
            # Проверяем, что в ответе есть поле "status" со значением "success".
            if data.get(API_KEY_STATUS) == API_STATUS_VALUE_SUCCESS:
                # Безопасно извлекаем список пар, возвращая {} если ключ отсутствует.
                return data.get(API_KEY_EXCLUDED_PAIRS, {})
            else:
                logger.error(f"API вернуло ошибку при получении исключенных пар: {data}")
                return None
        else:
            logger.error(f"Ошибка API при получении исключенных пар: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Не удалось подключиться к API для получения исключенных пар: {e}")
        return None


@api_ready_check
async def get_balances_from_api(mode: str) -> tuple[Optional[str], Optional[str]]:
    """
    Запрашивает отчет о балансах у API.
    Возвращает: (текст_отчета, финальный_режим) или (None, None) при ошибке
    """
    try:
        url = f"{API_BASE_URL}/balances/{mode}"
        timeout = httpx.Timeout(GET_BALANCE_TIMEOUT_SECONDS)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)

        if response.status_code in API_SUCCESS_CODES:
            data = response.json()
            return data.get("report_text"), data.get("mode", mode)
        else:
            logger.error(f"API ошибка при получении балансов: {response.status_code}")
            return None, None

    except Exception as e:
        logger.error(f"Не удалось подключиться к API для балансов: {e}")
        return None, None


@api_ready_check
async def get_all_assets_from_api() -> Optional[Dict]:
    """Запрашивает у API полный список уникальных активов со всех бирж."""
    try:
        url = f"{API_BASE_URL}/assets"
        # Используем увеличенный таймаут, так как сбор может занять время
        timeout = httpx.Timeout(GET_ALL_ASSETS_TIMEOUT_SECONDS)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)

        if response.status_code in API_SUCCESS_CODES:
            return response.json()
        else:
            logger.error(f"API ошибка при получении списка активов: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Не удалось подключиться к API для получения активов: {e}")
        return None


@api_ready_check
async def request_reconnaissance_scan(chat_id: int, message_id: int) -> Optional[Dict]:
    """ИСПРАВЛЕНО: Запрашивает разведку с передачей ID для прогресса."""
    headers = _get_auth_headers()
    payload = {"chat_id": chat_id, "message_id": message_id}

    try:
        timeout = httpx.Timeout(RECONNAISSANCE_TIMEOUT_SECONDS)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{API_BASE_URL}/scanner/reconnaissance",
                headers=headers,
                json=payload
            )

        logger.debug(f"Ответ от API /reconnaissance: Статус={response.status_code}, Тело='{response.text[:500]}...'")

        if response.status_code in API_SUCCESS_CODES:
            try:
                # Пытаемся декодировать JSON
                json_response = response.json()
                logger.debug("Ответ API успешно декодирован в JSON.")
                return json_response
            except Exception as json_error:
                # Если декодирование не удалось
                logger.error(f"Критическая ошибка: Не удалось декодировать JSON из ответа API! Ошибка: {json_error}")
                logger.error(f"Полный текст ответа: {response.text}")
                return None
        else:
            logger.error(f"API вернуло ошибку при разведке: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        logger.error(f"Ошибка при запросе разведки: {e}")
        return None


@api_ready_check
async def get_news_from_api(coins: List[str]) -> Optional[Dict]:
    """Запрашивает обработанные новости по списку монет."""
    # ==> ГЛАВНОЕ ИЗМЕНЕНИЕ: Вызываем нашу новую функцию для расчета таймаута
    timeout = _calculate_dynamic_timeout(len(coins))
    logger.info(f"Запрос новостей для {len(coins)} монет с динамическим таймаутом {timeout:.1f}с.")

    try:
        client = _get_internal_http_client()
        response = await client.post(
            f"{API_BASE_URL}{API_PREFIX_NEWS}/get",
            json={"mode": "custom", "coins": coins},
            headers=_get_auth_headers(),
            timeout=timeout  # <-- Используем рассчитанный таймаут
        )
        response.raise_for_status()
        return response.json()
    except httpx.ReadTimeout:
        logger.error(f"Таймаут ({timeout:.1f}с) при запросе новостей к API.")
        return None
    except httpx.HTTPError as e:
        logger.error(f"Ошибка API при получении новостей: {e}")
        return None


@api_ready_check
async def get_news_top10_from_api() -> Optional[Dict]:
    """Запрашивает новости по топ-10 монетам."""
    timeout = AI_REQUEST_TIMEOUT
    logger.info(f"Запрос новостей по топ-10 монетам с таймаутом {timeout:.1f}с.")
    try:
        client = _get_internal_http_client()
        response = await client.post(
            f"{API_BASE_URL}{API_PREFIX_NEWS}/get",
            json={"mode": "top10"},
            headers=_get_auth_headers(),
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Ошибка API при получении топ-10 новостей: {e}")
        return None


@api_ready_check
async def get_all_assets_from_api() -> Optional[Dict]:
    """Запрашивает у API полный список уникальных активов."""
    try:
        client = _get_internal_http_client()
        response = await client.get(
            f"{API_BASE_URL}/assets",
            timeout=GET_ALL_ASSETS_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Ошибка API при получении списка активов: {e}")
        return None


@api_ready_check
async def get_top_coins_from_api(limit: int = 10) -> Optional[List[str]]:
    """Запрашивает список топ-монет у API."""
    try:
        url = f"{API_BASE_URL}/system/coins/top"
        params = {"limit": limit}
        timeout = httpx.Timeout(DEFAULT_API_TIMEOUT)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)

        if response.status_code == 200:
            return response.json().get("coins", [])
        else:
            logger.error(f"API ошибка при получении топ монет: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Не удалось подключиться к API для получения топ монет: {e}")
        return None


@api_ready_check
async def get_market_intel_from_api() -> Optional[Dict]:
    """Запрашивает сводку рыночной аналитики у API."""
    try:
        url = f"{API_BASE_URL}/intel/summary"
        timeout = httpx.Timeout(NEWS_HTTP_TIMEOUT)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)

        if response.status_code == 200:
            data = response.json().get("data")
            # ИСПРАВЛЕНИЕ: Возвращаем данные, только если они не пустые
            if data and (data.get('trending') or data.get('gainers') or data.get('losers')):
                return data
            else:
                logger.info("API аналитики вернуло пустые данные.")
                return None
        else:
            logger.error(f"API ошибка при получении рыночной аналитики: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Не удалось подключиться к API для получения рыночной аналитики: {e}")
        return None
