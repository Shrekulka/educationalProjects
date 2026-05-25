# inter_exchange_arbitrage_bot/src/services/news_providers/cryptopanic_provider.py

from typing import List, Dict, Any, Set

import httpx

from src.constants.api_constants import CRYPTOPANIC_API_BASE_URL, NEWS_HTTP_TIMEOUT
from src.core.config import NewsProvidersConfig
from src.utils.helpers import parse_date_safe
from .base_provider import BaseNewsProvider


class CryptoPanicProvider(BaseNewsProvider):
    """
    ИСПРАВЛЕННЫЙ CryptoPanicProvider.
    Стратегия: Использует один агрегированный запрос для всех монет.
    ПАРАЛЛЕЛЬНЫЙ РЕЖИМ ОТКЛЮЧЕН, так как API не получает преимуществ от
    распределения монет по разным ключам. Ротация ключей работает в
    последовательном режиме при ошибках.
    """

    def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        super().__init__("CryptoPanic", api_config, http_session)

    def _supports_parallel_requests(self) -> bool:
        """API не предназначено для параллельных запросов по разным монетам."""
        return False

    async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        """
        РЕАЛИЗАЦИЯ АБСТРАКТНОГО МЕТОДА.
        Выполняет один запрос для всех монет. При ошибке выбрасывает исключение,
        что позволяет BaseProvider выполнить ротацию ключа.
        """
        if not coins:
            return []

        params = {
            'auth_token': api_key,
            'currencies': ",".join([c.upper() for c in coins]),
            'public': 'true'
        }

        # ВАЖНО: Нет блока try-except. Ошибки должны "пробрасываться" наверх.
        async with self._request_semaphore:
            response = await self._make_request(
                method="GET",
                url=CRYPTOPANIC_API_BASE_URL,
                key_index=key_index,
                params=params,
                timeout=NEWS_HTTP_TIMEOUT
            )
            # Выбросит исключение httpx.HTTPStatusError для кодов 4xx/5xx
            response.raise_for_status()
            data = response.json().get('results', [])

        return [
            self._format_news_item(
                title=i.get('title'),
                body=i.get('title'),
                url=i.get('url'),
                published_at_dt=parse_date_safe(i.get('created_at'), self.name) if i.get('created_at') else None
            )
            for i in data if i.get('url')
        ]

