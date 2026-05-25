# inter_exchange_arbitrage_bot/src/constants/api_constants.py

import os

# =================================================================
# =============== 🌐 Базовые настройки API 🌐 ===================
# =================================================================

# Базовый URL для API, берется из .env файла для гибкости
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Таймауты для HTTP-запросов (в секундах)
DEFAULT_API_TIMEOUT = 10.0          # Стандартный таймаут
SCANNER_OPERATION_TIMEOUT = 15.0    # Увеличенный таймаут для долгих операций (запуск/остановка)
STATUS_CHECK_TIMEOUT = 5.0          # Короткий таймаут для быстрых проверок

# Таймаут для "тяжелых" запросов, таких как получение баланса со всех бирж.
# Bybit и другие биржи иногда могут отвечать медленно.
GET_BALANCE_TIMEOUT_SECONDS = 20.0

# Таймаут для "тяжелых" запросов, таких как ПОЛУЧЕНИЕ ВСЕХ МОНЕТ с биржи для меню в боте.
GET_ALL_ASSETS_TIMEOUT_SECONDS = 25.0

# Таймаут для проверки "здоровья" соединения с биржей.
# Должен быть достаточно большим, чтобы обработать медленный ответ от testnet,
# но не слишком большим, чтобы быстро отсеять "упавшие" биржи.
SERVICE_HEALTH_CHECK_TIMEOUT_SECONDS = 15.0

# Время жизни кэша рынков в ServiceManager (в секундах)
MARKETS_CACHE_TTL_SECONDS = 300  # 5 минут

# Максимальный таймаут для полного цикла "Разведки" (сбор активов, стаканов, анализ).
# 600 секунд = 20 минут.
RECONNAISSANCE_TIMEOUT_SECONDS = 1200.0

# Таймаут для первоначальной инициализации и теста соединения с биржей (в секундах).
SERVICE_INITIALIZATION_TIMEOUT_SECONDS = 10.0

# =================================================================
# =============== 🔄 Retry и временные параметры 🔄 ===============
# =================================================================

# Настройки повторных попыток (для будущей реализации)
RETRY_INTERVALS = [1, 2, 3]         # Интервалы между попытками в секундах
MAX_RETRIES = 3

# Интервал для периодической проверки "здоровья" всех сервисов (в секундах).
# 300 секунд = 10 минут.
HEALTH_CHECK_INTERVAL_SECONDS = 600

# Интервал для отправки "heartbeat" сообщений ботом (в минутах)
HEARTBEAT_INTERVAL_MINUTES = 60

# Интервал основного цикла сканирования арбитража (в секундах)
ARBITRAGE_SCAN_INTERVAL_SECONDS = 60

# Период "тишины" после отправки уведомления о нехватке средств (в минутах)
INSUFFICIENT_FUNDS_WARNING_INTERVAL_MINUTES = 60

# =================================================================
# =============== 📊 HTTP коды и статусы 📊 ====================
# =================================================================

# Коды ответов API (полезно для проверок)
API_SUCCESS_CODES = [200, 201, 202]
API_CLIENT_ERROR_CODES = range(400, 500)
API_SERVER_ERROR_CODES = range(500, 600)

# =================================================================
# =============== 🔑 Заголовки HTTP 🔑 =========================
# =================================================================

# Название заголовка для внутреннего API ключа
HEADER_INTERNAL_API_KEY = "X-API-KEY"

# =================================================================
# =============== 🛣️ Эндпоинты API 🛣️ ===========================
# =================================================================

# Общие префиксы
API_PREFIX_SCANNER = "/scanner"     # Общий префикс для всех эндпоинтов сканера
API_PREFIX_ADMIN = "/admin"         # Общий префикс для административных эндпоинтов
API_PREFIX_NEWS = "/news"

# --- Теги для группировки в OpenAPI (Swagger) ---
API_TAG_SCANNER = "Scanner"
API_TAG_SYSTEM = "System"
API_TAG_ADMIN = "Admin"
API_TAG_BOT_FACING = "Bot Facing"
API_TAG_NEWS = "News"

# --- Идентификаторы фоновых задач ---
SCHEDULER_JOB_ID_ARBITRAGE = "arbitrage_job"

