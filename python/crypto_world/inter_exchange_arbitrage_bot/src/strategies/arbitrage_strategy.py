# inter_exchange_arbitrage_bot/src/strategies/arbitrage_strategy.py

import asyncio
import copy
import datetime
import html
from collections import defaultdict
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import List, Any, Tuple, Optional, Dict, Callable, Coroutine

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

import src.core.state as app_state
from src.bot.keyboards.scanner_keyboard import get_scanner_menu_keyboard
from src.bot.logic.settings_logic import get_user_settings
from src.constants.api_constants import (HEARTBEAT_INTERVAL_MINUTES)
from src.constants.system_constants import (SCANNER_STATUS_STOPPED, SCANNER_STATUS_RUNNING,
                                            SYSTEM_STATE_HEARTBEAT_MESSAGE_ID)
from src.constants.telegram_constants import RECON_PROGRESS_UPDATES_COUNT
from src.constants.trading_constants import (
    MIN_EXCHANGES_FOR_ARBITRAGE, BALANCE_FETCH_TIMEOUT_SECONDS, TRADE_AMOUNT_SAFETY_MARGIN, ORDER_BOOK_ASKS,
    BALANCE_CHANGE_TOLERANCE_FACTOR, DEFAULT_EXCHANGE_FEES, POST_TRADE_BALANCE_VALIDATION_DELAY_S, ORDER_BOOK_BIDS,
    BALANCE_VALIDATION_FILL_RATIO_THRESHOLD, ORDER_BOOK_ANALYSIS_PRECISION_USD, MINIMUM_MEANINGFUL_PROFIT_USD,
    USD_REPORT_PRECISION, ORDERBOOK_EMPTY_SLIPPAGE_PERCENT, FLOAT_COMPARISON_EPSILON, MIN_SELL_TO_BUY_FILL_RATIO,
    MARKET_FIELD_PRECISION,
    MARKET_PRECISION_AMOUNT, DEFAULT_PRECISION_AMOUNT, INVALID_SPREAD_VALUE,
    FEES_TAKER, BALANCE_ISSUE_KEY_TYPE, BALANCE_ISSUE_TYPE_INSUFFICIENT_USDT, BALANCE_ISSUE_KEY_CURRENCY,
    BALANCE_ISSUE_KEY_NEEDED, PRIMARY_QUOTE_CURRENCY, BALANCE_ISSUE_KEY_AVAILABLE, BALANCE_ISSUE_KEY_SHORTAGE,
    FAILURE_REASON_INSUFFICIENT_BALANCE, DEFAULT_NUMERIC_VALUE, STABLECOIN_PRICE, BALANCE_ISSUE_TYPE_INSUFFICIENT_COIN,
    PERCENTAGE_MULTIPLIER, FAILURE_REASON_UNPROFITABLE_TRADE, FAILURE_REASON_EXECUTION_FAILED, OPERATION_TYPE_BUY,
    OPERATION_TYPE_SELL, FLOAT_PRECISION_TOLERANCE, ERROR_MESSAGE_TRUNCATE_LENGTH, FAILURE_REASON_CRITICAL_ERROR,
    LIMIT_SAFETY_MULTIPLIER, DEFAULT_TRADE_AMOUNT_USD, MARKET_FIELD_LIMITS_AMOUNT_MIN, CCXT_ORDER_FIELD_FILLED,
    CCXT_ORDER_FIELD_COST, CCXT_ORDER_FIELD_AVERAGE, EXCHANGE_BYBIT, CCXT_ORDER_FIELD_INFO,
    BYBIT_ORDER_INFO_FIELD_CUM_EXEC_QTY, BYBIT_ORDER_INFO_FIELD_CUM_EXEC_VALUE, ORDER_FILL_SUCCESS_THRESHOLD,
    FEE_METHOD_UNKNOWN, FEE_METHOD_DEFAULT_EXCHANGE, FEE_METHOD_DEFAULT_FALLBACK, FEE_METHOD_MARKET_DIRECT,
    PRIORITY_SYMBOLS_FOR_FEES, FEE_METHOD_MARKET_GENERAL, MARKET_MAKER_KEY, MARKET_TAKER_KEY, MARKET_FEES_KEY,
    MARKET_FEES_TRADING_KEY, FEE_METHOD_MARKET_FEES, FEE_METHOD_API_FETCH, MIN_VALID_FEE, MAX_VALID_FEE,
    DEFAULT_FALLBACK_SYMBOL, ORDER_BOOK_DEPTH, STABLE_COINS, FALLBACK_MIN_TRADE_AMOUNT_USD,
    OPPORTUNITY_CLASSIFICATION_TIERS, MINIMUM_MEANINGFUL_ABSOLUTE_PROFIT, MINIMUM_PRACTICAL_TRADE_VOLUME,
)
from src.core.config import config
from src.core.database import async_session_factory
from src.lexicon import LEXICON_RU
from src.models.arbitrage_attempt import ArbitrageStatus
from src.models.system_models import SystemState
from src.models.user_models import UserCoin
from src.services import scanner_api_service, service_manager
from src.services.arbitrage_report_service import ArbitrageReportService
from src.services.blacklist_manager import blacklist_manager

from src.services.dynamic_pairs_manager import dynamic_pairs_manager
from src.services.exchange_service import ExchangeService
from src.services.notifier_service import NotifierService
from src.services.scanner_state_service import get_scanner_state_from_db
from src.strategies.enums import OpportunityType, RSIStatus, MACDSignal, BollingerBandStatus, RiskLevel
from src.utils import safe_get_numeric, format_precision_amount
from src.utils.logger import logger


# Вложенные датаклассы для структурирования аналитических данных

@dataclass
class MarketData:
    """Структура для хранения фундаментальных рыночных данных."""
    price: float = 0.0
    price_24h_change: float = 0.0
    volume_24h_usd: float = 0.0
    market_cap_usd: float = 0.0
    listings_count: int = 0


@dataclass
class TechnicalAnalysis:
    """Структура для хранения всех технических индикаторов."""
    rsi_14: float = 0.0
    rsi_status: RSIStatus = RSIStatus.HEALTHY
    macd_signal: MACDSignal = MACDSignal.NEUTRAL
    bollinger_band_status: BollingerBandStatus = BollingerBandStatus.INSIDE_BANDS
    price_trend_sparkline: str = ""
    volume_spike_ratio: float = 1.0


@dataclass
class ArbitrageOpportunity:
    """
    Финальная, расширенная структура для хранения полной информации об арбитражной возможности.
    Использует вложенные датаклассы для лучшей организации данных.
    """
    # --- Базовые идентификаторы ---
    symbol: str
    coin: str
    buy_exchange_id: str
    sell_exchange_id: str

    # --- Ключевые метрики связки ---
    roi_percent: float = 0.0
    potential_profit_usd: float = 0.0
    max_volume_usd: float = 0.0
    min_trade_amount_usd: float = 0.0
    breakeven_threshold_percent: float = 0.0
    effective_buy_price: float = 0.0
    effective_sell_price: float = 0.0

    # --- Детальный анализ для торговли (если применимо) ---
    buy_analysis: Optional['OrderBookAnalysis'] = field(default=None, repr=False)
    sell_analysis: Optional['OrderBookAnalysis'] = field(default=None, repr=False)

    # --- СТРУКТУРИРОВАННЫЕ АНАЛИТИЧЕСКИЕ ПОЛЯ ---
    market_data: MarketData = field(default_factory=MarketData)
    technical_analysis: TechnicalAnalysis = field(default_factory=TechnicalAnalysis)
    liquidity_usd: float = 0.0
    execution_time_seconds: float = 0.0
    potential_reason: Optional[str] = None
    action_recommendation: Optional[str] = None


    # --- Метаданные и классификация ---
    ai_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.UNDEFINED
    opportunity_type: OpportunityType = OpportunityType.LOW_PROFIT
    is_phantom: bool = False
    phantom_reason: Optional[str] = None
    drivers: List[str] = field(default_factory=list)
    cmc_slug: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    is_trending: bool = False
    pattern: Optional[str] = None


@dataclass
class OrderBookAnalysis:
    """Хранит результат детального анализа стакана ордеров."""
    effective_price: float
    filled_amount: float
    total_cost: float
    slippage_percent: float
    available_liquidity_usd: float
    available_liquidity_coin: float


