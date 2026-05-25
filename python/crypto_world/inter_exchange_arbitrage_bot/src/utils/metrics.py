# inter_exchange_arbitrage_bot/src/utils/metrics.py

from prometheus_client import Counter, Gauge, Histogram

# Счетчик ошибок API для каждой биржи
API_ERRORS_TOTAL = Counter(
    "api_errors_total",
    "Total count of API errors per exchange and error type",
    ["exchange_id", "error_type"]
)

# Gauge для времени выполнения разведки
RECON_DURATION_SECONDS = Gauge(
    "reconnaissance_duration_seconds",
    "Duration of the last reconnaissance scan in seconds"
)

# Histogram для отслеживания распределения спредов
ARBITRAGE_SPREAD_PERCENT = Histogram(
    "arbitrage_spread_percent",
    "Distribution of found arbitrage spreads in percent",
    buckets=(0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 5.0)
)