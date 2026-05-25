# inter_exchange_arbitrage_bot/src/services/news_providers/coinmarketcap_provider.py

from typing import List, Dict, Any, Set

import httpx

from src.constants.api_constants import CMC_PRO_API_BASE_URL, CMC_QUOTES_LATEST_ENDPOINT, NEWS_HTTP_TIMEOUT
from src.core.config import NewsProvidersConfig
from src.utils.helpers import parse_date_safe
from src.utils.logger import logger
from .base_provider import BaseNewsProvider


class CoinMarketCapProvider(BaseNewsProvider):
    """
    ИСПРАВЛЕННЫЙ CoinMarketCapProvider.
    Ключевая оптимизация (сохранена): делает один консолидированный запрос для группы монет.
    Новая логика: теперь полностью поддерживает параллельный режим, разделяя большие
    группы монет между несколькими ключами.
    """

    def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        super().__init__("CoinMarketCap", api_config, http_session)

    def _supports_parallel_requests(self) -> bool:
        """Включаем параллельный режим, если есть несколько ключей."""
        return len(self._api_keys) > 1

    def _distribute_coins_among_keys(self, coins: Set[str], available_keys: List[str]) -> List[Set[str]]:
        """
        ПЕРЕОПРЕДЕЛЕНИЕ (сохранено): Для CMC оптимальнее группировать монеты большими группами.
        Эта логика остается, так как она специфична для данного API.
        """
        coins_list = list(coins)
        if len(coins_list) <= 10 or len(available_keys) == 1:
            return [coins]
        num_keys = len(available_keys)
        coin_groups = [set() for _ in range(num_keys)]
        for i, coin in enumerate(coins_list):
            coin_groups[i % num_keys].add(coin)
        return coin_groups

    async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        """
        РЕАЛИЗАЦИЯ АБСТРАКТНОГО МЕТОДА.
        Выполняет один запрос для всей группы монет. Выбрасывает исключение при ошибке.
        """
        if not coins:
            return []

        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
        symbols_str = ",".join([c.upper() for c in coins])
        params = {'symbol': symbols_str, 'convert': 'USD'}
        url = f"{CMC_PRO_API_BASE_URL}{CMC_QUOTES_LATEST_ENDPOINT}"

        try:
            async with self._request_semaphore:
                response = await self._make_request(
                    method="GET",
                    url=url,
                    key_index=key_index,
                    headers=headers,
                    params=params,
                    timeout=NEWS_HTTP_TIMEOUT
                )
                # Выбросит исключение для кодов 4xx/5xx, что позволит BaseProvider сменить ключ
                response.raise_for_status()
                data = response.json().get('data', {})

            formatted_news = []
            for symbol, coin_data_list in data.items():
                # API может вернуть { "BTC": [..], "ETH": null }
                if not isinstance(coin_data_list, list) or not coin_data_list:
                    continue

                coin_data = coin_data_list[0]  # Берем первый элемент, как и раньше
                quote = coin_data.get('quote', {}).get('USD', {})
                price = quote.get('price')

                if price is None: continue

                percent_change_24h = quote.get('percent_change_24h')
                volume_24h = quote.get('volume_24h')
                title = f"Обновление рынка: {coin_data.get('name', symbol)} ({symbol})"
                body_parts = [f"Цена: ${price:,.4f}"]
                if percent_change_24h is not None:
                    change_str = f"+{percent_change_24h:.2f}%" if percent_change_24h >= 0 else f"{percent_change_24h:.2f}%"
                    body_parts.append(f"24ч: {change_str}")
                if volume_24h is not None:
                    body_parts.append(f"Объем: ${volume_24h:,.0f}")
                body = " | ".join(body_parts)

                formatted_news.append(self._format_news_item(
                    title=title, body=body,
                    url=f"https://coinmarketcap.com/currencies/{coin_data.get('slug', symbol.lower())}/",
                    published_at_dt=parse_date_safe(quote.get('last_updated'), self.name)
                ))
            return formatted_news

        except httpx.HTTPStatusError as e:
            # Логируем специфичные ошибки, но пробрасываем исключение дальше,
            # чтобы BaseProvider мог отреагировать.
            logger.error(
                f"[{self.name}] (Ключ #{key_index + 1}): HTTP ошибка {e.response.status_code} - {e.response.text}")
            raise e
        except Exception as e:
            logger.error(f"[{self.name}] (Ключ #{key_index + 1}): Неожиданная ошибка: {e}", exc_info=True)
            raise e  # Пробрасываем дальше




