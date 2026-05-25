# inter_exchange_arbitrage_bot/src/services/news_service.py
import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Set

import httpx

from src.constants.api_constants import NEWS_FETCH_DAYS_AGO
from src.core.config import NewsProvidersConfig
from src.utils.logger import logger
from .news_providers import (
    CryptoCompareProvider,
    NewsApiProvider,
    CryptoPanicProvider,
    MessariProvider,
    AlphaVantageProvider,
    CoinCapProvider,
    CoinMarketCapProvider,
    BaseNewsProvider
)
from .news_providers.diagnostic_wrapper import DiagnosticProviderWrapper
from ..constants.service_constants import NEWS_PROVIDER_DIAGNOSTIC_WRAPPER_TARGETS, \
    NEWS_PROVIDER_DIAGNOSTIC_TIMEOUT_SECONDS


class NewsService:
    """
    АРГУМЕНТАЦИЯ: Этот сервис теперь выступает в роли "оркестратора".
    Он не содержит логики для конкретных API, а только управляет списком
    провайдеров. Это делает код чистым, легко расширяемым и отказоустойчивым.
    Добавление нового API теперь сводится к созданию нового файла-провайдера
    и добавлению его класса в `_initialize_providers`.
    """

    def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        self.config = api_config
        self.session = http_session
        self.providers: List[BaseNewsProvider] = self._initialize_providers()

    def _initialize_providers(self) -> List[BaseNewsProvider]:
        """Динамически создает провайдеров с диагностической оберткой для проблемных."""
        provider_classes = [
            CoinMarketCapProvider,
            CryptoCompareProvider,
            NewsApiProvider,
            CryptoPanicProvider,
            MessariProvider,
            AlphaVantageProvider,
            CoinCapProvider,
        ]

        active_providers = []
        for ProviderClass in provider_classes:
            provider = ProviderClass(self.config, self.session)
            if provider.is_configured():
                # 3. ИСПОЛЬЗУЕМ КОНСТАНТЫ
                if provider.name in NEWS_PROVIDER_DIAGNOSTIC_WRAPPER_TARGETS:
                    wrapped_provider = DiagnosticProviderWrapper(
                        provider,
                        timeout_seconds=NEWS_PROVIDER_DIAGNOSTIC_TIMEOUT_SECONDS
                    )
                    active_providers.append(wrapped_provider)
                    logger.info(f"✅ Новостной провайдер '{provider.name}' активирован (под диагностической оберткой).")
                else:
                    active_providers.append(provider)
                    logger.info(f"✅ Новостной провайдер '{provider.name}' активирован.")

        if not active_providers:
            logger.warning("⚠️ Ни один новостной провайдер не сконфигурирован в .env файле.")

        return active_providers

    async def fetch_all_raw_news_by_source(self, coins: Set[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Оркестрирует асинхронный сбор новостей. Надежно и отказоустойчиво.
        """
        if not self.providers:
            return {}

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=NEWS_FETCH_DAYS_AGO)

        tasks = {
            # Используем .name от обертки или оригинального провайдера
            provider.name: provider.fetch(coins, cutoff_date)
            for provider in self.providers
        }

        results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        news_by_source: Dict[str, List[Dict[str, Any]]] = {}
        provider_names = list(tasks.keys())

        for i, provider_name in enumerate(provider_names):
            result = results[i]

            if isinstance(result, list):
                news_by_source[provider_name] = result
                if result:
                    logger.debug(f"Провайдер '{provider_name}' вернул {len(result)} новостей.")
            else:
                # Этот блок теперь ловит Исключения и любые другие неожиданные типы
                error_type = type(result).__name__
                logger.error(
                    f"❌ Провайдер '{provider_name}' не вернул список. Результат: {error_type}. Устанавливаю пустой список.")
                news_by_source[provider_name] = []

        return news_by_source
