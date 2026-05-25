# inter_exchange_arbitrage_bot/src/services/market_intelligence_service.py

import asyncio
import json
import time
from typing import Dict, Any, Optional, List, Set

import httpx

from src.constants.api_constants import (
    COINGECKO_API_BASE_URL, NEWS_HTTP_TIMEOUT, COINGECKO_COMMON_SYMBOL_TO_ID_MAP,
    COINGECKO_COIN_LIST_CACHE_TTL_SECONDS, COINGECKO_EVENTS_REQUEST_DELAY_SECONDS,
    COINGECKO_MARKETS_PER_PAGE_LIMIT, COINGECKO_TOP_GAINERS_LOSERS_COUNT,
    COINGECKO_MIN_VOLUME_FOR_GAINERS_LOSERS, COINGECKO_MAX_CONCURRENT_REQUESTS
)
from src.core.config import NewsProvidersConfig
from src.utils.decorators import check_api_key
from src.utils.helpers import get_canonical_symbol
from src.utils.logger import logger


class MarketIntelligenceService:
    def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        self.config = api_config
        self.session = http_session
        self._coin_list_cache: Optional[List[Dict]] = None
        self._coin_list_cache_time: float = 0
        self._symbol_to_id_cache: Dict[str, str] = {}
        self._api_semaphore = asyncio.Semaphore(COINGECKO_MAX_CONCURRENT_REQUESTS)

    def get_coingecko_auth_params(self) -> Dict[str, str]:
        """
        Возвращает параметры аутентификации для CoinGecko Demo API.
        ИСПРАВЛЕНО: использует первый ключ из списка.
        """
        # Проверяем, что список ключей не пуст и первый ключ не является пустой строкой
        if self.config.coingecko and self.config.coingecko[0]:
            # Берем первый ключ из списка
            return {'x_cg_demo_api_key': self.config.coingecko[0]}
        return {}

    async def _get_full_coin_list(self) -> List[Dict]:
        """Кэширует полный список монет от CoinGecko (кэш 1 час)."""
        if self._coin_list_cache and (
                time.time() - self._coin_list_cache_time < COINGECKO_COIN_LIST_CACHE_TTL_SECONDS):  # <-- ИСПОЛЬЗУЕМ КОНСТАНТУ
            return self._coin_list_cache
        try:
            url = f"{COINGECKO_API_BASE_URL}/coins/list"
            params = self.get_coingecko_auth_params()
            response = await self.session.get(url, params=params, timeout=NEWS_HTTP_TIMEOUT)
            response.raise_for_status()
            coin_list = response.json()
            self._coin_list_cache = coin_list
            self._coin_list_cache_time = time.time()
            self._symbol_to_id_cache.clear()
            logger.info(f"CoinGecko: Кэш ID монет обновлен ({len(coin_list)} монет).")
            return coin_list
        except Exception as e:
            logger.error(f"CoinGecko: Не удалось обновить список монет: {e}")
            return self._coin_list_cache or []

    @check_api_key(api_name="CoinGecko", config_key="coingecko")
    async def get_top_coin_symbols(self, limit: int = 10) -> List[str]:
        """
        Получает список тикеров топ-N монет по рыночной капитализации с CoinGecko.
        """
        try:
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                **self.get_coingecko_auth_params()
            }
            url = f"{COINGECKO_API_BASE_URL}/coins/markets"
            response = await self.session.get(url, params=params, timeout=NEWS_HTTP_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            symbols = [coin.get('symbol').upper() for coin in data if coin.get('symbol')]
            logger.info(f"CoinGecko: Успешно получено топ-{len(symbols)} монет по капитализации.")
            return symbols
        except Exception as e:
            logger.error(f"Ошибка API CoinGecko Markets (для get_top_coin_symbols): {e}")
            return []

    async def get_coin_id_by_symbol(self, symbol: str) -> Optional[str]:
        """
        Находит coin_id по тикеру, используя гибридный подход:
        1. Нормализация символа ('BITCOIN' -> 'BTC').
        2. Поиск в статическом кэше популярных монет.
        3. Поиск в динамическом кэше ранее найденных монет.
        4. Поиск по полному списку с API.
        """
        canonical_symbol = get_canonical_symbol(symbol)

        if canonical_symbol in COINGECKO_COMMON_SYMBOL_TO_ID_MAP:
            return COINGECKO_COMMON_SYMBOL_TO_ID_MAP[canonical_symbol]

        if canonical_symbol in self._symbol_to_id_cache:
            return self._symbol_to_id_cache[canonical_symbol]

        coin_list = await self._get_full_coin_list()

        matches = []
        for coin in coin_list:
            if coin.get('symbol', '').upper() == canonical_symbol:
                matches.append(coin)

        if not matches:
            logger.warning(f"CoinGecko: не удалось найти ID для символа '{symbol}'...")
            return None

        matches.sort(key=lambda c: len(c.get('id', '')))

        best_match = matches[0]
        coin_id = best_match.get('id')

        if coin_id:
            self._symbol_to_id_cache[canonical_symbol] = coin_id
            return coin_id

        logger.warning(f"CoinGecko: не удалось найти ID для символа '{symbol}' (канонический: '{canonical_symbol}')")
        return None

    async def _fetch_events_for_coin(self, coin_symbol: str, coin_id: str) -> List[Dict]:
        """
        Вспомогательная функция для получения событий для ОДНОЙ монеты.
        Именно здесь мы применяем семафор, чтобы контролировать каждый отдельный запрос.
        """
        # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
        logger.debug(f"CoinGecko Events (Task): Начинаю запрос для {coin_symbol} ({coin_id})...")
        task_start_time = time.time()
        # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====

        async with self._api_semaphore:
            try:
                await asyncio.sleep(COINGECKO_EVENTS_REQUEST_DELAY_SECONDS)

                url = f"{COINGECKO_API_BASE_URL}/coins/{coin_id}/events"
                params = self.get_coingecko_auth_params()
                response = await self.session.get(url, params=params, timeout=NEWS_HTTP_TIMEOUT)

                if response.status_code == 404:
                    logger.debug(f"События для {coin_symbol} недоступны (404)")
                    return []

                response.raise_for_status()
                data = response.json().get('events', [])

                # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
                task_time = time.time() - task_start_time
                logger.debug(
                    f"CoinGecko Events (Task): Успешный ответ для {coin_symbol} за {task_time:.2f} сек. Найдено {len(data)} событий.")
                # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====

                return [{
                    'title': f"Событие для {coin_symbol.upper()}: {event.get('title')}",
                    'body': event.get('description'),
                    'url': event.get('website'),
                    'source': f"CoinGecko Events ({event.get('type')})"
                } for event in data]

            except Exception as e:
                # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
                task_time = time.time() - task_start_time
                logger.error(
                    f"CoinGecko Events (Task): Ошибка для {coin_symbol} ({coin_id}) через {task_time:.2f} сек: {type(e).__name__} - {e}")
                # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
                return []

    # async def _fetch_events_for_coin(self, coin_symbol: str, coin_id: str) -> List[Dict]:
    #     """
    #     Вспомогательная функция для получения событий для ОДНОЙ монеты.
    #     Именно здесь мы применяем семафор, чтобы контролировать каждый отдельный запрос.
    #     """
    #     async with self._api_semaphore:
    #         try:
    #             await asyncio.sleep(COINGECKO_EVENTS_REQUEST_DELAY_SECONDS)  # <-- ИСПОЛЬЗУЕМ КОНСТАНТУ
    #
    #             url = f"{COINGECKO_API_BASE_URL}/coins/{coin_id}/events"
    #             params = self.get_coingecko_auth_params()
    #             response = await self.session.get(url, params=params, timeout=NEWS_HTTP_TIMEOUT)
    #
    #             if response.status_code == 404:
    #                 logger.debug(f"События для {coin_symbol} недоступны (404)")
    #                 return []
    #
    #             response.raise_for_status()
    #             data = response.json().get('events', [])
    #
    #             return [{
    #                 'title': f"Событие для {coin_symbol.upper()}: {event.get('title')}",
    #                 'body': event.get('description'),
    #                 'url': event.get('website'),
    #                 'source': f"CoinGecko Events ({event.get('type')})"
    #             } for event in data]
    #
    #         except Exception as e:
    #             logger.error(f"Ошибка API CoinGecko Events для {coin_id}: {e}")
    #             return []

    @check_api_key(api_name="CoinGecko", config_key="coingecko")
    async def get_coingecko_events(self, coins: Set[str]) -> List[Dict]:
        """
        Получает события для списка монет параллельно, но с ограничением
        через семафор для избежания rate limit.
        """
        # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
        logger.debug(f"CoinGecko Events: Начало сбора событий для {len(coins)} монет: {coins}")
        start_time = time.time()
        # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====

        tasks = []
        for coin_symbol in coins:
            # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
            logger.debug(f"CoinGecko Events: Поиск ID для символа '{coin_symbol}'...")
            # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====

            coin_id = await self.get_coin_id_by_symbol(coin_symbol)
            if not coin_id:
                # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
                logger.debug(f"CoinGecko Events: ID для '{coin_symbol}' не найден, пропуск.")
                # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
                continue

            # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
            logger.debug(f"CoinGecko Events: ID для '{coin_symbol}' найден: '{coin_id}'. Создаю задачу.")
            # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
            tasks.append(self._fetch_events_for_coin(coin_symbol, coin_id))

        if not tasks:
            # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
            logger.debug("CoinGecko Events: Не создано ни одной задачи для получения событий.")
            # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
            return []

        # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
        logger.debug(f"CoinGecko Events: Запускаю asyncio.gather для {len(tasks)} задач...")
        gather_start_time = time.time()
        # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====

        results = await asyncio.gather(*tasks)

        # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
        gather_time = time.time() - gather_start_time
        logger.debug(f"CoinGecko Events: asyncio.gather ЗАВЕРШЕН за {gather_time:.2f} сек.")
        # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====

        all_events = [event for sublist in results for event in sublist]

        # ===== НАЧАЛО ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====
        total_time = time.time() - start_time
        logger.debug(
            f"CoinGecko Events: Сбор событий ЗАВЕРШЕН за {total_time:.2f} сек. Всего найдено: {len(all_events)} событий.")
        # ===== КОНЕЦ ИЗМЕНЕНИЙ (ЛОГИРОВАНИЕ) =====

        return all_events

    # @check_api_key(api_name="CoinGecko", config_key="coingecko")
    # async def get_coingecko_events(self, coins: Set[str]) -> List[Dict]:
    #     """
    #     Получает события для списка монет параллельно, но с ограничением
    #     через семафор для избежания rate limit.
    #     """
    #     tasks = []
    #     for coin_symbol in coins:
    #         coin_id = await self.get_coin_id_by_symbol(coin_symbol)
    #         if not coin_id:
    #             continue
    #
    #         tasks.append(self._fetch_events_for_coin(coin_symbol, coin_id))
    #
    #     if not tasks:
    #         return []
    #
    #     results = await asyncio.gather(*tasks)
    #
    #     all_events = [event for sublist in results for event in sublist]
    #     return all_events

    @check_api_key(api_name="CoinGecko", config_key="coingecko")
    async def get_trending_coins(self) -> List[Dict[str, Any]]:
        """Получает список трендовых монет с CoinGecko."""
        if not self.config.coingecko:
            return []
        try:
            url = f"{COINGECKO_API_BASE_URL}/search/trending"
            params = self.get_coingecko_auth_params()
            response = await self.session.get(url, params=params, timeout=NEWS_HTTP_TIMEOUT)
            response.raise_for_status()
            data = response.json().get('coins', [])
            logger.debug(f"Сырой ответ от CoinGecko Trending ({len(data)} шт.): {json.dumps(data, indent=2)}")
            return [
                {
                    "name": coin['item'].get('name'),
                    "symbol": coin['item'].get('symbol'),
                    "market_cap_rank": coin['item'].get('market_cap_rank')
                } for coin in data
            ]
        except Exception as e:
            logger.error(f"Ошибка API CoinGecko Trending: {e}")
            return []

    @check_api_key(api_name="CoinGecko", config_key="coingecko")
    async def get_top_gainers_losers(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Получает лидеров роста и падения через эндпоинт /coins/markets.
        """
        try:
            params = {
                'vs_currency': 'usd',
                'per_page': COINGECKO_MARKETS_PER_PAGE_LIMIT,  # <-- ИСПОЛЬЗУЕМ КОНСТАНТУ
                'price_change_percentage': '24h',
                **self.get_coingecko_auth_params()
            }
            url = f"{COINGECKO_API_BASE_URL}/coins/markets"

            response = await self.session.get(url, params=params, timeout=NEWS_HTTP_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            valid_coins = [
                c for c in data
                if c.get('total_volume', 0) > COINGECKO_MIN_VOLUME_FOR_GAINERS_LOSERS and c.get(
                    'price_change_percentage_24h') is not None  # <-- ИСПОЛЬЗУЕМ КОНСТАНТУ
            ]

            valid_coins.sort(key=lambda x: x['price_change_percentage_24h'], reverse=True)
            top_gainers = valid_coins[:COINGECKO_TOP_GAINERS_LOSERS_COUNT]  # <-- ИСПОЛЬЗУЕМ КОНСТАНТУ

            top_losers = sorted(valid_coins, key=lambda x: x['price_change_percentage_24h'])[
                         :COINGECKO_TOP_GAINERS_LOSERS_COUNT]  # <-- ИСПОЛЬЗУЕМ КОНСТАНТУ

            result = {
                "gainers": [{"name": g.get('name'), "symbol": g.get('symbol').upper(),
                             "change_24h": g.get('price_change_percentage_24h')} for g in top_gainers],
                "losers": [{"name": l.get('name'), "symbol": l.get('symbol').upper(),
                            "change_24h": l.get('price_change_percentage_24h')} for l in top_losers]
            }
            return result
        except Exception as e:
            logger.error(f"Ошибка API CoinGecko Markets (gainers/losers): {e}")
            return {"gainers": [], "losers": []}

    async def check_api_usage(self) -> Optional[Dict[str, Any]]:
        """
        Проверяет доступность CoinGecko API через эндпоинт /ping
        для Demo-ключа.
        """
        if not self.config.coingecko:
            logger.warning("CoinGecko ключ не настроен, проверка использования невозможна.")
            return None
        try:
            url = f"{COINGECKO_API_BASE_URL}/ping"
            params = self.get_coingecko_auth_params()
            response = await self.session.get(url, params=params, timeout=NEWS_HTTP_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            if data.get("gecko_says") == "(V3) To the Moon!":
                logger.info("CoinGecko Demo API: Ping успешен. API работает.")
                # Для Demo-ключа мы не можем получить точные лимиты, поэтому возвращаем заглушку
                return {"status": "operational", "current_remaining_monthly_calls": "N/A (Demo Plan)"}
            else:
                logger.warning(f"CoinGecko Demo API: Ping вернул неожиданный ответ: {data}")
                return {"status": "unresponsive", "message": "Ping провален или неожиданный ответ"}
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.warning("Не удалось проверить использование CoinGecko API: ключ невалиден.")
            else:
                logger.error(f"Ошибка API CoinGecko Usage Check: {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка API CoinGecko Usage Check: {e}")
            return None
