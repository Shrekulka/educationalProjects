# inter_exchange_arbitrage_bot/src/services/news_providers/messari_provider.py

import asyncio
from typing import List, Dict, Any, Set

import httpx

from src.constants.api_constants import MESSARI_API_URL, NEWS_HTTP_TIMEOUT
from src.core.config import NewsProvidersConfig
from src.utils.helpers import parse_date_safe
from src.utils.logger import logger
from .base_provider import BaseNewsProvider
from ...core.resilience import retry_with_backoff


class MessariProvider(BaseNewsProvider):
    """
    ИСПРАВЛЕННЫЙ MessariProvider.
    Стратегия: Использует множественные API ключи для параллельного запроса
    новостей по разным группам монет.
    """

    def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        super().__init__("Messari", api_config, http_session)

    def _supports_parallel_requests(self) -> bool:
        """Включаем параллельный режим, если есть несколько ключей."""
        return len(self._api_keys) > 1

    async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        """
        РЕАЛИЗАЦИЯ АБСТРАКТНОГО МЕТОДА.
        Для переданной группы монет и ключа запрашивает новости по каждой монете параллельно.
        """
        if not coins:
            return []

        headers = {'x-messari-api-key': api_key}
        tasks = [self._fetch_for_coin(coin, headers, key_index) for coin in coins]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_news = []
        has_critical_error = False
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"[{self.name}] (Ключ #{key_index + 1}): Ошибка в подзапросе: {result}")
                if isinstance(result, httpx.HTTPStatusError) and result.response.status_code in [401, 403, 429]:
                    has_critical_error = True

        if has_critical_error:
            raise Exception(f"Критическая ошибка API с ключом #{key_index + 1}")

        return all_news

    @retry_with_backoff(max_retries=3)  # Декоратор retry здесь уместен
    async def _fetch_for_coin(self, coin: str, headers: Dict, key_index: int) -> List[Dict]:
        """
        Запрос новостей для одной монеты. Выбрасывает исключение при ошибке.
        """
        url = f"{MESSARI_API_URL}?assetKeys={coin.lower()}"

        async with self._request_semaphore:
            response = await self._make_request(
                method="GET",
                url=url,
                key_index=key_index,
                headers=headers,
                timeout=NEWS_HTTP_TIMEOUT
            )

            if response.status_code == 404:
                logger.debug(f"[{self.name}] (ключ #{key_index + 1}): Нет данных для {coin}")
                return []

            # Выбросит исключение при других ошибках
            response.raise_for_status()
            data = response.json().get('data')

            if not data:
                return []

            return [
                self._format_news_item(
                    title=item.get('title'), body=item.get('content'), url=item.get('url'),
                    published_at_dt=parse_date_safe(item.get('published_at'), self.name) if item.get(
                        'published_at') else None
                ) for item in data if item.get('url')
            ]


