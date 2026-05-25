# inter_exchange_arbitrage_bot/src/core/enhanced_ai_resilience.py

import asyncio
import re
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Callable, Any, Set

from src.constants.api_constants import AI_FAILOVER_ATTEMPT_DELAY_SECONDS, AI_PROVIDER_SEMAPHORES
from src.utils import logger


class ProviderStatus(Enum):
    AVAILABLE = "available"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"
    UNAVAILABLE = "unavailable"


@dataclass
class TokenUsage:
    """Трекинг использования токенов"""
    used_tokens: int = 0
    estimated_tokens: int = 0
    reset_time: float = 0
    limit_per_minute: int = 6000

    def can_handle_request(self, estimated_tokens: int) -> bool:
        current_time = time.time()
        if current_time >= self.reset_time:
            self.used_tokens = 0
            self.reset_time = current_time + 60

        return (self.used_tokens + estimated_tokens) <= (self.limit_per_minute * 0.85)


@dataclass
class ProviderConfig:
    """Конфигурация AI-провайдера"""
    name: str
    api_key: str
    model: str
    tokens_per_minute: int
    max_tokens_per_request: int
    base_delay: float
    priority: int


class EnhancedAIRateLimitManager:
    def __init__(self):
        self.providers: Dict[str, ProviderConfig] = {}
        self.provider_states: Dict[str, Dict] = {}
        self._token_usage: Dict[str, TokenUsage] = {}
        self._max_wait_cycles = 3
        self._wait_cycle_base_duration = 15.0
        self._semaphores = {
            name: asyncio.Semaphore(limit)
            for name, limit in AI_PROVIDER_SEMAPHORES.items()
        }
        self._default_semaphore = self._semaphores['default']

    def register_provider(self, config: ProviderConfig):
        """Регистрация AI-провайдера с его лимитами"""
        self.providers[config.name] = config
        self.provider_states[config.name] = {
            'status': ProviderStatus.AVAILABLE,
            'rate_limit_until': 0,
            'failure_count': 0,
            'last_success': time.time(),
            'consecutive_429s': 0
        }
        self._token_usage[config.name] = TokenUsage(limit_per_minute=config.tokens_per_minute)

    def estimate_tokens(self, text: str) -> int:
        """Примерная оценка количества токенов в тексте"""
        char_count = len(text)
        if any(ord(c) > 127 for c in text):
            return int(char_count * 0.4)
        return int(char_count * 0.25)

    def get_best_available_provider(self, estimated_tokens: int, excluded_providers: Optional[Set[str]] = None) -> \
            Optional[str]:
        """Выбирает лучший доступный провайдер для запроса"""
        current_time, available_providers, excluded = time.time(), [], excluded_providers or set()
        for name, config in self.providers.items():
            if name in excluded:
                continue
            state = self.provider_states[name]
            if state['rate_limit_until'] > current_time or not self._token_usage[name].can_handle_request(
                    estimated_tokens):
                continue
            available_providers.append((name, config.priority, state['failure_count']))
        if not available_providers:
            return None
        available_providers.sort(key=lambda x: (x[1], x[2]))
        return available_providers[0][0]

    async def execute_with_failover(self, request_func: Callable, prompt: str, **kwargs) -> Any:
        """Выполняет запрос, используя несколько циклов ожидания."""
        estimated_tokens = self.estimate_tokens(prompt)
        last_error = None

        for cycle in range(self._max_wait_cycles):
            logger.debug(f"Цикл отказоустойчивости {cycle + 1}/{self._max_wait_cycles}...")

            excluded_in_this_cycle: Set[str] = set()
            for _ in range(len(self.providers)):
                provider_name = self.get_best_available_provider(estimated_tokens,
                                                                 excluded_providers=excluded_in_this_cycle)

                if not provider_name:
                    break

                try:
                    result = await self._attempt_single_provider(provider_name, request_func, prompt, estimated_tokens,
                                                                 **kwargs)
                    logger.info(f"Запрос успешно выполнен через {provider_name} на цикле {cycle + 1}.")
                    return result
                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"Быстрый failover: {provider_name} не справился ({type(e).__name__}). Пробую следующего.")
                    await self._handle_provider_error(provider_name, e, estimated_tokens)
                    excluded_in_this_cycle.add(provider_name)
                    logger.debug(f"Пауза {AI_FAILOVER_ATTEMPT_DELAY_SECONDS}с перед следующей попыткой failover...")
                    await asyncio.sleep(AI_FAILOVER_ATTEMPT_DELAY_SECONDS)

            if cycle < self._max_wait_cycles - 1:
                wait_time = self._get_intelligent_wait_time(cycle)
                logger.warning(f"Все AI-провайдеры недоступны. Пауза {wait_time:.1f}с перед циклом #{cycle + 2}.")
                await asyncio.sleep(wait_time)

        logger.error("Все циклы ожидания исчерпаны. Не удалось обработать запрос.")
        raise Exception(
            f"Не удалось выполнить запрос после {self._max_wait_cycles} циклов. Последняя ошибка: {last_error}")

    async def _attempt_single_provider(self, provider_name: str, request_func: Callable, prompt: str,
                                       estimated_tokens: int, **kwargs) -> Any:
        provider_type = provider_name.split('-')[0].lower()  # 'Gemini-1-model_x' -> 'gemini'
        semaphore = self._semaphores.get(provider_type, self._default_semaphore)
        async with semaphore:
            config = self.providers[provider_name]

            api_key = config.api_key
            masked_key = f"sk-...{api_key[-4:]}" if "sk-" in api_key else f"{api_key[:4]}...{api_key[-4:]}"
            logger.debug(f"AI_REQUEST -> Provider: {config.name} | Key: {masked_key} | Model: {config.model}")

            await asyncio.sleep(config.base_delay)
            self._token_usage[provider_name].used_tokens += estimated_tokens

            try:
                result = await request_func(provider_name_override=provider_name, prompt=prompt, **kwargs)
                self._handle_success(provider_name)
                return result
            except Exception:
                self._token_usage[provider_name].used_tokens = max(0, self._token_usage[
                    provider_name].used_tokens - estimated_tokens)
                raise

    def _get_intelligent_wait_time(self, current_cycle: int) -> float:
        """Вычисляет время ожидания."""
        shortest_wait = self._get_shortest_wait_time()
        if shortest_wait > 0:
            return min(shortest_wait + 5.0, self._wait_cycle_base_duration * (current_cycle + 2))
        return self._wait_cycle_base_duration * (2 ** current_cycle)

    def _get_shortest_wait_time(self) -> float:
        """Возвращает время до разблокирования ближайшего провайдера"""
        current_time = time.time()
        wait_times = [
            state['rate_limit_until'] - current_time
            for state in self.provider_states.values()
            if state['rate_limit_until'] > current_time
        ]
        return min(wait_times) if wait_times else 0

    def _handle_success(self, provider_name: str):
        """ДОПОЛНЕННАЯ ВЕРСИЯ: Обрабатывает успешный запрос с полным сбросом."""
        state = self.provider_states[provider_name]
        if state['status'] != ProviderStatus.AVAILABLE:
            logger.info(f"RECOVERY: Провайдер {provider_name} восстановил работу.")

        state['failure_count'] = 0
        state['consecutive_429s'] = 0
        state['last_success'] = time.time()
        state['status'] = ProviderStatus.AVAILABLE
        state['rate_limit_until'] = 0

    def _extract_error_code_safe(self, error_str: str) -> str:
        """Безопасное извлечение HTTP кода с несколькими стратегиями."""
        patterns = [
            r'[\'"](\d{3})[\'"]',  # '503' или "503"
            r'\((\d{3})\)',  # (503)
            r'error[:\s]+(\d{3})',  # error: 503 или error 503
            r'status[:\s]+(\d{3})',  # status: 503
            r'(\d{3})\s+\w+',  # 503 Service
        ]
        for pattern in patterns:
            match = re.search(pattern, error_str)
            if match:
                return match.group(1)
        return 'N/A'

    async def _handle_provider_error(self, provider_name: str, error: Exception, estimated_tokens: int):
        """ФИНАЛЬНАЯ ВЕРСИЯ: Обработка ошибок с надежным парсингом и структурированным логированием."""
        state = self.provider_states[provider_name]
        state['failure_count'] += 1
        error_str = str(error).lower()
        error_code = self._extract_error_code_safe(error_str)

        if error_code.startswith('4') and error_code != '429':
            block_duration = 3600
            state['rate_limit_until'] = time.time() + block_duration
            state['status'] = ProviderStatus.UNAVAILABLE
            logger.critical(
                f"CRITICAL_CONFIG_ERROR {provider_name}: Client error {error_code}. "
                f"Check .env configuration (API key/model). "
                f"Provider blocked for 1h. Error: {str(error)[:200]}"
            )

        elif error_code == '429' or "rate limit" in error_str:
            state['consecutive_429s'] += 1
            wait_time = self._extract_wait_time_from_error(error_str)
            block_duration = (wait_time + 5) if wait_time else min(300, 30 * (2 ** state['consecutive_429s']))
            state['rate_limit_until'] = time.time() + block_duration
            state['status'] = ProviderStatus.RATE_LIMITED
            logger.warning(f"RATE_LIMIT {provider_name}: Blocked for {block_duration:.1f}s")
            self._token_usage[provider_name].used_tokens = max(0,
                                                               self._token_usage[
                                                                   provider_name].used_tokens - estimated_tokens)

        elif error_code.startswith('5'):
            block_duration = min(90, 15 * state['failure_count'])
            state['rate_limit_until'] = time.time() + block_duration
            state['status'] = ProviderStatus.ERROR
            logger.warning(
                f"SERVER_TEMP_ERROR {provider_name}: Server error {error_code}. "
                f"Retry in {block_duration:.1f}s. Attempt #{state['failure_count']}"
            )

        else:
            block_duration = min(120, 30 * state['failure_count'])
            state['rate_limit_until'] = time.time() + block_duration
            state['status'] = ProviderStatus.ERROR
            logger.error(
                f"UNKNOWN_ERROR {provider_name}: Code {error_code}. "
                f"Retry in {block_duration:.1f}s. Error: {str(error)[:200]}"
            )

    def _extract_wait_time_from_error(self, error_str: str) -> Optional[float]:
        """Извлекает время ожидания из сообщения об ошибке"""
        match = re.search(r'try again in ([\d.]+)s', error_str)
        if match:
            return float(match.group(1))
        return None

    def get_status_report(self) -> Dict[str, Any]:
        """Возвращает подробный отчет о состоянии всех провайдеров"""
        current_time = time.time()
        report = {}

        for name, state in self.provider_states.items():
            token_usage = self._token_usage[name]
            report[name] = {
                'status': state['status'].value,
                'available': state['rate_limit_until'] <= current_time,
                'tokens_used': token_usage.used_tokens,
                'tokens_limit': token_usage.limit_per_minute,
                'utilization': f"{(token_usage.used_tokens / token_usage.limit_per_minute) * 100:.1f}%" if token_usage.limit_per_minute > 0 else "0.0%",
                'failure_count': state['failure_count'],
                'blocked_until': state['rate_limit_until'] if state['rate_limit_until'] > current_time else None,
            }

        return report


