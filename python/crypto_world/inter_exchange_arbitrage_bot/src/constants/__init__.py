# inter_exchange_arbitrage_bot/src/constants/__init__.py
"""
Единая точка входа для всех констант приложения.
Это позволяет импортировать любую константу напрямую из `src.constants`,
не задумываясь о том, в каком именно файле она определена.
"""

# Импортируем все константы из соответствующих модулей.
# Звездочка (*) здесь оправдана, так как мы явно контролируем
# публичный API через __all__ ниже.
from .api_constants import *
from .rate_limiting_constants import *
from .system_constants import *
from .telegram_constants import *
from .trading_constants import *

# __all__ определяет публичный API пакета 'constants'.
__all__ = [
    # === Из api_constants.py ===
    # --- Базовые настройки API ---
    'API_BASE_URL',
    'DEFAULT_API_TIMEOUT',
    'SCANNER_OPERATION_TIMEOUT',
    'STATUS_CHECK_TIMEOUT',
    'GET_BALANCE_TIMEOUT_SECONDS',
    'GET_ALL_ASSETS_TIMEOUT_SECONDS',
    'SERVICE_HEALTH_CHECK_TIMEOUT_SECONDS',
    'SERVICE_INITIALIZATION_TIMEOUT_SECONDS',

    # --- Retry и временные параметры ---
    'RETRY_INTERVALS',
    'MAX_RETRIES',
    'HEALTH_CHECK_INTERVAL_SECONDS',
    'HEARTBEAT_INTERVAL_MINUTES',
    'ARBITRAGE_SCAN_INTERVAL_SECONDS',
    'INSUFFICIENT_FUNDS_WARNING_INTERVAL_MINUTES',

    # --- HTTP коды и статусы ---
    'API_SUCCESS_CODES',
    'API_CLIENT_ERROR_CODES',
    'API_SERVER_ERROR_CODES',

    # --- Заголовки HTTP ---
    'HEADER_INTERNAL_API_KEY',

    # --- Эндпоинты API ---
    'API_PREFIX_SCANNER',
    'API_PREFIX_ADMIN',
    'API_ENDPOINT_SCANNER_STATUS',
    'API_ENDPOINT_SCANNER_START',
    'API_ENDPOINT_SCANNER_STOP',
    'API_ENDPOINT_SCANNER_STATUS_DETAILED',
    'API_ENDPOINT_ADMIN_CACHE_STATS',
    'API_ENDPOINT_ADMIN_EXCLUDE_PAIR',
    'API_ENDPOINT_ADMIN_INCLUDE_PAIR',
    'API_ENDPOINT_ADMIN_EXCLUDED_PAIRS',

    # --- Ключи полей в JSON ответах ---
    'API_KEY_STATUS',
    'API_KEY_EXCLUDED_PAIRS',
    'API_KEY_EXCHANGE',
    'API_KEY_SYMBOL',

    # --- Значения статусов в JSON ответах ---
    'API_STATUS_VALUE_RUNNING',
    'API_STATUS_VALUE_STOPPED',
    'API_STATUS_VALUE_SUCCESS',

    # === Из rate_limiting_constants.py ===
    'EXCHANGE_RATE_LIMITS',
    'DEFAULT_RATE_LIMIT_CONFIG',
    'RATE_LIMIT_ERROR_CODES',
    'RATE_LIMIT_RETRY_CONFIG',

    # === Из system_constants.py ===
    'SYSTEM_STATE_SCANNER_STATUS',
    'SCANNER_STATUS_RUNNING',
    'SCANNER_STATUS_STOPPED',

    # === Из telegram_constants.py ===
    # --- Базовые параметры ---
    'TYPING_INDICATOR_INTERVAL',
    'TELEGRAM_MESSAGE_MAX_LENGTH',
    'DEFAULT_NOTIFICATION_TIMEOUT_SECONDS',
    'HTTP_OK_STATUS',

    # --- Callback префиксы ---
    'CALLBACK_GET_REPORT',
    'CALLBACK_SHOW_FULL_LIST',
    'CALLBACK_PAGE_SWITCH',

    # --- Настройки отчетов ---
    'ALLOWED_REPORT_HOURS',
    'DEFAULT_REPORT_PERIOD_HOURS',

    # --- Форматирование ---
    'REPORT_SECTION_SEPARATOR_CHAR',
    'REPORT_SECTION_SEPARATOR_LENGTH',
    'REPORT_DATE_FORMAT',

    # --- Функции ---
    'get_telegram_api_url',

    # === Из trading_constants.py ===
    # --- Названия бирж ---
    'EXCHANGE_BYBIT',
    'EXCHANGE_YOBIT',
    'EXCHANGE_BINANCE',
    'EXCHANGE_OKX',
    'EXCHANGE_KUCOIN',

    # --- Основные валюты и символы ---
    'PRIMARY_QUOTE_CURRENCY',
    'DEFAULT_FALLBACK_SYMBOL',
    'STABLE_COINS',

    # --- Базовые торговые параметры ---
    'DEFAULT_PROFIT_THRESHOLD',
    'DEFAULT_TRADE_AMOUNT_USD',
    'ARBITRAGE_EXECUTION_MODE',

    # --- Лимиты и минимальные значения ---
    'EXCHANGE_MIN_ORDER_VALUES',
    'MIN_PROFIT_THRESHOLD_PERCENT',
    'MAX_PROFIT_THRESHOLD_PERCENT',
    'MINIMUM_VALUE_THRESHOLD',
    'MINIMUM_QUANTITY_THRESHOLD',
    'MIN_EXCHANGES_FOR_ARBITRAGE',

    # --- Параметры безопасности ---
    'LIMIT_SAFETY_MULTIPLIER',
    'TRADE_AMOUNT_SAFETY_MARGIN',
    'MIN_BALANCE_CHECK_RATIO',
    'MIN_SELL_TO_BUY_FILL_RATIO',
    'ORDER_FILL_SUCCESS_THRESHOLD',
    'BALANCE_CHANGE_TOLERANCE_FACTOR',
    'BALANCE_SAFETY_BUFFER',

    # --- Пороги предупреждений ---
    'LOW_BALANCE_WARNING_THRESHOLD',
    'CRITICAL_BALANCE_THRESHOLD',

    # --- Временные параметры ---
    'MAX_ARBITRAGE_EXECUTION_TIME',
    'SELL_ORDER_RETRY_INTERVALS_S',
    'API_RETRY_DELAY',
    'BALANCE_FETCH_TIMEOUT_SECONDS',
    'POST_TRADE_BALANCE_VALIDATION_DELAY_S',

    # --- Точность расчетов ---
    'FLOAT_COMPARISON_EPSILON',
    'FLOAT_PRECISION_TOLERANCE',
    'DEFAULT_PRECISION_AMOUNT',

    # --- Параметры исполнения ---
    'MIN_ORDER_FILL_RATIO',
    'MAX_VOLUME_DIFFERENCE_PERCENT',
    'BALANCE_VALIDATION_FILL_RATIO_THRESHOLD',

    # --- Комиссии по умолчанию ---
    'DEFAULT_EXCHANGE_FEES',

    # --- Динамические лимиты ---
    'DYNAMIC_LIMITS_CONFIG',
    'DEFAULT_DYNAMIC_LIMITS_CONFIG',
    'MARKET_DETAILS_TIMEOUT',
    'MAX_MARKET_DETAILS_RETRIES',
    'MIN_API_LIMIT_THRESHOLD',
    'MIN_API_LIMIT_THRESHOLD_YOBIT',
    'MAX_API_LIMIT_VALIDATION_THRESHOLD',
    'YOBIT_SAFE_MINIMUM_LIMIT_USD',

    # --- Критические ошибки ---
    'CRITICAL_API_ERROR_CODES',

    # --- Оценка возможностей ---
    'OPPORTUNITY_SCORE_SPREAD_WEIGHT',
    'OPPORTUNITY_SCORE_LIQUIDITY_WEIGHT',
    'LIQUIDITY_NORMALIZATION_FACTOR',
    'SLIPPAGE_PENALTY_FACTOR',
    'LIQUIDITY_AVERAGING_DIVISOR',
    'INVALID_SPREAD_VALUE',

    # --- Анализ стакана ордеров ---
    'ORDER_BOOK_DEPTH',
    'ORDERBOOK_EMPTY_SLIPPAGE_PERCENT',
    'ORDER_BOOK_ANALYSIS_PRECISION_USD',

    # --- Отчеты и форматирование ---
    'TRADE_REPORT_PRECISION',
    'PRICE_REPORT_PRECISION',
    'USD_REPORT_PRECISION',
    'ERROR_MESSAGE_TRUNCATE_LENGTH',
    'OPERATION_TYPE_BUY',
    'OPERATION_TYPE_SELL',

    # --- Управление торговыми парами ---
    'DYNAMIC_PAIRS_CONFIG',
    'GLOBAL_INVALID_PAIRS',
    'TRADING_PAIR_PATTERN',
    'PAIR_UNAVAILABLE_REASON_NOT_IN_LIST',
    'PAIR_UNAVAILABLE_REASON_NOT_FOUND',
    'PAIR_UNAVAILABLE_REASON_INACTIVE',
    'PAIR_UNAVAILABLE_REASON_API_ERROR',
    'CRITICAL_UNAVAILABLE_PAIRS_RATIO',
    'CRITICAL_ACTIVE_PAIRS_THRESHOLD',
    'ADMIN_EXCLUSION_REASON_MANUAL',

    # --- Значения по умолчанию ---
    'DEFAULT_NUMERIC_VALUE',
    'PERCENTAGE_MULTIPLIER',
    'MINIMUM_MEANINGFUL_PROFIT_USD',
    'STABLECOIN_PRICE',

    # --- Ключи полей API ---
    'MARKET_FIELD_LIMITS',
    'MARKET_FIELD_PRECISION',
    'MARKET_FIELD_BASE',
    'MARKET_FIELD_ACTIVE',
    'MARKET_FIELD_SPOT',
    'MARKET_FIELD_QUOTE',
    'MARKET_FIELD_MARKETS',
    'MARKET_FIELD_LIMITS_AMOUNT_MIN',
    'MARKET_PRECISION_AMOUNT',

    # --- Ключи стакана ордеров ---
    'ORDER_BOOK_ASKS',
    'ORDER_BOOK_BIDS',

    # --- Ключи комиссий ---
    'FEES_TRADING',
    'FEES_MAKER',
    'FEES_TAKER',

    # --- Ключи CCXT ордеров ---
    'CCXT_ORDER_FIELD_FILLED',
    'CCXT_ORDER_FIELD_COST',
    'CCXT_ORDER_FIELD_AVERAGE',
    'CCXT_ORDER_FIELD_INFO',

    # --- Bybit специфичные ---
    'BYBIT_ORDER_INFO_FIELD_CUM_EXEC_QTY',
    'BYBIT_ORDER_INFO_FIELD_CUM_EXEC_VALUE',
    'BYBIT_DEFAULT_TYPE_SPOT',
    'BYBIT_RECV_WINDOW_MS',

    # --- Режимы работы ---
    'SANDBOX_MODE_ENABLED',

    # --- Причины сбоев ---
    'FAILURE_REASON_INSUFFICIENT_BALANCE',
    'FAILURE_REASON_EXECUTION_FAILED',
    'FAILURE_REASON_UNPROFITABLE_TRADE',
    'FAILURE_REASON_CRITICAL_ERROR',

    # --- Типы проблем с балансом ---
    'BALANCE_ISSUE_TYPE_INSUFFICIENT_USDT',
    'BALANCE_ISSUE_TYPE_INSUFFICIENT_COIN',
    'BALANCE_ISSUE_KEY_TYPE',
    'BALANCE_ISSUE_KEY_CURRENCY',
    'BALANCE_ISSUE_KEY_NEEDED',
    'BALANCE_ISSUE_KEY_AVAILABLE',
    'BALANCE_ISSUE_KEY_SHORTAGE',
]