# Эндпоинты сканера
API_ENDPOINT_SCANNER_STATUS = f"{API_PREFIX_SCANNER}/status"
API_ENDPOINT_SCANNER_START = f"{API_PREFIX_SCANNER}/start"
API_ENDPOINT_SCANNER_STOP = f"{API_PREFIX_SCANNER}/stop"
API_ENDPOINT_SCANNER_STATUS_DETAILED = f"{API_PREFIX_SCANNER}/status/detailed"

# Эндпоинты администратора
API_ENDPOINT_ADMIN_CACHE_STATS = f"{API_PREFIX_ADMIN}/cache-stats"
API_ENDPOINT_ADMIN_EXCLUDE_PAIR = f"{API_PREFIX_ADMIN}/exclude-pair"
API_ENDPOINT_ADMIN_INCLUDE_PAIR = f"{API_PREFIX_ADMIN}/include-pair"
API_ENDPOINT_ADMIN_EXCLUDED_PAIRS = f"{API_PREFIX_ADMIN}/excluded-pairs"

# =================================================================
# =============== 🏷️ Ключи полей в JSON ответах 🏷️ ================
# =================================================================

# Ключи для статусов и данных
API_KEY_STATUS = "status"                   # Ключ для статуса в JSON-ответах
API_KEY_EXCLUDED_PAIRS = "excluded_pairs"   # Ключ для списка исключенных пар в JSON-ответах
# Ключ в ответе /health, указывающий на полную готовность к арбитражу.
API_KEY_READY_FOR_ARBITRAGE = "ready_for_arbitrage"

# --- Ключи для ответов API, предназначенных для бота ---
API_KEY_MESSAGE = "message"
API_KEY_SERVICES_READY = "services_ready"
API_KEY_HEALTHY_SERVICES = "healthy_services"
API_KEY_TOTAL_SERVICES = "total_services"
API_KEY_SERVICE_DETAILS = "service_details"
API_KEY_HUMAN_REPORT = "human_readable_report"
API_KEY_ASSETS = "assets"
API_KEY_SOURCES = "sources"
API_KEY_REPORT_TEXT = "report_text"
API_KEY_MODE = "mode"
API_KEY_TOTAL_COUNT = "total_count"
API_KEY_SERVICES_INITIALIZED = "services_initialized"
API_KEY_CACHES_INITIALIZED = "caches_initialized"

# Ключи для запросов
API_KEY_EXCHANGE = "exchange"               # Ключ для названия биржи в JSON-запросах
API_KEY_SYMBOL = "symbol"                   # Ключ для символа торговой пары в JSON-запросах

API_KEY_HUMAN_STATUS = "human_readable_status"


# =================================================================
# =============== 📋 Значения статусов в JSON ответах 📋 ==========
# =================================================================

API_STATUS_VALUE_RUNNING = "running"       # Значение для статуса "запущен"
API_STATUS_VALUE_STOPPED = "stopped"       # Значение для статуса "остановлен"
API_STATUS_VALUE_SUCCESS = "success"       # Значение для общего успешного статуса
# --- Статусы для health_check ---
HEALTH_STATUS_HEALTHY = "healthy"          # Система полностью в рабочем состоянии.
HEALTH_STATUS_DEGRADED = "degraded"        # Система работает, но есть проблемы (например, одна из бирж недоступна).
HEALTH_STATUS_INITIALIZING = "initializing" # Система в процессе запуска.

SERVICE_STATUS_HEALTHY = "healthy"         # Отдельный сервис (биржа) работает нормально.
SERVICE_STATUS_UNHEALTHY = "unhealthy"     # Отдельный сервис недоступен.

# --- Режимы отображения баланса ---
BALANCE_MODE_TRACKED = "tracked"
BALANCE_MODE_ALL = "all"

# =================================================================
# =============== 🚦 Graceful Startup & Health Check 🚦 ================
# =================================================================

# Настройки для механизма ожидания готовности API при запуске бота.
HEALTH_CHECK_RETRY_COUNT = 20         # Количество попыток проверки, прежде чем сдаться.
HEALTH_CHECK_RETRY_DELAY_SECONDS = 3  # Пауза в секундах между попытками проверки.

# Длительность хранения в кэше успешного статуса "API готово" (в секундах).
# Помогает избежать лишних запросов к /health при частых действиях пользователя.
HEALTH_CHECK_CACHE_DURATION_SECONDS = 5