enhanced_ai_manager = EnhancedAIRateLimitManager()


# import asyncio
# import re
# import time
# from dataclasses import dataclass
# from enum import Enum
# from typing import Dict, Optional, Callable, Any, Set
#
# from src.constants.api_constants import AI_FAILOVER_ATTEMPT_DELAY_SECONDS
# from src.utils import logger
#
#
# class ProviderStatus(Enum):
#     AVAILABLE = "available"
#     RATE_LIMITED = "rate_limited"
#     ERROR = "error"
#     UNAVAILABLE = "unavailable"
#
#
# @dataclass
# class TokenUsage:
#     """Трекинг использования токенов"""
#     used_tokens: int = 0
#     estimated_tokens: int = 0
#     reset_time: float = 0
#     limit_per_minute: int = 6000
#
#     def can_handle_request(self, estimated_tokens: int) -> bool:
#         current_time = time.time()
#         if current_time >= self.reset_time:
#             self.used_tokens = 0
#             self.reset_time = current_time + 60
#
#         return (self.used_tokens + estimated_tokens) <= (self.limit_per_minute * 0.85)
#
#
# @dataclass
# class ProviderConfig:
#     """Конфигурация AI-провайдера"""
#     name: str
#     api_key: str
#     model: str
#     tokens_per_minute: int
#     max_tokens_per_request: int
#     base_delay: float
#     priority: int
#
#
# class EnhancedAIRateLimitManager:
#     def __init__(self):
#         self.providers: Dict[str, ProviderConfig] = {}
#         self.provider_states: Dict[str, Dict] = {}
#         self._token_usage: Dict[str, TokenUsage] = {}
#         self._global_semaphore = asyncio.Semaphore(2)
#         self._max_wait_cycles = 3
#         self._wait_cycle_base_duration = 15.0
#
#     def register_provider(self, config: ProviderConfig):
#         """Регистрация AI-провайдера с его лимитами"""
#         self.providers[config.name] = config
#         self.provider_states[config.name] = {
#             'status': ProviderStatus.AVAILABLE,
#             'rate_limit_until': 0,
#             'failure_count': 0,
#             'last_success': time.time(),
#             'consecutive_429s': 0
#         }
#         self._token_usage[config.name] = TokenUsage(limit_per_minute=config.tokens_per_minute)
#
#     def estimate_tokens(self, text: str) -> int:
#         """Примерная оценка количества токенов в тексте"""
#         char_count = len(text)
#         if any(ord(c) > 127 for c in text):
#             return int(char_count * 0.4)
#         return int(char_count * 0.25)
#
#     def get_best_available_provider(self, estimated_tokens: int, excluded_providers: Optional[Set[str]] = None) -> \
#     Optional[str]:
#         """Выбирает лучший доступный провайдер для запроса"""
#         current_time, available_providers, excluded = time.time(), [], excluded_providers or set()
#         for name, config in self.providers.items():
#             if name in excluded:
#                 continue
#             state = self.provider_states[name]
#             if state['rate_limit_until'] > current_time or not self._token_usage[name].can_handle_request(
#                     estimated_tokens):
#                 continue
#             available_providers.append((name, config.priority, state['failure_count']))
#         if not available_providers:
#             return None
#         available_providers.sort(key=lambda x: (x[1], x[2]))
#         return available_providers[0][0]
#
#     async def execute_with_failover(self, request_func: Callable, prompt: str, **kwargs) -> Any:
#         """Выполняет запрос, используя несколько циклов ожидания."""
#         estimated_tokens = self.estimate_tokens(prompt)
#         last_error = None
#
#         for cycle in range(self._max_wait_cycles):
#             logger.debug(f"Цикл отказоустойчивости {cycle + 1}/{self._max_wait_cycles}...")
#
#             excluded_in_this_cycle: Set[str] = set()
#
#             for _ in range(len(self.providers)):
#                 provider_name = self.get_best_available_provider(estimated_tokens,
#                                                                  excluded_providers=excluded_in_this_cycle)
#
#                 if not provider_name:
#                     break
#
#                 try:
#                     result = await self._attempt_single_provider(provider_name, request_func, prompt, estimated_tokens,
#                                                                  **kwargs)
#                     logger.info(f"Запрос успешно выполнен через {provider_name} на цикле {cycle + 1}.")
#                     return result
#
#                 except Exception as e:
#                     last_error = e
#                     logger.warning(f"Быстрый failover: {provider_name} не справился ({e}). Пробую следующего.")
#                     await self._handle_provider_error(provider_name, e, estimated_tokens)
#                     excluded_in_this_cycle.add(provider_name)
#
#                     # Делаем короткую паузу перед следующей попыткой внутри цикла.
#                     logger.debug(f"Пауза {AI_FAILOVER_ATTEMPT_DELAY_SECONDS}с перед следующей попыткой failover...")
#                     await asyncio.sleep(AI_FAILOVER_ATTEMPT_DELAY_SECONDS)
#
#             if cycle < self._max_wait_cycles - 1:
#                 wait_time = self._get_intelligent_wait_time(cycle)
#                 logger.warning(f"Все AI-провайдеры недоступны. Пауза {wait_time:.1f}с перед циклом #{cycle + 2}.")
#                 await asyncio.sleep(wait_time)
#
#         logger.error("Все циклы ожидания исчерпаны. Не удалось обработать запрос.")
#         raise Exception(
#             f"Не удалось выполнить запрос после {self._max_wait_cycles} циклов. Последняя ошибка: {last_error}")
#
#     async def _attempt_single_provider(self, provider_name: str, request_func: Callable, prompt: str,
#                                        estimated_tokens: int, **kwargs) -> Any:
#         """Вспомогательный метод для выполнения запроса к одному провайдеру."""
#         async with self._global_semaphore:
#             config = self.providers[provider_name]
#
#             api_key = config.api_key
#             masked_key = f"sk-...{api_key[-4:]}" if "sk-" in api_key else f"{api_key[:4]}...{api_key[-4:]}"
#
#             # Логируем с уровнем DEBUG, чтобы не засорять основной лог, но иметь детали при необходимости.
#             logger.debug(f"🤖 AI Request -> Provider: {config.name} | Key: {masked_key} | Model: {config.model}")
#
#             await asyncio.sleep(config.base_delay)
#             self._token_usage[provider_name].used_tokens += estimated_tokens
#
#             try:
#                 result = await request_func(provider_name_override=provider_name, prompt=prompt, **kwargs)
#                 self._handle_success(provider_name)
#                 return result
#             except Exception:
#                 self._token_usage[provider_name].used_tokens = max(0, self._token_usage[
#                     provider_name].used_tokens - estimated_tokens)
#                 raise
#
#     def _get_intelligent_wait_time(self, current_cycle: int) -> float:
#         """Вычисляет время ожидания."""
#         shortest_wait = self._get_shortest_wait_time()
#         if shortest_wait > 0:
#             return min(shortest_wait + 5.0, self._wait_cycle_base_duration * (current_cycle + 2))
#         return self._wait_cycle_base_duration * (2 ** current_cycle)
#
#     def _get_shortest_wait_time(self) -> float:
#         """Возвращает время до разблокирования ближайшего провайдера"""
#         current_time = time.time()
#         wait_times = [
#             state['rate_limit_until'] - current_time
#             for state in self.provider_states.values()
#             if state['rate_limit_until'] > current_time
#         ]
#         return min(wait_times) if wait_times else 0
#
#     def _handle_success(self, provider_name: str):
#         """Обрабатывает успешный запрос"""
#         state = self.provider_states[provider_name]
#         state['failure_count'] = 0
#         state['consecutive_429s'] = 0
#         state['last_success'] = time.time()
#         state['status'] = ProviderStatus.AVAILABLE
#
#     def _extract_error_code(self, error_str: str) -> str:
#         """Извлекает HTTP код ошибки для лучшей диагностики"""
#         match = re.search(r'\'(\d{3})\'', error_str)
#         return match.group(1) if match else 'N/A'
#
#     async def _handle_provider_error(self, provider_name: str, error: Exception, estimated_tokens: int):
#         """Улучшенная обработка ошибок с разной логикой для разных кодов."""
#         state = self.provider_states[provider_name]
#         state['failure_count'] += 1
#         error_str = str(error).lower()
#         error_code = self._extract_error_code(error_str)
#
#         if provider_name.startswith("Groq") and error_code == '400':
#             if "token" in error_str or "context" in error_str:
#                 block_duration = 7200
#                 logger.critical(
#                     f"🔥 {provider_name}: Критическая ошибка размера контекста. Необходимо уменьшить размер батчей. Блокировка на {block_duration / 3600:.1f}ч")
#             elif "model" in error_str:
#                 block_duration = 3600
#                 logger.critical(f"🔥 {provider_name}: Неверная модель в конфигурации. Проверьте .env")
#             else:
#                 block_duration = 1800
#                 logger.error(f"❌ {provider_name}: Неизвестная ошибка 400: {error_str[:200]}")
#
#             state['rate_limit_until'] = time.time() + block_duration
#             state['status'] = ProviderStatus.UNAVAILABLE
#
#         elif error_code == '429' or "rate limit" in error_str:
#             state['consecutive_429s'] += 1
#             wait_time = self._extract_wait_time_from_error(error_str)
#             block_duration = (wait_time + 5) if wait_time else min(300, 30 * (2 ** state['consecutive_429s']))
#             state['rate_limit_until'] = time.time() + block_duration
#             state['status'] = ProviderStatus.RATE_LIMITED
#             logger.warning(f"🚫 {provider_name}: Rate limit. Блокировка на {block_duration:.1f} сек.")
#             self._token_usage[provider_name].used_tokens = max(0, self._token_usage[
#                 provider_name].used_tokens - estimated_tokens)
#
#         elif error_code.startswith('4'):
#             block_duration = 3600
#             state['rate_limit_until'] = time.time() + block_duration
#             state['status'] = ProviderStatus.UNAVAILABLE
#             logger.critical(f"🔥 {provider_name}: Критическая ошибка клиента (код: {error_code}). "
#                             f"Вероятно, проблема в .env (ключ/модель) или в формировании запроса. "
#                             f"Провайдер отключен на 1 час. Ошибка: {str(error)[:250]}")
#
#         else:
#             block_duration = 120
#             state['rate_limit_until'] = time.time() + block_duration
#             state['status'] = ProviderStatus.ERROR
#             logger.error(
#                 f"❌ {provider_name}: Ошибка сервера или сети (код: {error_code}). Повторная попытка через {block_duration} сек. Ошибка: {str(error)[:250]}")
#
#     def _extract_wait_time_from_error(self, error_str: str) -> Optional[float]:
#         """Извлекает время ожидания из сообщения об ошибке"""
#         match = re.search(r'try again in ([\d.]+)s', error_str)
#         if match:
#             return float(match.group(1))
#         return None
#
#     def get_status_report(self) -> Dict[str, Any]:
#         """Возвращает подробный отчет о состоянии всех провайдеров"""
#         current_time = time.time()
#         report = {}
#
#         for name, state in self.provider_states.items():
#             token_usage = self._token_usage[name]
#             report[name] = {
#                 'status': state['status'].value,
#                 'available': state['rate_limit_until'] <= current_time,
#                 'tokens_used': token_usage.used_tokens,
#                 'tokens_limit': token_usage.limit_per_minute,
#                 'utilization': f"{(token_usage.used_tokens / token_usage.limit_per_minute) * 100:.1f}%",
#                 'failure_count': state['failure_count'],
#                 'blocked_until': state['rate_limit_until'] if state['rate_limit_until'] > current_time else None,
#             }
#
#         return report
#
# # Глобальный экземпляр
# enhanced_ai_manager = EnhancedAIRateLimitManager()