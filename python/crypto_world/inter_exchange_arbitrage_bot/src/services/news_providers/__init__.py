# inter_exchange_arbitrage_bot/src/services/news_providers/__init__.py

# АРГУМЕНТАЦИЯ: Этот файл позволяет нам импортировать все классы-провайдеры одной строкой,
# что делает код в NewsService чище и удобнее для расширения.

from .base_provider import BaseNewsProvider
from .cryptocompare_provider import CryptoCompareProvider
from .newsapi_provider import NewsApiProvider
from .cryptopanic_provider import CryptoPanicProvider
from .messari_provider import MessariProvider
from .alphavantage_provider import AlphaVantageProvider
from .coinmarketcap_provider import CoinMarketCapProvider
from .coincap_provider import CoinCapProvider

__all__ = [
    'BaseNewsProvider',
    'CryptoCompareProvider',
    'NewsApiProvider',
    'CryptoPanicProvider',
    'MessariProvider',
    'AlphaVantageProvider',
    'CoinCapProvider',
    'CoinMarketCapProvider'
]