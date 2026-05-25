# inter_exchange_arbitrage_bot/src/services/news_providers/coincap_provider.py

import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Set

import httpx

from src.constants.api_constants import COINCAP_API_BASE_URL, NEWS_HTTP_TIMEOUT
from src.core.config import NewsProvidersConfig
from src.utils.logger import logger
from .base_provider import BaseNewsProvider


class CoinCapProvider(BaseNewsProvider):
    """
    ИСПРАВЛЕННЫЙ CoinCapProvider.
    Стратегия: Полностью использует возможности BaseNewsProvider для параллелизации.
    Запросы по разным группам монет выполняются параллельно на разных ключах.
    Внутри каждого ключа запросы к отдельным монетам также выполняются параллельно.
    """

    def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        super().__init__("CoinCap", api_config, http_session)

    def _supports_parallel_requests(self) -> bool:
        """Включаем параллельный режим, если есть несколько ключей."""
        return len(self._api_keys) > 1

    async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        """
        РЕАЛИЗАЦИЯ АБСТРАКТНОГО МЕТОДА.
        Выполняет параллельные запросы для группы монет, используя один ключ.
        """
        if not coins:
            return []

        headers = {'Authorization': f'Bearer {api_key}'}
        # Задачи создаются для каждой монеты в группе, переданной от BaseNewsProvider
        tasks = [self._fetch_single_coin(coin, headers, key_index) for coin in coins]

        # Используем gather для параллельного выполнения запросов ВНУТРИ ОДНОГО КЛЮЧА
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_news = []
        has_critical_error = False
        for result in results:
            if isinstance(result, list):  # _fetch_single_coin теперь возвращает список
                all_news.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"[{self.name}] (Ключ #{key_index + 1}): Ошибка в подзапросе: {result}")
                # Если произошла ошибка авторизации или лимитов, нужно "провалить" весь ключ
                if isinstance(result, httpx.HTTPStatusError) and result.response.status_code in [401, 403, 429]:
                    has_critical_error = True

        # Если была критическая ошибка, пробрасываем ее, чтобы BaseProvider мог сменить ключ в sequential режиме
        if has_critical_error:
            raise Exception(f"Критическая ошибка API (например, 401/429) с ключом #{key_index + 1}")

        return all_news

    async def _fetch_single_coin(self, coin: str, headers: Dict, key_index: int) -> List[Dict[str, Any]]:
        """
        Вспомогательная функция для получения данных по одной монете.
        ПРИМЕЧАНИЕ: Выбрасывает исключение при ошибке для обработки в _fetch_logic.
        Возвращает список с одним элементом или пустой список.
        """
        asset_id = coin.lower()
        url = f"{COINCAP_API_BASE_URL}/assets/{asset_id}"

        async with self._request_semaphore:
            response = await self._make_request(
                method="GET",
                url=url,
                key_index=key_index,
                headers=headers,
                timeout=NEWS_HTTP_TIMEOUT
            )

        if response.status_code == 404:
            logger.debug(f"[{self.name}] (Ключ #{key_index + 1}): Актив '{asset_id}' не найден.")
            return []  # Не является ошибкой, просто нет данных

        # Этот вызов выбросит исключение (например, httpx.HTTPStatusError) при кодах 4xx/5xx
        response.raise_for_status()
        asset = response.json().get('data')

        if not asset or not asset.get('priceUsd'):
            return []

        name = asset.get('name', asset.get('id'))
        symbol = asset.get('symbol', coin).upper()
        price_usd = float(asset['priceUsd'])
        change_24h = float(asset.get('changePercent24Hr', 0.0))

        title = f"Обновление {symbol}: {name}"
        change_sign = "+" if change_24h >= 0 else ""
        body = f"Цена: ${price_usd:,.4f} | 24ч: {change_sign}{change_24h:.2f}%"

        # Возвращаем список, чтобы было консистентно с другими провайдерами
        return [self._format_news_item(
            title=title,
            body=body,
            url=f"https://coincap.io/assets/{asset.get('id')}",
            published_at_dt=datetime.now(timezone.utc)
        )]

