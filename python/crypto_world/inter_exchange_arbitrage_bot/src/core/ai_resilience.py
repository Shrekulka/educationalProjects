# # inter_exchange_arbitrage_bot/src/core/ai_resilience.py
#
# import asyncio
# import logging
# import time
# from typing import Dict
#
# from src.constants.api_constants import AI_MAX_CONCURRENT_REQUESTS
# from src.utils import logger
#
#
# class AIRateLimitManager:
#     """
#     Централизованный менеджер для управления rate limits AI провайдеров.
#     Предотвращает каскадные ошибки 429 и обеспечивает плавную деградацию сервиса.
#     """
#
#     def __init__(self):
#         self._provider_states: Dict[str, Dict] = {}
#         self._global_semaphore = asyncio.Semaphore(AI_MAX_CONCURRENT_REQUESTS)
#
#     def _get_provider_state(self, provider_name: str) -> Dict:
#         """Получает или создает состояние провайдера."""
#         if provider_name not in self._provider_states:
#             self._provider_states[provider_name] = {
#                 'rate_limit_until': 0,
#                 'failure_count': 0,
#                 'last_success': time.time(),
#                 'consecutive_429s': 0
#             }
#         return self._provider_states[provider_name]
#
#     async def can_make_request(self, provider_name: str) -> bool:
#         """Проверяет, можно ли делать запрос к провайдеру."""
#         state = self._get_provider_state(provider_name)
#         current_time = time.time()
#
#         if state['rate_limit_until'] > current_time:
#             remaining = int(state['rate_limit_until'] - current_time)
#             logger.warning(f"AI провайдер {provider_name} заблокирован еще на {remaining} секунд")
#             return False
#
#         return True
#
#     async def execute_request(self, provider_name: str, request_func, *args, **kwargs):
#         """Выполняет запрос к AI провайдеру с контролем rate limit."""
#         async with self._global_semaphore:
#             if not await self.can_make_request(provider_name):
#                 raise Exception(f"AI провайдер {provider_name} временно недоступен из-за rate limit")
#
#             state = self._get_provider_state(provider_name)
#
#             try:
#                 # Минимальная задержка между всеми AI запросами
#                 await asyncio.sleep(0.5)
#
#                 result = await request_func(*args, **kwargs)
#
#                 # Сброс счетчиков при успехе
#                 state['failure_count'] = 0
#                 state['consecutive_429s'] = 0
#                 state['last_success'] = time.time()
#
#                 logger.debug(f"✅ Успешный запрос к AI провайдеру {provider_name}")
#                 return result
#
#             except Exception as e:
#                 await self._handle_request_error(provider_name, e)
#                 raise
#
#     async def _handle_request_error(self, provider_name: str, error: Exception):
#         """Обрабатывает ошибки запросов и устанавливает блокировки."""
#         state = self._get_provider_state(provider_name)
#         state['failure_count'] += 1
#
#         error_str = str(error).lower()
#
#         if "429" in error_str or "rate limit" in error_str:
#             state['consecutive_429s'] += 1
#             # Экспоненциальная блокировка: 60, 120, 240, 300 секунд
#             block_duration = min(300, 60 * (2 ** state['consecutive_429s']))
#
#             state['rate_limit_until'] = time.time() + block_duration
#
#             logger.error(
#                 f"🚫 AI провайдер {provider_name}: rate limit exceeded. "
#                 f"Блокирован на {block_duration} секунд. "
#                 f"Подряд 429 ошибок: {state['consecutive_429s']}"
#             )
#
#         elif "timeout" in error_str:
#             state['rate_limit_until'] = time.time() + 30
#             logger.warning(f"⏰ AI провайдер {provider_name}: timeout. Блокирован на 30 секунд.")
#
#         else:
#             state['rate_limit_until'] = time.time() + 10
#             logger.warning(f"❌ AI провайдер {provider_name}: {error}. Блокирован на 10 секунд.")
#
#     def get_provider_status(self, provider_name: str) -> Dict:
#         """Возвращает текущий статус провайдера."""
#         state = self._get_provider_state(provider_name)
#         current_time = time.time()
#
#         return {
#             'available': state['rate_limit_until'] <= current_time,
#             'blocked_until': state['rate_limit_until'] if state['rate_limit_until'] > current_time else None,
#             'failure_count': state['failure_count'],
#             'consecutive_rate_limits': state['consecutive_429s'],
#             'last_success_ago': int(current_time - state['last_success'])
#         }
#
#
# # Глобальный экземпляр менеджера
# ai_rate_manager = AIRateLimitManager()
