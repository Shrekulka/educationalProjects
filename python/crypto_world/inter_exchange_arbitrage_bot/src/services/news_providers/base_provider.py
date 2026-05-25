# inter_exchange_arbitrage_bot/src/services/news_providers/base_provider.py

import asyncio
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List, Dict, Any, Set, Optional

import httpx
import src.core.state as app_state
from src.core.config import NewsProvidersConfig, config
from src.core.resilience import APICircuitBreaker, CircuitBreakerException
from src.utils.logger import logger


class BaseNewsProvider(ABC):
    def __init__(self, name: str, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
        self.name = name
        self.config = api_config
        self.session = http_session
        self.breaker = APICircuitBreaker(service_name=self.name, failure_threshold=3, timeout=120)

        self._api_keys: List[str] = self._get_api_keys_for_provider()
        self._current_key_index: int = 0
        self._request_semaphore = asyncio.Semaphore(min(5, len(self._api_keys) * 2 if self._api_keys else 5))

    def _get_api_keys_for_provider(self) -> List[str]:
        config_field_name = self.name.lower().replace(" ", "")
        keys = getattr(self.config, config_field_name, [])
        return [key for key in keys if key]

    def _get_current_api_key(self) -> Optional[str]:
        if not self._api_keys or self._current_key_index >= len(self._api_keys):
            return None
        return self._api_keys[self._current_key_index]

    def _rotate_to_next_key(self) -> bool:
        self._current_key_index += 1
        if self._current_key_index < len(self._api_keys):
            logger.warning(f"{self.name}: Переключение на ключ #{self._current_key_index + 1}/{len(self._api_keys)}")
            return True
        else:
            logger.error(f"{self.name}: Исчерпаны все {len(self._api_keys)} API ключа.")
            return False

    def _reset_key_rotation(self):
        self._current_key_index = 0

    def _get_current_healthy_proxies(self) -> List[str]:
        """
        Получает АКТУАЛЬНЫЙ список 'здоровых' прокси из глобального менеджера.
        Вызывается перед каждым HTTP запросом.
        """
        if app_state.proxy_manager:
            proxies = app_state.proxy_manager.get_healthy_proxies()
            if proxies:
                return proxies
        return []

    async def _make_request(
            self,
            method: str,
            url: str,
            key_index: int,
            **kwargs
    ) -> httpx.Response:
        """
        ФИНАЛЬНАЯ ВЕРСИЯ: Реализует отказоустойчивую стратегию смены IP
        с возможностью полного отключения и корректной поддержкой Tor.
        """
        # --- Стратегия #0: Проверка глобального флага отключения ---
        if not config.network.ip_rotation_enabled:
            logger.debug(f"[{self.name}] (Ключ #{key_index + 1}) ➡️ Прямое соединение (ротация IP отключена).")
            return await self.session.request(method, url, **kwargs)

        # --- Стратегия #1: Прямое соединение для первого ключа ---
        if key_index == 0:
            logger.info(f"[{self.name}] (Ключ #{key_index + 1}) ➡️ Прямое соединение (первый ключ).")
            return await self.session.request(method, url, **kwargs)

        # --- Стратегия #2: Перебор всех прокси из ProxyManager ---
        if 'proxy_fallback' in config.network.ip_rotation_strategy:
            healthy_proxies = self._get_current_healthy_proxies()
            if healthy_proxies:
                logger.debug(f"[{self.name}] (Ключ #{key_index + 1}) Запускаю перебор {len(healthy_proxies)} прокси...")
                for i, proxy_str in enumerate(healthy_proxies):
                    full_proxy_url = f"http://{proxy_str}"
                    try:
                        transport = httpx.AsyncHTTPTransport(proxy=full_proxy_url)
                        # ✅ ИСПРАВЛЕНИЕ: Используем правильный таймаут из глобального конфига
                        async with httpx.AsyncClient(transport=transport,
                                                     timeout=config.network.proxy_check_timeout) as client:
                            response = await client.request(method, url, **kwargs)
                            response.raise_for_status()
                            logger.info(
                                f"[{self.name}] (Ключ #{key_index + 1}) ✅ Успешно через прокси #{i + 1} ({proxy_str})")
                            return response
                    except Exception as e:
                        logger.debug(f"[{self.name}] ❌ Прокси #{i + 1} ({proxy_str}) не сработал: {type(e).__name__}")
                        continue
            else:
                logger.warning(f"[{self.name}] (Ключ #{key_index + 1}) Список 'здоровых' прокси пуст.")

        # --- Стратегия #3: Tor (если все прокси провалились) ---
        if 'tor_fallback' in config.network.ip_rotation_strategy:
            logger.debug(f"[{self.name}] (Ключ #{key_index + 1}) Пробую стратегию 'tor_fallback'...")
            if app_state.proxy_manager and app_state.proxy_manager.is_tor_available:
                try:
                    import httpx_socks
                    transport = httpx_socks.AsyncProxyTransport.from_url(config.network.tor_proxy_url)
                    async with httpx.AsyncClient(transport=transport,
                                                 timeout=config.network.proxy_check_timeout) as client:
                        response = await client.request(method, url, **kwargs)
                        response.raise_for_status()
                        logger.info(f"[{self.name}] (Ключ #{key_index + 1}) ✅ Успешный запрос через Tor.")
                        return response
                except ImportError:
                    logger.warning(f"[{self.name}] ❌ Попытка через Tor не удалась: библиотека httpx_socks не найдена.")
                except Exception as e:
                    logger.warning(f"[{self.name}] ❌ Попытка через Tor не удалась: {type(e).__name__}")
            else:
                logger.warning(f"[{self.name}] (Ключ #{key_index + 1}) Tor недоступен или отключен.")

        # --- Стратегия #4: Прямое соединение (последняя надежда) ---
        logger.warning(
            f"[{self.name}] (Ключ #{key_index + 1}) ⚠️ Все стратегии ротации IP не сработали. Прямой запрос.")
        return await self.session.request(method, url, **kwargs)

    async def fetch(self, coins: Set[str], cutoff_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        if not self.is_configured(): return []
        logger.debug(f"ПРОВАЙДЕР [{self.name}]: Начало сбора новостей...")
        start_time = time.time()
        raw_news = []
        try:
            if self._supports_parallel_requests():
                raw_news = await self.breaker.call(self._do_fetch_parallel, coins)
            else:
                raw_news = await self.breaker.call(self._do_fetch_sequential, coins)
            elapsed = time.time() - start_time
            news_count = len(raw_news) if raw_news else 0
            logger.debug(
                f"ПРОВАЙДЕР [{self.name}]: Сбор новостей ЗАВЕРШЕН за {elapsed:.2f} сек. Найдено: {news_count} шт.")
            return self._filter_by_date(raw_news or [], cutoff_date)
        except CircuitBreakerException as e:
            logger.warning(f"[{self.name}]: Circuit Breaker открыт. Запрос прерван. {e}")
            return []
        except Exception as e:
            logger.critical(f"[{self.name}]: Критическая неперехваченная ошибка на уровне fetch: {e}", exc_info=True)
            return []

    async def _do_fetch_sequential(self, coins: Set[str]) -> List[Dict[str, Any]]:
        self._reset_key_rotation()
        while self._get_current_api_key():
            try:
                # В последовательном режиме _fetch_logic должен выбрасывать исключения для ротации
                return await self._fetch_logic(coins, self._get_current_api_key(), self._current_key_index)
            except Exception as e:
                logger.warning(f"[{self.name}] Ошибка с ключом #{self._current_key_index + 1}: {e}")
                if not self._rotate_to_next_key(): break
        logger.error(f"[{self.name}]: Ни один ключ не сработал в последовательном режиме.")
        return []

    async def _do_fetch_parallel(self, coins: Set[str]) -> List[Dict[str, Any]]:
        available_keys = self._api_keys[:]
        if not available_keys: return []
        coin_groups = self._distribute_coins_among_keys(coins, available_keys)
        tasks = []
        for i, coin_group in enumerate(coin_groups):
            if coin_group and i < len(available_keys):
                api_key = available_keys[i]
                tasks.append(self._execute_tolerant_fetch(coin_group, api_key, i))
        if not tasks: return []
        logger.debug(f"[{self.name}] Запуск параллельного режима: {len(tasks)} задач для {len(available_keys)} ключей")
        results = await asyncio.gather(*tasks)
        return [item for sublist in results if isinstance(sublist, list) for item in sublist]

    async def _execute_tolerant_fetch(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        """Безопасная обертка для параллельного режима."""
        try:
            return await self._fetch_logic(coins, api_key, key_index)
        except Exception as e:
            logger.error(
                f"[{self.name}] Изолированная ошибка в параллельной задаче (ключ #{key_index + 1}): {type(e).__name__} - {e}")
            return []

    def _distribute_coins_among_keys(self, coins: Set[str], available_keys: List[str]) -> List[Set[str]]:
        if not coins or not available_keys:
            return []
        coins_list = list(coins)
        num_keys = len(available_keys)
        coin_groups = [set() for _ in range(num_keys)]
        for i, coin in enumerate(coins_list):
            coin_groups[i % num_keys].add(coin)
        return coin_groups

    def _supports_parallel_requests(self) -> bool:
        return len(self._api_keys) > 1

    def is_configured(self) -> bool:
        return bool(self._api_keys)

    def _filter_by_date(self, news_list: List[Dict[str, Any]], cutoff_date: Optional[datetime]) -> List[Dict[str, Any]]:
        """✅ РЕАЛИЗАЦИЯ: Полная логика фильтрации по дате."""
        if not cutoff_date:
            return news_list

        fresh_news = []
        for item in news_list:
            published_at = item.get('published_at_dt')
            if not published_at or not isinstance(published_at, datetime):
                continue  # Игнорируем новости без корректной даты

            # Убеждаемся, что обе даты имеют информацию о таймзоне для корректного сравнения
            if published_at.tzinfo is None:
                published_at = published_at.replace(tzinfo=timezone.utc)
            if cutoff_date.tzinfo is None:
                cutoff_date = cutoff_date.replace(tzinfo=timezone.utc)

            if published_at >= cutoff_date:
                fresh_news.append(item)

        filtered_count = len(news_list) - len(fresh_news)
        if filtered_count > 0:
            logger.debug(f"[{self.name}]: Отфильтровано {filtered_count} старых новостей.")

        return fresh_news

    def _format_news_item(self, **kwargs) -> Dict[str, Any]:
        return {
            'title': kwargs.get('title', 'Без заголовка'),
            'body': kwargs.get('body') or kwargs.get('title', ''),
            'url': kwargs.get('url'),
            'source': self.name,
            'published_at_dt': kwargs.get('published_at_dt'),
            'image_url': kwargs.get('image_url')
        }

    @abstractmethod
    async def _fetch_logic(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
        """Единственный метод, который должны реализовать дочерние классы."""
        pass
