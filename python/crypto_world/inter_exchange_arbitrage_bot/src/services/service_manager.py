# inter_exchange_arbitrage_bot/src/services/service_manager.py

import asyncio
import time
from contextlib import asynccontextmanager
from typing import Dict, Optional, Set, List, Tuple

import ccxt.async_support as ccxt

import src.core.state as app_state
from src.constants.api_constants import (
    GET_BALANCE_TIMEOUT_SECONDS, SERVICE_HEALTH_CHECK_TIMEOUT_SECONDS,
    SERVICE_INITIALIZATION_TIMEOUT_SECONDS, HEALTH_CHECK_INTERVAL_SECONDS, MARKETS_CACHE_TTL_SECONDS,
    MARKETS_LOAD_TIMEOUT_SECONDS
)
from src.constants.trading_constants import (MIN_EXCHANGES_FOR_ARBITRAGE, DYNAMIC_PAIRS_CONFIG, PRIMARY_QUOTE_CURRENCY,
                                             MARKET_FIELD_BASE, MARKET_FIELD_QUOTE, MARKET_FIELD_SPOT)
from src.services.blacklist_manager import blacklist_manager
from src.services.dynamic_pairs_manager import dynamic_pairs_manager
from src.services.exchange_service import ExchangeService
from src.utils.helpers import get_configured_exchanges
from src.utils.logger import logger


