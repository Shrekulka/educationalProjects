# inter_exchange_arbitrage_bot/src/services/news_providers/diagnostic_wrapper.py

import asyncio
import time
from typing import Set, List, Dict, Any, Optional
from datetime import datetime

# Важно: импортируем ABC-версию, а не старый файл
from src.services.news_providers.base_provider import BaseNewsProvider
from src.utils.logger import logger


class DiagnosticProviderWrapper(BaseNewsProvider):
    """
    ИСПРАВЛЕННАЯ диагностическая обертка.
    Корректно наследуется от BaseNewsProvider и делегирует вызовы,
    добавляя таймаут и детальное логирование для выявления "зависающих" провайдеров.
    """

    def __init__(self, provider: BaseNewsProvider, timeout_seconds: int = 45):
        # 1. ИСПРАВЛЕНО: Корректный вызов __init__ родительского класса.
        # Мы передаем в super() все необходимые атрибуты из "обернутого" провайдера,
        # чтобы наш wrapper вел себя как полноценный наследник.
        super().__init__(
            name=f"Diagnostic[{provider.name}]",  # Используем особое имя для логов
            api_config=provider.config,
            http_session=provider.session
        )
        self.provider = provider
        self.timeout_seconds = timeout_seconds

    # --- Методы, которые мы не меняем, а просто делегируем ---

    def is_configured(self) -> bool:
        return self.provider.is_configured()

    def _supports_parallel_requests(self) -> bool:
        # Логика параллелизма полностью определяется "внутренним" провайдером
        return self.provider._supports_parallel_requests()

    def _distribute_coins_among_keys(self, coins: Set[str], available_keys: List[str]) -> List[Set[str]]:
        # Если у провайдера есть своя логика распределения, мы ее используем
        return self.provider._distribute_coins_among_keys(coins, available_keys)

    # 2. ИСПРАВЛЕНО: Реализуем _fetch_logic вместо старых _do_fetch
    async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        """
        Делегируем основной логический вызов оригинальному провайдеру.
        Обертка fetch() добавит к этому вызову таймаут.
        """
        return await self.provider._fetch_logic(coins, api_key, key_index)

    # --- Основная логика обертки (здесь добавляется таймаут) ---

    async def fetch(self, coins: Set[str], cutoff_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Обертка над методом fetch с таймаутом и детальным логированием.
        Эта логика остается ключевой для данного класса.
        """
        start_time = time.time()
        logger.debug(f"[{self.name}]: Начало fetch для {len(coins)} монет (таймаут: {self.timeout_seconds}с)...")

        try:
            # Используем asyncio.wait_for для обертывания вызова fetch из BaseNewsProvider.
            # BaseNewsProvider сам решит, какой режим (параллельный/последовательный) использовать.
            result = await asyncio.wait_for(
                # Вызываем super().fetch, чтобы запустить всю логику BaseNewsProvider
                super().fetch(coins, cutoff_date),
                timeout=self.timeout_seconds
            )
            elapsed = time.time() - start_time
            logger.debug(f"[{self.name}]: Успешное завершение за {elapsed:.2f}с, получено {len(result)} новостей.")
            return result

        except asyncio.TimeoutError:
            elapsed = time.time() - start_time
            logger.error(
                f"[{self.name}]: TIMEOUT! Провайдер '{self.provider.name}' завис и был принудительно остановлен после {elapsed:.2f}с!")
            return []

        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(
                f"[{self.name}]: Провайдер '{self.provider.name}' выбросил исключение после {elapsed:.2f}с: {type(e).__name__} - {e}")
            return []