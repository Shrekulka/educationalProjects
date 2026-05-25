# inter_exchange_arbitrage_bot/src/services/news_providers/cryptocompare_provider.py

import asyncio
from typing import List, Dict, Any, Set
import httpx

from src.constants.api_constants import CRYPTOCOMPARE_API_URL, NEWS_HTTP_TIMEOUT
from src.core.config import NewsProvidersConfig
from src.utils.logger import logger
from src.utils.helpers import parse_date_safe
from .base_provider import BaseNewsProvider


class CryptoCompareProvider(BaseNewsProvider):
    """
    ИСПРАВЛЕННЫЙ CryptoCompareProvider.
    Стратегия: Использует несколько ключей для параллельного запроса новостей
    по разным группам монет. Внутри каждого запроса параллельно запрашиваются
    новости на RU и EN языках.
    """

    def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        super().__init__("CryptoCompare", api_config, http_session)

    def _supports_parallel_requests(self) -> bool:
        """Включаем параллельный режим, если есть несколько ключей."""
        return len(self._api_keys) > 1

    async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        """
        РЕАЛИЗАЦИЯ АБСТРАКТНОГО МЕТОДА.
        Для переданной группы монет и ключа запрашивает новости на двух языках параллельно.
        """
        if not coins:
            return []

        ru_task = self._fetch_lang(coins, 'RU', api_key, key_index)
        en_task = self._fetch_lang(coins, 'EN', api_key, key_index)

        # return_exceptions=True важно для параллельного режима, чтобы одна ошибка не остановила всё.
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

    async def _fetch_lang(self, coins: Set[str], lang: str, api_key: str, key_index: int) -> List[Dict]:
        """
        Запрос новостей для определенного языка. Выбрасывает исключение при ошибке.
        """
        categories = ",".join([c.upper() for c in coins if c.lower() not in {'bitcoin', 'general'}])
        if not categories:
            return []

        headers = {'authorization': f'Apikey {api_key}'}
        params = {'categories': categories, 'lang': lang}

        async with self._request_semaphore:
            response = await self._make_request(
                method="GET",
                url=CRYPTOCOMPARE_API_URL,
                key_index=key_index,
                headers=headers,
                params=params,
                timeout=NEWS_HTTP_TIMEOUT
            )
            # Выбросит исключение при ошибках 4xx/5xx
            response.raise_for_status()
            data = response.json().get('Data', [])

        return [
            self._format_news_item(
                title=i.get('title'), body=i.get('body'), url=i.get('url'),
                image_url=i.get('imageurl'),
                published_at_dt=parse_date_safe(str(i.get('published_on')), self.name) if i.get(
                    'published_on') else None
            ) for i in data if i.get('url')
        ]