class ServiceManager:
    """
    Singleton-менеджер для централизованного управления сервисами бирж.

    Этот класс гарантирует, что для каждой биржи существует только один
    экземпляр сервиса на протяжении всей жизни приложения. Он управляет
    инициализацией, проверкой "здоровья" и корректным завершением работы сервисов.
    """
    _instance: Optional['ServiceManager'] = None
    _initialized: bool = False

    def __new__(cls) -> 'ServiceManager':
        # Реализация паттерна Singleton, чтобы гарантировать единственный экземпляр.
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # __init__ вызывается при каждом обращении к ServiceManager(),
        # поэтому используем флаг _initialized для однократной инициализации.
        if not self._initialized:
            self.services: Dict[str, ExchangeService] = {}  # Словарь всех созданных сервисов.
            self.healthy_services: Set[str] = set()  # Множество ID только "здоровых" сервисов.
            self.markets_cache: Dict[str, Tuple[Dict, float]] = {}  # (data, timestamp)
            self.last_health_check: Optional[float] = None  # Временная метка последней проверки здоровья.
            self._lock = asyncio.Lock()  # Блокировка для защиты от гонок при инициализации.
            ServiceManager._initialized = True

    async def initialize(self, force_refresh: bool = False) -> None:
        """
        Инициализирует все настроенные в .env сервисы бирж.

        Выполняет тест соединения для каждой биржи и, если успешно,
        инициализирует кэш торговых пар и черный список бирж.

        Args:
            force_refresh: Если True, принудительно закроет старые и создаст новые соединения.
        """
        # Блокируем, чтобы избежать двойной инициализации из разных частей программы.
        async with self._lock:
            # Если сервисы уже созданы и не требуется принудительное обновление, выходим.
            if self.services and not force_refresh:
                logger.debug("ServiceManager уже инициализирован, пропускаю.")
                return

            logger.info("🔧 Инициализация ServiceManager...")

            # Если требуется, сначала корректно закрываем все существующие соединения.
            if force_refresh and self.services:
                await self._close_all_services()

            # Получаем список бирж, для которых есть API-ключи в .env.
            configured_exchanges = get_configured_exchanges()
            logger.info(f"Найдено настроенных бирж: {configured_exchanges}")

            init_tasks = []
            for ex_id in configured_exchanges:
                init_tasks.append(self._initialize_single_service(ex_id))
                # Даем event loop'у шанс обработать другие задачи после добавления каждой новой
                await asyncio.sleep(0)

            results = await asyncio.gather(*init_tasks, return_exceptions=True)
            successful = sum(1 for r in results if r is True)
            logger.info(f"✅ ServiceManager: инициализировано {successful}/{len(configured_exchanges)} сервисов")

            # НОВОЕ: Инициализируем BlacklistManager после успешной инициализации сервисов
            if self.services:
                logger.info("🔄 Построение динамического черного списка бирж...")
                await blacklist_manager.build_blacklist(self.services, force_rebuild=force_refresh)

                # Выводим статистику BlacklistManager
                stats = blacklist_manager.get_statistics()
                logger.info(
                    f"📊 Статистика пакетной поддержки: "
                    f"{stats['supported']}/{stats['total_tested']} бирж поддерживают пакетные запросы"
                )

            # Кэш торговых пар имеет смысл только если у нас есть хотя бы 2 биржи для арбитража.
            if successful >= MIN_EXCHANGES_FOR_ARBITRAGE:
                logger.info("🔄 Инициализация кэша торговых пар...")
                await self._initialize_pairs_cache()

    async def _initialize_pairs_cache(self):
        """
        ИСПРАВЛЕНО: Теперь этот метод также кэширует рынки.
        """
        try:
            healthy_services = {ex_id: s for ex_id, s in self.services.items() if ex_id in self.healthy_services}

            cache_tasks = []
            for ex_id, service in healthy_services.items():
                # Создаем одну задачу на биржу, которая сделает две вещи
                cache_tasks.append(self._load_and_cache_markets_for_exchange(ex_id, service))

            results = await asyncio.gather(*cache_tasks, return_exceptions=True)

            successful_caches = sum(1 for r in results if isinstance(r, dict) and r)
            logger.info(f"✅ Кэш пар инициализирован для {successful_caches} бирж")
        except Exception as e:
            logger.error(f"Ошибка инициализации кэша пар: {e}")

    async def _load_and_cache_markets_for_exchange(self, exchange_id: str, service: ExchangeService):
        try:
            # Оборачиваем медленный вызов в собственный тайм-аут
            markets = await asyncio.wait_for(
                service.client.load_markets(True),
                timeout=MARKETS_LOAD_TIMEOUT_SECONDS
            )

            self.markets_cache[exchange_id] = (markets, time.monotonic())
            return await dynamic_pairs_manager.bulk_update_exchange_pairs(exchange_id, service)

        # Явно ловим ОБА типа ошибок тайм-аута
        except (asyncio.TimeoutError, ccxt.RequestTimeout) as e:
            logger.error(
                f"⏰ Таймаут ({MARKETS_LOAD_TIMEOUT_SECONDS}с) при загрузке рынков с {exchange_id}. "
                f"Биржа будет пропущена на этом этапе. Ошибка: {type(e).__name__}"
            )
            self.markets_cache.pop(exchange_id, None)
            return {}

        except Exception as e:
            logger.error(f"Ошибка загрузки рынков для {exchange_id}: {type(e).__name__} - {e}")
            self.markets_cache.pop(exchange_id, None)
            return {}

    async def get_markets(self, exchange_id: str) -> Dict:
        """Получает рынки для биржи, обновляя кэш, если он устарел."""
        cache_entry = self.markets_cache.get(exchange_id)
        if cache_entry:
            data, timestamp = cache_entry
            if time.monotonic() - timestamp < MARKETS_CACHE_TTL_SECONDS:
                return data

        logger.info(f"Кэш рынков для {exchange_id} устарел или отсутствует. Обновляю...")
        service = self.services.get(exchange_id)
        if service:
            await self._load_and_cache_markets_for_exchange(exchange_id, service)
            # Возвращаем только данные, без временной метки
            return self.markets_cache.get(exchange_id, ({}, 0))[0]
        return {}

    async def start_background_refresh(self):
        """Запускает фоновую задачу для периодического обновления кэша пар."""

        async def refresh_loop():
            while True:
                try:
                    await asyncio.sleep(DYNAMIC_PAIRS_CONFIG['background_refresh_interval'])

                    # Используем правильную блокировку
                    async with app_state.cache_refresh_lock:
                        healthy_services = {ex_id: s for ex_id, s in self.services.items() if
                                            ex_id in self.healthy_services}
                        if healthy_services:
                            await dynamic_pairs_manager.periodic_refresh(healthy_services)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Ошибка в фоновом обновлении пар: {e}")

        # Создаем и запускаем фоновую задачу, которая не блокирует основной поток.
        asyncio.create_task(refresh_loop())
        logger.info("🔄 Фоновое обновление кэша пар запущено")

    async def _initialize_single_service(self, exchange_id: str) -> bool:
        """
        ФИНАЛЬНАЯ ВЕРСИЯ: Инициализирует и проверяет сервис для одной биржи
        с гарантированной очисткой ресурсов в случае любой неудачи.
        """
        service = None
        try:
            logger.debug(f"Инициализация сервиса {exchange_id}...")
            # Создаем экземпляр. В этот момент может быть создана aiohttp сессия внутри ccxt.
            service = ExchangeService(exchange_id)

            # Тестируем соединение с таймаутом.
            connection_test = await asyncio.wait_for(
                service.test_connection(),
                timeout=SERVICE_INITIALIZATION_TIMEOUT_SECONDS
            )

            if connection_test:
                # Только в случае полного успеха добавляем сервис в менеджер.
                self.services[exchange_id] = service
                self.healthy_services.add(exchange_id)
                logger.info(f"✅ {exchange_id}: сервис готов к работе")
                return True
            else:
                # Если тест соединения не пройден, сервис не добавляется,
                # и блок finally корректно закроет его.
                logger.warning(f"❌ {exchange_id}: тест соединения не пройден")
                return False

        except Exception as e:
            # Ловим абсолютно любую ошибку во время инициализации.
            logger.error(f"💥 {exchange_id}: критическая ошибка инициализации: {e}")
            return False
        finally:
            # Этот блок выполнится всегда, даже если были ошибки.
            # Если сервис был создан (service is not None), но не был успешно добавлен
            # в self.services, значит что-то пошло не так, и его ресурсы нужно освободить.
            if service and exchange_id not in self.services:
                logger.debug(f"Очистка ресурсов для неудачно инициализированного сервиса {exchange_id}...")
                await service.close()

    async def get_healthy_services(self) -> Dict[str, ExchangeService]:
        """Возвращает словарь только со "здоровыми", работающими сервисами."""
        current_time = asyncio.get_event_loop().time()
        # Запускаем проверку, если она еще не проводилась или прошел заданный интервал.
        if self.last_health_check is None or (current_time - self.last_health_check > HEALTH_CHECK_INTERVAL_SECONDS):
            await self._health_check()
        return {ex_id: s for ex_id, s in self.services.items() if ex_id in self.healthy_services}

    async def _health_check(self) -> None:
        """Выполняет быструю параллельную проверку здоровья всех сервисов."""
        if not self.services: return
        logger.debug("🔍 Выполняю health check сервисов...")
        # Собираем задачи для параллельного выполнения.
        health_tasks = [self._check_service_health(ex_id, s) for ex_id, s in self.services.items()]
        results = await asyncio.gather(*health_tasks, return_exceptions=True)
        # Формируем новое множество "здоровых" сервисов на основе результатов.
        new_healthy = {ex_id for ex_id, res in zip(self.services.keys(), results) if res is True}
        # Если состав "здоровых" сервисов изменился, логируем это.
        if new_healthy != self.healthy_services:
            unhealthy, recovered = self.healthy_services - new_healthy, new_healthy - self.healthy_services
            if unhealthy: logger.warning(f"🚨 Сервисы стали недоступны: {unhealthy}")
            if recovered: logger.info(f"💚 Сервисы восстановились: {recovered}")
        # Обновляем состояние.
        self.healthy_services = new_healthy
        self.last_health_check = asyncio.get_event_loop().time()
        logger.debug(f"Health check завершен. Здоровых сервисов: {len(self.healthy_services)}")

    async def _check_service_health(self, exchange_id: str, service: ExchangeService) -> bool:
        """Проверяет доступность одного сервиса с таймаутом."""
        try:
            is_healthy = await asyncio.wait_for(
                service.test_connection(), timeout=SERVICE_HEALTH_CHECK_TIMEOUT_SECONDS
            )
            return is_healthy
        except Exception as e:
            logger.debug(f"Health check для {exchange_id} провален: {type(e).__name__}")
            return False

    async def get_all_balances(self) -> Dict[str, Dict[str, float]]:
        """Получает балансы со всех здоровых сервисов параллельно."""
        healthy_services = await self.get_healthy_services()
        if not healthy_services:
            logger.warning("Нет здоровых сервисов для получения балансов")
            return {}
        balance_tasks, exchange_ids = [], []
        for ex_id, service in healthy_services.items():
            task = asyncio.wait_for(service.get_balance(), timeout=GET_BALANCE_TIMEOUT_SECONDS)
            balance_tasks.append(task)
            exchange_ids.append(ex_id)
        results = await asyncio.gather(*balance_tasks, return_exceptions=True)
        all_balances = {}
        for ex_id, result in zip(exchange_ids, results):
            if isinstance(result, dict):
                all_balances[ex_id] = result
                logger.debug(f"✅ Баланс получен с {ex_id}")
            else:
                logger.warning(f"❌ Ошибка получения баланса с {ex_id}: {type(result).__name__}")
                # Если биржа не отдала баланс, временно считаем ее нездоровой.
                self.healthy_services.discard(ex_id)
        return all_balances

    def get_all_spot_assets_from_cache(self) -> List[str]:
        if not self.markets_cache:
            logger.warning("Попытка получить активы из пустого кэша рынков.")
            return []

        all_assets = set()
        # Итерируемся по данным, которые уже прошли проверку TTL или были только что обновлены
        for exchange_id, (markets, _) in self.markets_cache.items():
            if not isinstance(markets, dict): continue

            for market_data in markets.values():
                is_spot = market_data.get(MARKET_FIELD_SPOT, False)
                quote_currency = market_data.get(MARKET_FIELD_QUOTE, '')

                if is_spot and quote_currency == PRIMARY_QUOTE_CURRENCY:
                    base_currency = market_data.get(MARKET_FIELD_BASE)
                    if base_currency:
                        all_assets.add(base_currency)

        logger.debug(f"Извлечено {len(all_assets)} уникальных активов из кэша ServiceManager.")
        return sorted(list(all_assets))

    async def _close_all_services(self) -> None:
        """
        ФИНАЛЬНАЯ ВЕРСИЯ: Явно закрывает каждый сервис перед очисткой.
        """
        if not self.services:
            return

        logger.info(f"🔄 Закрытие {len(self.services)} сервисных соединений...")

        # Создаем задачи для параллельного вызова метода .close() у каждого сервиса
        close_tasks = [service.close() for service in self.services.values()]

        # Выполняем все задачи параллельно с обработкой исключений
        await asyncio.gather(*close_tasks, return_exceptions=True)

        # Теперь, когда все соединения гарантированно закрыты, можно очищать коллекции
        self.services.clear()
        self.healthy_services.clear()
        logger.info("✅ Все сервисы бирж остановлены и их соединения закрыты.")

    async def shutdown(self) -> None:
        """Полностью останавливает менеджер и очищает все ресурсы."""
        async with self._lock:
            logger.info("🛑 Начало процедуры shutdown для ServiceManager...")
            await self._close_all_services()
            logger.info("✅ ServiceManager корректно отключен")

    @property
    def is_ready_for_arbitrage(self) -> bool:
        """Проверяет, готово ли приложение к арбитражу (достаточно ли здоровых бирж)."""
        return len(self.healthy_services) >= MIN_EXCHANGES_FOR_ARBITRAGE

    async def rebuild_blacklist(self) -> None:
        """
        НОВЫЙ МЕТОД: Принудительно пересобирает черный список бирж.
        Полезно для обновления после изменений в библиотеке ccxt.
        """
        if self.services:
            await blacklist_manager.force_rebuild(self.services)
        else:
            logger.warning("Нет активных сервисов для пересборки черного списка")


# Глобальный экземпляр для использования во всем приложении
service_manager = ServiceManager()


@asynccontextmanager
async def managed_services():
    """Контекстный менеджер для автоматического управления жизненным циклом ServiceManager."""
    await service_manager.initialize()
    try:
        yield service_manager
    finally:
        # В этой простой реализации cleanup не требуется, так как shutdown вызывается в lifespan.
        pass