class ArbitrageStrategy:
    """
    Основной класс стратегии, теперь работающий с новой, расширенной моделью ArbitrageOpportunity.
    """

    def __init__(self, user_id: int, validated_services: Dict[str, ExchangeService],
                 profit_threshold: float,
                 initial_balances: Dict[str, Dict[str, float]],
                 buy_capable_exchanges: List[str],
                 notifier: NotifierService, report_service: ArbitrageReportService,
                 tracked_coins_to_scan: List[str],
                 trade_amount: Optional[float] = None,
                 progress_callback: Optional[Callable[..., Coroutine[Any, Any, None]]] = None):

        if len(validated_services) < MIN_EXCHANGES_FOR_ARBITRAGE:
            raise ValueError(f"Для арбитража требуется как минимум {MIN_EXCHANGES_FOR_ARBITRAGE} сервиса.")

        if not isinstance(tracked_coins_to_scan, list) or not all(isinstance(c, str) for c in tracked_coins_to_scan):
            raise TypeError(f"tracked_coins_to_scan должен быть списком строк, получен {type(tracked_coins_to_scan)}")
        if progress_callback and not callable(progress_callback):
            raise TypeError("progress_callback должен быть вызываемым объектом")

        self.user_id = user_id
        self.services = validated_services
        self.buy_capable_exchanges = set(buy_capable_exchanges)
        self.trade_amount = trade_amount or DEFAULT_TRADE_AMOUNT_USD
        self.profit_threshold = profit_threshold
        self.initial_balances = initial_balances
        self.notifier = notifier
        self.report_service = report_service
        self.trading_fees_cache: Dict[str, Dict[str, float]] = {}
        self.tracked_coins_to_scan = tracked_coins_to_scan
        self.progress_callback = progress_callback

        logger.info(LEXICON_RU['log_strategy_init'].format(
            user_id=self.user_id, trade_amount=self.trade_amount,
            profit_threshold=self.profit_threshold, services=', '.join(self.services.keys())
        ))
        logger.critical(f"+++++ СОЗДАНА СТРАТЕГИЯ ID: {id(self)}")

    def __del__(self):
        logger.critical(f"----- УНИЧТОЖЕНА СТРАТЕГИЯ ID: {id(self)}")

    def _get_opportunity_thresholds(self, symbol: str, price: float) -> Tuple[dict, str]:
        """
        Определяет, какой набор порогов использовать в зависимости от типа и цены актива.
        Возвращает кортеж (словарь_порогов, название_тира).
        """
        base_symbol = symbol.split('/')[0]
        if base_symbol in STABLE_COINS or PRIMARY_QUOTE_CURRENCY in base_symbol:
            return OPPORTUNITY_CLASSIFICATION_TIERS['stable_coins'], 'stable_coins'

        # Проходим по тирам от меньшего к большему
        if price <= OPPORTUNITY_CLASSIFICATION_TIERS['micro_cap']['price_upper_bound']:
            return OPPORTUNITY_CLASSIFICATION_TIERS['micro_cap'], 'micro_cap'
        if price <= OPPORTUNITY_CLASSIFICATION_TIERS['meme_coins']['price_upper_bound']:
            return OPPORTUNITY_CLASSIFICATION_TIERS['meme_coins'], 'meme_coins'
        if price <= OPPORTUNITY_CLASSIFICATION_TIERS['mid_cap']['price_upper_bound']:
            return OPPORTUNITY_CLASSIFICATION_TIERS['mid_cap'], 'mid_cap'

        return OPPORTUNITY_CLASSIFICATION_TIERS['large_cap'], 'large_cap'

    def _get_asset_price_for_classification(self, symbol: str, exchanges_data: Dict) -> float:
        """Получает репрезентативную (медианную) цену актива для классификации."""
        prices = []
        for exchange_id, order_book in exchanges_data.items():
            asks = order_book.get('asks')
            bids = order_book.get('bids')
            if asks and bids and asks[0] and bids[0]:
                buy_price = asks[0][0]
                sell_price = bids[0][0]
                if buy_price > 0 and sell_price > 0:
                    prices.append((buy_price + sell_price) / 2)

        if prices:
            prices.sort()
            return prices[len(prices) // 2]

        # Возвращаем цену стейблкоина как безопасное fallback-значение.
        # Это гарантирует, что актив без цены будет классифицирован
        # в тир по умолчанию ('mid_cap' или 'large_cap'), а не в 'micro_cap'.
        logger.warning(f"Не удалось получить цену для {symbol}, используется fallback-цена: {STABLECOIN_PRICE}")
        return STABLECOIN_PRICE

    def _classify_opportunity(
            self,
            opportunity: ArbitrageOpportunity,
            min_trade_amount_from_exchanges: float,
            asset_price: float
    ) -> None:
        """
        Классифицирует возможность с учетом АБСОЛЮТНОЙ прибыли
        и экономической целесообразности, а не только относительного ROI.
        """
        if not isinstance(min_trade_amount_from_exchanges, (int, float)) or min_trade_amount_from_exchanges <= 0:
            logger.warning(f"Некорректный min_trade_amount: {min_trade_amount_from_exchanges}. Использую fallback.")
            min_trade_amount_from_exchanges = FALLBACK_MIN_TRADE_AMOUNT_USD

        if not isinstance(asset_price, (int, float)) or asset_price <= 0:
            logger.warning(f"Некорректная цена {asset_price} для {opportunity.symbol}. Использую fallback.")
            asset_price = 1.0

        thresholds, tier_name = self._get_opportunity_thresholds(opportunity.symbol, asset_price)

        logger.debug(
            f"Классификация {opportunity.symbol}: "
            f"Цена=${asset_price:,.6f}, Тир='{tier_name}', "
            f"Применяемые пороги: CRITICAL_ROI={thresholds['CRITICAL_ROI_THRESHOLD']}%, "
            f"SUSPICIOUS_ROI={thresholds['SUSPICIOUS_ROI_THRESHOLD']}%, "
            f"LOW_LIQUIDITY_VOL=${thresholds['LOW_LIQUIDITY_VOLUME_USD']}"
        )

        roi_percent = opportunity.roi_percent
        max_volume = opportunity.max_volume_usd
        potential_profit = opportunity.potential_profit_usd

        # ДОБАВЛЯЕМ ПРОВЕРКИ НА ЭКОНОМИЧЕСКУЮ ЦЕЛЕСООБРАЗНОСТЬ

        # 1. Проверка лимитов биржи
        if max_volume < min_trade_amount_from_exchanges:
            opportunity.is_phantom = True
            opportunity.opportunity_type = OpportunityType.PHANTOM_LIMITS
            opportunity.phantom_reason = html.escape(
                f"Объем ${max_volume:.2f} < мин. лимита ${min_trade_amount_from_exchanges:.2f}")
            return

        # 2. Проверка на аномально высокий ROI
        if roi_percent > thresholds['CRITICAL_ROI_THRESHOLD']:
            opportunity.is_phantom = True
            opportunity.opportunity_type = OpportunityType.PHANTOM_ROI
            opportunity.phantom_reason = html.escape(
                f"ROI {roi_percent:.0f}% > крит. порога {thresholds['CRITICAL_ROI_THRESHOLD']:.0f}%")
            return

        # 3. ПРОВЕРКА: Минимальная абсолютная прибыль для экономической целесообразности
        # Если абсолютная прибыль меньше $1, это экономически бессмысленно
        if potential_profit < MINIMUM_MEANINGFUL_ABSOLUTE_PROFIT:
            opportunity.is_phantom = True
            opportunity.opportunity_type = OpportunityType.PHANTOM_LIQUIDITY
            opportunity.phantom_reason = html.escape(
                f"Прибыль ${potential_profit:.2f} < мин. значимой прибыли ${MINIMUM_MEANINGFUL_ABSOLUTE_PROFIT}")
            return

        # 4. Проверка на подозрительную связку низкой ликвидности
        # Делаем пороги более разумными для выявления реальных проблем
        if (roi_percent > thresholds['SUSPICIOUS_ROI_THRESHOLD'] and
                opportunity.max_volume_usd < thresholds['LOW_LIQUIDITY_VOLUME_USD']):
            opportunity.is_phantom = True
            opportunity.opportunity_type = OpportunityType.PHANTOM_LIQUIDITY
            opportunity.phantom_reason = html.escape(
                f"ROI {roi_percent:.2f}% подозрительно высок при малом объеме ${max_volume:.2f}")
            return

        # 5. ПРОВЕРКА: Слишком малый объем для практической торговли
        # Если объем меньше разумного минимума (например, $50), помечаем как неликвидный
        if max_volume < MINIMUM_PRACTICAL_TRADE_VOLUME:
            opportunity.is_phantom = True
            opportunity.opportunity_type = OpportunityType.PHANTOM_LIQUIDITY
            opportunity.phantom_reason = html.escape(
                f"Объем ${max_volume:.2f} слишком мал для практической торговли")
            return

        # === КЛАССИФИКАЦИЯ РЕАЛЬНЫХ ВОЗМОЖНОСТЕЙ ===
        # Только возможности, прошедшие ВСЕ проверки выше, попадают сюда

        if opportunity.roi_percent / 100.0 >= self.profit_threshold:
            opportunity.opportunity_type = OpportunityType.HIGH_PROFIT
        else:
            opportunity.opportunity_type = OpportunityType.LOW_PROFIT

        logger.debug(
            f"Классификация {opportunity.symbol}: "
            f"Цена=${asset_price:,.6f}, Тир='{tier_name}', "
            f"ROI={opportunity.roi_percent:.2f}%, "
            f"Объем=${opportunity.max_volume_usd:,.2f}, "
            f"Прибыль=${opportunity.potential_profit_usd:.2f} "
            f"-> Итог: {opportunity.opportunity_type.value}"
        )

    async def _get_trading_fees(self, exchange_id: str, symbol: str = None) -> Dict[str, float]:
        if exchange_id in self.trading_fees_cache:
            return self.trading_fees_cache[exchange_id]

        service = self.services[exchange_id]
        default_fees = DEFAULT_EXCHANGE_FEES.get(exchange_id, DEFAULT_EXCHANGE_FEES['default'])

        extracted_fees, method_used = {}, FEE_METHOD_UNKNOWN

        try:
            if symbol:
                extracted_fees, method_used = await self._try_extract_fees_from_specific_market(service, exchange_id,
                                                                                                symbol)

            if not extracted_fees:
                extracted_fees, method_used = await self._try_extract_fees_from_general_markets(service, exchange_id)

            if not extracted_fees:
                extracted_fees, method_used = await self._try_extract_fees_from_api(service, exchange_id)

            if not extracted_fees:
                extracted_fees = default_fees.copy()
                method_used = FEE_METHOD_DEFAULT_EXCHANGE if exchange_id in DEFAULT_EXCHANGE_FEES else FEE_METHOD_DEFAULT_FALLBACK

            validated_fees = self._validate_and_cache_fees(exchange_id, extracted_fees, default_fees)
            self._log_fee_extraction_result(exchange_id, validated_fees, method_used)
            return validated_fees

        except Exception as e:
            logger.error(LEXICON_RU['fee_log_error'].format(exchange=exchange_id, error=e))
            self.trading_fees_cache[exchange_id] = default_fees
            logger.info(LEXICON_RU['fee_log_default'].format(exchange=exchange_id, fees=default_fees))
            return default_fees

    async def _get_cached_limit(self, exchange_id: str, symbol: str, limits_cache: Dict[str, float]) -> float:
        """
        Получает лимит из кэша или запрашивает через API с кэшированием.
        """
        cache_key = f"{exchange_id}:{symbol}"
        if cache_key not in limits_cache:
            service = self.services[exchange_id]
            limits_cache[cache_key] = await service.get_reliable_min_order_value(symbol)
            logger.debug(f"Кэш лимитов: сохранен {cache_key} = {limits_cache[cache_key]:.2f}")
        else:
            logger.debug(f"Кэш лимитов: использован {cache_key} = {limits_cache[cache_key]:.2f}")
        return limits_cache[cache_key]

    async def _try_extract_fees_from_specific_market(self, service: ExchangeService, exchange_id: str, symbol: str) -> \
            Tuple[Dict[str, float], str]:
        try:
            markets = await service.client.load_markets()
            if symbol in markets and markets[symbol]:
                return self._extract_fees_from_market_data(markets[symbol], f"{FEE_METHOD_MARKET_DIRECT}_{symbol}")
            return {}, FEE_METHOD_UNKNOWN
        except Exception as e:
            logger.debug(f"🔍 Не удалось извлечь комиссии из market для {exchange_id} ({symbol}): {e}")
            return {}, FEE_METHOD_UNKNOWN

    async def _try_extract_fees_from_general_markets(self, service: ExchangeService, exchange_id: str) -> Tuple[
        Dict[str, float], str]:
        try:
            markets = await service.client.load_markets()
            for priority_symbol in PRIORITY_SYMBOLS_FOR_FEES:
                if priority_symbol in markets:
                    fees, _ = self._extract_fees_from_market_data(markets[priority_symbol], "")
                    if fees: return fees, f"{FEE_METHOD_MARKET_GENERAL}_{priority_symbol}"

            for market_symbol, market_data in markets.items():
                if market_data and isinstance(market_data, dict):
                    fees, _ = self._extract_fees_from_market_data(market_data, "")
                    if fees: return fees, f"{FEE_METHOD_MARKET_GENERAL}_{market_symbol}"
            return {}, FEE_METHOD_UNKNOWN
        except Exception as e:
            logger.debug(f"🔍 Не удалось извлечь общие комиссии из markets для {exchange_id}: {e}")
            return {}, FEE_METHOD_UNKNOWN

    def _extract_fees_from_market_data(self, market_data: dict, method_prefix: str) -> Tuple[Dict[str, float], str]:
        if market_data.get(MARKET_MAKER_KEY) is not None and market_data.get(MARKET_TAKER_KEY) is not None:
            return {
                MARKET_MAKER_KEY: float(market_data[MARKET_MAKER_KEY]),
                MARKET_TAKER_KEY: float(market_data[MARKET_TAKER_KEY])
            }, method_prefix

        fees_obj = market_data.get(MARKET_FEES_KEY, {})
        if fees_obj.get(MARKET_FEES_TRADING_KEY):
            trading = fees_obj[MARKET_FEES_TRADING_KEY]
            if trading.get(MARKET_MAKER_KEY) is not None and trading.get(MARKET_TAKER_KEY) is not None:
                return {
                    MARKET_MAKER_KEY: float(trading[MARKET_MAKER_KEY]),
                    MARKET_TAKER_KEY: float(trading[MARKET_TAKER_KEY])
                }, f"{FEE_METHOD_MARKET_FEES}_{method_prefix}".strip('_')

        return {}, FEE_METHOD_UNKNOWN

    async def _try_extract_fees_from_api(self, service: ExchangeService, exchange_id: str) -> Tuple[
        Dict[str, float], str]:
        try:
            fees_data = await service.client.fetch_trading_fees()
            if fees_data and fees_data.get(MARKET_FEES_TRADING_KEY):
                trading = fees_data[MARKET_FEES_TRADING_KEY]
                if trading.get(MARKET_MAKER_KEY) is not None and trading.get(MARKET_TAKER_KEY) is not None:
                    return {
                        MARKET_MAKER_KEY: float(trading[MARKET_MAKER_KEY]),
                        MARKET_TAKER_KEY: float(trading[MARKET_TAKER_KEY])
                    }, FEE_METHOD_API_FETCH
            return {}, FEE_METHOD_UNKNOWN
        except Exception as e:
            logger.debug(f"🔍 fetchTradingFees не поддерживается для {exchange_id}: {e}")
            return {}, FEE_METHOD_UNKNOWN

    def _validate_and_cache_fees(self, exchange_id: str, extracted_fees: Dict, default_fees: Dict) -> Dict:
        validated_fees = {}
        for fee_type in [MARKET_MAKER_KEY, MARKET_TAKER_KEY]:
            fee_value = extracted_fees.get(fee_type, default_fees[fee_type])
            try:
                fee_float = float(fee_value)
                if MIN_VALID_FEE <= fee_float <= MAX_VALID_FEE:
                    validated_fees[fee_type] = fee_float
                else:
                    logger.warning(
                        LEXICON_RU['fee_log_unreasonable_value'].format(fee_type=fee_type, exchange=exchange_id,
                                                                        value=fee_float))
                    validated_fees[fee_type] = default_fees[fee_type]
            except (ValueError, TypeError):
                logger.warning(LEXICON_RU['fee_log_invalid_value'].format(fee_type=fee_type, exchange=exchange_id,
                                                                          value=fee_value))
                validated_fees[fee_type] = default_fees[fee_type]
        self.trading_fees_cache[exchange_id] = validated_fees
        return validated_fees

    def _log_fee_extraction_result(self, exchange_id: str, fees: Dict, method_used: str):
        if method_used.startswith('default'):
            logger.info(LEXICON_RU['fee_log_default'].format(exchange=exchange_id, fees=fees))
        else:
            logger.debug(LEXICON_RU['fee_log_success'].format(exchange=exchange_id, method=method_used, fees=fees))

    async def _preload_trading_fees_for_all_exchanges(self, available_pairs: List[Tuple[str, List[str]]]):
        logger.debug("🔄 Предварительная загрузка торговых комиссий...")
        exchange_symbols_map = {}
        for symbol, exchanges in available_pairs:
            for exchange_id in exchanges:
                if exchange_id not in exchange_symbols_map:
                    exchange_symbols_map[exchange_id] = []
                exchange_symbols_map[exchange_id].append(symbol)

        fee_tasks = []
        for exchange_id, symbols in exchange_symbols_map.items():
            preferred_symbol = self._select_preferred_symbol_for_fees(symbols)
            fee_tasks.append(self._get_trading_fees(exchange_id, preferred_symbol))

        if fee_tasks:
            await asyncio.gather(*fee_tasks, return_exceptions=True)

    def _select_preferred_symbol_for_fees(self, available_symbols: List[str]) -> str:
        for priority_symbol in PRIORITY_SYMBOLS_FOR_FEES:
            if priority_symbol in available_symbols:
                return priority_symbol
        return available_symbols[0] if available_symbols else DEFAULT_FALLBACK_SYMBOL

    def _analyze_order_book_for_buy(self, order_book: Dict, trade_amount_usd: float) -> OrderBookAnalysis:
        """
        Анализирует стакан ордеров на покупку для расчета эффективной цены и проскальзывания.

        Метод проходит по предложениям на продажу (asks), чтобы определить, сколько монет
        можно купить на заданную сумму в USD, и какова будет средняя цена исполнения.

        Args:
            order_book: Словарь с данными стакана ордеров ('asks', 'bids').
            trade_amount_usd: Желаемая сумма покупки в USD.

        Returns:
            Объект OrderBookAnalysis с результатами анализа.
        """
        # Получаем список ордеров на продажу (аски).
        asks = order_book.get(ORDER_BOOK_ASKS, [])

        # Считаем общую доступную ликвидность в стакане
        total_available_liquidity_usd = sum(price * amount for price, amount in asks)
        total_available_liquidity_coin = sum(amount for _, amount in asks)

        # Если асков нет, то купить ничего нельзя.
        if not asks:
            # Возвращаем "пустой" результат с максимальным проскальзыванием из константы.
            return OrderBookAnalysis(effective_price=0,
                                     filled_amount=0,
                                     total_cost=0,
                                     slippage_percent=ORDERBOOK_EMPTY_SLIPPAGE_PERCENT,
                                     available_liquidity_usd=0.0,
                                     available_liquidity_coin=0.0
                                     )

        # Лучшая (самая низкая) цена продажи используется для расчета проскальзывания.
        best_ask = asks[0][0]
        # Оставшаяся сумма в USD, которую нужно потратить.
        remaining_usd_to_spend = trade_amount_usd
        # Общее количество купленных монет.
        total_coins_bought = 0.0
        # Общая стоимость покупки в USD.
        total_cost_in_usd = 0.0

        # Итерируемся по уровням цен в стакане.
        for price, amount in asks:
            # Если мы уже потратили почти всю сумму, выходим из цикла (используем константу для точности).
            if remaining_usd_to_spend <= ORDER_BOOK_ANALYSIS_PRECISION_USD:
                # Прерываем цикл.
                break

            # Рассчитываем стоимость покупки всех монет на данном ценовом уровне.
            level_cost = price * amount

            # Если мы можем выкупить весь уровень, не превысив остаток бюджета.
            if level_cost <= remaining_usd_to_spend:
                # Покупаем все монеты на этом уровне.
                total_coins_bought += amount
                # Увеличиваем общую стоимость.
                total_cost_in_usd += level_cost
                # Уменьшаем остаток бюджета.
                remaining_usd_to_spend -= level_cost
            else:
                # Если денег хватает только на часть уровня.
                # Рассчитываем, сколько монет мы можем купить на оставшиеся деньги.
                partial_amount_to_buy = remaining_usd_to_spend / price
                # Добавляем частичное количество к общему.
                total_coins_bought += partial_amount_to_buy
                # Обновляем общую стоимость (потратили всё, что было).
                total_cost_in_usd += remaining_usd_to_spend
                # Бюджет исчерпан.
                remaining_usd_to_spend = 0

        # Если в итоге ничего не было куплено (например, стакан был слишком "тонким").
        if total_coins_bought == 0 or total_cost_in_usd == 0:
            # Возвращаем "пустой" результат с максимальным проскальзыванием.
            return OrderBookAnalysis(effective_price=0,
                                     filled_amount=0,
                                     total_cost=0,
                                     slippage_percent=ORDERBOOK_EMPTY_SLIPPAGE_PERCENT,
                                     available_liquidity_usd=total_available_liquidity_usd,
                                     available_liquidity_coin=total_available_liquidity_coin
                                     )

        # Рассчитываем эффективную (среднюю) цену покупки.
        effective_price = total_cost_in_usd / total_coins_bought
        # Рассчитываем проскальзывание в процентах от лучшей цены.
        slippage = ((effective_price - best_ask) / best_ask) * 100 if best_ask > 0 else 0

        # Возвращаем объект с полным результатом анализа.
        return OrderBookAnalysis(
            effective_price=effective_price,
            filled_amount=total_coins_bought,
            total_cost=total_cost_in_usd,
            slippage_percent=slippage,
            available_liquidity_usd=total_available_liquidity_usd,
            available_liquidity_coin=total_available_liquidity_coin
        )

    def _analyze_order_book_for_sell(self, order_book: Dict, coin_amount: float) -> OrderBookAnalysis:
        """
        Анализирует стакан ордеров на продажу для расчета эффективной цены и проскальзывания.

        Метод проходит по заявкам на покупку (bids), чтобы определить, сколько USD
        можно получить за продажу заданного количества монет.

        Args:
            order_book: Словарь с данными стакана ордеров ('asks', 'bids').
            coin_amount: Количество монет для продажи.

        Returns:
            Объект OrderBookAnalysis с результатами анализа.
        """
        # Получаем список ордеров на покупку (биды).
        bids = order_book.get(ORDER_BOOK_BIDS, [])

        # Считаем общую доступную ликвидность в стакане
        total_available_liquidity_usd = sum(price * amount for price, amount in bids)
        total_available_liquidity_coin = sum(amount for _, amount in bids)

        # Если бидов нет, то продать ничего нельзя.
        if not bids:
            # Возвращаем "пустой" результат с максимальным проскальзыванием из константы.
            return OrderBookAnalysis(effective_price=0,
                                     filled_amount=0,
                                     total_cost=0,
                                     slippage_percent=ORDERBOOK_EMPTY_SLIPPAGE_PERCENT,
                                     available_liquidity_usd=0.0,
                                     available_liquidity_coin=0.0
                                     )

        # Лучшая (самая высокая) цена покупки используется для расчета проскальзывания.
        best_bid = bids[0][0]
        # Оставшееся количество монет, которое нужно продать.
        remaining_coins_to_sell = coin_amount
        # Общая выручка от продажи в USD.
        total_revenue_in_usd = 0.0
        # Общее количество проданных монет.
        total_coins_sold = 0.0

        # Итерируемся по уровням цен в стакане.
        for price, amount in bids:
            # Если мы уже продали почти всё, выходим из цикла (используем константу для точности).
            if remaining_coins_to_sell <= FLOAT_COMPARISON_EPSILON:
                # Прерываем цикл.
                break

            # Если объем спроса на этом уровне меньше, чем нам нужно продать.
            if amount <= remaining_coins_to_sell:
                # Продаем всё в этот уровень.
                total_revenue_in_usd += price * amount
                # Увеличиваем количество проданных монет.
                total_coins_sold += amount
                # Уменьшаем остаток монет для продажи.
                remaining_coins_to_sell -= amount
            else:
                # Если нам нужно продать меньше, чем есть спроса на этом уровне.
                # Продаем оставшуюся часть наших монет.
                total_revenue_in_usd += price * remaining_coins_to_sell
                # Добавляем это количество к проданным.
                total_coins_sold += remaining_coins_to_sell
                # Все монеты проданы.
                remaining_coins_to_sell = 0

        # Если в итоге ничего не было продано.
        if total_coins_sold == 0 or total_revenue_in_usd == 0:
            # Возвращаем "пустой" результат с максимальным проскальзыванием.
            return OrderBookAnalysis(effective_price=0,
                                     filled_amount=0,
                                     total_cost=0,
                                     slippage_percent=ORDERBOOK_EMPTY_SLIPPAGE_PERCENT,
                                     available_liquidity_usd=total_available_liquidity_usd,
                                     available_liquidity_coin=total_available_liquidity_coin
                                     )

        # Рассчитываем эффективную (среднюю) цену продажи.
        effective_price = total_revenue_in_usd / total_coins_sold
        # Рассчитываем проскальзывание в процентах от лучшей цены.
        slippage = ((best_bid - effective_price) / best_bid) * 100 if best_bid > 0 else 0

        # Возвращаем объект с полным результатом анализа.
        return OrderBookAnalysis(
            effective_price=effective_price,
            filled_amount=total_coins_sold,
            total_cost=total_revenue_in_usd,  # Для продажи 'total_cost' фактически является выручкой.
            slippage_percent=slippage,
            available_liquidity_usd=total_available_liquidity_usd,
            available_liquidity_coin=total_available_liquidity_coin
        )

    def _calculate_net_spread_with_fees(self, buy_analysis: OrderBookAnalysis, sell_analysis: OrderBookAnalysis,
                                        buy_exchange_id: str, sell_exchange_id: str) -> float:
        """
        Вычисляет чистый спред (прибыль в процентах) с учетом комиссий и проскальзывания.

        Args:
            buy_analysis: Результат анализа стакана на покупку.
            sell_analysis: Результат анализа стакана на продажу.
            buy_exchange_id: ID биржи покупки.
            sell_exchange_id: ID биржи продажи.

        Returns:
            Чистый спред в виде десятичной дроби (например, 0.01 для 1%).
        """
        # Получаем комиссии из кэша. Если в кэше нет, используем дефолтные значения из констант.
        buy_fees = self.trading_fees_cache.get(buy_exchange_id, DEFAULT_EXCHANGE_FEES.get(buy_exchange_id,
                                                                                          DEFAULT_EXCHANGE_FEES[
                                                                                              'default']))
        sell_fees = self.trading_fees_cache.get(sell_exchange_id, DEFAULT_EXCHANGE_FEES.get(sell_exchange_id,
                                                                                            DEFAULT_EXCHANGE_FEES[
                                                                                                'default']))

        # Рассчитываем полную стоимость покупки, включая комиссию биржи (используем TAKER комиссию).
        buy_cost_with_fee = buy_analysis.total_cost * (1 + buy_fees[FEES_TAKER])

        # Рассчитываем итоговую выручку от продажи, вычитая комиссию биржи (используем TAKER комиссию).
        sell_revenue_with_fee = sell_analysis.total_cost * (1 - sell_fees[FEES_TAKER])

        # Чистая прибыль - это разница между чистой выручкой и полными затратами.
        net_profit = sell_revenue_with_fee - buy_cost_with_fee

        # Считаем спред как отношение чистой прибыли к затратам на покупку.
        net_spread = (net_profit / buy_cost_with_fee) if buy_cost_with_fee > 0 else INVALID_SPREAD_VALUE

        # Возвращаем чистый спред.
        return net_spread

    async def find_and_execute_opportunity(self) -> bool:
        """
        Ищет, фильтрует по порогу прибыльности и исполняет ЛУЧШУЮ возможность.
        """
        from src.services.data_enricher_service import data_enricher
        # В обычном режиме флаги по умолчанию (False), поведение не меняется
        profitable_opportunities = await self._find_all_opportunities(ignore_threshold=False, ignore_sell_balance=False)

        if not profitable_opportunities:
            logger.info(LEXICON_RU['log_no_opportunities_found'])
            return False

        # Обогащаем данные перед сортировкой
        enriched_opportunities = await data_enricher.enrich_opportunities(profitable_opportunities, self.services)

        # Сортируем по новой AI-оценке
        enriched_opportunities.sort(key=lambda x: x.ai_score, reverse=True)

        best_opportunity = profitable_opportunities[0]

        # Сообщаем менеджеру о попытке торговли, чтобы активировать кулдаун.
        dynamic_pairs_manager.report_trade_attempt(best_opportunity.symbol)

        success = await self._execute_best_opportunity_with_order_book_data(best_opportunity)
        if success:
            logger.info(LEXICON_RU['log_execution_success'])
            return True
        else:
            logger.warning(LEXICON_RU['log_execution_failed_trying_next'].format(symbol=best_opportunity.symbol))
            return False

    async def run_reconnaissance_scan(self) -> List[ArbitrageOpportunity]:
        """
        Явное указание режима разведки.
        """
        from src.services.data_enricher_service import data_enricher
        logger.info("🚀 Запуск режима 'Разведка'...")
        all_opportunities = await self._find_all_opportunities(
            ignore_threshold=True,
            ignore_sell_balance=True,
            reconnaissance_mode=True
        )
        # 2. Обогащаем найденные возможности данными
        logger.info(f"Найдено {len(all_opportunities)} потенциальных связок. Начинаю обогащение данных...")
        enriched_opportunities = await data_enricher.enrich_opportunities(all_opportunities, self.services)

        # 3. Сортируем уже обогащенные данные по AI-оценке
        enriched_opportunities.sort(key=lambda x: x.ai_score, reverse=True)

        logger.info(f"🛰️ Разведка и анализ завершены. Итого возможностей: {len(enriched_opportunities)}")
        return enriched_opportunities

    async def _find_all_opportunities(self, ignore_threshold: bool = False,
                                      ignore_sell_balance: bool = False,
                                      reconnaissance_mode: bool = False) -> List[ArbitrageOpportunity]:
        """
        ИСПРАВЛЕНО: Управляет блокировкой и делегирует поиск основной логике.
        Этот метод является "диспетчером".
        """
        if reconnaissance_mode:
            # В режиме разведки захватываем блокировку, чтобы фоновые задачи обновления кэша не мешали.
            async with app_state.cache_refresh_lock:
                return await self._execute_opportunities_logic(
                    ignore_threshold, ignore_sell_balance, reconnaissance_mode
                )
        else:
            # В обычном торговом режиме (каждую минуту) выполняем без дополнительной блокировки,
            # чтобы не замедлять основной цикл.
            return await self._execute_opportunities_logic(
                ignore_threshold, ignore_sell_balance, reconnaissance_mode
            )

    async def _execute_opportunities_logic(self, ignore_threshold: bool,
                                           ignore_sell_balance: bool,
                                           reconnaissance_mode: bool) -> List[ArbitrageOpportunity]:
        """
        Основная логика поиска арбитражных возможностей с кэшем лимитов.
        """
        limits_cache: Dict[str, float] = {}

        coins_to_process = [coin for coin in self.tracked_coins_to_scan
                            if coin not in STABLE_COINS]

        if not coins_to_process:
            logger.warning("Нет валидных монет для анализа в стратегии.")
            return []

        logger.info(f"Анализ арбитражных возможностей для {len(coins_to_process)} монет.")

        available_pairs = await dynamic_pairs_manager.get_available_pairs_for_scanning(
            self.services,
            coins_to_process,
            force_refresh=reconnaissance_mode
        )

        if not available_pairs:
            logger.info("Нет доступных пар для сканирования.")
            return []

        await self._preload_trading_fees_for_all_exchanges(available_pairs)
        order_books = await self._fetch_all_order_books(available_pairs)

        if not order_books:
            logger.warning("Не удалось получить ни одного стакана заявок.")
            return []

        potential_opportunities: List[ArbitrageOpportunity] = []

        for symbol, exchanges_data in order_books.items():

            coin = symbol.split('/')[0]
            available_exchanges = list(exchanges_data.keys())

            if len(available_exchanges) < MIN_EXCHANGES_FOR_ARBITRAGE:
                continue

            for i in range(len(available_exchanges)):
                for j in range(i + 1, len(available_exchanges)):
                    ex1, ex2 = available_exchanges[i], available_exchanges[j]

                    for buy_ex, sell_ex in [(ex1, ex2), (ex2, ex1)]:
                        opportunity = await self._analyze_arbitrage_opportunity(
                            symbol, coin, buy_ex, sell_ex, exchanges_data,
                            ignore_threshold, ignore_sell_balance, reconnaissance_mode,
                            limits_cache=limits_cache
                        )
                        if opportunity:
                            potential_opportunities.append(opportunity)

        # potential_opportunities.sort(key=lambda x: x.score, reverse=True)

        logger.info(f"Найдено {len(potential_opportunities)} потенциальных арбитражных возможностей.")
        return potential_opportunities

    def _find_max_arbitrage_volume(self, buy_book: List[List[float]], sell_book: List[List[float]],
                                   buy_fee: float, sell_fee: float) -> Tuple[float, float, float, float, float]:
        """
        Безопасный расчет максимального объема без изменения исходных данных.
        """
        if not buy_book or not sell_book:
            return 0.0, 0.0, 0.0, 0.0, 0.0

        # ИСПРАВЛЕНИЕ 1: Создаем безопасные копии данных
        buy_levels = copy.deepcopy(buy_book)
        sell_levels = copy.deepcopy(sell_book)

        buy_idx, sell_idx = 0, 0
        total_volume_usd, total_profit_usd, total_coins_traded = 0.0, 0.0, 0.0

        while buy_idx < len(buy_levels) and sell_idx < len(sell_levels):
            buy_price, buy_amount = buy_levels[buy_idx]
            sell_price, sell_amount = sell_levels[sell_idx]

            # ИСПРАВЛЕНИЕ 2: Валидация входных данных
            if buy_price <= 0 or sell_price <= 0 or buy_amount <= 0 or sell_amount <= 0:
                logger.warning(
                    f"Некорректные данные в стакане: buy={buy_price}@{buy_amount}, sell={sell_price}@{sell_amount}")
                break

            buy_price_with_fee = buy_price * (1 + buy_fee)
            sell_price_with_fee = sell_price * (1 - sell_fee)

            # Если спред исчерпан, выходим
            if buy_price_with_fee >= sell_price_with_fee:
                break

            tradeable_amount = min(buy_amount, sell_amount)

            profit_per_coin = sell_price_with_fee - buy_price_with_fee
            trade_profit = tradeable_amount * profit_per_coin

            total_profit_usd += trade_profit
            total_volume_usd += tradeable_amount * buy_price
            total_coins_traded += tradeable_amount

            # Обновляем копии данных
            buy_levels[buy_idx][1] -= tradeable_amount
            sell_levels[sell_idx][1] -= tradeable_amount

            if buy_levels[buy_idx][1] < FLOAT_PRECISION_TOLERANCE:
                buy_idx += 1
            if sell_levels[sell_idx][1] < FLOAT_PRECISION_TOLERANCE:
                sell_idx += 1

        # 3: Безопасный расчет среднего спреда
        avg_spread = (total_profit_usd / total_volume_usd) if total_volume_usd > FLOAT_PRECISION_TOLERANCE else 0.0

        effective_buy_price = total_volume_usd / total_coins_traded if total_coins_traded > 0 else 0.0

        # Вычисляем общую выручку с учетом комиссий, чтобы найти эффективную цену продажи
        total_revenue_with_fee = total_volume_usd * (1 + avg_spread) * (1 - sell_fee)
        effective_sell_price = total_revenue_with_fee / total_coins_traded if total_coins_traded > 0 else 0.0

        return total_volume_usd, total_profit_usd, avg_spread, effective_buy_price, effective_sell_price

    async def _analyze_arbitrage_opportunity(self, symbol: str, coin: str,
                                             buy_ex: str, sell_ex: str,
                                             exchanges_data: Dict,
                                             ignore_threshold: bool = False,
                                             ignore_sell_balance: bool = False,
                                             reconnaissance_mode: bool = False,
                                             limits_cache: Dict[str, float] = None) -> Optional[ArbitrageOpportunity]:
        """
        ФИНАЛЬНАЯ ВЕРСИЯ: Анализирует арбитражную возможность с использованием кэша лимитов,
        поддерживая два режима работы: обычный и разведывательный.
        """
        # 1. --- Начальная подготовка и проверки ---
        if limits_cache is None:
            limits_cache = {}

        # Проверяем, может ли биржа вообще совершать покупки (хватает ли USDT)
        if buy_ex not in self.buy_capable_exchanges:
            logger.debug(f"⚠️ {symbol}: Пропуск {buy_ex}→{sell_ex} - биржа {buy_ex} не может покупать")
            return None

        # Извлекаем данные стаканов ордеров
        buy_order_book = exchanges_data[buy_ex].get(ORDER_BOOK_ASKS, [])
        sell_order_book = exchanges_data[sell_ex].get(ORDER_BOOK_BIDS, [])

        # Если хотя бы один стакан пуст, арбитраж невозможен
        if not buy_order_book or not sell_order_book:
            return None

        # Получаем предварительно загруженные комиссии из кэша
        buy_fees = self.trading_fees_cache.get(
            buy_ex,
            DEFAULT_EXCHANGE_FEES.get(buy_ex, DEFAULT_EXCHANGE_FEES['default'])
        )
        sell_fees = self.trading_fees_cache.get(
            sell_ex,
            DEFAULT_EXCHANGE_FEES.get(sell_ex, DEFAULT_EXCHANGE_FEES['default'])
        )
        buy_taker_fee = buy_fees.get(FEES_TAKER, 0.002)
        sell_taker_fee = sell_fees.get(FEES_TAKER, 0.002)

        # РАСЧЕТ ПОРОГА БЕЗУБЫТОЧНОСТИ (для обоих режимов)
        breakeven_threshold = (buy_taker_fee + sell_taker_fee) * 100

        logger.debug(
            f"Комиссии {symbol}: {buy_ex}={buy_taker_fee:.4f}, {sell_ex}={sell_taker_fee:.4f}, порог={breakeven_threshold:.2f}%")

        # 2. --- Единое получение лимитов (для обоих режимов) ---
        min_buy_limit = await self._get_cached_limit(buy_ex, symbol, limits_cache)
        min_sell_limit = await self._get_cached_limit(sell_ex, symbol, limits_cache)
        # Минимальная сумма для сделки определяется как максимальный из минимальных лимитов двух бирж.
        min_trade_amount = max(min_buy_limit, min_sell_limit)

        # 3. --- Ветвление логики в зависимости от режима ---
        if reconnaissance_mode:
            # ---- РЕЖИМ РАЗВЕДКИ: Анализ максимального объема ----

            # Анализируем всю глубину стаканов, чтобы найти максимальный возможный объем сделки
            max_volume, potential_profit, avg_spread, eff_buy, eff_sell = self._find_max_arbitrage_volume(
                buy_order_book, sell_order_book, buy_taker_fee, sell_taker_fee
            )

            # Отсекаем микро-возможности, которые не представляют интереса
            if potential_profit < MINIMUM_MEANINGFUL_PROFIT_USD or max_volume < 1.0:
                return None

            # Создаем объект возможности с данными для разведки
            # ИСПОЛЬЗУЕМ НОВУЮ СТРУКТУРУ
            opportunity = ArbitrageOpportunity(
                symbol=symbol,
                coin=coin,
                buy_exchange_id=buy_ex,
                sell_exchange_id=sell_ex,
                max_volume_usd=max_volume,
                potential_profit_usd=potential_profit,
                roi_percent=avg_spread * PERCENTAGE_MULTIPLIER,
                min_trade_amount_usd=min_trade_amount,
                breakeven_threshold_percent=breakeven_threshold,
                effective_buy_price=eff_buy,
                effective_sell_price=eff_sell
            )

            # Получаем репрезентативную цену и классифицируем
            asset_price = self._get_asset_price_for_classification(symbol, exchanges_data)
            self._classify_opportunity(opportunity, min_trade_amount, asset_price)

            # Отсеиваем не-призрачные, но бессмысленные возможности
            if not opportunity.is_phantom and (
                    opportunity.potential_profit_usd < MINIMUM_MEANINGFUL_ABSOLUTE_PROFIT or opportunity.max_volume_usd < MINIMUM_PRACTICAL_TRADE_VOLUME):
                return None

            # Логируем найденную возможность
            buy_price = buy_order_book[0][0]
            sell_price = sell_order_book[0][0]
            logger.info(f"✅ РАЗВЕДКА [{opportunity.opportunity_type.value}]:  {symbol} {buy_ex}→{sell_ex} "
                        f"Объем=${max_volume:.2f}, Профит=${potential_profit:.2f} ({avg_spread:.2%}) | "
                        f"Цены(Buy/Sell): {buy_price:.6f}/{sell_price:.6f}")

            return opportunity

        else:
            # ---- ОБЫЧНЫЙ РЕЖИМ: Анализ для фиксированной суммы ----

            # Проверяем баланс монеты на бирже продажи (если требуется)
            if not ignore_sell_balance:
                sell_balances = self.initial_balances.get(sell_ex, {})
                # Используем цену из стакана для более точной оценки
                if not buy_order_book: return None
                estimated_coin_needed = self.trade_amount / buy_order_book[0][0]
                available_balance = sell_balances.get(coin, 0.0)

                if available_balance < estimated_coin_needed:
                    logger.debug(f"⚠️ {symbol}: Пропуск {buy_ex}→{sell_ex} - недостаточно {coin} на {sell_ex}")
                    return None

            # Рассчитываем реальные параметры сделки на заданную сумму с учетом ликвидности
            buy_analysis = self._analyze_order_book_for_buy(exchanges_data[buy_ex], self.trade_amount)
            if buy_analysis.total_cost < self.trade_amount * MIN_SELL_TO_BUY_FILL_RATIO:
                logger.debug(f"⚠️ {symbol}: Пропуск {buy_ex}→{sell_ex} - недостаточно ликвидности для покупки")
                return None

            sell_analysis = self._analyze_order_book_for_sell(exchanges_data[sell_ex], buy_analysis.filled_amount)
            if sell_analysis.filled_amount < buy_analysis.filled_amount * MIN_SELL_TO_BUY_FILL_RATIO:
                logger.debug(f"⚠️ {symbol}: Пропуск {buy_ex}→{sell_ex} - недостаточно ликвидности для продажи")
                return None

            # Рассчитываем чистый спред с учетом комиссий
            net_spread = self._calculate_net_spread_with_fees(buy_analysis, sell_analysis, buy_ex, sell_ex)

            # Проверяем спред по порогу прибыльности
            threshold_to_check = 0 if ignore_threshold else self.profit_threshold
            if net_spread < threshold_to_check:
                logger.debug(
                    LEXICON_RU['log_unprofitable_opportunity_found'].format(
                        symbol=symbol, buy_ex=buy_ex, sell_ex=sell_ex, net_spread=net_spread * 100,
                        profit_threshold=self.profit_threshold * 100, buy_price=buy_analysis.effective_price,
                        sell_price=sell_analysis.effective_price, buy_slip=buy_analysis.slippage_percent,
                        sell_slip=sell_analysis.slippage_percent
                    )
                )
                return None

            # Если все проверки пройдены, создаем объект возможности
            # ИСПОЛЬЗУЕМ НОВУЮ СТРУКТУРУ
            opportunity = ArbitrageOpportunity(
                symbol=symbol,
                coin=coin,
                buy_exchange_id=buy_ex,
                sell_exchange_id=sell_ex,
                buy_analysis=buy_analysis,
                sell_analysis=sell_analysis,
                roi_percent=net_spread * PERCENTAGE_MULTIPLIER,
                potential_profit_usd=sell_analysis.total_cost - buy_analysis.total_cost,
                max_volume_usd=buy_analysis.total_cost,
                min_trade_amount_usd=min_trade_amount,
                breakeven_threshold_percent=breakeven_threshold,
                effective_buy_price=buy_analysis.effective_price,
                effective_sell_price=sell_analysis.effective_price
            )

            # Логируем найденную прибыльную возможность
            logger.info(
                f"✅ ВОЗМОЖНОСТЬ: {symbol} {buy_ex}→{sell_ex} спред={net_spread:.4%}")

            return opportunity

    async def _fetch_all_order_books(self, available_pairs: List[Tuple[str, List[str]]]) -> Dict[str, Dict[str, Dict]]:
        """
        Надежный гибридный сбор стаканов с динамическим черным списком,
        интеллектуальным fallback, обратной связью и оптимизированным выполнением.
        """
        logger.info(LEXICON_RU['log_fetching_order_books'])
        start_time = asyncio.get_event_loop().time()

        # 1. Группируем символы по биржам
        symbols_by_exchange = defaultdict(set)
        for symbol, exchanges in available_pairs:
            for exchange_id in exchanges:
                symbols_by_exchange[exchange_id].add(symbol)

        # 2. Разделяем биржи на поддерживающие пакетные запросы и нет
        batch_capable_exchanges = {}
        single_only_exchanges = {}

        for exchange_id, symbols in symbols_by_exchange.items():
            symbol_list = list(symbols)
            if blacklist_manager.is_batch_supported(exchange_id):
                batch_capable_exchanges[exchange_id] = symbol_list
            else:
                single_only_exchanges[exchange_id] = symbol_list

        # 3. Создаем задачи для обоих типов запросов
        all_tasks = []
        all_metadata = []

        if batch_capable_exchanges:
            await self._report_progress(
                f"<b>🚀 Этап 1:</b> <i>Быстрый сбор данных с {len(batch_capable_exchanges)} бирж</i>")
            for exchange_id, symbol_list in batch_capable_exchanges.items():
                service = self.services[exchange_id]
                fetch_task = service.client.fetch_order_books(symbol_list, limit=ORDER_BOOK_DEPTH)
                all_tasks.append(fetch_task)
                all_metadata.append({'type': 'batch', 'exchange': exchange_id, 'symbols': symbol_list})

        if single_only_exchanges:
            total_single_requests = sum(len(s) for s in single_only_exchanges.values())
            await self._report_progress(
                f"<b>🔍 Этап 2:</b> <i>Детальная проверка {total_single_requests} пар по отдельности</i>")
            for exchange_id, symbol_list in single_only_exchanges.items():
                service = self.services[exchange_id]
                for symbol in symbol_list:
                    fetch_task = service.client.fetch_order_book(symbol, limit=ORDER_BOOK_DEPTH)
                    all_tasks.append(fetch_task)
                    all_metadata.append({'type': 'single', 'exchange': exchange_id, 'symbol': symbol})

        if not all_tasks:
            return {}

        # Правильно считаем общее количество СИМВОЛОВ
        total_symbols_to_process = sum(len(md.get('symbols', [md.get('symbol')])) for md in all_metadata)

        processed_count = 0
        lock = asyncio.Lock()

        # Адаптивная частота обновлений (не более ~20 раз)
        update_frequency = max(1, total_symbols_to_process // RECON_PROGRESS_UPDATES_COUNT)

        async def task_wrapper(async_task, metadata):
            nonlocal processed_count
            try:
                task_result = await async_task
                return task_result
            finally:
                symbol_count = len(metadata.get('symbols', [metadata.get('symbol')]))
                should_update = False
                processed_symbols_count = 0

                # Вынос callback из критической секции
                async with lock:
                    processed_count += symbol_count
                    processed_symbols_count = processed_count
                    if (processed_count % update_frequency == 0) or (processed_count >= total_symbols_to_process):
                        should_update = True

                if should_update and self.progress_callback:
                    await self.progress_callback(
                        f"<b>📊 Процесс анализа рынка...</b>",
                        current=processed_symbols_count,
                        total=total_symbols_to_process
                    )

        wrapped_tasks = [task_wrapper(async_task, metadata) for async_task, metadata in zip(all_tasks, all_metadata)]

        results = await asyncio.gather(*wrapped_tasks, return_exceptions=True)

        # 4. Обрабатываем результаты
        order_books: Dict[str, Dict[str, Dict]] = defaultdict(dict)
        successful_fetches, failed_fetches = 0, 0
        failed_batch_exchanges = set()

        for i, metadata in enumerate(all_metadata):
            fetch_result = results[i]
            exchange_id = metadata['exchange']

            if isinstance(fetch_result, Exception):
                if metadata['type'] == 'batch':
                    # Если пакетный запрос упал, "жалуемся" менеджеру
                    blacklist_manager.report_batch_failure(exchange_id)
                    failed_batch_exchanges.add(exchange_id)
                    failed_fetches += len(metadata['symbols'])
                    logger.error(f"❌ Пакетный запрос к {exchange_id} упал: {type(fetch_result).__name__}")
                else:
                    failed_fetches += 1
                # Важно: сообщаем менеджеру о неудаче
                symbols_in_task = metadata.get('symbols', [metadata.get('symbol')])
                for symbol in symbols_in_task:
                    if symbol:
                        dynamic_pairs_manager.report_failure(symbol, exchange_id,
                                                             f"fetch_error: {type(fetch_result).__name__}")
                continue

            if metadata['type'] == 'batch' and isinstance(fetch_result, dict):
                for symbol, order_book in fetch_result.items():
                    if order_book and order_book.get('asks') and order_book.get('bids'):
                        order_books[symbol][exchange_id] = order_book
                        successful_fetches += 1
                        dynamic_pairs_manager.report_success(symbol, exchange_id)
                    else:
                        failed_fetches += 1
                        dynamic_pairs_manager.report_failure(symbol, exchange_id, "empty_batch_result")
            elif metadata['type'] == 'single' and isinstance(fetch_result, dict):
                symbol = metadata['symbol']
                if fetch_result.get('asks') and fetch_result.get('bids'):
                    order_books[symbol][exchange_id] = fetch_result
                    successful_fetches += 1
                    dynamic_pairs_manager.report_success(symbol, exchange_id)
                else:
                    failed_fetches += 1
                    dynamic_pairs_manager.report_failure(symbol, exchange_id, "empty_single_result")

        # 5. Fallback-механизм для упавших пакетных запросов
        if failed_batch_exchanges:
            logger.warning(
                f"🔄 Запуск fallback для {len(failed_batch_exchanges)} бирж: {', '.join(failed_batch_exchanges)}")
            fallback_tasks, fallback_metadata = [], []
            for exchange_id in failed_batch_exchanges:
                service = self.services[exchange_id]
                for symbol in batch_capable_exchanges[exchange_id]:
                    fallback_task = service.client.fetch_order_book(symbol, limit=ORDER_BOOK_DEPTH)
                    fallback_tasks.append(fallback_task)
                    fallback_metadata.append({'exchange': exchange_id, 'symbol': symbol})

            if fallback_tasks:
                await self._report_progress(
                    f"⚠️ Одна из бирж не поддерживает быструю загрузку.\nПерехожу на детальную проверку...\nПовторяю {len(fallback_tasks)} запросов в детальном режиме...")
                fallback_results = await asyncio.gather(*fallback_tasks, return_exceptions=True)

                for i, metadata in enumerate(fallback_metadata):
                    fallback_result = fallback_results[i]
                    symbol, exchange_id = metadata['symbol'], metadata['exchange']
                    if isinstance(fallback_result, dict) and fallback_result.get('asks') and fallback_result.get(
                            'bids'):
                        order_books[symbol][exchange_id] = fallback_result
                        successful_fetches += 1
                        failed_fetches -= 1
                        dynamic_pairs_manager.report_success(symbol, exchange_id)

        fetch_time = asyncio.get_event_loop().time() - start_time
        final_message = f"✅ Стаканы получены за {fetch_time:.2f}с. Успешно: {successful_fetches}, ошибок: {failed_fetches}"
        await self._report_progress(final_message)
        logger.info(final_message)

        return order_books

    async def _execute_best_opportunity_with_order_book_data(self, opportunity: ArbitrageOpportunity) -> bool:
        """
        Исполняет выбранную арбитражную возможность с точным расчетом количества.

        Метод определяет наиболее строгую точность (precision) для количества
        монет среди двух бирж, форматирует объем сделки, формирует детальный
        отчет для пользователя из лексикона и инициирует исполнение ордеров.

        Args:
            opportunity: Объект ArbitrageOpportunity с данными для сделки.

        Returns:
            True, если сделка была успешно инициирована, иначе False.
        """
        # Шаг 1: Извлекаем основные данные из объекта возможности.
        symbol = opportunity.symbol
        coin = opportunity.coin
        buy_exchange_id = opportunity.buy_exchange_id
        sell_exchange_id = opportunity.sell_exchange_id
        effective_trade_amount = opportunity.buy_analysis.total_cost

        # Шаг 2: Получаем доступ к сервисам бирж и информации о рынках из кэша ccxt.
        buy_market = (await service_manager.get_markets(buy_exchange_id)).get(symbol)
        sell_market = (await service_manager.get_markets(sell_exchange_id)).get(symbol)
        # Проверяем, что информация о рынках доступна.
        if not buy_market or not sell_market:
            # Логируем предупреждение и отменяем сделку.
            logger.warning(LEXICON_RU['log_market_details_missing'].format(symbol=symbol))
            return False

        # Шаг 3: Безопасно получаем и преобразуем точность в объект Decimal для надежных вычислений.
        try:
            # Получаем значение точности, используя константы для ключей и fallback значение из констант.
            buy_precision_str = str(
                buy_market.get(MARKET_FIELD_PRECISION, {}).get(MARKET_PRECISION_AMOUNT, DEFAULT_PRECISION_AMOUNT))
            sell_precision_str = str(
                sell_market.get(MARKET_FIELD_PRECISION, {}).get(MARKET_PRECISION_AMOUNT, DEFAULT_PRECISION_AMOUNT))
            # Создаем объекты Decimal.
            buy_precision_decimal = Decimal(buy_precision_str)
            sell_precision_decimal = Decimal(sell_precision_str)
        except InvalidOperation:
            # Логируем ошибку, если значение точности некорректно.
            logger.error(LEXICON_RU['log_invalid_precision'].format(symbol=symbol))
            return False

        # Шаг 4: Извлекаем exponent (показатель степени), который отражает количество знаков после запятой.
        buy_exponent = buy_precision_decimal.as_tuple().exponent
        sell_exponent = sell_precision_decimal.as_tuple().exponent

        # Шаг 5: Проверяем, что exponent является числом (а не 'NaN' или 'Infinity').
        if not isinstance(buy_exponent, int) or not isinstance(sell_exponent, int):
            # Логируем предупреждение в случае некорректного значения.
            logger.warning(LEXICON_RU['log_invalid_precision_exponent'].format(symbol=symbol))
            return False

        # Шаг 6: Теперь можно безопасно вычислить количество знаков (взяв модуль от exponent) и выбрать самое строгое (минимальное).
        buy_decimals = abs(buy_exponent)
        sell_decimals = abs(sell_exponent)
        precision_digits = min(buy_decimals, sell_decimals)
        # Логируем отладочную информацию о точности.
        logger.debug(
            LEXICON_RU['log_precision_info'].format(
                symbol=symbol, buy_decimals=buy_decimals, sell_decimals=sell_decimals, precision_digits=precision_digits
            )
        )

        # Шаг 7: Получаем "сырое" количество из анализа стакана и форматируем его с вычисленной точностью.
        raw_amount = opportunity.buy_analysis.filled_amount
        amount_to_trade = format_precision_amount(raw_amount, precision_digits)
        # Проверяем, что после форматирования количество не стало нулевым.
        if amount_to_trade <= 0:
            logger.warning(LEXICON_RU['log_amount_zero_after_format'].format(symbol=symbol))
            return False

        # Логируем процесс форматирования для отладки.
        logger.info(
            LEXICON_RU['log_amount_formatting_info'].format(
                raw_amount=raw_amount, formatted_amount=amount_to_trade, precision=precision_digits
            )
        )

        # Шаг 8: Продолжаем выполнение с уже отформатированным и безопасным количеством.
        logger.info(LEXICON_RU['log_executing_arbitrage'].format(symbol=symbol))
        logger.info(
            LEXICON_RU['log_executing_buy'].format(
                amount=amount_to_trade, precision=precision_digits, coin=coin,
                exchange=buy_exchange_id, trade_value=effective_trade_amount
            )
        )
        logger.info(
            LEXICON_RU['log_executing_sell'].format(
                amount=amount_to_trade, precision=precision_digits, coin=coin, exchange=sell_exchange_id
            )
        )

        # Шаг 9: Подготавливаем параметры для шаблона сообщения из лексикона.
        message_params = {
            "symbol": symbol,
            "net_spread": opportunity.roi_percent / 100.0,
            "profit_threshold": self.profit_threshold,
            "score": getattr(opportunity, 'ai_score', 0.0),
            "buy_exchange_name": buy_exchange_id.capitalize(),
            "amount": amount_to_trade,
            "precision": precision_digits,
            "coin": coin,
            "buy_price": opportunity.buy_analysis.effective_price,
            "buy_slippage": opportunity.buy_analysis.slippage_percent,
            "sell_exchange_name": sell_exchange_id.capitalize(),
            "sell_price": opportunity.sell_analysis.effective_price,
            "sell_slippage": opportunity.sell_analysis.slippage_percent,
        }

        # Формируем первую часть сообщения на основе шаблона из лексикона.
        initial_message = LEXICON_RU['opportunity_execution_summary'].format(**message_params)

        # Шаг 10: Вызываем внутренний метод для фактического исполнения сделки и получения отчета.
        # <-- ИСПРАВЛЕНО: spread_percent теперь берется напрямую из roi_percent -->
        trade_success, trade_report = await self._execute_trade(
            symbol=symbol, coin=coin,
            buy_exchange_id=buy_exchange_id, sell_exchange_id=sell_exchange_id,
            amount_to_trade=amount_to_trade,
            spread_percent=opportunity.roi_percent, # <-- ИСПРАВЛЕНО
            buy_price=opportunity.buy_analysis.effective_price,
            sell_price=opportunity.sell_analysis.effective_price,
            effective_trade_amount=effective_trade_amount
        )

        # Шаг 11: Собираем финальное сообщение, объединяя информационный блок и отчет о сделке.
        final_message = f"{initial_message}\n\n{trade_report}"

        # Получаем текущий статус сканера для отображения правильной клавиатуры.
        is_running = await scanner_api_service.get_scanner_status()
        # Импортируем клавиатуру прямо перед использованием, чтобы избежать циклических импортов.
        from src.bot.keyboards import get_back_to_scanner_menu_keyboard
        # Отправляем итоговое сообщение пользователю.
        await self.notifier.send_message(self.user_id, final_message,
                                         reply_markup=get_back_to_scanner_menu_keyboard(is_running))

        # Шаг 12: Возвращаем результат выполнения сделки.
        return trade_success

    async def _execute_trade(self, symbol: str, coin: str, buy_exchange_id: str,
                             sell_exchange_id: str, amount_to_trade: float,
                             spread_percent: float = 0.0, buy_price: float = None,
                             sell_price: float = None, effective_trade_amount: float = None) -> Tuple[bool, str]:
        """
        Выполняет арбитражную сделку, включая проверки балансов, размещение
        ордеров, анализ результатов и формирование итогового отчета.

        Args:
            symbol: Торговый символ (напр. "BTC/USDT").
            coin: Тикер монеты (напр. "BTC").
            buy_exchange_id: ID биржи для покупки.
            sell_exchange_id: ID биржи для продажи.
            amount_to_trade: Количество монеты для торговли.
            spread_percent: Ожидаемый спред в процентах.
            buy_price: Планируемая цена покупки.
            sell_price: Планируемая цена продажи.
            effective_trade_amount: Реальная стоимость сделки в USD.

        Returns:
            Кортеж (bool, str), где bool - успех сделки, str - отчет для пользователя.
        """
        # Шаг 0: Инициализация переменных.
        buy_service = self.services[buy_exchange_id]  # Получаем сервис для биржи покупки.
        sell_service = self.services[sell_exchange_id]  # Получаем сервис для биржи продажи.
        trade_amount_to_use = effective_trade_amount or self.trade_amount  # Определяем сумму сделки.

        # Логируем начало попытки исполнения сделки.
        logger.info(LEXICON_RU['log_trade_attempt'].format(symbol=symbol, amount=trade_amount_to_use))

        try:
            # --- ЭТАП 0: ПРОВЕРКА БАЛАНСОВ ПЕРЕД СДЕЛКОЙ ---
            logger.info(LEXICON_RU['log_trade_pre_check_start'])
            # Получаем предзагруженные балансы.
            initial_buy_balances = self.initial_balances.get(buy_exchange_id, {})
            initial_sell_balances = self.initial_balances.get(sell_exchange_id, {})

            # Если предзагруженных балансов нет, запрашиваем их в реальном времени.
            if not initial_buy_balances or not initial_sell_balances:
                logger.warning(LEXICON_RU['log_trade_balances_missing'])
                balance_tasks = [
                    asyncio.wait_for(buy_service.get_balance(), timeout=BALANCE_FETCH_TIMEOUT_SECONDS),
                    asyncio.wait_for(sell_service.get_balance(), timeout=BALANCE_FETCH_TIMEOUT_SECONDS)
                ]
                balance_results = await asyncio.gather(*balance_tasks, return_exceptions=True)
                initial_buy_balances, initial_sell_balances = balance_results

            # Проверяем, не было ли ошибок при получении балансов.
            if isinstance(initial_buy_balances, BaseException):
                raise ConnectionError(
                    LEXICON_RU['log_trade_balance_fetch_error'].format(exchange=buy_exchange_id.capitalize(),
                                                                       error=initial_buy_balances))
            if isinstance(initial_sell_balances, BaseException):
                raise ConnectionError(
                    LEXICON_RU['log_trade_balance_fetch_error'].format(exchange=sell_exchange_id.capitalize(),
                                                                       error=initial_sell_balances))

            # Проверка баланса USDT на бирже покупки.
            usdt_on_buy = initial_buy_balances.get(PRIMARY_QUOTE_CURRENCY, DEFAULT_NUMERIC_VALUE)
            required_usdt = trade_amount_to_use / TRADE_AMOUNT_SAFETY_MARGIN

            if usdt_on_buy < required_usdt:
                logger.warning(LEXICON_RU['log_trade_insufficient_usdt'].format(currency=PRIMARY_QUOTE_CURRENCY,
                                                                                exchange=buy_exchange_id,
                                                                                needed=required_usdt,
                                                                                available=usdt_on_buy))
                # Попытка скорректировать сумму сделки, если на балансе есть хоть какие-то средства.
                if usdt_on_buy > DEFAULT_NUMERIC_VALUE:
                    adjusted_trade_amount = usdt_on_buy * TRADE_AMOUNT_SAFETY_MARGIN
                    min_acceptable_amount = await self._get_min_acceptable_trade_amount(symbol, buy_exchange_id,
                                                                                        sell_exchange_id)
                    if adjusted_trade_amount >= min_acceptable_amount:
                        logger.info(
                            LEXICON_RU['log_trade_adjusting_trade_amount'].format(old_amount=trade_amount_to_use,
                                                                                  new_amount=adjusted_trade_amount))
                        adjusted_amount = adjusted_trade_amount / buy_price if buy_price else amount_to_trade
                        # Рекурсивный вызов с новой, уменьшенной суммой.
                        return await self._execute_trade(symbol, coin, buy_exchange_id, sell_exchange_id,
                                                         adjusted_amount, spread_percent, buy_price, sell_price,
                                                         adjusted_trade_amount)

                # Если коррекция невозможна, логируем ошибку и формируем отчет.
                balance_issues = {
                    buy_exchange_id: {
                        BALANCE_ISSUE_KEY_TYPE: BALANCE_ISSUE_TYPE_INSUFFICIENT_USDT,
                        BALANCE_ISSUE_KEY_CURRENCY: PRIMARY_QUOTE_CURRENCY,
                        BALANCE_ISSUE_KEY_NEEDED: required_usdt,
                        BALANCE_ISSUE_KEY_AVAILABLE: usdt_on_buy,
                        BALANCE_ISSUE_KEY_SHORTAGE: required_usdt - usdt_on_buy
                    }
                }
                await self._log_failed_attempt(symbol, coin, buy_exchange_id, sell_exchange_id, amount_to_trade,
                                               trade_amount_to_use, spread_percent,
                                               FAILURE_REASON_INSUFFICIENT_BALANCE, balance_issues, buy_price,
                                               sell_price)
                return False, self._create_balance_issue_report(symbol, balance_issues)

            # Проверка баланса монеты на бирже продажи.
            coin_on_sell = initial_sell_balances.get(coin, DEFAULT_NUMERIC_VALUE)
            required_coin = amount_to_trade / BALANCE_CHANGE_TOLERANCE_FACTOR

            if coin_on_sell < required_coin:
                logger.warning(
                    LEXICON_RU['log_trade_insufficient_coin'].format(coin=coin, exchange=sell_exchange_id,
                                                                     needed=required_coin, available=coin_on_sell))
                # Попытка скорректировать количество монеты для сделки.
                if coin_on_sell > DEFAULT_NUMERIC_VALUE:
                    adjusted_coin_amount = coin_on_sell * BALANCE_CHANGE_TOLERANCE_FACTOR
                    min_acceptable_coin = await self._get_min_acceptable_coin_amount(symbol, sell_exchange_id)
                    if adjusted_coin_amount >= min_acceptable_coin:
                        logger.info(LEXICON_RU['log_trade_adjusting_coin_amount'].format(old_amount=amount_to_trade,
                                                                                         new_amount=adjusted_coin_amount))
                        adjusted_trade_amount_from_coin = adjusted_coin_amount * (
                            sell_price if sell_price else buy_price or STABLECOIN_PRICE)
                        # Рекурсивный вызов с новым количеством.
                        return await self._execute_trade(symbol, coin, buy_exchange_id, sell_exchange_id,
                                                         adjusted_coin_amount, spread_percent, buy_price,
                                                         sell_price, adjusted_trade_amount_from_coin)

                # Если коррекция невозможна, логируем и формируем отчет.
                balance_issues = {
                    sell_exchange_id: {
                        BALANCE_ISSUE_KEY_TYPE: BALANCE_ISSUE_TYPE_INSUFFICIENT_COIN,
                        BALANCE_ISSUE_KEY_CURRENCY: coin,
                        BALANCE_ISSUE_KEY_NEEDED: required_coin,
                        BALANCE_ISSUE_KEY_AVAILABLE: coin_on_sell,
                        BALANCE_ISSUE_KEY_SHORTAGE: required_coin - coin_on_sell
                    }
                }
                await self._log_failed_attempt(symbol, coin, buy_exchange_id, sell_exchange_id, amount_to_trade,
                                               trade_amount_to_use, spread_percent,
                                               FAILURE_REASON_INSUFFICIENT_BALANCE, balance_issues, buy_price,
                                               sell_price)
                return False, self._create_balance_issue_report(symbol, balance_issues)

            # Если все проверки балансов пройдены.
            logger.info(LEXICON_RU['log_trade_balances_ok'])

            # --- ЭТАП 1: ВЫПОЛНЕНИЕ ОРДЕРОВ ---
            logger.info(LEXICON_RU['log_trade_starting_orders'])
            start_time = asyncio.get_event_loop().time()
            buy_task = buy_service.client.create_market_buy_order(symbol, amount_to_trade)
            sell_task = sell_service.client.create_market_sell_order(symbol, amount_to_trade)
            order_results = await asyncio.gather(buy_task, sell_task, return_exceptions=True)
            execution_time = asyncio.get_event_loop().time() - start_time
            buy_order_res, sell_order_res = order_results
            logger.info(LEXICON_RU['log_trade_orders_processed'].format(time=execution_time))

            # --- ЭТАП 2: ГИБРИДНЫЙ АНАЛИЗ РЕЗУЛЬТАТОВ ---
            logger.info(LEXICON_RU['log_trade_analyzing_results'])
            is_buy_success_api, buy_filled, buy_cost, buy_avg_price = self._analyze_order_result(buy_order_res,
                                                                                                 amount_to_trade,
                                                                                                 buy_exchange_id)
            is_sell_success_api, sell_filled, sell_revenue, sell_avg_price = self._analyze_order_result(
                sell_order_res, amount_to_trade, sell_exchange_id)
            final_buy_success, final_sell_success = is_buy_success_api, is_sell_success_api

            # Если API-анализ показал неполное исполнение, запускаем вторичную проверку по балансам.
            if not final_buy_success or not final_sell_success:
                logger.warning(LEXICON_RU['log_trade_api_incomplete_fill'])
                await asyncio.sleep(POST_TRADE_BALANCE_VALIDATION_DELAY_S)
                current_balances_res = await asyncio.gather(buy_service.get_balance(), sell_service.get_balance(),
                                                            return_exceptions=True)
                current_buy_balance, current_sell_balance = current_balances_res

                if not isinstance(current_buy_balance, Exception) and not isinstance(current_sell_balance,
                                                                                     Exception):
                    if not final_buy_success:
                        usdt_spent = initial_buy_balances.get(PRIMARY_QUOTE_CURRENCY,
                                                              DEFAULT_NUMERIC_VALUE) - current_buy_balance.get(
                            PRIMARY_QUOTE_CURRENCY, DEFAULT_NUMERIC_VALUE)
                        coin_gained = current_buy_balance.get(coin,
                                                              DEFAULT_NUMERIC_VALUE) - initial_buy_balances.get(
                            coin, DEFAULT_NUMERIC_VALUE)
                        if usdt_spent > (
                                trade_amount_to_use * BALANCE_VALIDATION_FILL_RATIO_THRESHOLD) and coin_gained > (
                                amount_to_trade * BALANCE_VALIDATION_FILL_RATIO_THRESHOLD):
                            logger.info(
                                LEXICON_RU['log_trade_buy_confirmed_by_balance'].format(exchange=buy_exchange_id))
                            final_buy_success, buy_filled, buy_cost, buy_avg_price = True, coin_gained, usdt_spent, (
                                usdt_spent / coin_gained if coin_gained > DEFAULT_NUMERIC_VALUE else DEFAULT_NUMERIC_VALUE)

                    if not final_sell_success:
                        usdt_gained = current_sell_balance.get(PRIMARY_QUOTE_CURRENCY,
                                                               DEFAULT_NUMERIC_VALUE) - initial_sell_balances.get(
                            PRIMARY_QUOTE_CURRENCY, DEFAULT_NUMERIC_VALUE)
                        coin_spent = initial_sell_balances.get(coin,
                                                               DEFAULT_NUMERIC_VALUE) - current_sell_balance.get(
                            coin, DEFAULT_NUMERIC_VALUE)
                        if usdt_gained > (
                                trade_amount_to_use * spread_percent / PERCENTAGE_MULTIPLIER * BALANCE_VALIDATION_FILL_RATIO_THRESHOLD) and coin_spent > (
                                amount_to_trade * BALANCE_VALIDATION_FILL_RATIO_THRESHOLD):
                            logger.info(
                                LEXICON_RU['log_trade_sell_confirmed_by_balance'].format(exchange=sell_exchange_id))
                            final_sell_success, sell_filled, sell_revenue, sell_avg_price = True, coin_spent, usdt_gained, (
                                usdt_gained / coin_spent if coin_spent > DEFAULT_NUMERIC_VALUE else DEFAULT_NUMERIC_VALUE)
                else:
                    logger.error(LEXICON_RU['log_trade_secondary_validation_failed'])

            # --- ЭТАП 3: ОПРЕДЕЛЕНИЕ СТАТУСА СДЕЛКИ ---
            technical_success = final_buy_success and final_sell_success
            arbitrage_status: ArbitrageStatus
            failure_reason: Optional[str] = None
            actual_profit = DEFAULT_NUMERIC_VALUE

            if technical_success:
                actual_profit = sell_revenue - buy_cost
                if actual_profit >= MINIMUM_MEANINGFUL_PROFIT_USD:
                    arbitrage_status = ArbitrageStatus.FULLY_SUCCESSFUL
                    logger.info(LEXICON_RU['log_trade_fully_successful'].format(profit=actual_profit))
                else:
                    arbitrage_status = ArbitrageStatus.EXECUTED_UNPROFITABLE
                    failure_reason = FAILURE_REASON_UNPROFITABLE_TRADE
                    logger.warning(LEXICON_RU['log_trade_executed_unprofitable'].format(profit=actual_profit))
            else:
                arbitrage_status = ArbitrageStatus.EXECUTION_FAILED
                failure_reason = FAILURE_REASON_EXECUTION_FAILED
                logger.error(LEXICON_RU['log_trade_execution_failed'])

            # --- ЭТАП 4: ФОРМИРОВАНИЕ ОТЧЕТА ДЛЯ ПОЛЬЗОВАТЕЛЯ ---
            report_lines = [LEXICON_RU['report_trade_final_header']]
            report_lines.extend(
                self._format_order_report_line(OPERATION_TYPE_BUY, buy_exchange_id, coin, amount_to_trade,
                                               buy_order_res, final_buy_success, buy_filled, buy_cost,
                                               buy_avg_price))
            report_lines.extend(
                self._format_order_report_line(OPERATION_TYPE_SELL, sell_exchange_id, coin, amount_to_trade,
                                               sell_order_res, final_sell_success, sell_filled, sell_revenue,
                                               sell_avg_price))

            if arbitrage_status == ArbitrageStatus.FULLY_SUCCESSFUL:
                roi_percent = (
                        actual_profit / buy_cost * PERCENTAGE_MULTIPLIER) if buy_cost > DEFAULT_NUMERIC_VALUE else DEFAULT_NUMERIC_VALUE
                report_lines.append(LEXICON_RU['report_trade_final_success'].format(profit=actual_profit,
                                                                                    precision=USD_REPORT_PRECISION,
                                                                                    roi=roi_percent))
            elif arbitrage_status == ArbitrageStatus.EXECUTED_UNPROFITABLE:
                roi_percent = (
                        actual_profit / buy_cost * PERCENTAGE_MULTIPLIER) if buy_cost > DEFAULT_NUMERIC_VALUE else DEFAULT_NUMERIC_VALUE
                report_lines.append(LEXICON_RU['report_trade_final_unprofitable'].format(loss=abs(actual_profit),
                                                                                         precision=USD_REPORT_PRECISION,
                                                                                         roi=roi_percent))
            else:  # EXECUTION_FAILED
                report_lines.append(LEXICON_RU['report_trade_final_failed'])
                imbalance = buy_filled - sell_filled
                if abs(imbalance) > FLOAT_PRECISION_TOLERANCE:
                    # (Логика отправки асинхронного уведомления о частичном исполнении остается)
                    asyncio.create_task(self.notifier.send_message(self.user_id,
                                                                   LEXICON_RU['bot_partial_fill_alert'].format(
                                                                       symbol=symbol,
                                                                       buy_exchange=buy_exchange_id.capitalize(),
                                                                       buy_filled=buy_filled, coin=coin,
                                                                       buy_cost=buy_cost,
                                                                       sell_exchange=sell_exchange_id.capitalize(),
                                                                       sell_filled=sell_filled,
                                                                       sell_revenue=sell_revenue,
                                                                       imbalance=imbalance)))

                # Добавляем диагностическую информацию.
                report_lines.append(LEXICON_RU['report_trade_failed_diagnostics_header'])
                if not final_buy_success:
                    report_lines.append(LEXICON_RU['report_trade_failed_buy_line'].format(filled=buy_filled,
                                                                                          planned=amount_to_trade))
                if not final_sell_success:
                    report_lines.append(LEXICON_RU['report_trade_failed_sell_line'].format(filled=sell_filled,
                                                                                           planned=amount_to_trade))

            report = "\n".join(report_lines)

            # --- ЭТАП 5: ЛОГИРОВАНИЕ В БД ---
            await self.report_service.log_arbitrage_attempt(
                user_id=self.user_id, symbol=symbol, coin=coin, buy_exchange=buy_exchange_id,
                sell_exchange=sell_exchange_id,
                planned_amount=amount_to_trade, trade_value_usd=trade_amount_to_use, spread_percent=spread_percent,
                status=arbitrage_status, failure_reason=failure_reason,
                buy_price=buy_avg_price if technical_success else buy_price,
                sell_price=sell_avg_price if technical_success else sell_price,
                actual_profit_usd=actual_profit if technical_success else None
            )

            return arbitrage_status == ArbitrageStatus.FULLY_SUCCESSFUL, report

        except Exception as e:
            # Обработка критических, непредвиденных ошибок.
            logger.critical(LEXICON_RU['log_trade_critical_error'].format(symbol=symbol, error=e), exc_info=True)
            await self._log_failed_attempt(symbol, coin, buy_exchange_id, sell_exchange_id, amount_to_trade,
                                           trade_amount_to_use, spread_percent, FAILURE_REASON_CRITICAL_ERROR)
            return False, LEXICON_RU['report_trade_critical_error'].format(
                error=str(e)[:ERROR_MESSAGE_TRUNCATE_LENGTH])

    async def _get_min_acceptable_trade_amount(self, symbol: str, buy_exchange_id: str,
                                               sell_exchange_id: str) -> float:
        """
        Получает минимально допустимую торговую сумму для пары на биржах.
        """
        try:
            # Получаем сервисы для обеих бирж.
            buy_service = self.services[buy_exchange_id]
            sell_service = self.services[sell_exchange_id]

            # Асинхронно запрашиваем минимальную стоимость ордера с каждой биржи.
            buy_min = await buy_service.get_reliable_min_order_value(symbol)
            sell_min = await sell_service.get_reliable_min_order_value(symbol)

            # Возвращаем максимальное из двух значений, умноженное на коэффициент безопасности.
            return max(buy_min, sell_min) * LIMIT_SAFETY_MULTIPLIER
        except Exception as e:
            # В случае ошибки логируем и возвращаем значение по умолчанию.
            logger.warning(LEXICON_RU['log_get_min_limits_error'].format(error=e))
            return DEFAULT_TRADE_AMOUNT_USD

    async def _get_min_acceptable_coin_amount(self, symbol: str, exchange_id: str) -> float:
        """
        Получает минимально допустимое количество монет для торговли на конкретной бирже.
        """
        try:
            # Получаем сервис для биржи.
            service = self.services[exchange_id]
            # Запрашиваем детали рынка.
            market_details = await service.get_market_details(symbol)

            # Если детали получены, извлекаем из них минимальное количество.
            if market_details:
                return market_details.get(MARKET_FIELD_LIMITS_AMOUNT_MIN, DEFAULT_NUMERIC_VALUE)
            # Если нет, возвращаем ноль.
            return DEFAULT_NUMERIC_VALUE
        except Exception as e:
            # В случае ошибки логируем и возвращаем ноль.
            logger.warning(LEXICON_RU['log_get_min_coin_error'].format(error=e))
            return DEFAULT_NUMERIC_VALUE

    async def _log_failed_attempt(self, symbol: str, coin: str, buy_exchange_id: str, sell_exchange_id: str,
                                  amount_to_trade: float, trade_value_usd: float, spread_percent: float,
                                  failure_reason: str, balance_issues: Dict = None,
                                  buy_price: float = None, sell_price: float = None):
        """
        Вспомогательный метод для логирования неудачных попыток арбитража в базу данных.
        """
        # Устанавливаем статус попытки как неудачный.
        status = ArbitrageStatus.EXECUTION_FAILED

        # Вызываем сервис для записи данных в базу.
        await self.report_service.log_arbitrage_attempt(
            user_id=self.user_id, symbol=symbol, coin=coin,
            buy_exchange=buy_exchange_id, sell_exchange=sell_exchange_id,
            planned_amount=amount_to_trade,
            trade_value_usd=trade_value_usd,
            spread_percent=spread_percent,
            status=status,
            failure_reason=failure_reason,
            balance_issues=balance_issues,
            buy_price=buy_price,
            sell_price=sell_price
        )

    def _create_balance_issue_report(self, symbol: str, issues: Dict) -> str:
        """
        Создает HTML-отчет для пользователя на основе информации о проблемах с балансом.
        """
        # Начинаем отчет с заголовка из лексикона.
        report_lines = [LEXICON_RU['report_balance_issue_header'].format(symbol=symbol)]
        # Проходим по всем проблемам в словаре.
        for exchange, details in issues.items():
            # Извлекаем детали проблемы.
            currency = details.get(BALANCE_ISSUE_KEY_CURRENCY, '')
            needed = details.get(BALANCE_ISSUE_KEY_NEEDED, DEFAULT_NUMERIC_VALUE)
            available = details.get(BALANCE_ISSUE_KEY_AVAILABLE, DEFAULT_NUMERIC_VALUE)

            # Формируем отчет в зависимости от типа проблемы.
            if details.get(BALANCE_ISSUE_KEY_TYPE) == BALANCE_ISSUE_TYPE_INSUFFICIENT_USDT:
                report_lines.append(LEXICON_RU['report_balance_issue_usdt_reason'].format(currency=currency,
                                                                                          exchange=exchange.capitalize()))
                report_lines.append(
                    LEXICON_RU['report_balance_issue_usdt_details'].format(needed=needed, available=available))
            elif details.get(BALANCE_ISSUE_KEY_TYPE) == BALANCE_ISSUE_TYPE_INSUFFICIENT_COIN:
                report_lines.append(LEXICON_RU['report_balance_issue_coin_reason'].format(currency=currency,
                                                                                          exchange=exchange.capitalize()))
                report_lines.append(
                    LEXICON_RU['report_balance_issue_coin_details'].format(needed=needed, available=available))

        # Объединяем строки в одно сообщение.
        return "\n".join(report_lines)

    def _analyze_order_result(self, order_res: Any, amount_to_trade: float, exchange_id: str) -> Tuple[
        bool, float, float, float]:
        """
        Анализирует результат выполнения ордера, полученный от ccxt.
        Включает специальную логику для биржи Bybit.
        """
        # Если пришел Exception или пустой ответ, считаем ордер полностью проваленным.
        if isinstance(order_res, Exception) or not order_res:
            return False, DEFAULT_NUMERIC_VALUE, DEFAULT_NUMERIC_VALUE, DEFAULT_NUMERIC_VALUE

        # Шаг 1: Пытаемся получить стандартные поля ccxt, используя константы.
        filled = safe_get_numeric(order_res, CCXT_ORDER_FIELD_FILLED, DEFAULT_NUMERIC_VALUE)
        cost = safe_get_numeric(order_res, CCXT_ORDER_FIELD_COST, DEFAULT_NUMERIC_VALUE)
        average = safe_get_numeric(order_res, CCXT_ORDER_FIELD_AVERAGE, DEFAULT_NUMERIC_VALUE)

        # Шаг 2: Специальная обработка для Bybit, если стандартные поля пусты.
        if exchange_id == EXCHANGE_BYBIT:
            info = order_res.get(CCXT_ORDER_FIELD_INFO, {})
            if isinstance(info, dict):
                # Bybit v5 API возвращает исполненное количество в 'cumExecQty'
                if filled == DEFAULT_NUMERIC_VALUE:
                    filled = safe_get_numeric(info, BYBIT_ORDER_INFO_FIELD_CUM_EXEC_QTY, DEFAULT_NUMERIC_VALUE)
                # Исполненная стоимость в 'cumExecValue'
                if cost == DEFAULT_NUMERIC_VALUE:
                    cost = safe_get_numeric(info, BYBIT_ORDER_INFO_FIELD_CUM_EXEC_VALUE, DEFAULT_NUMERIC_VALUE)

        # Шаг 3: Восстанавливаем недостающие значения, если это возможно.
        if filled > DEFAULT_NUMERIC_VALUE:
            if cost > DEFAULT_NUMERIC_VALUE and average == DEFAULT_NUMERIC_VALUE:
                average = cost / filled
            elif average > DEFAULT_NUMERIC_VALUE and cost == DEFAULT_NUMERIC_VALUE:
                cost = filled * average

        # Шаг 4: Проверяем успешность исполнения по порогу из константы.
        if amount_to_trade > DEFAULT_NUMERIC_VALUE:
            fill_ratio = filled / amount_to_trade
            if fill_ratio >= ORDER_FILL_SUCCESS_THRESHOLD:
                return True, filled, cost, average

        # Если ни одно из условий не выполнено, возвращаем неудачу.
        return False, filled, cost, average

    def _format_order_report_line(self, op_type: str, exchange: str, coin: str, amount_to_trade: float,
                                  order_res: Any, success: bool, filled: float, cost: float, avg_price: float) -> \
            List[str]:
        """
        Форматирует одну строку отчета о выполнении ордера для пользователя, используя шаблоны из лексикона.
        """
        lines = []
        if success:
            # Если ордер исполнен успешно.
            fill_percent = (
                    filled / amount_to_trade * PERCENTAGE_MULTIPLIER) if amount_to_trade > DEFAULT_NUMERIC_VALUE else DEFAULT_NUMERIC_VALUE
            lines.append(
                LEXICON_RU['report_order_line_success'].format(op_type=op_type, exchange=exchange.capitalize(),
                                                               filled=filled, coin=coin, cost=cost,
                                                               fill_percent=fill_percent))
            if avg_price > DEFAULT_NUMERIC_VALUE:
                lines.append(LEXICON_RU['report_order_line_avg_price'].format(avg_price=avg_price))
        else:
            # Если ордер не исполнен или исполнен частично.
            if isinstance(order_res, Exception):
                # Если произошла ошибка API.
                lines.append(LEXICON_RU['report_order_line_api_error'].format(op_type=op_type,
                                                                              exchange=exchange.capitalize()))
                error_details = str(order_res)[:ERROR_MESSAGE_TRUNCATE_LENGTH]
                lines.append(LEXICON_RU['report_order_line_api_error_details'].format(error=error_details))
            else:
                # Если исполнение просто не удалось (например, не хватило ликвидности).
                fill_percent = (
                        filled / amount_to_trade * PERCENTAGE_MULTIPLIER) if amount_to_trade > DEFAULT_NUMERIC_VALUE else DEFAULT_NUMERIC_VALUE
                lines.append(
                    LEXICON_RU['report_order_line_failed'].format(op_type=op_type, exchange=exchange.capitalize()))
                lines.append(
                    LEXICON_RU['report_order_line_failed_details'].format(filled=filled, planned=amount_to_trade,
                                                                          fill_percent=fill_percent))
        return lines

    async def _report_progress(self, message: str):
        if self.progress_callback:
            try:
                await self.progress_callback(message)
            except Exception as e:
                logger.warning(f"Ошибка в progress_callback: {e}")


async def run_optimized_arbitrage_scan():
    """
    ИСПРАВЛЕННАЯ ВЕРСИЯ: Корректная синхронизация с инициализацией приложения
    и улучшенная обработка ошибок.
    """
    # Блокировка для предотвращения одновременного запуска нескольких циклов
    scan_lock = asyncio.Lock()

    async with scan_lock:
        try:
            # ======================= КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ =======================
            # Ждем, пока приложение полностью не инициализируется
            # Если инициализация провалилась, событие никогда не будет установлено,
            # и эта строка будет ждать бесконечно (что правильно - не даем запускаться
            # арбитражным задачам с нерабочими сервисами)
            logger.debug("Ожидание завершения инициализации приложения...")
            await app_state.is_ready_event.wait()
            logger.debug("✅ Инициализация завершена, продолжаем выполнение...")
            # =====================================================================

            # Дополнительная проверка на случай, если что-то пошло не так
            if not app_state.balance_service:
                logger.warning("BalanceService не инициализирован после ожидания. Цикл сканирования пропущен.")
                return

            if not config.tg_bot.admin_ids:
                logger.warning("В конфигурации не указаны ADMIN_IDS. Цикл сканирования пропущен.")
                return

            # Используем первого админа как "владельца" настроек.
            user_id = config.tg_bot.admin_ids[0]

            # Heartbeat будет отправлен всем администраторам.
            await send_heartbeat_if_needed()

            logger.info("🔍 --- [Начало умного цикла сканирования] ---")

            # Эта проверка теперь будет выполняться ПОСЛЕ полной инициализации и будет корректной.
            if not service_manager.is_ready_for_arbitrage:
                logger.warning("ServiceManager не готов к арбитражу, пропуск цикла.")
                return

            trade_amount, profit_threshold = await get_user_settings(user_id)

            async with async_session_factory() as session:
                stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == user_id)
                tracked_coins = (await session.execute(stmt)).scalars().all()

            if not tracked_coins:
                logger.info("У пользователя нет отслеживаемых монет. Пропуск цикла.")
                return

            pre_flight_check = await app_state.balance_service.perform_pre_flight_check(trade_amount, tracked_coins)

            if pre_flight_check['warning_message']:
                # Предупреждение будет отправлено всем.
                await app_state.balance_service.send_warning_with_antispam(pre_flight_check['warning_message'])

            if not pre_flight_check['can_trade']:
                logger.warning(
                    f"Торговля невозможна по результатам pre-flight проверки (нет 'покупателей' или < {MIN_EXCHANGES_FOR_ARBITRAGE} бирж).")
                return

            coins_to_scan = pre_flight_check['sell_capability_info']['sellable_coins_list']
            if not coins_to_scan:
                logger.warning("Нет доступных монет для продажи после pre-flight проверки. Пропуск цикла.")
                return

            logger.info(f"Будут сканироваться монеты, доступные для продажи: {coins_to_scan}")

            all_healthy_services = await service_manager.get_healthy_services()

            if len(all_healthy_services) < MIN_EXCHANGES_FOR_ARBITRAGE:
                logger.warning(
                    f"Недостаточно здоровых сервисов для арбитража ({len(all_healthy_services)}/{MIN_EXCHANGES_FOR_ARBITRAGE}).")
                return

            strategy = ArbitrageStrategy(
                user_id=user_id,
                validated_services=all_healthy_services,
                trade_amount=trade_amount,
                profit_threshold=profit_threshold,
                initial_balances=pre_flight_check['balances'],
                buy_capable_exchanges=pre_flight_check['buy_capable_exchanges'],
                notifier=app_state.notifier_service,
                report_service=app_state.report_service,
                tracked_coins_to_scan=coins_to_scan
            )

            trade_executed = await strategy.find_and_execute_opportunity()

            if trade_executed:
                logger.info("🎯 Цикл завершен: выполнена арбитражная сделка")
            else:
                logger.info("📝 Цикл завершен: подходящих возможностей не найдено")

        except Exception as e:
            logger.critical(f"💥 Критическая ошибка в цикле сканирования: {e}", exc_info=True)


async def send_heartbeat_if_needed():
    """
    Редактирует или отправляет heartbeat-сообщение,
    обрабатывая все пограничные случаи.
    """
    key_ts = 'last_heartbeat_timestamp'
    # АРГУМЕНТАЦИЯ: Заменяем на timezone-aware аналог для консистентности
    # и соответствия современным стандартам.
    now = datetime.datetime.now(datetime.timezone.utc)

    async with async_session_factory() as session:
        stmt_get_ts = select(SystemState.value).where(SystemState.key == key_ts)
        last_ts_str = (await session.execute(stmt_get_ts)).scalar_one_or_none()

        if last_ts_str:
            # При сравнении оба объекта теперь будут timezone-aware, что надежнее.
            last_ts = datetime.datetime.fromisoformat(last_ts_str)
            if (now - last_ts).total_seconds() < HEARTBEAT_INTERVAL_MINUTES * 60:
                return

        logger.info(f"💓 Отправка/обновление heartbeat для администраторов: {config.tg_bot.admin_ids}")

        is_running = await get_scanner_state_from_db() == SCANNER_STATUS_RUNNING
        is_running_str = SCANNER_STATUS_RUNNING if is_running else SCANNER_STATUS_STOPPED

        message_text = LEXICON_RU['heartbeat_message_text']
        keyboard = get_scanner_menu_keyboard(is_running=is_running)

        for admin_id in config.tg_bot.admin_ids:
            message_id_key = SYSTEM_STATE_HEARTBEAT_MESSAGE_ID.format(admin_id=admin_id)
            # КЛЮЧ для хранения последнего отправленного статуса
            status_key = f'heartbeat_status_{admin_id}'

            # Получаем ID сообщения и его последний известный статус
            stmt_get_msg_id = select(SystemState.value).where(SystemState.key == message_id_key)
            stmt_get_status = select(SystemState.value).where(SystemState.key == status_key)

            saved_message_id_str = (await session.execute(stmt_get_msg_id)).scalar_one_or_none()
            saved_status = (await session.execute(stmt_get_status)).scalar_one_or_none()

            # Если у нас есть ID сообщения и его статус не изменился, пропускаем этого админа
            if saved_message_id_str and saved_status == is_running_str:
                logger.debug(f"Heartbeat для админа {admin_id} пропущен: статус не изменился.")
                continue

            new_message_id = None

            if saved_message_id_str:
                try:
                    message_id_to_edit = int(saved_message_id_str)
                    # Вызываем edit_message только если статус изменился
                    await app_state.notifier_service.edit_message(
                        chat_id=admin_id,
                        message_id=message_id_to_edit,
                        text=message_text,
                        reply_markup=keyboard
                    )
                    new_message_id = message_id_to_edit
                except Exception as e:
                    logger.error(f"Ошибка при редактировании сообщения {saved_message_id_str}: {e}")
                    # Если редактирование не удалось, сбрасываем ID, чтобы отправить новое сообщение
                    saved_message_id_str = None

            if not saved_message_id_str:
                response = await app_state.notifier_service.send_message(
                    admin_id, message_text, reply_markup=keyboard
                )
                if response and response.get("ok"):
                    new_message_id = response.get("result", {}).get("message_id")

            if new_message_id:
                # Сохраняем и ID сообщения, и его текущий статус
                stmt_set_msg_id = insert(SystemState).values(key=message_id_key, value=str(new_message_id))
                stmt_set_status = insert(SystemState).values(key=status_key, value=is_running_str)

                stmt_set_msg_id = stmt_set_msg_id.on_conflict_do_update(
                    index_elements=['key'], set_={'value': stmt_set_msg_id.excluded.value}
                )
                stmt_set_status = stmt_set_status.on_conflict_do_update(
                    index_elements=['key'], set_={'value': stmt_set_status.excluded.value}
                )
                await session.execute(stmt_set_msg_id)
                await session.execute(stmt_set_status)

                # Обновление временной метки остается без изменений
            stmt_set_ts = insert(SystemState).values(key=key_ts, value=now.isoformat())
            stmt_set_ts = stmt_set_ts.on_conflict_do_update(
                index_elements=['key'], set_={'value': stmt_set_ts.excluded.value}
            )
            await session.execute(stmt_set_ts)
            await session.commit()
