# inter_exchange_arbitrage_bot/src/services/dynamic_pairs_manager.py

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Set, Optional, List, Tuple

from src.constants.trading_constants import (
    DYNAMIC_PAIRS_CONFIG, GLOBAL_INVALID_PAIRS, MIN_EXCHANGES_FOR_ARBITRAGE, PRIMARY_QUOTE_CURRENCY,
    MARKET_FIELD_ACTIVE, MARKET_FIELD_QUOTE, PAIR_UNAVAILABLE_REASON_NOT_IN_LIST, PAIR_UNAVAILABLE_REASON_NOT_FOUND,
    PAIR_UNAVAILABLE_REASON_INACTIVE, MARKET_FIELD_SPOT, PAIR_UNAVAILABLE_REASON_API_ERROR, MARKET_FIELD_MARKETS,
    CRITICAL_UNAVAILABLE_PAIRS_RATIO, CRITICAL_ACTIVE_PAIRS_THRESHOLD, SUCCESSFUL_TRADE_COOLDOWN_SECONDS,
    SECONDS_IN_MINUTE,

)
from src.utils.logger import logger


class PairStatus(Enum):
    """Статусы торговых пар"""
    ACTIVE = "active"  # Пара активна и торгуется
    TEMPORARILY_UNAVAILABLE = "temp_unavailable"  # Временно недоступна
    EXCLUDED = "excluded"  # Исключена администратором
    UNKNOWN = "unknown"  # Статус неизвестен


@dataclass
class PairInfo:
    """Информация о торговой паре на конкретной бирже"""
    symbol: str
    exchange_id: str
    status: PairStatus = PairStatus.UNKNOWN
    last_check: float = field(default_factory=time.time)
    consecutive_failures: int = 0
    last_success: Optional[float] = None
    failure_reason: Optional[str] = None
    last_trade_attempt_time: Optional[float] = None

    @property
    def is_available(self) -> bool:
        """Доступна ли пара для торговли"""
        return self.status == PairStatus.ACTIVE

    @property
    def is_in_cooldown(self) -> bool:
        """Проверяет, находится ли пара в кулдауне после сделки."""
        if self.last_trade_attempt_time is None:
            return False

        time_since_attempt = time.time() - self.last_trade_attempt_time
        return time_since_attempt < SUCCESSFUL_TRADE_COOLDOWN_SECONDS

    @property
    def cooldown_remaining_minutes(self) -> float:
        """Рассчитывает, сколько минут осталось до конца кулдауна."""
        if not self.is_in_cooldown:
            return 0.0

        time_elapsed = time.time() - self.last_trade_attempt_time
        time_left_seconds = SUCCESSFUL_TRADE_COOLDOWN_SECONDS - time_elapsed
        return time_left_seconds / SECONDS_IN_MINUTE

    @property
    def should_retry(self) -> bool:
        """Нужно ли повторить проверку пары"""
        if self.status == PairStatus.ACTIVE:
            return False

        base_delay = DYNAMIC_PAIRS_CONFIG['retry_base_delay']
        max_delay = DYNAMIC_PAIRS_CONFIG['retry_max_delay']

        # Расчет задержки: 60с * (2^0), 60с * (2^1), 60с * (2^2), и т.д.
        # Пример: 1м, 2м, 4м, 8м, 16м, но не более 30м.
        backoff_multiplier = DYNAMIC_PAIRS_CONFIG['retry_backoff_multiplier']
        retry_delay = min(base_delay * (backoff_multiplier ** self.consecutive_failures), max_delay)
        # Проверяем, прошло ли достаточно времени с последней проверки.
        return time.time() - self.last_check > retry_delay