# Дополнительный буфер времени к общему таймауту на непредвиденные задержки.
HEALTH_CHECK_TIMEOUT_BUFFER_SECONDS = 5

# Общий таймаут на весь процесс ожидания готовности API.
# Вычисляется автоматически на основе количества попыток и задержки.
TOTAL_STARTUP_TIMEOUT_SECONDS = (HEALTH_CHECK_RETRY_COUNT * HEALTH_CHECK_RETRY_DELAY_SECONDS) + HEALTH_CHECK_TIMEOUT_BUFFER_SECONDS

# =================================================================
# =============== 🔗 URL Внешних API 🔗 ==========================
# =================================================================
# === КОНСТАНТЫ ДЛЯ ССЫЛОК (ЧТОБЫ НЕ ХАРДКОДИТЬ) ===
BASE_URLS = {
    "coinmarketcap": "https://coinmarketcap.com/ru/currencies/",
    "binance": "https://www.binance.com/en/trade/{base}_{quote}",
    "bybit": "https://www.bybit.com/en/trade/spot/{base}/{quote}",
    "kucoin": "https://www.kucoin.com/trade/{base}-{quote}",
    # Добавьте другие биржи по аналогии
}

CMC_PRO_API_BASE_URL = "https://pro-api.coinmarketcap.com"

# --- Эндпоинты CoinMarketCap ---
CMC_QUOTES_LATEST_ENDPOINT = "/v2/cryptocurrency/quotes/latest"
CMC_GLOBAL_METRICS_LATEST = "/v1/global-metrics/quotes/latest"
CMC_FEAR_AND_GREED_LATEST = "/v3/fear-and-greed/latest"
CMC_TRENDING_TOKENS_LATEST = "/v1/community/trending/token"
CMC_CRYPTO_INFO_ENDPOINT = "/v2/cryptocurrency/info"
CMC_LISTINGS_LATEST_ENDPOINT = "/v1/cryptocurrency/listings/latest"

# Базовый URL для CryptoPanic API v2 для вашего плана
CRYPTOPANIC_API_BASE_URL = "https://cryptopanic.com/api/developer/v2/posts/"

# Таймаут по умолчанию для HTTP-клиента в сервисе-обогатителе
ENRICHER_HTTP_TIMEOUT = 10.0

# Таймаут для загрузки полного списка рынков с одной биржи (в секундах)
MARKETS_LOAD_TIMEOUT_SECONDS = 30.0

# Таймаут по умолчанию для HTTP-клиента в сервисах новостей
NEWS_HTTP_TIMEOUT = 15.0

# URL для CoinCap API
COINCAP_API_BASE_URL = "https://api.coincap.io/v2"
# Лимит количества активов для запроса в CoinCap
COINCAP_ASSETS_FETCH_LIMIT = 2000 # Для получения полного списка активов

# ИСПРАВЛЕНО: Правильный базовый URL для CoinAPI.io (не CoinCap!)
# COINAPI_IO_URL = "https://rest.coinapi.io/v1"
# ИСПРАВЛЕНО: Правильный шаблон URL для CoinAPI.io
# COINAPI_ASSET_URL_TEMPLATE = "https://coinapi.io/asset/{asset_id}"


# URL для CryptoCompare
CRYPTOCOMPARE_API_URL = "https://min-api.cryptocompare.com/data/v2/news/"

# URL для NewsAPI
NEWSAPI_API_URL = "https://newsapi.org/v2/everything"

# -- СТРАТЕГИЯ ВЫБОРА (Приоритеты) --
# Определяют, в каком порядке система будет ПЫТАТЬСЯ использовать провайдеры.
# Чем меньше число, тем выше приоритет.

# Базовый приоритет для всех провайдеров типа Gemini. Самый предпочтительный вариант.
GEMINI_BASE_PRIORITY = 1
# Базовый приоритет для Groq. Второй по предпочтительности.
GROQ_BASE_PRIORITY = 10
# Базовый приоритет для OpenRouter. Используется как резервный, если первые два недоступны.
OPENROUTER_BASE_PRIORITY = 20

# Шаг, на который увеличивается приоритет для каждой следующей комбинации "ключ + модель".
# Пример: Gemini-key1-model1 будет иметь приоритет 1, а Gemini-key1-model2 - приоритет 2.
# Это позволяет системе сначала пробовать все модели с первым ключом, прежде чем переходить ко второму.
BACKUP_KEY_PRIORITY_STEP = 1


