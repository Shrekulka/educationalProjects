# inter_exchange_arbitrage_bot/src/services/proxy_manager.py

import asyncio
import random
import re
from typing import List, Set, Optional

import httpx

from src.constants.service_constants import MAX_PROXIES_TO_TEST
from src.core.config import NetworkConfig
from src.utils.logger import logger

try:
    import httpx_socks
    SOCKS_SUPPORTED = True
except ImportError:
    SOCKS_SUPPORTED = False
    logger.warning("Библиотека 'httpx_socks' не установлена. Поддержка SOCKS-прокси будет отключена.")


class ProxyManager:
    """
    ФИНАЛЬНАЯ ВЕРСИЯ: ProxyManager с неблокирующей инициализацией через asyncio.Event
    и безопасной поддержкой SOCKS-прокси.
    """

    def __init__(self, network_config: NetworkConfig, http_session: httpx.AsyncClient):
        self.config = network_config
        self.session = http_session
        self._healthy_proxies: List[str] = []
        self._lock = asyncio.Lock()
        self._refresh_task: Optional[asyncio.Task] = None
        self._initial_scan_completed = asyncio.Event()
        self.is_tor_available: bool = False

    async def run(self):
        logger.info("ProxyManager запускается в фоновом режиме...")
        self._refresh_task = asyncio.create_task(self._refresh_loop())
        logger.info("ProxyManager: фоновая задача обновления прокси запущена.")

    async def wait_for_initial_scan(self, timeout: float = 60.0):
        try:
            logger.info(f"Ожидание первого сканирования прокси (таймаут: {timeout}с)...")
            await asyncio.wait_for(self._initial_scan_completed.wait(), timeout=timeout)
            logger.info("Первое сканирование прокси успешно завершено.")
            return True
        except asyncio.TimeoutError:
            logger.warning(f"Таймаут ожидания первого сканирования прокси ({timeout}с).")
            self._initial_scan_completed.set()
            return False

    async def _refresh_loop(self):
        try:
            await self.refresh_proxies()
        except Exception as e:
            logger.error(f"ProxyManager: Ошибка во время первого сканирования: {e}", exc_info=True)
        finally:
            self._initial_scan_completed.set()

        while True:
            try:
                await asyncio.sleep(self.config.proxy_refresh_interval_seconds)
                await self.refresh_proxies()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"ProxyManager: критическая ошибка в цикле обновления: {e}", exc_info=True)

    async def _check_tor_availability(self):
        """
        АРГУМЕНТАЦИЯ: Новая функция для проверки доступности Tor в реальном времени.
        Вызывается при каждом обновлении, чтобы статус был всегда актуальным.
        """
        if not self.config.tor_proxy_enabled or not SOCKS_SUPPORTED:
            self.is_tor_available = False
            return

        logger.debug("Проверка доступности Tor-прокси...")
        try:
            transport = httpx_socks.AsyncProxyTransport.from_url(self.config.tor_proxy_url)
            async with httpx.AsyncClient(transport=transport, timeout=self.config.proxy_check_timeout) as client:
                response = await client.get(self.config.proxy_check_url)
                response.raise_for_status()
                if response.json().get('ip'):
                    logger.info("✅ Tor-прокси доступен и работает.")
                    self.is_tor_available = True
                else:
                    raise Exception("Tor-прокси не вернул IP-адрес")
        except Exception as e:
            logger.warning(f"⚠️ Tor-прокси недоступен. Ошибка: {type(e).__name__}")
            self.is_tor_available = False

    async def _test_proxy(self, proxy: str) -> Optional[str]:
        protocols_to_try = ["http://"]
        if SOCKS_SUPPORTED:
            protocols_to_try.extend(["socks5://", "socks4://"])

        for protocol in protocols_to_try:
            full_proxy_url = f"{protocol}{proxy}"
            try:
                if protocol.startswith("socks"):
                    transport = httpx_socks.AsyncProxyTransport.from_url(full_proxy_url)
                else:
                    transport = httpx.AsyncHTTPTransport(proxy=full_proxy_url)

                async with httpx.AsyncClient(transport=transport, timeout=self.config.proxy_check_timeout) as client:
                    response = await client.get(self.config.proxy_check_url)
                    response.raise_for_status()
                    if response.json().get('ip'):
                        logger.debug(f"✅ Рабочий прокси: {proxy} ({protocol.strip('://')})")
                        return proxy
            except Exception:
                # logger.debug(f"Прокси {proxy} с протоколом {protocol.strip('://')} не работает.")
                continue
        return None

    async def refresh_proxies(self):
        """Обновляет список прокси и проверяет доступность Tor."""
        logger.info("ProxyManager: Начинаю обновление списка прокси...")

        # АРГУМЕНТАЦИЯ: Проверяем Tor в начале каждого цикла обновления.
        await self._check_tor_availability()

        async with self._lock:
            # (остальной код метода refresh_proxies остается без изменений)
            fetch_tasks = [self._fetch_proxies_from_source(url) for url in self.config.proxy_sources]
            results = await asyncio.gather(*fetch_tasks)

            raw_proxies = set.union(*results) if results else set()
            if not raw_proxies:
                logger.error("ProxyManager: Не удалось загрузить прокси ни из одного источника.")
                self._healthy_proxies = []
                return

            logger.info(f"Загружено {len(raw_proxies)} уникальных прокси.")

            proxies_to_test = list(raw_proxies)
            if len(raw_proxies) > MAX_PROXIES_TO_TEST:
                logger.info(f"Слишком много прокси. Выбираю случайные {MAX_PROXIES_TO_TEST} из {len(raw_proxies)}.")
                proxies_to_test = random.sample(proxies_to_test, MAX_PROXIES_TO_TEST)

            logger.info(f"Начинаю тестирование {len(proxies_to_test)} прокси...")

            test_tasks = [self._test_proxy(p) for p in proxies_to_test]
            test_results = await asyncio.gather(*test_tasks)

            healthy_proxies = [p for p in test_results if p]

            if healthy_proxies:
                random.shuffle(healthy_proxies)
                self._healthy_proxies = healthy_proxies
                logger.info(f"✅ ProxyManager: Найдено {len(self._healthy_proxies)} рабочих прокси.")
            else:
                self._healthy_proxies = []
                logger.warning("ProxyManager: Не найдено ни одного рабочего прокси после тестирования.")

    async def _fetch_proxies_from_source(self, url: str) -> Set[str]:
        try:
            response = await self.session.get(url, timeout=15)
            response.raise_for_status()
            proxy_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\b')
            return set(proxy_pattern.findall(response.text))
        except Exception as e:
            logger.warning(f"Не удалось загрузить прокси с {url}: {e}")
            return set()

    def get_healthy_proxies(self) -> List[str]:
        if not self._healthy_proxies:
            logger.debug("ProxyManager: список 'здоровых' прокси пуст.")
        return self._healthy_proxies.copy()

    async def stop(self):
        if self._refresh_task and not self._refresh_task.done():
            self._refresh_task.cancel()
            try: await self._refresh_task
            except asyncio.CancelledError: pass
            logger.info("ProxyManager: фоновая задача обновления остановлена.")
