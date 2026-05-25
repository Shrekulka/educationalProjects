# inter_exchange_arbitrage_bot/src/services/blacklist_manager.py

import asyncio
from collections import defaultdict
from typing import Set, Dict, Optional, Tuple

import ccxt.async_support as ccxt

from src.constants.trading_constants import (DEFAULT_FALLBACK_SYMBOL, MAX_BATCH_FAILURES_BEFORE_BLACKLIST)
from src.utils.logger import logger


class BlacklistManager:
    """
    Singleton-менеджер для динамического определения бирж,
    не поддерживающих пакетные запросы fetch_order_books.

    Выполняет реальные пробные запросы при старте приложения
    для формирования актуального "черного списка".
    """
    _instance: Optional['BlacklistManager'] = None
    _initialized: bool = False

    def __new__(cls) -> 'BlacklistManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.batch_unsupported_exchanges: Set[str] = set()
        self.batch_failure_strikes: Dict[str, int] = defaultdict(int)
        self._lock = asyncio.Lock()
        self._test_results_cache: Dict[str, Tuple[bool, str]] = {}
        self._initialized = True
        logger.info("🔧 BlacklistManager инициализирован.")

    async def build_blacklist(self, services: Dict[str, any], force_rebuild: bool = False) -> None:
        """
        Проверяет все сервисы на реальную поддержку fetch_order_books
        и формирует динамический черный список.

        Args:
            services: Словарь {exchange_id: service}
            force_rebuild: Принудительно пересобрать список, игнорируя кэш
        """
        async with self._lock:
            if self.batch_unsupported_exchanges and not force_rebuild:
                logger.debug("✅ Черный список уже сформирован, пропускаем проверку.")
                return

            logger.info("🚀 Запуск динамического определения черного списка бирж...")

            # Очищаем предыдущие результаты при принудительном обновлении
            if force_rebuild:
                self.batch_unsupported_exchanges.clear()
                self._test_results_cache.clear()
                logger.info("🔄 Принудительное обновление: кэш очищен.")

            # Создаем задачи для проверки всех бирж
            check_tasks = []
            exchanges_to_check = []

            for exchange_id, service in services.items():
                check_tasks.append(self._check_exchange_support(exchange_id, service.client))
                exchanges_to_check.append(exchange_id)

            # Выполняем все проверки параллельно
            results = await asyncio.gather(*check_tasks, return_exceptions=True)

            # Обрабатываем результаты
            supported_count = 0
            unsupported_count = 0
            error_count = 0

            for i, result in enumerate(results):
                exchange_id = exchanges_to_check[i]

                if isinstance(result, Exception):
                    # Ошибка при проверке - считаем, что поддержка есть (консервативный подход)
                    logger.warning(f"⚠️ Ошибка проверки {exchange_id}: {result}. Считаем, что поддержка есть.")
                    self._test_results_cache[exchange_id] = (True, f"error: {type(result).__name__}")
                    error_count += 1
                    continue

                exchange_id_result, is_supported, test_method = result
                self._test_results_cache[exchange_id] = (is_supported, test_method)

                if is_supported:
                    supported_count += 1
                    logger.debug(f"✅ {exchange_id}: поддерживает пакетные запросы ({test_method})")
                else:
                    self.batch_unsupported_exchanges.add(exchange_id)
                    unsupported_count += 1
                    logger.debug(f"❌ {exchange_id}: НЕ поддерживает пакетные запросы ({test_method})")

            # Итоговая статистика
            total_checked = len(services)
            logger.info(
                f"✅ Анализ завершен: {total_checked} бирж проверено\n"
                f"📊 Поддерживают пакетные запросы: {supported_count}\n"
                f"📊 НЕ поддерживают: {unsupported_count}\n"
                f"📊 Ошибки проверки: {error_count}"
            )

            if self.batch_unsupported_exchanges:
                logger.info(f"🚫 Черный список: {sorted(self.batch_unsupported_exchanges)}")
            else:
                logger.info("🎉 Все биржи поддерживают пакетные запросы!")

    async def _check_exchange_support(self, exchange_id: str, client: ccxt.Exchange) -> Tuple[str, bool, str]:
        """
        Выполняет реальную проверку поддержки fetch_order_books для одной биржи.
        ИСПРАВЛЕНИЕ: убираем ненадежную проверку флага, основываемся только на реальном тесте.
        """
        logger.debug(f"🔍 Проверка поддержки пакетных запросов для {exchange_id}...")

        # --- Шаг 1: Проверяем наличие метода (быстрая проверка) ---
        if not hasattr(client, 'fetch_order_books') or not callable(getattr(client, 'fetch_order_books', None)):
            logger.debug(f"❌ {exchange_id}: метод fetch_order_books отсутствует.")
            return exchange_id, False, "method_check"

        # --- Шаг 2: Реальный пробный запрос (основная проверка) ---
        try:
            # Делаем минимальный запрос с одним символом и маленькой глубиной
            test_symbols = [DEFAULT_FALLBACK_SYMBOL]
            result = await client.fetch_order_books(test_symbols, limit=5)

            # Проверяем, что ответ - это словарь и он не пустой
            if isinstance(result, dict) and result:
                order_book = result.get(DEFAULT_FALLBACK_SYMBOL, {})
                # Убеждаемся, что внутри есть корректные данные стакана
                if isinstance(order_book, dict) and order_book.get('asks') and order_book.get('bids'):
                    logger.debug(f"✅ {exchange_id}: пробный пакетный запрос успешен.")
                    return exchange_id, True, "real_test_success"

            logger.warning(f"⚠️ {exchange_id}: пакетный запрос вернул пустой или некорректный ответ.")
            return exchange_id, False, "real_test_empty_response"

        except ccxt.NotSupported as e:
            # Библиотека явно говорит, что метод не поддерживается
            logger.debug(f"❌ {exchange_id}: ccxt выбросил NotSupported - {e}")
            return exchange_id, False, "real_test_not_supported"

        except ccxt.AuthenticationError as e:
            # Ошибка ключей не говорит об отсутствии поддержки
            logger.critical(f"🔑 {exchange_id}: Ошибка аутентификации при проверке. Проверьте API ключи! Ошибка: {e}")
            # Считаем, что поддержка есть, чтобы не заблокировать биржу из-за проблем с ключами
            return exchange_id, True, "real_test_auth_error"

        except ccxt.NetworkError as e:
            # Сетевые ошибки - временная проблема
            logger.warning(f"🌐 {exchange_id}: сетевая ошибка при проверке, считаем, что поддержка есть. Ошибка: {e}")
            return exchange_id, True, "real_test_network_error"

        except Exception as e:
            # Любая другая ошибка также временная
            logger.warning(
                f"⚠️ {exchange_id}: неожиданная ошибка при проверке, считаем, что поддержка есть. Ошибка: {e}")
            return exchange_id, True, f"real_test_other_error_{type(e).__name__}"

    def report_batch_failure(self, exchange_id: str):
        """Регистрирует сбой пакетного запроса для биржи."""
        exchange_id = exchange_id.lower()
        self.batch_failure_strikes[exchange_id] += 1
        logger.warning(
            f"Зафиксирован сбой пакетного запроса для {exchange_id}. "
            f"Всего сбоев: {self.batch_failure_strikes[exchange_id]}/{MAX_BATCH_FAILURES_BEFORE_BLACKLIST}"
        )

        if self.batch_failure_strikes[exchange_id] >= MAX_BATCH_FAILURES_BEFORE_BLACKLIST:
            if exchange_id not in self.batch_unsupported_exchanges:
                logger.critical(
                    f"🚨 Биржа {exchange_id} превысила лимит ошибок и динамически добавлена в черный список!")
                self.batch_unsupported_exchanges.add(exchange_id)

    def is_batch_supported(self, exchange_id: str) -> bool:
        """
        Проверяет, поддерживает ли биржа пакетные запросы.

        Args:
            exchange_id: Идентификатор биржи

        Returns:
            True, если биржа поддерживает пакетные запросы
        """
        return exchange_id.lower() not in self.batch_unsupported_exchanges

    def get_test_result(self, exchange_id: str) -> Optional[Tuple[bool, str]]:
        """
        Получает детальный результат тестирования биржи.

        Returns:
            Кортеж (is_supported, test_method) или None, если биржа не тестировалась
        """
        return self._test_results_cache.get(exchange_id)

    def get_statistics(self) -> Dict[str, any]:
        """
        Возвращает статистику по результатам тестирования.
        """
        total_tested = len(self._test_results_cache)
        supported = sum(1 for is_supported, _ in self._test_results_cache.values() if is_supported)
        unsupported = len(self.batch_unsupported_exchanges)

        return {
            'total_tested': total_tested,
            'supported': supported,
            'unsupported': unsupported,
            'unsupported_exchanges': sorted(self.batch_unsupported_exchanges),
            'test_cache': dict(self._test_results_cache)
        }

    async def force_rebuild(self, services: Dict[str, any]) -> None:
        """
        Принудительно пересобирает черный список.
        """
        logger.info("🔄 Принудительное обновление черного списка...")
        await self.build_blacklist(services, force_rebuild=True)


# Глобальный экземпляр для удобного доступа
blacklist_manager = BlacklistManager()