class DynamicPairsManager:
    """
    Динамический менеджер торговых пар с автоматическим обнаружением
    новых листингов и восстановлением недоступных пар.
    """

    def __init__(self):
        # Кэш состояния пар: {exchange_id: {symbol: PairInfo}}
        self._pair_cache: Dict[str, Dict[str, PairInfo]] = {}

        # Жестко исключенные пары (устанавливается администратором)
        self._admin_excluded: Dict[str, Set[str]] = {}

        # Глобально невалидные пары (одинаковые стейблкоины и т.д.)
        self._global_invalid = GLOBAL_INVALID_PAIRS

        # Настройки обновления
        self._full_refresh_interval = DYNAMIC_PAIRS_CONFIG['cache_refresh_interval']
        self._last_full_refresh = 0
        self._update_lock = asyncio.Lock()
        self._last_known_active_pairs: Set[str] = set()  # Для отслеживания новых пар и отправки уведомлений
        self.notifier: Optional[any] = None
        self.config = None
        self._is_initialized = False

    def initialize(self, notifier, config_obj):
        """
        Инициализирует менеджер, передавая ему внешние зависимости.

        Args:
            notifier: NotifierService для отправки уведомлений
            config_obj: Объект конфигурации с настройками
        """
        self.notifier = notifier
        self.config = config_obj
        self._is_initialized = True
        logger.info("DynamicPairsManager инициализирован с зависимостями.")

    def add_admin_exclusion(self, exchange_id: str, symbol: str, reason: str = MARKET_FIELD_ACTIVE):
        """Добавляет пару в административные исключения"""
        if exchange_id not in self._admin_excluded:
            self._admin_excluded[exchange_id] = set()

        self._admin_excluded[exchange_id].add(symbol)

        # Обновляем статус в кэше
        if exchange_id in self._pair_cache and symbol in self._pair_cache[exchange_id]:
            self._pair_cache[exchange_id][symbol].status = PairStatus.EXCLUDED
            self._pair_cache[exchange_id][symbol].failure_reason = reason

        logger.info(f"Пара {symbol} исключена администратором для {exchange_id}: {reason}")

    def remove_admin_exclusion(self, exchange_id: str, symbol: str):
        """Удаляет пару из административных исключений"""
        if exchange_id in self._admin_excluded:
            self._admin_excluded[exchange_id].discard(symbol)

        # Помечаем для повторной проверки
        if exchange_id in self._pair_cache and symbol in self._pair_cache[exchange_id]:
            self._pair_cache[exchange_id][symbol].status = PairStatus.UNKNOWN
            self._pair_cache[exchange_id][symbol].consecutive_failures = 0

        logger.info(f"Пара {symbol} возвращена в проверку для {exchange_id}")

    async def is_pair_available(self, symbol: str, exchange_id: str, service=None) -> bool:
        """
        Основной метод проверки доступности пары.
        """
        # 1. Быстрые проверки без блокировок
        if symbol in self._global_invalid or \
                (exchange_id in self._admin_excluded and symbol in self._admin_excluded[exchange_id]):
            return False

        # 2. Получаем информацию о паре из кэша
        pair_info = self.get_pair_info(symbol, exchange_id)

        # 2.1 ПРОВЕРКА НА КУЛДАУН
        if pair_info.is_in_cooldown:
            logger.info(
                f"⏳ Пара {symbol} на {exchange_id} пропущена: в кулдауне еще {pair_info.cooldown_remaining_minutes:.1f} мин."
            )
            return False

        # 3. Проверяем статус
        if pair_info.status == PairStatus.ACTIVE:
            return True  # Пара точно доступна, API можно не проверять

        # Если пара ИЗВЕСТНА как недоступная, применяем логику задержки
        if pair_info.status == PairStatus.TEMPORARILY_UNAVAILABLE:
            if not pair_info.should_retry:
                # Еще не время для повторной проверки, считаем пару недоступной
                return False

        # Если статус UNKNOWN (пара новая) или если для TEMPORARILY_UNAVAILABLE
        # пришло время повторной проверки, мы продолжаем выполнение.

        # 4. Если есть сервис, выполняем проверку через API
        if service:
            return await self._check_pair_availability(symbol, exchange_id, service)

        # 5. Если сервис не передан, считаем пару недоступной
        return False

    def get_pair_info(self, symbol: str, exchange_id: str) -> PairInfo:
        """Получает информацию о паре из кэша или создает новую (потокобезопасно)"""
        if exchange_id not in self._pair_cache:
            self._pair_cache[exchange_id] = {}

        if symbol not in self._pair_cache[exchange_id]:
            # Проверяем снова после создания словаря (double-checked locking pattern)
            if symbol not in self._pair_cache[exchange_id]:
                self._pair_cache[exchange_id][symbol] = PairInfo(symbol, exchange_id)

        return self._pair_cache[exchange_id][symbol]

    def get_admin_excluded_pairs(self) -> Dict[str, List[str]]:
        """Возвращает публичную копию списка исключенных пар."""
        # Преобразуем set в отсортированный list для стабильного вывода
        return {exchange: sorted(list(symbols)) for exchange, symbols in self._admin_excluded.items() if symbols}

    async def _check_pair_availability(self, symbol: str, exchange_id: str, service) -> bool:
        """Проверяет доступность пары через API биржи"""
        pair_info = self.get_pair_info(symbol, exchange_id)

        try:
            # Загружаем рынки если необходимо
            if not hasattr(service.client, MARKET_FIELD_MARKETS) or not service.client.markets:
                await service.client.load_markets()

            # Проверяем наличие пары
            if symbol in service.client.markets:
                market = service.client.markets[symbol]

                # Дополнительные проверки активности
                is_active = market.get(MARKET_FIELD_ACTIVE, True)
                is_spot = market.get(MARKET_FIELD_SPOT, True)

                if is_active and is_spot:
                    # Пара доступна
                    pair_info.status = PairStatus.ACTIVE
                    pair_info.last_success = time.time()
                    pair_info.consecutive_failures = 0
                    pair_info.failure_reason = None
                    logger.debug(f"✅ {symbol} активна на {exchange_id}")
                    return True
                else:
                    # Пара найдена, но неактивна
                    pair_info.status = PairStatus.TEMPORARILY_UNAVAILABLE
                    pair_info.failure_reason = f"{PAIR_UNAVAILABLE_REASON_INACTIVE}: active={is_active}, spot={is_spot}"
            else:
                # Пара не найдена
                pair_info.status = PairStatus.TEMPORARILY_UNAVAILABLE
                pair_info.failure_reason = PAIR_UNAVAILABLE_REASON_NOT_FOUND

            # Обновляем информацию о неудаче
            pair_info.consecutive_failures += 1
            pair_info.last_check = time.time()

            logger.debug(f"❌ {symbol} недоступна на {exchange_id}: {pair_info.failure_reason}")
            return False

        except Exception as e:
            # Ошибка при проверке
            pair_info.status = PairStatus.TEMPORARILY_UNAVAILABLE
            pair_info.failure_reason = f"{PAIR_UNAVAILABLE_REASON_API_ERROR}: {type(e).__name__}"
            pair_info.consecutive_failures += 1
            pair_info.last_check = time.time()

            logger.warning(f"Ошибка проверки {symbol} на {exchange_id}: {e}")
            return False

    async def bulk_update_exchange_pairs(self, exchange_id: str, service) -> Dict[str, bool]:
        """
        Массовое обновление статуса пар для биржи.
        Используется для периодического обновления кэша.
        --- ПОЛНАЯ ИСПРАВЛЕННАЯ ВЕРСИЯ ---
        """
        # Блокируем метод, чтобы избежать одновременного обновления для одной биржи из разных потоков
        async with self._update_lock:
            logger.info(f"Запуск массового обновления пар для {exchange_id}")

            try:
                # 1. ПОЛУЧЕНИЕ АКТУАЛЬНЫХ ДАННЫХ С БИРЖИ
                # Принудительно загружаем самый свежий список рынков с биржи
                markets = await service.client.load_markets(True)

                # Формируем множество (set) символов, которые биржа считает активными для спотовой USDT торговли
                active_symbols_from_exchange = {
                    symbol for symbol, market in markets.items()
                    if (market.get(MARKET_FIELD_QUOTE) == PRIMARY_QUOTE_CURRENCY and
                        market.get(MARKET_FIELD_SPOT, True) and
                        market.get(MARKET_FIELD_ACTIVE, True))
                }
                logger.info(
                    f"Найдено {len(active_symbols_from_exchange)} активных {PRIMARY_QUOTE_CURRENCY} пар на {exchange_id}")

                # 2. ПОДГОТОВКА ЛОКАЛЬНЫХ ДАННЫХ
                # Инициализируем хранилище для биржи в кэше, если его еще нет
                if exchange_id not in self._pair_cache:
                    self._pair_cache[exchange_id] = {}

                # Получаем множество (set) символов, которые уже есть у нас в кэше для этой биржи
                cached_symbols = set(self._pair_cache[exchange_id].keys())
                current_time = time.time()

                # 3. СИНХРОНИЗАЦИЯ КЭША

                # --- ШАГ 3.1: ОБРАБОТКА НОВЫХ ПАР ---
                # Находим символы, которые есть на бирже, но отсутствуют в нашем кэше
                new_symbols = active_symbols_from_exchange - cached_symbols
                for symbol in new_symbols:
                    # Игнорируем глобально невалидные пары и те, что уже в ручном исключении
                    if symbol in self._global_invalid or \
                            (exchange_id in self._admin_excluded and symbol in self._admin_excluded[exchange_id]):
                        continue

                    # Добавляем новую пару в кэш с корректным "чистым" статусом
                    pair_info = self.get_pair_info(symbol, exchange_id)
                    pair_info.status = PairStatus.ACTIVE
                    pair_info.last_check = current_time
                    pair_info.last_success = current_time
                    pair_info.consecutive_failures = 0
                    pair_info.failure_reason = None

                # --- ШАГ 3.2: ОБРАБОТКА УДАЛЕННЫХ (ДЕЛИСТНУТЫХ) ПАР ---
                # Находим символы, которые есть в нашем кэше, но больше не приходят в списке с биржи
                delisted_symbols = cached_symbols - active_symbols_from_exchange
                for symbol in delisted_symbols:
                    pair_info = self.get_pair_info(symbol, exchange_id)
                    # Важная проверка: меняем статус, только если он был ACTIVE.
                    # Это предотвращает изменение статуса у пар, которые уже были помечены
                    # как недоступные по другой причине или исключены вручную.
                    if pair_info.status == PairStatus.ACTIVE:
                        pair_info.status = PairStatus.TEMPORARILY_UNAVAILABLE
                        pair_info.failure_reason = PAIR_UNAVAILABLE_REASON_NOT_IN_LIST
                        pair_info.last_check = current_time

                # --- ШАГ 3.3: СУЩЕСТВУЮЩИЕ ПАРЫ ---
                # Пары, которые есть и на бирже, и в кэше, намеренно НЕ ТРОГАЮТСЯ.
                # Их статус (ACTIVE или TEMPORARILY_UNAVAILABLE) сохранится.
                # Актуализацией их статуса занимается основной цикл сканирования,
                # когда пытается получить для них стакан ордеров.

                # 4. ФОРМИРОВАНИЕ ОТЧЕТА И ЗАВЕРШЕНИЕ
                # Считаем итоговое количество пар со статусом ACTIVE в кэше
                active_count = sum(1 for p in self._pair_cache[exchange_id].values() if p.status == PairStatus.ACTIVE)
                logger.info(f"Обновление {exchange_id} завершено: {active_count} активных пар в кэше")

                # Возвращаем словарь со всеми активными парами с биржи.
                # Это может использоваться другими частями системы.
                return {s: True for s in active_symbols_from_exchange}

            except Exception as e:
                # В случае любой ошибки (например, API биржи недоступно) логируем ее
                # и возвращаем пустой словарь, чтобы не сломать вызывающий код.
                logger.error(f"Ошибка при массовом обновлении {exchange_id}: {e}", exc_info=True)
                return {}

    async def get_available_pairs_for_scanning(self, exchanges: Dict[str, any],
                                               coins: List[str], force_refresh: bool = False) -> List[
        Tuple[str, List[str]]]:
        """
        ФИНАЛЬНАЯ ВЕРСИЯ: Улучшенная логика с поддержкой "вежливой" отмены.
        """
        if not coins:
            logger.warning("Передан пустой список монет для сканирования")
            return []

        logger.info(f"🔍 Проверка доступности {len(coins)} монет на {len(exchanges)} биржах")

        if force_refresh:
            logger.info("Принудительное обновление кэша пар по запросу...")

            bulk_check_tasks = [
                self.bulk_update_exchange_pairs(ex_id, srv)
                for ex_id, srv in exchanges.items()
            ]
            # Этот gather будет прерван, если вся задача run_reconnaissance_task будет отменена.
            await asyncio.gather(*bulk_check_tasks, return_exceptions=True)

        # if force_refresh:
        #     logger.info("Принудительное обновление кэша пар по запросу...")
        #
        #     # --- НОВЫЙ БЛОК С ПОДДЕРЖКОЙ ОТМЕНЫ ---
        #     cancel_task = asyncio.create_task(app_state.recon_cancel_event.wait())
        #     bulk_check_tasks = {
        #         asyncio.create_task(self.bulk_update_exchange_pairs(ex_id, srv)): ex_id
        #         for ex_id, srv in exchanges.items()
        #     }
        #
        #     # Собираем все задачи в один список для asyncio.wait
        #     all_tasks = list(bulk_check_tasks.keys()) + [cancel_task]
        #
        #     # Ждем, пока либо все задачи обновления завершатся, либо сработает отмена
        #     done, pending = await asyncio.wait(all_tasks, return_when=asyncio.FIRST_COMPLETED)
        #
        #     # Проверяем, была ли отмена
        #     if cancel_task in done:
        #         logger.info("Отмена во время массового обновления пар.")
        #         # Отменяем все еще работающие задачи
        #         for task in pending:
        #             task.cancel()
        #         await asyncio.gather(*pending, return_exceptions=True)  # Даем им завершиться
        #         return []  # Возвращаем пустой список
        #
        #     # Если отмены не было, значит все задачи обновления завершились
        #     # Нужно отменить нашу сторожевую задачу, чтобы она не висела в фоне
        #     cancel_task.cancel()
        #     # ----------------------------------------

        # --- Логика после обновления кэша остается без изменений ---
        available_pairs = []
        exchange_stats = {ex_id: {'checked': 0, 'available': 0, 'unavailable': 0}
                          for ex_id in exchanges.keys()}

        for coin in coins:
            symbol = f"{coin}/{PRIMARY_QUOTE_CURRENCY}"
            available_exchanges = []

            for exchange_id in exchanges.keys():
                exchange_stats[exchange_id]['checked'] += 1

                if await self.is_pair_available(symbol, exchange_id, service=None):
                    available_exchanges.append(exchange_id)
                    exchange_stats[exchange_id]['available'] += 1
                else:
                    exchange_stats[exchange_id]['unavailable'] += 1

            if len(available_exchanges) >= MIN_EXCHANGES_FOR_ARBITRAGE:
                available_pairs.append((symbol, available_exchanges))

        # Логируем статистику
        logger.info(f"📊 Результаты сканирования: {len(available_pairs)} доступных пар")
        for exchange_id, stats in exchange_stats.items():
            logger.debug(f"   {exchange_id}: {stats['available']}/{stats['checked']} пар доступны "
                         f"({stats['available'] / max(stats['checked'], 1) * 100:.1f}%)")

        return available_pairs

    async def periodic_refresh(self, services: Dict[str, any]):
        """Периодическое обновление кэша (вызывается в фоне)"""
        current_time = time.time()

        if current_time - self._last_full_refresh < self._full_refresh_interval:
            return

        logger.info("🔄 Запуск периодического обновления кэша пар")

        tasks = []
        for exchange_id, service in services.items():
            task = self.bulk_update_exchange_pairs(exchange_id, service)
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
        self._last_full_refresh = current_time

        logger.info("✅ Периодическое обновление кэша завершено")

        # После обновления кэша, проверяем на наличие новых пар и критические условия
        await self.notify_on_new_pairs()
        await self.check_critical_conditions()

    async def notify_on_new_pairs(self):
        """Проверяет, появились ли новые активные пары, и уведомляет администратора."""
        # Проверяем, что зависимости инициализированы
        if not self._is_initialized or not self.notifier or not self.config:
            logger.debug("Уведомления отключены: зависимости не инициализированы")
            return

        current_active_pairs = set()
        for exchange_id, pairs in self._pair_cache.items():
            for symbol, info in pairs.items():
                if info.status == PairStatus.ACTIVE:
                    current_active_pairs.add(f"{exchange_id}:{symbol}")

        # Сравниваем с предыдущим состоянием, только если оно уже было зафиксировано
        if self._last_known_active_pairs:
            newly_discovered_pairs = current_active_pairs - self._last_known_active_pairs
            if newly_discovered_pairs:
                message = "🆕 <b>Обнаружены новые активные торговые пары:</b>\n\n"
                for pair_str in sorted(list(newly_discovered_pairs)):
                    exchange, symbol = pair_str.split(':')
                    message += f"• `{symbol}` на <b>{exchange.capitalize()}</b>\n"

                logger.info(f"Обнаружены новые пары: {newly_discovered_pairs}")

                # Используем инжектированные зависимости
                try:
                    for admin_id in self.config.tg_bot.admin_ids:
                        await self.notifier.send_message(admin_id, message)
                except Exception as e:
                    logger.error(f"Ошибка отправки уведомления о новых парах: {e}")

        self._last_known_active_pairs = current_active_pairs

    async def check_critical_conditions(self):
        """Проверяет кэш на критические состояния и отправляет алерты."""
        # Проверяем, что зависимости инициализированы
        if not self._is_initialized or not self.notifier or not self.config:
            logger.debug("Алерты отключены: зависимости не инициализированы")
            return

        stats = self.get_cache_stats()
        alerts = []

        for exchange, data in stats.items():
            total_pairs = data.get('total_pairs', 0)
            if total_pairs == 0:
                continue

            unavailable_ratio = data.get('temp_unavailable', 0) / total_pairs

            # Алерт, если более 75% пар на бирже внезапно стали недоступны
            if unavailable_ratio > CRITICAL_UNAVAILABLE_PAIRS_RATIO and data.get('active_pairs',
                                                                                 0) < CRITICAL_ACTIVE_PAIRS_THRESHOLD:
                alert = f"🚨 <b>Критический алерт по бирже {exchange.capitalize()}!</b>\n" \
                        f"Более {unavailable_ratio:.0%} пар стали недоступны. " \
                        f"Возможны проблемы с API биржи."
                alerts.append(alert)

        if alerts:
            # Используем инжектированные зависимости ---
            try:
                final_alert = "\n\n".join(alerts)
                logger.warning(f"Критические состояния системы: {final_alert}")
                for admin_id in self.config.tg_bot.admin_ids:
                    await self.notifier.send_message(admin_id, final_alert)
            except Exception as e:
                logger.error(f"Ошибка отправки критических алертов: {e}")

    def get_cache_stats(self) -> Dict[str, any]:
        """Получает статистику кэша для мониторинга"""
        stats = {}
        for exchange_id, pairs in self._pair_cache.items():
            # Получаем список исключенных пар из _admin_excluded
            admin_excluded_list = sorted(list(self._admin_excluded.get(exchange_id, set())))

            temp_unavailable_list = sorted([
                p.symbol for p in pairs.values()
                if p.status == PairStatus.TEMPORARILY_UNAVAILABLE
            ])

            stats[exchange_id] = {
                'total_pairs': len(pairs),
                'active_pairs': sum(1 for p in pairs.values() if p.status == PairStatus.ACTIVE),
                'temp_unavailable': len(temp_unavailable_list),
                'admin_excluded': len(admin_excluded_list),  # Обновляем счетчик для консистентности
                'temp_unavailable_list': temp_unavailable_list,
                'admin_excluded_list': admin_excluded_list  # Используем исправленный список
            }

        return stats

    def report_trade_attempt(self, symbol: str):
        """
        Фиксирует попытку торговли по паре, активируя кулдаун.
        Этот метод нужно вызывать для ВСЕХ бирж, участвующих в сделке.
        """
        current_time = time.time()
        # Обновляем таймстемп для всех кэшей, где есть эта пара
        for exchange_id, pairs in self._pair_cache.items():
            if symbol in pairs:
                self._pair_cache[exchange_id][symbol].last_trade_attempt_time = current_time

        cooldown_minutes = SUCCESSFUL_TRADE_COOLDOWN_SECONDS / SECONDS_IN_MINUTE
        logger.info(f"⏳ Пара {symbol} отправлена в кулдаун на {cooldown_minutes:.1f} мин после попытки торговли.")

    def report_success(self, symbol: str, exchange_id: str):
        """
        Сообщает менеджеру об успешной операции с парой.
        Сбрасывает счетчик ошибок и обновляет статус на ACTIVE.
        """
        pair_info = self.get_pair_info(symbol, exchange_id)

        # Если пара восстановилась после сбоя - это важное событие для лога
        if pair_info.status == PairStatus.TEMPORARILY_UNAVAILABLE:
            logger.info(f"✅ Восстановлена пара {symbol} на {exchange_id} (была недоступна).")

        pair_info.status = PairStatus.ACTIVE
        pair_info.consecutive_failures = 0
        pair_info.failure_reason = None
        pair_info.last_success = time.time()
        pair_info.last_check = time.time()

    def report_failure(self, symbol: str, exchange_id: str, reason: str):
        """
        Сообщает менеджеру о неудачной операции с парой.
        Увеличивает счетчик ошибок и обновляет статус на TEMPORARILY_UNAVAILABLE.
        """
        pair_info = self.get_pair_info(symbol, exchange_id)

        pair_info.status = PairStatus.TEMPORARILY_UNAVAILABLE
        pair_info.consecutive_failures += 1
        pair_info.failure_reason = reason
        pair_info.last_check = time.time()

        logger.debug(
            f"❌ Зафиксирована ошибка для {symbol} на {exchange_id}: {reason}. Попыток: {pair_info.consecutive_failures}")

    def clear_cache(self, exchange_id: Optional[str] = None):
        """Очищает кэш полностью или для конкретной биржи"""
        if exchange_id:
            self._pair_cache.pop(exchange_id, None)
            logger.info(f"Кэш очищен для {exchange_id}")
        else:
            self._pair_cache.clear()
            logger.info("Кэш полностью очищен")

    def get_cache_diagnostic_info(self) -> Dict[str, any]:
        """
        НОВЫЙ МЕТОД: Получение диагностической информации о состоянии кэша
        для отладки проблем с парами.
        """
        diagnostic_info = {
            'total_exchanges': len(self._pair_cache),
            'exchanges': {},
            'global_invalid_pairs': len(self._global_invalid),
            'admin_exclusions': {}
        }

        total_pairs = 0
        total_active = 0

        for exchange_id, pairs in self._pair_cache.items():
            exchange_info = {
                'total_pairs': len(pairs),
                'active_pairs': 0,
                'temp_unavailable': 0,
                'excluded_pairs': 0,
                'unknown_pairs': 0,
                'in_cooldown': 0,
                'last_refresh': self._last_full_refresh
            }

            for symbol, pair_info in pairs.items():
                total_pairs += 1

                if pair_info.status == PairStatus.ACTIVE:
                    exchange_info['active_pairs'] += 1
                    total_active += 1
                elif pair_info.status == PairStatus.TEMPORARILY_UNAVAILABLE:
                    exchange_info['temp_unavailable'] += 1
                elif pair_info.status == PairStatus.EXCLUDED:
                    exchange_info['excluded_pairs'] += 1
                else:
                    exchange_info['unknown_pairs'] += 1

                if pair_info.is_in_cooldown:
                    exchange_info['in_cooldown'] += 1

            diagnostic_info['exchanges'][exchange_id] = exchange_info

        # Информация об админских исключениях
        for exchange_id, excluded_pairs in self._admin_excluded.items():
            diagnostic_info['admin_exclusions'][exchange_id] = len(excluded_pairs)

        diagnostic_info['totals'] = {
            'all_pairs': total_pairs,
            'active_pairs': total_active,
            'active_percentage': (total_active / max(total_pairs, 1)) * 100
        }

        return diagnostic_info

    async def force_refresh_specific_coins(self, coins: List[str],
                                           exchanges: Dict[str, any]) -> Dict[str, Dict[str, bool]]:
        """
        НОВЫЙ МЕТОД: Принудительное обновление информации о конкретных монетах.
        Полезно для диагностики проблем с конкретными парами.
        """
        logger.info(f"🔄 Принудительное обновление {len(coins)} монет на {len(exchanges)} биржах")

        results = {}

        for coin in coins:
            symbol = f"{coin}/{PRIMARY_QUOTE_CURRENCY}"
            results[symbol] = {}

            for exchange_id, service in exchanges.items():
                try:
                    # Принудительная проверка через API (игнорируя кэш)
                    is_available = await self._check_pair_availability(symbol, exchange_id, service)
                    results[symbol][exchange_id] = is_available

                    logger.debug(f"{'✅' if is_available else '❌'} {symbol} на {exchange_id}")

                except Exception as e:
                    logger.error(f"Ошибка проверки {symbol} на {exchange_id}: {e}")
                    results[symbol][exchange_id] = False

        return results

    def clear_problematic_pairs(self, min_success_rate: float = 0.1):
        """
        НОВЫЙ МЕТОД: Очистка кэша от пар с очень низким процентом успешности.
        """
        logger.info(f"🧹 Очистка проблемных пар (успешность < {min_success_rate * 100}%)")

        cleared_count = 0

        for exchange_id, pairs in list(self._pair_cache.items()):
            for symbol, pair_info in list(pairs.items()):
                # Если пара давно не была успешной и много раз падала
                if (pair_info.consecutive_failures > 5 and
                        pair_info.last_success is None and
                        pair_info.status == PairStatus.TEMPORARILY_UNAVAILABLE):
                    logger.debug(f"Удаление проблемной пары {symbol} на {exchange_id} "
                                 f"({pair_info.consecutive_failures} неудач)")
                    del pairs[symbol]
                    cleared_count += 1

        logger.info(f"Очищено {cleared_count} проблемных пар из кэша")


# Глобальный экземпляр
dynamic_pairs_manager = DynamicPairsManager()
