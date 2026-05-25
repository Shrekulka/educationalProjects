# inter_exchange_arbitrage_bot/src/services/news_providers/newsapi_provider.py

import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Set

import httpx

from src.constants.api_constants import (NEWSAPI_API_URL, NEWS_HTTP_TIMEOUT, NEWS_FETCH_DAYS_AGO)
from src.core.config import NewsProvidersConfig
from src.utils.logger import logger
from .base_provider import BaseNewsProvider
from ...utils.helpers import parse_date_safe


class NewsApiProvider(BaseNewsProvider):
    """
    ИСПРАВЛЕННЫЙ NewsApiProvider.
    Стратегия: Распределяет группы монет между доступными ключами и выполняет
    запросы параллельно. Для каждой группы запрашивает RU и EN языки также параллельно.
    """

    def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        super().__init__("NewsAPI", api_config, http_session)

    def _supports_parallel_requests(self) -> bool:
        """Включаем параллельный режим, если есть несколько ключей."""
        return len(self._api_keys) > 1

    async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        """
        РЕАЛИЗАЦИЯ АБСТРАКТНОГО МЕТОДА.
        Выполняет запросы с конкретным API ключом, запрашивая оба языка параллельно.
        """
        if not coins:
            return []

        ru_task = self._fetch_lang(coins, 'ru', api_key, key_index)
        en_task = self._fetch_lang(coins, 'en', api_key, key_index)

        results = await asyncio.gather(ru_task, en_task, return_exceptions=True)

        all_news = []
        has_critical_error = False
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"[{self.name}] (Ключ #{key_index + 1}): Ошибка в языковом подзапросе: {result}")
                if isinstance(result, httpx.HTTPStatusError) and result.response.status_code in [401, 403, 429]:
                    has_critical_error = True

        if has_critical_error:
            raise Exception(f"Критическая ошибка API с ключом #{key_index + 1}")

        return all_news

    async def _fetch_lang(self, coins: Set[str], language: str, api_key: str, key_index: int) -> List[Dict]:
        """
        Запрос новостей для определенного языка. Выбрасывает исключение при ошибке.
        """
        query = " OR ".join(f'"{c}"' for c in coins)
        from_date = (datetime.now(timezone.utc) - timedelta(days=NEWS_FETCH_DAYS_AGO)).strftime('%Y-%m-%d')

        params = {
            'qInTitle': query, 'sortBy': 'publishedAt', 'language': language,
            'apiKey': api_key, 'excludeDomains': "habr.com,rg.ru", 'from': from_date
        }

        async with self._request_semaphore:
            response = await self._make_request(
                method="GET",
                url=NEWSAPI_API_URL,
                key_index=key_index,
                params=params,
                timeout=NEWS_HTTP_TIMEOUT
            )
            # Выбросит исключение при ошибке для ротации ключей
            response.raise_for_status()
            articles = response.json().get('articles', [])

        return [
            self._format_news_item(
                title=i.get('title'), body=i.get('description'), url=i.get('url'),
                image_url=i.get('urlToImage'),
                published_at_dt=parse_date_safe(i.get('publishedAt'), self.name) if i.get('publishedAt') else None
            ) for i in articles if i.get('url')
        ]

# class NewsApiProvider(BaseNewsProvider):
#     """
#     ОПТИМИЗИРОВАННЫЙ NewsApiProvider с поддержкой параллельных запросов.
#
#     СТРАТЕГИЯ ОПТИМИЗАЦИИ:
#     1. Распределяет языки (RU/EN) и группы монет между доступными ключами
#     2. Выполняет все запросы параллельно
#     3. Значительно сокращает время выполнения при наличии нескольких ключей
#     """
#
#     def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
#         super().__init__("NewsAPI", api_config, http_session)
#
#     def _supports_parallel_requests(self) -> bool:
#         """NewsAPI поддерживает параллельные запросы при наличии нескольких ключей."""
#         return False
#
#     async def _do_fetch_with_key(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
#         """
#         Выполняет запросы с конкретным API ключом.
#         ОПТИМИЗАЦИЯ: Каждый ключ обрабатывает как RU, так и EN для своей группы монет.
#         """
#         if not coins:
#             return []
#
#         # Каждый ключ запрашивает оба языка параллельно для своей группы монет
#         ru_task = self._fetch_lang(coins, 'ru', api_key, key_index)
#         en_task = self._fetch_lang(coins, 'en', api_key, key_index)
#
#         logger.debug(f"[{self.name}] (Ключ #{key_index + 1}): Начинаю внутренний gather для 2 языковых задач...")
#
#         results = await asyncio.gather(ru_task, en_task, return_exceptions=True)
#
#         logger.debug(f"[{self.name}] (Ключ #{key_index + 1}): Внутренний gather ЗАВЕРШЕН.")
#
#         all_news = []
#         for result in results:
#             if isinstance(result, list):
#                 all_news.extend(result)
#             elif isinstance(result, Exception):
#                 logger.debug(f"{self.name} (ключ #{key_index + 1}): Ошибка в одном из языковых запросов: {result}")
#
#         return all_news
#
#     async def _do_fetch(self, coins: Set[str]) -> List[Dict[str, Any]]:
#         """LEGACY: Сохранен для совместимости при использовании одного ключа."""
#         current_key = self._get_current_api_key()
#         if not current_key or not coins:
#             return []
#
#         return await self._do_fetch_with_key(coins, current_key, 0)
#
#     async def _fetch_lang(self, coins: Set[str], language: str, api_key: str, key_index: int = 0) -> List[Dict]:
#         """
#         Запрос новостей для определенного языка.
#         ОБНОВЛЕНО: Добавлен параметр key_index для логирования.
#         """
#         query = " OR ".join(f'"{c}"' for c in coins)
#         from_date = (datetime.now(timezone.utc) - timedelta(days=NEWS_FETCH_DAYS_AGO)).strftime('%Y-%m-%d')
#
#         params = {
#             'qInTitle': query,
#             'sortBy': 'publishedAt',
#             'language': language,
#             'apiKey': api_key,
#             'excludeDomains': "habr.com,rg.ru",
#             'from': from_date
#         }
#
#         try:
#             async with self._request_semaphore:
#                 response = await self.session.get(NEWSAPI_API_URL, params=params, timeout=NEWS_HTTP_TIMEOUT)
#                 response.raise_for_status()
#                 articles = response.json().get('articles', [])
#
#                 news_items = [
#                     self._format_news_item(
#                         title=i.get('title'),
#                         body=i.get('description'),
#                         url=i.get('url'),
#                         image_url=i.get('urlToImage'),
#                         published_at_dt=parse_date_safe(i.get('publishedAt'), self.name)
#                         if i.get('publishedAt') else None
#                     )
#                     for i in articles if i.get('url')
#                 ]
#
#                 logger.debug(f"{self.name} (ключ #{key_index + 1}, {language}): Получено {len(news_items)} новостей")
#                 return news_items
#
#         except Exception as e:
#             logger.error(f"{self.name} (ключ #{key_index + 1}, language={language}): Ошибка: {e}")
#             return []




