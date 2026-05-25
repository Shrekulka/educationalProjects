# # inter_exchange_arbitrage_bot/src/services/news_providers/coinapi_provider.py
#
# import urllib.parse
# from datetime import datetime, timezone
# from typing import List, Dict, Any, Set
#
# import httpx
#
# from src.constants.api_constants import NEWS_HTTP_TIMEOUT, COINAPI_ASSET_URL_TEMPLATE, COINAPI_IO_URL
# from src.core.config import NewsProvidersConfig
# from src.utils.logger import logger
# from .base_provider import BaseNewsProvider
#
#
# class CoinApiProvider(BaseNewsProvider):
#     """
#     ФИНАЛЬНАЯ ВЕРСИЯ: Радикально упрощенный CoinApiProvider.
#     - Использует только один, стандартный метод аутентификации.
#     - Полагается на BaseProvider для ротации ключей при ошибках.
#     - Делает один агрегированный запрос для всех монет.
#     """
#
#     def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
#         super().__init__("CoinAPI", api_config, http_session)
#
#     async def _do_fetch(self, coins: Set[str]) -> List[Dict[str, Any]]:
#         """Выполняет один API-запрос для всех монет с правильной аутентификацией."""
#         current_key = self._get_current_api_key()
#         if not current_key or not coins:
#             return []
#
#         headers = {'X-CoinAPI-Key': current_key}
#         params = {'filter_asset_id': ",".join([coin.upper() for coin in coins])}
#         url = f"{COINAPI_IO_URL}/assets"
#
#         try:
#             # Семафор используется для контроля общего числа одновременных запросов от всех провайдеров
#             async with self._request_semaphore:
#                 response = await self.session.get(url, headers=headers, params=params, timeout=NEWS_HTTP_TIMEOUT)
#                 response.raise_for_status()  # Выбросит исключение для кодов 4xx/5xx
#
#             data = response.json()
#             if not isinstance(data, list):
#                 logger.warning(f"{self.name}: API вернул неожиданный тип данных: {type(data)}")
#                 return []
#
#             all_news = []
#             for asset in data:
#                 asset_id = asset.get('asset_id')
#                 if not asset_id: continue
#
#                 name = asset.get('name', asset_id)
#                 price_usd = asset.get('price_usd')
#                 title = f"Обновление актива: {name} ({asset_id})"
#                 body = f"Цена: ${price_usd:,.4f}" if price_usd is not None else "Данные о цене недоступны"
#
#                 news_url = COINAPI_ASSET_URL_TEMPLATE.format(asset_id=urllib.parse.quote_plus(asset_id))
#
#                 all_news.append(
#                     self._format_news_item(
#                         title=title, body=body, url=news_url, published_at_dt=datetime.now(timezone.utc)
#                     )
#                 )
#             return all_news
#
#         except httpx.HTTPStatusError as e:
#             # Логируем ошибку и пробрасываем ее дальше. BaseProvider поймает ее
#             # и вызовет ротацию ключа, если это 401, 403 или 429.
#             logger.warning(f"{self.name} API error with key ...{current_key[-4:]}: {e.response.status_code}")
#             raise e
#         except Exception as e:
#             logger.error(f"{self.name}: Unexpected error: {e}", exc_info=True)
#             raise e
#
#     async def _do_fetch_with_key(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
#         """Этот провайдер не поддерживает параллельную логику, он всегда делает один запрос."""
#         return await self._do_fetch(coins)
#
#
# # # inter_exchange_arbitrage_bot/src/services/news_providers/coinapi_provider.py
# #
# # import urllib.parse
# # from datetime import datetime, timezone
# # from typing import List, Dict, Any, Set
# #
# # import httpx
# #
# # from src.constants.api_constants import NEWS_HTTP_TIMEOUT, COINAPI_ASSET_URL_TEMPLATE, COINAPI_IO_URL
# # from src.core.config import NewsProvidersConfig
# # from src.utils.logger import logger
# # from .base_provider import BaseNewsProvider
# #
# #
# # class CoinApiProvider(BaseNewsProvider):
# #     """
# #     ОПТИМИЗИРОВАННЫЙ CoinApiProvider.
# #     Стратегия: Использует один агрегированный запрос для всех монет.
# #     """
# #
# #     def __init__(self, api_config: NewsProvidersConfig, http_session: httpx.AsyncClient):
# #         super().__init__("CoinAPI", api_config, http_session)
# #
# #     async def _do_fetch(self, coins: Set[str]) -> List[Dict[str, Any]]:
# #         """Получает информацию об активах одним запросом с улучшенной обработкой ошибок."""
# #         current_key = self._get_current_api_key()
# #         if not current_key or not coins:
# #             logger.warning(f"{self.name}: Нет API ключа или монет для запроса")
# #             return []
# #
# #         filter_assets_str = ",".join([coin.upper() for coin in coins])
# #         url = f"{COINAPI_IO_URL}/assets"
# #
# #         # Логируем информацию для отладки (скрываем большую часть ключа)
# #         masked_key = f"{current_key[:8]}...{current_key[-4:]}" if len(current_key) > 12 else current_key[:4] + "..."
# #         logger.debug(f"{self.name}: Запрос к {url} с ключом {masked_key} для монет: {filter_assets_str}")
# #
# #         # Пробуем разные методы аутентификации
# #         auth_methods = [
# #             {
# #                 "name": "X-CoinAPI-Key header",
# #                 "headers": {'X-CoinAPI-Key': current_key},
# #                 "params": {'filter_asset_id': filter_assets_str}
# #             },
# #             {
# #                 "name": "Query parameter",
# #                 "headers": {},
# #                 "params": {
# #                     'filter_asset_id': filter_assets_str,
# #                     'apikey': current_key
# #                 }
# #             },
# #             {
# #                 "name": "Authorization header",
# #                 "headers": {'Authorization': current_key},
# #                 "params": {'filter_asset_id': filter_assets_str}
# #             }
# #         ]
# #
# #         last_exception = None
# #
# #         for method in auth_methods:
# #             try:
# #                 logger.debug(f"{self.name}: Пробуем метод аутентификации: {method['name']}")
# #
# #                 async with self._request_semaphore:
# #                     response = await self.session.get(
# #                         url,
# #                         headers=method['headers'],
# #                         params=method['params'],
# #                         timeout=NEWS_HTTP_TIMEOUT
# #                     )
# #
# #                     # Логируем детали ответа для отладки
# #                     logger.debug(f"{self.name}: Статус ответа: {response.status_code}")
# #                     if response.headers.get('X-RateLimit-Remaining'):
# #                         logger.debug(f"{self.name}: Осталось запросов: {response.headers.get('X-RateLimit-Remaining')}")
# #
# #                     response.raise_for_status()
# #                     data = response.json()
# #
# #                     # Успешно получили данные
# #                     logger.info(f"{self.name}: Успешно получено {len(data)} активов методом: {method['name']}")
# #                     break
# #
# #             except httpx.HTTPStatusError as e:
# #                 last_exception = e
# #                 status_code = e.response.status_code
# #
# #                 logger.warning(f"{self.name}: HTTP ошибка {status_code} с методом '{method['name']}'")
# #
# #                 # Если 401/403 - пробуем следующий метод аутентификации
# #                 if status_code in {401, 403}:
# #                     try:
# #                         error_details = e.response.json()
# #                         error_msg = error_details.get('error', 'Неизвестная ошибка')
# #                         logger.warning(f"{self.name}: Детали ошибки: {error_msg}")
# #                     except:
# #                         logger.warning(f"{self.name}: Не удалось получить детали ошибки")
# #
# #                     # Если это последний метод, прерываем
# #                     if method == auth_methods[-1]:
# #                         logger.error(f"{self.name}: Все методы аутентификации неуспешны")
# #                         raise e
# #                     else:
# #                         continue
# #
# #                 # Для других HTTP ошибок (429, 5xx) сразу выбрасываем исключение
# #                 elif status_code == 429:
# #                     logger.error(f"{self.name}: Превышен лимит запросов (429)")
# #                     raise e
# #                 elif status_code >= 500:
# #                     logger.error(f"{self.name}: Серверная ошибка ({status_code})")
# #                     raise e
# #                 else:
# #                     logger.error(f"{self.name}: Неожиданная HTTP ошибка ({status_code})")
# #                     raise e
# #
# #             except httpx.TimeoutException as e:
# #                 last_exception = e
# #                 logger.error(f"{self.name}: Таймаут запроса с методом '{method['name']}'")
# #                 if method == auth_methods[-1]:
# #                     raise e
# #                 continue
# #
# #             except Exception as e:
# #                 last_exception = e
# #                 logger.error(f"{self.name}: Неожиданная ошибка с методом '{method['name']}': {type(e).__name__}: {e}")
# #                 if method == auth_methods[-1]:
# #                     raise e
# #                 continue
# #
# #         # Если мы дошли сюда без успешного ответа, выбрасываем последнее исключение
# #         if 'data' not in locals():
# #             if last_exception:
# #                 raise last_exception
# #             else:
# #                 raise Exception(f"{self.name}: Не удалось получить данные ни одним методом")
# #
# #         # Обрабатываем полученные данные
# #         all_news = []
# #
# #         if not isinstance(data, list):
# #             logger.warning(f"{self.name}: Неожиданный формат ответа API (не список): {type(data)}")
# #             return []
# #
# #         processed_count = 0
# #         skipped_count = 0
# #
# #         for asset in data:
# #             if not isinstance(asset, dict):
# #                 skipped_count += 1
# #                 continue
# #
# #             asset_id = asset.get('asset_id')
# #             name = asset.get('name', asset_id)
# #             price_usd = asset.get('price_usd')
# #
# #             # Проверяем обязательные поля
# #             if not asset_id:
# #                 skipped_count += 1
# #                 continue
# #
# #             # Если цена отсутствует, все равно создаем новость
# #             if price_usd is not None:
# #                 title = f"Обновление актива: {name} ({asset_id})"
# #                 body = f"Цена: ${price_usd:,.4f}"
# #             else:
# #                 title = f"Информация об активе: {name} ({asset_id})"
# #                 body = f"Актив {name} доступен для торговли"
# #
# #             try:
# #                 encoded_asset_id = urllib.parse.quote_plus(asset_id)
# #                 news_url = COINAPI_ASSET_URL_TEMPLATE.format(asset_id=encoded_asset_id)
# #             except Exception as e:
# #                 logger.warning(f"{self.name}: Ошибка при создании URL для {asset_id}: {e}")
# #                 news_url = None
# #
# #             all_news.append(
# #                 self._format_news_item(
# #                     title=title,
# #                     body=body,
# #                     url=news_url,
# #                     published_at_dt=datetime.now(timezone.utc)
# #                 )
# #             )
# #             processed_count += 1
# #
# #         logger.info(f"{self.name}: Обработано {processed_count} активов, пропущено {skipped_count}")
# #         return all_news
# #
# #
# #     async def _do_fetch_with_key(self, coins: Set[str], api_key: str, key_index: int) -> List[Dict[str, Any]]:
# #         """Метод-заглушка, не используется."""
# #         return await self._do_fetch(coins)
# #
