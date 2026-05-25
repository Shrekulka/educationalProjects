# inter_exchange_arbitrage_bot/src/services/density_screener_service.py

import asyncio
import time
from collections import defaultdict
from typing import List, Dict, Optional, Tuple

import ccxt.async_support as ccxt
import httpx

from src.constants.api_constants import ENRICHER_HTTP_TIMEOUT
from src.constants.trading_constants import DENSITY_SCREENER_CONFIG
from src.models.screener_models import Density
from src.services import service_manager
from src.services.exchange_service import ExchangeService
from src.utils.logger import logger


class DensityScreenerService:
    """
    Сервис для сканирования плотностей с учетом rate limit,
    кэширования, батчинга и фильтрации.
    """

    def __init__(self, services: Dict[str, ExchangeService]):
        self.services = services
        self.config = DENSITY_SCREENER_CONFIG
        # Семафор для контроля одновременных запросов к API
        self.semaphore = asyncio.Semaphore(self.config['MAX_CONCURRENT_REQUESTS'])
        self._cache: Optional[Dict[str, Dict]] = None
        self._cache_timestamp: float = 0.0
        self._cached_symbols: Optional[List[str]] = None
        """Инициализирует HTTP-клиент для внешних API."""
        self.http_client = httpx.AsyncClient(timeout=ENRICHER_HTTP_TIMEOUT)

    async def scan_for_densities(self, symbols_to_scan: List[str]) -> Dict[str, Dict]:
        """
        Возвращает словарь с плотностями и средней ценой для каждого символа.
        """
        now = time.time()
        # 1. Проверка кэша
        if (self._cache is not None and
                (now - self._cache_timestamp < self.config['CACHE_TTL_SECONDS']) and
                self._cached_symbols == symbols_to_scan):
            logger.info(
                f"📋 Используем кэшированные результаты скринера (еще {self.config['CACHE_TTL_SECONDS'] - (now - self._cache_timestamp):.0f} сек)")
            return self._cache

        logger.info(f"🚀 Запуск скринера плотностей для {len(symbols_to_scan)} активов...")

        # 2. Безопасное получение стаканов с контролем нагрузки
        order_books = await self._fetch_all_order_books_safely(symbols_to_scan)

        if not order_books:
            logger.warning("Не удалось получить стаканы ордеров для анализа плотностей.")
            return {}

        results = {}
        for symbol, exchanges_data in order_books.items():
            symbol_densities = []
            all_mid_prices = []
            for exchange_id, book in exchanges_data.items():
                densities, mid_price = self._analyze_single_order_book(symbol, exchange_id, book)
                if densities:
                    symbol_densities.extend(densities)
                if mid_price:
                    all_mid_prices.append(mid_price)

            if symbol_densities:
                symbol_densities.sort(key=lambda d: d.volume_usd, reverse=True)
                results[symbol] = {
                    'densities': symbol_densities,
                    'mid_price': sum(all_mid_prices) / len(all_mid_prices) if all_mid_prices else 0
                }
            # ✅ ИЗМЕНЕНИЕ: Логируем, если для монеты не найдено плотностей, соответствующих критериям.
            else:
                logger.warning(f"[{symbol}] Не найдено плотностей, соответствующих критериям. Актив не будет включен в отчет.")

        # Сохраняем в кэш и данные, и список символов
        self._cache = results
        self._cached_symbols = symbols_to_scan
        self._cache_timestamp = now

        logger.info(f"✅ Скринер завершил работу. Найдено плотностей для {len(results)} активов.")
        return results

    async def _fetch_single_book_with_semaphore(self, symbol: str, exchange_id: str, service: ExchangeService) -> \
            Optional[Dict]:
        """Оборачивает один API-вызов в семафор и задержку для соблюдения rate limit."""
        async with self.semaphore:
            try:
                await asyncio.sleep(self.config['REQUEST_DELAY_MS'] / 1000.0)
                return await service.client.fetch_order_book(symbol, limit=self.config['ORDER_BOOK_DEPTH'])
            except ccxt.RateLimitExceeded:
                logger.warning(f"Превышен Rate Limit для {exchange_id} при запросе {symbol}. Пропускаем.")
            except Exception as e:
                logger.debug(f"Ошибка загрузки стакана {symbol} на {exchange_id}: {type(e).__name__}")
            return None

    async def _fetch_all_order_books_safely(self, symbols: List[str]) -> Dict[str, Dict[str, Dict]]:
        """Проверяет наличие символа на бирже ПЕРЕД запросом."""
        tasks = []
        metadata = []

        for symbol in symbols:
            for exchange_id, service in self.services.items():
                markets_cache = service_manager.markets_cache.get(exchange_id, ({}, 0))[0]
                if symbol in markets_cache:
                    task = self._fetch_single_book_with_semaphore(symbol, exchange_id, service)
                    tasks.append(task)
                    metadata.append({'symbol': symbol, 'exchange': exchange_id})
                else:
                    logger.debug(f"Пропуск {symbol} на {exchange_id}: пара не торгуется.")

        if not tasks: return {}

        results = await asyncio.gather(*tasks)

        order_books = defaultdict(dict)
        for i, res in enumerate(results):
            if res:
                meta = metadata[i]
                order_books[meta['symbol']][meta['exchange']] = res

        return order_books

    def _analyze_single_order_book(self, symbol: str, exchange_id: str, book: Dict) -> Tuple[
        List[Density], Optional[float]]:
        """
        ✅ УЛУЧШЕННАЯ ВЕРСИЯ: Анализирует стакан с адаптивным поиском, который продолжается
        до тех пор, пока не будут найдены И поддержка, И сопротивление,
        сохраняя при этом самые первые (наиболее строгие) найденные результаты.
        """
        bids, asks = book.get('bids', []), book.get('asks', [])
        if not bids or not asks or not bids[0] or not asks[0]:
            return [], None

        mid_price = (bids[0][0] + asks[0][0]) / 2
        if mid_price == 0:
            return [], None

        def _perform_analysis(current_price_range: float, current_min_usd: float) -> Tuple[
            List[Density], List[Density]]:
            """Внутренняя функция, возвращающая поддержки и сопротивления раздельно."""
            supports, resistances = [], []
            # Анализ поддержек (bids)
            for price, amount in bids:
                order_value_usd = price * amount
                distance = abs(price - mid_price) / mid_price * 100
                if order_value_usd >= current_min_usd and distance <= current_price_range:
                    supports.append(
                        Density(symbol, exchange_id, price, order_value_usd, self.config['DENSITY_TYPE_BID'], distance))
            # Анализ сопротивлений (asks)
            for price, amount in asks:
                order_value_usd = price * amount
                distance = abs(price - mid_price) / mid_price * 100
                if order_value_usd >= current_min_usd and distance <= current_price_range:
                    resistances.append(
                        Density(symbol, exchange_id, price, order_value_usd, self.config['DENSITY_TYPE_ASK'], distance))
            return supports, resistances

        # --- Логика адаптивного поиска ---
        final_supports: List[Density] = []
        final_resistances: List[Density] = []

        # Получаем базовые настройки
        initial_price_range = self.config['PRICE_RANGE_PERCENT']
        initial_min_usd = self.config['MIN_USD_VALUE']
        adaptive_enabled = self.config.get('ADAPTIVE_SEARCH_ENABLED', False)

        # Определяем общее количество попыток (1 стандартная + N адаптивных)
        max_attempts = self.config.get('ADAPTIVE_SEARCH_ATTEMPTS', 3) if adaptive_enabled else 0

        # Единый цикл для всех попыток. Попытка 0 - это стандартный поиск.
        for attempt in range(max_attempts + 1):
            if attempt == 0:
                # Первая попытка со стандартными, самыми строгими параметрами
                current_range = initial_price_range
                current_usd = initial_min_usd
                logger.debug(
                    f"[{symbol} на {exchange_id}] Стандартный поиск: Диапазон={current_range}%, Объем=${current_usd:,.0f}")
            else:
                # Последующие попытки с ослабленными параметрами
                range_step = self.config.get('ADAPTIVE_PRICE_RANGE_STEP_PERCENT', 2.0)
                usd_decrease_ratio = self.config.get('ADAPTIVE_MIN_USD_DECREASE_RATIO', 0.8)
                current_range = initial_price_range + (range_step * attempt)
                current_usd = initial_min_usd * (usd_decrease_ratio ** attempt)
                logger.debug(
                    f"[{symbol} на {exchange_id}] Адаптивная попытка #{attempt}: Диапазон={current_range:.1f}%, Объем=${current_usd:,.0f}")

            # Выполняем анализ с текущими параметрами
            current_supports, current_resistances = _perform_analysis(current_range, current_usd)

            # "Замораживаем" результаты, как только они найдены.
            # Если `final_supports` еще пуст, мы записываем в него то, что нашли на этой итерации.
            # На следующих итерациях это условие уже не выполнится, и первые результаты не будут перезаписаны.
            if not final_supports and current_supports:
                final_supports = current_supports
                logger.info(f"  ✅ [{symbol}] Уровни ПОДДЕРЖКИ найдены на попытке #{attempt}.")

            if not final_resistances and current_resistances:
                final_resistances = current_resistances
                logger.info(f"  ✅ [{symbol}] Уровни СОПРОТИВЛЕНИЯ найдены на попытке #{attempt}.")

            # Проверяем условие выхода: если найдены ОБА типа уровней, прекращаем поиск.
            if final_supports and final_resistances:
                logger.info(f"  🎯 [{symbol}] Найдены оба типа уровней. Поиск завершен.")
                break

        # Если цикл завершился, а мы так и не нашли оба типа уровней (или адаптивный поиск был выключен)
        if not (final_supports and final_resistances):
            logger.warning(f"[{symbol} на {exchange_id}] Поиск завершен, но найден только один тип уровней или ничего.")

        # Возвращаем комбинацию из лучших найденных поддержек и сопротивлений
        return final_supports + final_resistances, mid_price

    # def _analyze_single_order_book(self, symbol: str, exchange_id: str, book: Dict) -> Tuple[List[Density], Optional[float]]:
    #     """
    #     ✅ ИЗМЕНЕНО: Анализирует стакан с поддержкой адаптивного поиска, если
    #     стандартный поиск не дал результатов.
    #     """
    #     bids, asks = book.get('bids', []), book.get('asks', [])
    #     if not bids or not asks or not bids[0] or not asks[0]:
    #         return [], None
    #
    #     mid_price = (bids[0][0] + asks[0][0]) / 2
    #     if mid_price == 0:
    #         return [], None
    #
    #     def _perform_analysis(current_price_range: float, current_min_usd: float) -> List[Density]:
    #         """Внутренняя функция для выполнения одного цикла анализа."""
    #         densities = []
    #         # Анализ поддержек (bids)
    #         for price, amount in bids:
    #             order_value_usd = price * amount
    #             distance = abs(price - mid_price) / mid_price * 100
    #             if order_value_usd >= current_min_usd and distance <= current_price_range:
    #                 densities.append(
    #                     Density(symbol, exchange_id, price, order_value_usd, self.config['DENSITY_TYPE_BID'],
    #                             distance))
    #         # Анализ сопротивлений (asks)
    #         for price, amount in asks:
    #             order_value_usd = price * amount
    #             distance = abs(price - mid_price) / mid_price * 100
    #             if order_value_usd >= current_min_usd and distance <= current_price_range:
    #                 densities.append(
    #                     Density(symbol, exchange_id, price, order_value_usd, self.config['DENSITY_TYPE_ASK'],
    #                             distance))
    #         return densities
    #
    #     # --- Шаг 1: Стандартный поиск ---
    #     initial_price_range = self.config['PRICE_RANGE_PERCENT']
    #     initial_min_usd = self.config['MIN_USD_VALUE']
    #     found_densities = _perform_analysis(initial_price_range, initial_min_usd)
    #
    #     # --- Шаг 2: Адаптивный поиск (если стандартный не дал результатов) ---
    #     if not found_densities and self.config.get('ADAPTIVE_SEARCH_ENABLED', False):
    #         logger.info(
    #             f"[{symbol} на {exchange_id}] Стандартный поиск не дал результатов. Запуск адаптивного сканирования...")
    #
    #         # Получаем настройки для цикла
    #         attempts = self.config.get('ADAPTIVE_SEARCH_ATTEMPTS', 3)
    #         range_step = self.config.get('ADAPTIVE_PRICE_RANGE_STEP_PERCENT', 2.0)
    #         usd_decrease_ratio = self.config.get('ADAPTIVE_MIN_USD_DECREASE_RATIO', 0.8)
    #
    #         # Инициализируем переменные для цикла
    #         current_range = initial_price_range
    #         current_usd = initial_min_usd
    #
    #         for attempt in range(1, attempts + 1):
    #             # Ослабляем критерии
    #             current_range += range_step
    #             current_usd *= usd_decrease_ratio
    #
    #             logger.debug(f"  Попытка #{attempt}: Диапазон={current_range:.1f}%, Мин. объем=${current_usd:,.0f}")
    #
    #             # Повторяем анализ с новыми параметрами
    #             found_densities = _perform_analysis(current_range, current_usd)
    #
    #             if found_densities:
    #                 logger.info(f"  ✅ Плотности найдены на попытке #{attempt} с расширенными параметрами.")
    #                 break  # Выходим из цикла, если что-то нашли
    #         else:
    #             logger.warning(f"[{symbol} на {exchange_id}] Адаптивный поиск завершен, плотностей не найдено.")
    #
    #     return found_densities, mid_price
