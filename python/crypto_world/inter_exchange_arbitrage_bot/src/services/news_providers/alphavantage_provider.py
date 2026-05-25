# inter_exchange_arbitrage_bot/src/services/news_providers/alphavantage_provider.py

import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Set

import httpx

from src.constants.api_constants import (
    ALPHAVANTAGE_API_URL, NEWS_HTTP_TIMEOUT, NEWS_FETCH_DAYS_AGO,
    ALPHAVANTAGE_NEWS_FETCH_LIMIT, ALPHAVANTAGE_SUPPORTED_CRYPTO_SYMBOLS,
    ALPHAVANTAGE_RATE_LIMIT_DELAY_SECONDS
)
from src.core.config import NewsProvidersConfig
from .base_provider import BaseNewsProvider
from ...utils.helpers import parse_date_safe


class AlphaVantageProvider(BaseNewsProvider):
    def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        super().__init__("AlphaVantage", api_config, http_session)
        self._general_news_cache: List[Dict[str, Any]] = []
        self._cache_lock = asyncio.Lock()

    async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        from_time_str = (datetime.now(timezone.utc) - timedelta(days=NEWS_FETCH_DAYS_AGO)).strftime('%Y%m%dT%H%M')
        all_news = []
        supported_coins = {c.upper() for c in coins if c.upper() in ALPHAVANTAGE_SUPPORTED_CRYPTO_SYMBOLS}

        for coin in supported_coins:
            params = {
                'function': 'NEWS_SENTIMENT',
                'tickers': f"CRYPTO:{coin}",
                'apikey': api_key,
                'limit': ALPHAVANTAGE_NEWS_FETCH_LIMIT,
                'time_from': from_time_str,
                'sort': 'LATEST'
            }
            news_items = await self._perform_api_request(params, key_index)
            all_news.extend(news_items)

            if coin != list(supported_coins)[-1]:
                await asyncio.sleep(ALPHAVANTAGE_RATE_LIMIT_DELAY_SECONDS)

        unsupported_coins = coins - supported_coins
        if key_index == 0 and (not all_news or unsupported_coins):
            # Этот вызов тоже может выбросить исключение
            await self._fetch_general_news_once(api_key, from_time_str, all_news, key_index)

        return all_news

    async def _fetch_general_news_once(self, api_key: str, from_time_str: str, existing_news: List, key_index: int) -> None:
        async with self._cache_lock:
            if self._general_news_cache:
                existing_news.extend(self._general_news_cache)
                return
            params = {
                'function': 'NEWS_SENTIMENT',
                'topics': 'blockchain',
                'apikey': api_key,
                'limit': ALPHAVANTAGE_NEWS_FETCH_LIMIT,
                'time_from': from_time_str,
                'sort': 'LATEST'
            }
            general_news = await self._perform_api_request(params, key_index)
            self._general_news_cache = general_news
            existing_news.extend(general_news)

    async def _perform_api_request(self, params: Dict[str, Any], key_index: int) -> List[Dict[str, Any]]:
        async with self._request_semaphore:
            response = await self._make_request(
                method="GET",
                url=ALPHAVANTAGE_API_URL,
                key_index=key_index,
                params=params,
                timeout=NEWS_HTTP_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            if "Information" in data or "Error Message" in data:
                error_msg = data.get("Information") or data.get("Error Message", "Unknown API error")
                raise Exception(error_msg)
            feed = data.get('feed', [])
            return [
                self._format_news_item(
                    title=item.get('title'),
                    body=item.get('summary'),
                    url=item.get('url'),
                    image_url=item.get('banner_image'),
                    published_at_dt=parse_date_safe(item.get('time_published'), self.name)
                ) for item in feed
            ]

# class AlphaVantageProvider(BaseNewsProvider):
#     """
#     Чистая реализация AlphaVantageProvider с явным разделением логики
#     для последовательного (строгого) и параллельного (толерантного) режимов.
#     """
#
#     def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
#         super().__init__("AlphaVantage", api_config, http_session)
#         self._general_news_cache: List[Dict[str, Any]] = []
#         self._cache_lock = asyncio.Lock()
#
#     async def _do_fetch(self, coins: Set[str]) -> List[Dict[str, Any]]:
#         current_key = self._get_current_api_key()
#         if not current_key: return []
#         # Вызываем строгий метод, который пробрасывает исключения для ротации
#         return await self._fetch_logic(coins, current_key, self._current_key_index, is_strict=True)
#
#         # --- Метод для ПАРАЛЛЕЛЬНОГО режима (толерантный) ---
#
#     async def _do_fetch_with_key(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
#         # Этот метод уже обернут в safe_parallel_execution, поэтому все исключения будут пойманы
#         return await self._fetch_logic(coins, api_key, key_index, is_strict=False)
#
#         # --- Единая бизнес-логика с контекстом ---
#
#     async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int, is_strict: bool) -> List[
#         Dict[str, Any]]:
#         from_time_str = (datetime.now(timezone.utc) - timedelta(days=NEWS_FETCH_DAYS_AGO)).strftime('%Y%m%dT%H%M')
#         all_news = []
#         supported_coins = {c.upper() for c in coins if c.upper() in ALPHAVANTAGE_SUPPORTED_CRYPTO_SYMBOLS}
#         unsupported_coins = coins - supported_coins
#
#         if unsupported_coins:
#             logger.debug(f"[{self.name}] (Ключ #{key_index + 1}): Пропущены тикеры: {unsupported_coins}")
#
#         # Цикл по монетам: обрабатываем ошибки в зависимости от режима
#         for coin in supported_coins:
#             try:
#                 params = {
#                     'function': 'NEWS_SENTIMENT',
#                     'tickers': f"CRYPTO:{coin}",
#                     'apikey': api_key,
#                     'limit': ALPHAVANTAGE_NEWS_FETCH_LIMIT,
#                     'time_from': from_time_str,
#                     'sort': 'LATEST'
#                 }
#                 news_items = await self._perform_api_request(params)
#                 all_news.extend(news_items)
#                 if coin != list(supported_coins)[-1]:
#                     await asyncio.sleep(ALPHAVANTAGE_RATE_LIMIT_DELAY_SECONDS)
#             except Exception as e:
#                 logger.error(f"[{self.name}] (Ключ #{key_index + 1}): Ошибка для {coin}: {e}")
#                 if is_strict:
#                     raise e  # В строгом режиме пробрасываем ошибку
#                 else:
#                     continue  # В толерантном режиме просто пропускаем монету
#
#         # Загрузка общих новостей: обрабатываем ошибки в зависимости от режима
#         if key_index == 0 and (not all_news or unsupported_coins):
#             try:
#                 await self._fetch_general_news_once(api_key, from_time_str, all_news)
#             except Exception as e:
#                 logger.error(f"[{self.name}] (Ключ #{key_index + 1}): Ошибка при загрузке общих новостей: {e}")
#                 if is_strict:
#                     raise e  # В строгом режиме пробрасываем
#
#         return all_news
#
#     async def _fetch_general_news_once(self, api_key: str, from_time_str: str, existing_news: List) -> None:
#         async with self._cache_lock:
#             if self._general_news_cache:
#                 existing_news.extend(self._general_news_cache)
#                 return
#
#             params = {
#                 'function': 'NEWS_SENTIMENT', 'topics': 'blockchain', 'apikey': api_key,
#                 'limit': ALPHAVANTAGE_NEWS_FETCH_LIMIT, 'time_from': from_time_str, 'sort': 'LATEST'
#             }
#             # _perform_api_request выбросит исключение, если что-то пойдет не так.
#             # Мы его здесь не ловим, чтобы ошибка была видна вызывающему коду.
#             general_news = await self._perform_api_request(params)
#             self._general_news_cache = general_news
#             existing_news.extend(general_news)
#
#     async def _perform_api_request(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
#         """Единый метод API запроса. Всегда выбрасывает исключение при ошибке."""
#         try:
#             response = await self.session.get(ALPHAVANTAGE_API_URL, params=params, timeout=NEWS_HTTP_TIMEOUT)
#             response.raise_for_status()
#             data = response.json()
#
#             if "Information" in data or "Error Message" in data:
#                 error_msg = data.get("Information") or data.get("Error Message", "Unknown API error")
#                 raise Exception(error_msg)
#
#             feed = data.get('feed', [])
#             return [
#                 self._format_news_item(
#                     title=item.get('title'),
#                     body=item.get('summary'),
#                     url=item.get('url'),
#                     image_url=item.get('banner_image'),
#                     published_at_dt=parse_date_safe(item.get('time_published'), self.name)
#                 ) for item in feed
#             ]
#         except Exception as e:
#             raise e