# -- УПРАВЛЕНИЕ РЕСУРСАМИ (Семафоры) --
# Ограничивают, сколько ОДНОВРЕМЕННЫХ запросов может быть отправлено каждому типу провайдеров.
# Это защита от получения ошибок "429 Too Many Requests" (Rate Limit).

AI_PROVIDER_SEMAPHORES = {
    # Groq быстрый и позволяет до 3 одновременных запросов.
    'groq': 3,
    # Gemini более чувствителен к нагрузке, ограничиваем 2 одновременными запросами.
    'gemini': 2,
    # OpenRouter (особенно бесплатные модели) также стоит ограничить.
    'openrouter': 2,
    # Значение по умолчанию для любого будущего провайдера, не указанного в этом списке.
    'default': 1
}

# Пауза в секундах между быстрыми попытками failover ВНУТРИ ОДНОГО ЦИКЛА.
# Предотвращает слишком агрессивные повторные запросы при каскадном отказе.
AI_FAILOVER_ATTEMPT_DELAY_SECONDS = 2.0

# === URL И ШАБЛОНЫ ДЛЯ AI API ===
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# ВАША РЕКОМЕНДАЦИЯ: Улучшенная читаемость шаблона Gemini
GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_API_URL_TEMPLATE = f"{GEMINI_API_BASE_URL}/models/{{model_name}}:generateContent"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- Новостные и рыночные API ---
COINGECKO_API_BASE_URL = "https://api.coingecko.com/api/v3"
# Время жизни кэша полного списка монет CoinGecko (в секундах)
COINGECKO_COIN_LIST_CACHE_TTL_SECONDS = 3600 # 1 час
# Задержка между запросами к CoinGecko Events API (в секундах)
COINGECKO_EVENTS_REQUEST_DELAY_SECONDS = 2.0
# Максимальное количество результатов на странице для CoinGecko Markets
COINGECKO_MARKETS_PER_PAGE_LIMIT = 250
# Количество лидеров роста/падения для извлечения
COINGECKO_TOP_GAINERS_LOSERS_COUNT = 5
# Минимальный объем для включения в список лидеров роста/падения
COINGECKO_MIN_VOLUME_FOR_GAINERS_LOSERS = 50000
# Порог предупреждения об использовании API ключа CoinGecko
COINGECKO_API_USAGE_WARNING_THRESHOLD = 1000
# Максимальное количество одновременных запросов к CoinGecko API (для семафора)
COINGECKO_MAX_CONCURRENT_REQUESTS = 3

MESSARI_API_URL = "https://data.messari.io/api/v1/news"
CRYPTOPANIC_API_URL = "https://cryptopanic.com/api/v1/posts/"

ALPHAVANTAGE_API_URL = "https://www.alphavantage.co/query"

# Whitelist основных криптовалют, которые, как известно, поддерживаются AlphaVantage
ALPHAVANTAGE_SUPPORTED_CRYPTO_SYMBOLS = {
    'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT', 'LINK',
    'MATIC', 'LTC', 'BCH', 'UNI', 'AVAX', 'ATOM', 'TRX', 'ETC', 'XLM'
}
# Пауза между запросами для соблюдения лимита бесплатного ключа (5 запросов/мин -> 12 секунд)
ALPHAVANTAGE_RATE_LIMIT_DELAY_SECONDS = 12.5 # С небольшим запасом

# Определяем новые константы
API_PREFIX_INTEL = "/intel"
API_TAG_INTEL = "Market Intelligence"

# Централизованный статический маппинг для самых частых запросов к CoinGecko
COINGECKO_COMMON_SYMBOL_TO_ID_MAP = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'BNB': 'binancecoin',
    'XRP': 'ripple',
    'USDT': 'tether',
    'USDC': 'usd-coin',
    'ADA': 'cardano',
    'DOGE': 'dogecoin',
    'TRX': 'tron',
    'LINK': 'chainlink',
    'DOT': 'polkadot',
    'MATIC': 'matic-network'
}

