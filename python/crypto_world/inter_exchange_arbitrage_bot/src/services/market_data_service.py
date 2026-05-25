# inter_exchange_arbitrage_bot/src/services/market_data_service.py

import asyncio

import httpx
from typing import Dict, Set, Any, Optional

from src.constants.api_constants import COINCAP_API_BASE_URL, NEWS_HTTP_TIMEOUT, COINGECKO_API_BASE_URL, COINCAP_ASSETS_FETCH_LIMIT # <-- ИМПОРТИРУЙТЕ НОВУЮ КОНСТАНТУ
from src.services.market_intelligence_service import MarketIntelligenceService
from src.utils.logger import logger


class MarketDataService:
    """
    Сервис отвечает ИСКЛЮЧИТЕЛЬНО за получение рыночных данных (цены, объемы, капитализация)
    из различных источников, таких как CoinCap, CoinGecko и др.
    """

    def __init__(self, http_session: httpx.AsyncClient, market_intel_service: MarketIntelligenceService):
        self.session = http_session
        self._market_intel_service = market_intel_service
        self._coincap_id_cache: Optional[Dict[str, str]] = None
        self._cache_lock = asyncio.Lock()

    def _safe_float_conversion(self, value, field_name: str = "unknown") -> float:
        """
        Безопасно конвертирует значение в float с обработкой ошибок.

        Args:
            value: Значение для конвертации
            field_name: Имя поля для логирования ошибок

        Returns:
            float: Сконвертированное значение или 0.0 в случае ошибки
        """
        if value is None:
            return 0.0

        try:
            converted = float(value)
            # Проверяем на NaN и бесконечность
            if not (converted == converted) or converted == float('inf') or converted == float('-inf'):
                logger.warning(f"Получено некорректное значение для поля {field_name}: {value}")
                return 0.0
            return converted
        except (ValueError, TypeError) as e:
            logger.warning(f"Ошибка конвертации поля {field_name} со значением '{value}': {e}")
            return 0.0

    async def get_assets_market_data(self, coin_symbols: Set[str]) -> Dict[str, Dict[str, Any]]:
        """
        Основной метод получения рыночных данных.
        Приоритет отдается CoinGecko, CoinCap используется как fallback.
        """
        if not coin_symbols:
            return {}

        # 1. Основная попытка через CoinGecko (надежный источник)
        coingecko_data = await self._fetch_coingecko_market_data(coin_symbols)
        if coingecko_data:
            logger.info(f"MarketData: Успешно получены данные для {len(coingecko_data)} активов через CoinGecko.")
            return coingecko_data

        # 2. Fallback-попытка через CoinCap, если CoinGecko не вернул данные
        logger.warning("Не удалось получить данные через CoinGecko, переключаюсь на CoinCap (fallback)...")
        coincap_data = await self._fetch_coincap_data(coin_symbols)
        if coincap_data:
            logger.info(f"MarketData: Успешно получены данные для {len(coincap_data)} активов через CoinCap.")

        return coincap_data

    async def _fetch_coingecko_market_data(self, symbols: Set[str]) -> Dict[str, Dict[str, Any]]:
        """Получает рыночные данные через CoinGecko API, используя существующую логику получения ID."""
        if not symbols or not self._market_intel_service:
            return {}

        coin_ids, symbol_to_id_map = [], {}
        for symbol in symbols:
            coin_id = await self._market_intel_service.get_coin_id_by_symbol(symbol)
            if coin_id:
                coin_ids.append(coin_id)
                symbol_to_id_map[coin_id] = symbol.upper()

        if not coin_ids: return {}

        try:
            url = f"{COINGECKO_API_BASE_URL}/simple/price"
            params = {
                'ids': ','.join(coin_ids).lower(),
                'vs_currencies': 'usd',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true',
                'include_24hr_change': 'true',
                **self._market_intel_service.get_coingecko_auth_params()
            }
            response = await self.session.get(url, params=params, timeout=NEWS_HTTP_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            market_data = {}
            for coin_id, price_data in data.items():
                symbol = symbol_to_id_map.get(coin_id)
                if symbol:
                    market_data[symbol] = {
                        'price_usd': self._safe_float_conversion(price_data.get('usd'), 'price_usd'),
                        'change_24h': self._safe_float_conversion(price_data.get('usd_24h_change'), 'change_24h'),
                        'market_cap_usd': self._safe_float_conversion(price_data.get('usd_market_cap'),
                                                                      'market_cap_usd'),
                        'volume_24h': self._safe_float_conversion(price_data.get('usd_24h_vol'), 'volume_24h')
                    }
            return market_data
        except Exception as e:
            logger.error(f"Ошибка получения market data через CoinGecko: {e}")
            return {}

    async def _ensure_coincap_id_cache(self):
        """
        АРГУМЕНТАЦИЯ: Этот метод гарантирует, что маппинг 'тикер -> id' для CoinCap
        загружен. Он делает это только один раз. Это полностью динамический подход,
        который избегает как хардкода, так и неэффективной загрузки всех данных при каждом запросе.
        """
        if self._coincap_id_cache is not None:
            return

        async with self._cache_lock:
            if self._coincap_id_cache is not None:
                return

            logger.info("Кэш ID для CoinCap пуст, создаю его динамически...")
            temp_cache = {}
            try:
                url = f"{COINCAP_API_BASE_URL}/assets"
                response = await self.session.get(url, params={'limit': COINCAP_ASSETS_FETCH_LIMIT}, timeout=NEWS_HTTP_TIMEOUT) # <-- ИСПОЛЬЗУЕМ КОНСТАНТУ
                response.raise_for_status()
                assets = response.json().get('data', [])

                for asset in assets:
                    symbol = asset.get('symbol')
                    asset_id = asset.get('id')
                    if symbol and asset_id:
                        temp_cache[symbol.upper()] = asset_id

                self._coincap_id_cache = temp_cache
                logger.info(
                    f"Кэш ID для CoinCap успешно создан. Загружено {len(self._coincap_id_cache)} сопоставлений.")
            except Exception as e:
                logger.error(f"Не удалось создать кэш ID для CoinCap: {e}")
                self._coincap_id_cache = {}

    async def _fetch_coincap_data(self, symbols: Set[str]) -> Dict[str, Dict[str, Any]]:
        if not symbols:
            return {}

        await self._ensure_coincap_id_cache()
        if not self._coincap_id_cache:
            return {}

        search_ids = [self._coincap_id_cache.get(s.upper()) for s in symbols]
        search_ids_str = ','.join([sid for sid in search_ids if sid])

        if not search_ids_str:
            logger.warning(f"CoinCap: не удалось найти ID для запрошенных символов в кэше: {symbols}")
            return {}

        url = f"{COINCAP_API_BASE_URL}/assets"
        try:
            response = await self.session.get(
                url,
                params={'ids': search_ids_str},
                timeout=NEWS_HTTP_TIMEOUT
            )
            response.raise_for_status()

            assets = response.json().get('data', [])
            market_data = {}

            for asset in assets:
                symbol = asset.get('symbol')
                if symbol:
                    market_data[symbol.upper()] = {
                        'price_usd': self._safe_float_conversion(asset.get('priceUsd'), 'price_usd'),
                        'change_24h': self._safe_float_conversion(asset.get('changePercent24Hr'), 'change_24h'),
                        'market_cap_usd': self._safe_float_conversion(asset.get('marketCapUsd'), 'market_cap_usd'),
                        'volume_24h': self._safe_float_conversion(asset.get('volumeUsd24Hr'), 'volume_24h')
                    }
            return market_data
        except Exception as e:
            logger.error(f"Ошибка при получении данных от CoinCap: {e}")
            return {}