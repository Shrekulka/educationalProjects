# inter_exchange_arbitrage_bot/src/core/config.py

from dataclasses import dataclass, field
from typing import List, Optional

from environs import Env


@dataclass
class TgBot:
    """Конфигурация Telegram-бота."""
    token: str
    admin_ids: List[int]


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных."""
    engine: str
    name: str
    user: str
    password: str
    host: str
    port: str


# 1. Базовый класс только с ОБЯЗАТЕЛЬНЫМИ полями
@dataclass
class BaseExchangeConfig:
    """Базовый конфиг с общими обязательными полями для любой биржи."""
    api_key: str
    api_secret: str


# 2. Конкретные конфиги наследуются и добавляют свои поля
@dataclass
class BinanceConfig(BaseExchangeConfig):
    """Конфигурация для Binance с опциональным полем testnet."""
    testnet: bool = False


@dataclass
class KuCoinConfig(BaseExchangeConfig):
    """Конфигурация для KuCoin, добавляет обязательный passphrase и опциональный testnet."""
    api_passphrase: str
    testnet: bool = False


@dataclass
class BybitConfig(BaseExchangeConfig):
    """Конфигурация для Bybit с опциональным полем testnet."""
    testnet: bool = False


# Создаем dataclass для Yobit. Так как у него нет особых полей, он может просто наследовать BaseExchangeConfig.
@dataclass
class YobitConfig(BaseExchangeConfig):
    """Конфигурация для Yobit."""
    # У Yobit нет testnet, поэтому поле здесь не нужно
    pass


@dataclass
class NetworkConfig:
    """Конфигурация сети и безопасности."""
    allowed_ip: Optional[str]
    ip_rotation_enabled: bool = True
    proxy_sources: List[str] = field(default_factory=list)
    proxy_check_url: str = "https://api.ipify.org?format=json"
    proxy_check_timeout: int = 10
    proxy_refresh_interval_seconds: int = 1800
    ip_rotation_strategy: List[str] = field(default_factory=list)
    tor_proxy_enabled: bool = False
    tor_proxy_url: str = "socks5://127.0.0.1:9050"


@dataclass
class NewsProvidersConfig:
    """Конфигурация для внешних НОВОСТНЫХ API с поддержкой нескольких ключей."""
    coinmarketcap: List[str] = field(default_factory=list)
    cryptopanic: List[str] = field(default_factory=list)
    coingecko: List[str] = field(default_factory=list)
    cryptocompare: List[str] = field(default_factory=list)
    # coinapi: List[str] = field(default_factory=list)
    coincap: List[str] = field(default_factory=list)
    newsapi: List[str] = field(default_factory=list)
    alphavantage: List[str] = field(default_factory=list)
    messari: List[str] = field(default_factory=list)


@dataclass
class AIProviderConfig:
    """УПРОЩЕННАЯ конфигурация для одного AI-провайдера."""
    models: List[str] = field(default_factory=list)
    keys: List[str] = field(default_factory=list)


@dataclass
class AIConfig:
    """Конфигурация для всех AI-провайдеров."""
    groq: AIProviderConfig = field(default_factory=AIProviderConfig)
    gemini: AIProviderConfig = field(default_factory=AIProviderConfig)
    openrouter: AIProviderConfig = field(default_factory=AIProviderConfig)


@dataclass
class Config:
    """Главный класс конфигурации всего приложения."""
    tg_bot: TgBot
    db: Optional[DatabaseConfig]
    debug: bool
    network: NetworkConfig
    binance: Optional[BinanceConfig]
    kucoin: Optional[KuCoinConfig]
    bybit: Optional[BybitConfig]
    yobit: Optional[YobitConfig]

    # Используем новые, разделенные классы конфигурации
    news_providers: NewsProvidersConfig
    ai_providers: AIConfig

    internal_api_key: Optional[str] = None

    def __init__(self, env_path: Optional[str] = None):
        env = Env()
        env.read_env(env_path)

        self.debug = env.bool("DEBUG", False)

        # Загружаем API ключ для внутренних запросов
        self.internal_api_key = env.str("INTERNAL_API_KEY", None)

        # Блок для новостных API
        self.news_providers = NewsProvidersConfig(
            coinmarketcap=env.list("COINMARKETCAP_API_KEY", []),
            cryptopanic=env.list("CRYPTOPANIC_API_KEY", []),
            coingecko=env.list("COINGECKO_API_KEY", []),
            cryptocompare=env.list("CRYPTOCOMPARE_API_KEY", []),
            # coinapi=env.list("COINAPI_API_KEY", []),
            coincap=env.list("COINCAP_API_KEY", []),
            newsapi=env.list("NEWSAPI_API_KEY", []),
            alphavantage=env.list("ALPHAVANTAGE_API_KEY", []),
            messari=env.list("MESSARI_API_KEY", []),
        )

        # Блок для AI API с поддержкой списков ключей и моделей
        self.ai_providers = AIConfig(
            groq=AIProviderConfig(
                models=env.list("GROQ_MODELS", [env.str("GROQ_MODEL", "llama-3.1-8b-instant")]),
                keys=env.list("GROQ_API_KEYS", [])
            ),
            gemini=AIProviderConfig(
                models=env.list("GEMINI_MODELS", [env.str("GEMINI_MODEL", "gemini-2.0-flash")]),
                keys=env.list("GEMINI_API_KEYS", [])
            ),
            openrouter=AIProviderConfig(
                models=env.list("OPENROUTER_MODELS",
                                [env.str("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")]),
                keys=env.list("OPENROUTER_API_KEYS", [])
            )
        )

        self.network = NetworkConfig(
            allowed_ip=env.str("ALLOWED_IP", None),
            ip_rotation_enabled=env.bool("IP_ROTATION_ENABLED", True),
            proxy_sources=env.list("PROXY_SOURCES", []),
            proxy_check_url=env.str("PROXY_CHECK_URL", "https://api.ipify.org?format=json"),
            proxy_check_timeout=env.int("PROXY_CHECK_TIMEOUT", 10),
            proxy_refresh_interval_seconds=env.int("PROXY_REFRESH_INTERVAL_SECONDS", 1800),
            ip_rotation_strategy=env.list("IP_ROTATION_STRATEGY", []),
            tor_proxy_enabled=env.bool("TOR_PROXY_ENABLED", False),
            tor_proxy_url=env.str("TOR_PROXY_URL", "socks5://127.0.0.1:9050")
        )

        self.tg_bot = TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=[int(admin_id) for admin_id in env.list("ADMIN_IDS", [])]
        )

        if env.str("DB_HOST", None):
            self.db = DatabaseConfig(
                engine=env.str('DB_ENGINE', 'postgresql'),
                name=env.str('DB_NAME'),
                user=env.str('DB_USER'),
                password=env.str('DB_PASSWORD'),
                host=env.str('DB_HOST'),
                port=env.str('DB_PORT', '5432')
            )
        else:
            self.db = None

        if env.str("BINANCE_API_KEY", None):
            self.binance = BinanceConfig(
                api_key=env.str("BINANCE_API_KEY"),
                api_secret=env.str("BINANCE_API_SECRET"),
                testnet=env.bool("BINANCE_TESTNET", False)
            )
        else:
            self.binance = None

        if env.str("KUCOIN_API_KEY", None):
            self.kucoin = KuCoinConfig(
                api_key=env.str("KUCOIN_API_KEY"),
                api_secret=env.str("KUCOIN_API_SECRET"),
                api_passphrase=env.str("KUCOIN_API_PASSPHRASE"),
                testnet=env.bool("KUCOIN_TESTNET", False)
            )
        else:
            self.kucoin = None

        if env.str("BYBIT_API_KEY", None):
            self.bybit = BybitConfig(
                api_key=env.str("BYBIT_API_KEY"),
                api_secret=env.str("BYBIT_API_SECRET"),
                testnet=env.bool("BYBIT_TESTNET", False)
            )
        else:
            self.bybit = None

        if env.str("YOBIT_API_KEY", None):
            self.yobit = YobitConfig(
                api_key=env.str("YOBIT_API_KEY"),
                api_secret=env.str("YOBIT_API_SECRET")
            )
        else:
            self.yobit = None


# Создаем единый экземпляр конфига для импорта в других модулях
config = Config()