# Маппинг псевдонимов и альтернативных названий
COINGECKO_SYMBOL_ALIASES = {
    # Псевдонимы для Bitcoin
    'BITCOIN': 'BTC',
    'БИТКОИН': 'BTC',

    # Псевдонимы для Ethereum
    'ETHEREUM': 'ETH',
    'ЭФИРИУМ': 'ETH',
    'ЭФИР': 'ETH',

    # Псевдонимы для других популярных монет
    'SOLANA': 'SOL',
    'СОЛЬ': 'SOL',
    'СОЛАНА': 'SOL',

    'BINANCE COIN': 'BNB',
    'BINANCE': 'BNB',

    'RIPPLE': 'XRP',
    'РИПЛ': 'XRP',

    'CARDANO': 'ADA',
    'КАРДАНО': 'ADA',

    'DOGECOIN': 'DOGE',
    'ДОГЕ': 'DOGE',
    'ДОЖКОИН': 'DOGE',

    'TRON': 'TRX',
    'ТРОН': 'TRX',

    'CHAINLINK': 'LINK',
    'ЧЕЙНЛИНК': 'LINK',

    'POLKADOT': 'DOT',
    'ПОЛКАДОТ': 'DOT',

    'POLYGON': 'MATIC',
    'ПОЛИГОН': 'MATIC'
}


# Выносим количество дней для запроса новостей в константу.
# Это позволяет централизованно управлять "свежестью" новостей и избегать хардкода.
# Устанавливаем значение 1, чтобы получать новости только за последние 24 часа.
NEWS_FETCH_DAYS_AGO = 1

# Выносим лимит количества новостей для AlphaVantage в константу.
# Это убирает "магическое число" из кода и позволяет легко настраивать
# глубину поиска новостей в одном месте.
ALPHAVANTAGE_NEWS_FETCH_LIMIT = 50

# АРГУМЕНТАЦИЯ: Выносим размер пакета для обработки новостей AI в константу.
# Это позволяет легко настраивать параметр без изменения кода, если лимиты AI изменятся.
AI_NEWS_PROCESSING_BATCH_SIZE = 5

# Пауза в секундах между отправкой пакетов новостей в AI-сервис.
# Помогает соблюдать лимиты RPM (requests per minute).
AI_REQUEST_DELAY_SECONDS = 8.0

# АРГУМЕНТАЦИЯ: Минимальный интервал между запросами к AI для избежания rate limits.
# Это более надежно, чем фиксированная пауза. Значение 12.0 сек выбрано для Groq free tier.
AI_MIN_REQUEST_INTERVAL_SECONDS = 12.0

# АРГУМЕНТАЦИЯ: Таймаут для ОДНОГО запроса к AI-модели.
AI_SINGLE_REQUEST_TIMEOUT = 300

# АРГУМЕНТАЦИЯ: Общий таймаут для всего процесса получения новостей через API.
# Должен быть достаточно большим, чтобы обработать все пакеты с задержками.
AI_REQUEST_TIMEOUT = 1000.0

# АРГУМЕНТАЦИЯ: Порог количества новостей, после которого мы уменьшаем размер пакета.
AI_LARGE_BATCH_THRESHOLD = 100

# Ограничение количества новостей в режиме отказа (fallback)
FALLBACK_NEWS_LIMIT = 15

# Максимальное количество одновременных запросов к AI
AI_MAX_CONCURRENT_REQUESTS = 3

# Количество монет, которые считаются одной "волной" параллельной обработки.
# Подбирается экспериментально, исходя из того, сколько запросов может эффективно выполняться параллельно.
TIMEOUT_COIN_WAVE_SIZE = 5

# Дополнительное время в секундах, которое добавляется на каждую "волну" обработки монет сверх первой.
TIMEOUT_PER_WAVE_ADDITION_SECONDS = 180.0

# АРГУМЕНТАЦИЯ: Процент от лимита токенов, который мы используем,
# чтобы оставить "запас прочности" на случай неточностей в оценке.
AI_PROVIDER_SAFETY_MARGIN = 0.8  # Используем 80% от лимита

# АРГУМЕНТАЦИЯ: Приблизительная оценка размера системного промпта в токенах.
# Вычитается из лимита, чтобы рассчитать полезную нагрузку.
AI_SYSTEM_PROMPT_TOKENS_ESTIMATE = 250

# АРГУМЕНТАЦИЯ: Консервативный лимит токенов, безопасный для самого "слабого"
# провайдера (Groq). Используется как базовый лимит для формирования батчей.
AI_CONSERVATIVE_TOKEN_LIMIT = 1000 # Лимит Groq max_tokens_per_request


