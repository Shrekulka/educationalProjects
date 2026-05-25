# inter_exchange_arbitrage_bot/src/services/exchange_service.py
import asyncio
from typing import Dict, Any, Optional, List, Tuple

import ccxt.async_support as ccxt
import src.core.state as app_state
from src.constants.rate_limiting_constants import (EXCHANGE_RATE_LIMITS, DEFAULT_RATE_LIMIT_CONFIG,
                                                   RATE_LIMIT_RETRY_CONFIG, RATE_LIMIT_ERROR_CODES)
from src.constants.trading_constants import (EXCHANGE_BYBIT, BYBIT_DEFAULT_TYPE_SPOT, BYBIT_RECV_WINDOW_MS,
                                             EXCHANGE_MIN_ORDER_VALUES, DYNAMIC_LIMITS_CONFIG, LIMIT_SAFETY_MULTIPLIER,
                                             MARKET_FIELD_LIMITS, EXCHANGE_YOBIT, DEFAULT_TRADE_AMOUNT_USD,
                                             DEFAULT_FALLBACK_SYMBOL, PRIMARY_QUOTE_CURRENCY, MARKET_FIELD_PRECISION,
                                             MIN_API_LIMIT_THRESHOLD_YOBIT, MIN_API_LIMIT_THRESHOLD,
                                             YOBIT_SAFE_MINIMUM_LIMIT_USD, DEFAULT_DYNAMIC_LIMITS_CONFIG,
                                             API_RETRY_DELAY, MAX_API_LIMIT_VALIDATION_THRESHOLD, MARKET_FIELD_SPOT,
                                             MARKET_FIELD_QUOTE, MARKET_FIELD_BASE
                                             )
from src.core.config import config, KuCoinConfig
from src.utils import safe_get_numeric
from src.utils.logger import logger
from src.utils.metrics import API_ERRORS_TOTAL


class ExchangeService:
    def __init__(self, exchange_id: str):
        self.exchange_id = exchange_id.lower()
        self.exchange_config = self._get_exchange_config()
        if not self.exchange_config:
            raise ValueError(f"Конфигурация для биржи '{self.exchange_id}' не найдена.")
        self.client = self._create_client()
        logger.critical(f"+++++ СОЗДАН ЭКЗЕМПЛЯР ExchangeService для {self.exchange_id.upper()} ID: {id(self)}")
        logger.info(f"Сервис для биржи '{self.exchange_id.capitalize()}' инициализирован.")

    def __del__(self):
        # ЛОГГИРОВАНИЕ УНИЧТОЖЕНИЯ
        logger.critical(f"----- УНИЧТОЖЕН ЭКЗЕМПЛЯР ExchangeService для {self.exchange_id.upper()} ID: {id(self)}")

    def _get_exchange_config(self) -> Optional[Any]:
        return getattr(config, self.exchange_id, None)

    def _create_client(self) -> ccxt.Exchange:
        """
        МОДЕРНИЗИРОВАННАЯ ВЕРСИЯ: Использует индивидуальные настройки rate limiting.
        """
        exchange_class = getattr(ccxt, self.exchange_id)

        # Получаем специфичные настройки для биржи или дефолтные
        rate_config = EXCHANGE_RATE_LIMITS.get(self.exchange_id, DEFAULT_RATE_LIMIT_CONFIG)

        # Извлекаем options и удаляем его из основного конфига ---
        client_options = rate_config.pop('options', {})

        # Базовые параметры аутентификации
        params = {
            'apiKey': self.exchange_config.api_key,
            'secret': self.exchange_config.api_secret,
            'asyncio_session': app_state.aiohttp_session,
            'options': client_options,
            **rate_config  # Распаковываем все настройки rate limiting
        }
        # Возвращаем options обратно в rate_config, чтобы не изменять исходный объект
        if client_options:
            rate_config['options'] = client_options

        # Специфичные настройки для Bybit
        if self.exchange_id == EXCHANGE_BYBIT:
            params['options'] = {
                'defaultType': BYBIT_DEFAULT_TYPE_SPOT,  # Используем спотовую торговлю
                'recvWindow': BYBIT_RECV_WINDOW_MS,  # Окно получения для API
            }

            # Для testnet Bybit нужно установить sandbox режим ДО создания клиента
            if getattr(self.exchange_config, 'testnet', False):
                params['sandbox'] = True
                logger.warning(f"Биржа '{self.exchange_id.capitalize()}' работает в режиме TESTNET!")

        # Для KuCoin добавляем passphrase
        if isinstance(self.exchange_config, KuCoinConfig):
            params['password'] = self.exchange_config.api_passphrase

        # Создаем клиент с параметрами
        client = exchange_class(params)

        # Для остальных бирж устанавливаем sandbox режим после создания
        if self.exchange_id != EXCHANGE_BYBIT and getattr(self.exchange_config, 'testnet', False):
            try:
                client.set_sandbox_mode(True)
                logger.warning(f"Биржа '{self.exchange_id.capitalize()}' работает в режиме TESTNET!")
            except Exception as e:
                logger.warning(f"Не удалось установить sandbox режим для {self.exchange_id}: {e}")

        return client

    async def _safe_api_call(self, api_method, *args, **kwargs):
        """
        Централизованная обертка для всех API вызовов с обработкой rate limiting.
        """
        max_retries = RATE_LIMIT_RETRY_CONFIG['max_retries']
        delay = RATE_LIMIT_RETRY_CONFIG['base_delay_seconds']

        for attempt in range(max_retries):
            try:
                return await api_method(*args, **kwargs)


            except (ccxt.RateLimitExceeded, ccxt.DDoSProtection) as e:
                logger.warning(f"[{self.exchange_id}] Rate limit exceeded (attempt {attempt + 1}/{max_retries})")
                API_ERRORS_TOTAL.labels(exchange_id=self.exchange_id, error_type="RateLimit").inc()

            except (ccxt.NetworkError, ccxt.ExchangeNotAvailable) as e:
                logger.warning(f"[{self.exchange_id}] Network error (attempt {attempt + 1}/{max_retries})")
                API_ERRORS_TOTAL.labels(exchange_id=self.exchange_id, error_type="NetworkError").inc()

            except ccxt.ExchangeError as e:
                error_codes = RATE_LIMIT_ERROR_CODES.get(self.exchange_id, [])
                if any(str(code) in str(e) for code in error_codes):
                    logger.warning(f"[{self.exchange_id}] Detected rate limit error by code")
                    API_ERRORS_TOTAL.labels(exchange_id=self.exchange_id, error_type="RateLimit").inc()
                else:
                    API_ERRORS_TOTAL.labels(exchange_id=self.exchange_id, error_type="ExchangeError").inc()
                    raise  # Пробрасываем ошибку, если это не rate limiting

            # Ждем перед повторной попыткой
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
                delay = min(delay * RATE_LIMIT_RETRY_CONFIG['backoff_multiplier'],
                            RATE_LIMIT_RETRY_CONFIG['max_delay_seconds'])

        # Если все попытки исчерпаны
        raise ccxt.RateLimitExceeded(f"Max retries exceeded for {self.exchange_id}")

    async def get_market_details(self, symbol: str) -> Optional[dict]:
        """
        ✨ УЛУЧШЕННАЯ ВЕРСИЯ: Получает ключевые детали рынка с особой обработкой для разных бирж.
        """
        try:
            markets = await self._safe_api_call(self.client.load_markets)
            if symbol not in markets:
                logger.warning(f"❌ Символ {symbol} не найден на {self.exchange_id.capitalize()}.")
                return None

            market = markets[symbol]
            logger.debug(f"📊 Сырые данные рынка {symbol} на {self.exchange_id}: {market}")

            # Извлекаем основные лимиты
            limits = market.get(MARKET_FIELD_LIMITS, {})
            amount_limits = limits.get('amount', {})
            cost_limits = limits.get('cost', {})
            precision = market.get(MARKET_FIELD_PRECISION, {})

            # Особая обработка для Yobit
            if self.exchange_id == EXCHANGE_YOBIT:
                logger.debug(f"🔧 Применяю специальную логику для {EXCHANGE_YOBIT}")

                # Проверяем есть ли хоть какие-то лимиты
                amount_min = amount_limits.get('min')
                cost_min = cost_limits.get('min')

                logger.debug(f"Yobit лимиты: amount_min={amount_min}, cost_min={cost_min}")

                # Yobit возвращает реальные, но очень маленькие лимиты
                # Не перезаписываем их, а оставляем для дальнейшей обработки в get_reliable_min_order_value

            # Стандартная обработка для других бирж
            result = {
                'amount_min': amount_limits.get('min'),
                'cost_min': cost_limits.get('min'),
                'precision_amount': precision.get('amount')
            }

            logger.debug(f"📋 Итоговые лимиты для {symbol} на {self.exchange_id}: {result}")
            return result

        except Exception as e:
            logger.error(f"❌ Ошибка при получении деталей рынка {symbol} с '{self.exchange_id.capitalize()}': {e}")
            return None

    def format_amount_to_precision(self, symbol: str, amount: float) -> Optional[float]:
        """
        Форматирует (округляет) количество актива до точности,
        требуемой рынком на данной бирже.
        """
        try:
            # Убеждаемся, что рынки загружены
            if symbol not in self.client.markets:
                self.client.load_markets()

            # Используем встроенный метод ccxt для форматирования
            formatted_amount = self.client.amount_to_precision(symbol, amount)
            return float(formatted_amount)
        except Exception as e:
            logger.error(f"Не удалось отформатировать количество для {symbol} на {self.exchange_id}: {e}")
            return None

    async def get_reliable_min_order_value(self, symbol: str = DEFAULT_FALLBACK_SYMBOL) -> float:
        """
        ✨ ФИНАЛЬНАЯ ВЕРСИЯ: Получение минимального лимита с детальным логированием и флагами.
        """
        limits_config = DYNAMIC_LIMITS_CONFIG.get(self.exchange_id, DEFAULT_DYNAMIC_LIMITS_CONFIG)
        max_attempts = limits_config['retry_attempts']
        timeout = limits_config['timeout']

        api_attempt_made = False
        received_invalid_limit = False
        last_invalid_value = None

        for attempt in range(max_attempts):
            try:
                logger.debug(
                    f"Попытка {attempt + 1}/{max_attempts}: получение лимитов для {symbol} на {self.exchange_id}"
                )

                market_details = await asyncio.wait_for(
                    self.get_market_details(symbol),
                    timeout=timeout
                )

                logger.debug(f"Полученные market_details для {self.exchange_id}: {market_details}")

                if (market_details and isinstance(market_details, dict) and
                        market_details.get('cost_min') is not None):

                    api_attempt_made = True

                    try:
                        dynamic_min = float(market_details['cost_min'])
                        logger.debug(f"Сырой cost_min для {self.exchange_id}: {dynamic_min}")

                        min_threshold = (MIN_API_LIMIT_THRESHOLD_YOBIT
                                         if self.exchange_id == EXCHANGE_YOBIT
                                         else MIN_API_LIMIT_THRESHOLD)

                        if min_threshold <= dynamic_min <= MAX_API_LIMIT_VALIDATION_THRESHOLD:
                            adjusted_min = (max(dynamic_min, YOBIT_SAFE_MINIMUM_LIMIT_USD)
                                            if self.exchange_id == EXCHANGE_YOBIT
                                            else dynamic_min)

                            safe_min = adjusted_min * LIMIT_SAFETY_MULTIPLIER

                            logger.info(
                                f"✅ Получен динамический лимит для {self.exchange_id.upper()}: "
                                f"{dynamic_min:.2f} {PRIMARY_QUOTE_CURRENCY} (до корректировки) → "
                                f"{safe_min:.2f} {PRIMARY_QUOTE_CURRENCY} (с запасом)"
                            )
                            return safe_min
                        else:
                            received_invalid_limit = True
                            last_invalid_value = dynamic_min
                            logger.warning(
                                f"❌ Неразумный лимит для {self.exchange_id}: {dynamic_min:.6f} "
                                f"(порог: {min_threshold}-{MAX_API_LIMIT_VALIDATION_THRESHOLD})"
                            )

                    except (ValueError, TypeError) as e:
                        api_attempt_made = True
                        received_invalid_limit = True
                        logger.warning(
                            f"❌ Ошибка преобразования cost_min для {self.exchange_id}: {e}"
                        )
                else:
                    api_attempt_made = True
                    logger.warning(
                        f"❌ Некорректные market_details для {self.exchange_id}: "
                        f"type={type(market_details)}, "
                        f"cost_min={market_details.get('cost_min') if market_details else 'None'}"
                    )

            except asyncio.TimeoutError:
                api_attempt_made = True
                logger.warning(
                    f"⏰ Таймаут ({timeout}s) при получении лимитов для {self.exchange_id} "
                    f"(попытка {attempt + 1}/{max_attempts})"
                )
            except Exception as e:
                api_attempt_made = True
                logger.warning(
                    f"❌ Ошибка при получении лимитов для {self.exchange_id}: "
                    f"{type(e).__name__}: {e}"
                )

            if attempt < max_attempts - 1:
                await asyncio.sleep(API_RETRY_DELAY)

        # --- БЛОК FALLBACK ЛОГИКИ ---
        fallback_value = EXCHANGE_MIN_ORDER_VALUES.get(self.exchange_id, DEFAULT_TRADE_AMOUNT_USD)

        if fallback_value <= 0:
            fallback_value = DEFAULT_TRADE_AMOUNT_USD
            logger.warning(
                f"⚠️ Fallback для {self.exchange_id.upper()} некорректный, "
                f"использую DEFAULT: ${fallback_value:.2f}"
            )

        if api_attempt_made and received_invalid_limit:
            logger.warning(
                f"⚠️ Лимит для {self.exchange_id.upper()} от API ({last_invalid_value:.6f} USDT) "
                f"слишком мал или невалиден. Применяется безопасный fallback из констант: ${fallback_value:.2f} USDT."
            )
        elif api_attempt_made:
            logger.info(
                f"🔄 Использую fallback лимит для {self.exchange_id.upper()}: "
                f"${fallback_value:.2f} USD (API не ответило корректно)"
            )
        else:
            logger.info(
                f"🔄 Использую fallback лимит для {self.exchange_id.upper()}: "
                f"${fallback_value:.2f} USD (попытки API не предпринимались)"
            )

        return fallback_value

    async def get_min_order_amount(self, symbol: str = DEFAULT_FALLBACK_SYMBOL) -> Optional[float]:
        """
        ✨ ОБНОВЛЕННЫЙ МЕТОД: Упрощенная версия для обратной совместимости.
        Теперь просто вызывает новый надежный метод.
        """
        try:
            return await self.get_reliable_min_order_value(symbol)
        except Exception as e:
            logger.error(f"Критическая ошибка при получении минимального лимита: {e}")
            # Возвращаем консервативный fallback в крайнем случае
            return EXCHANGE_MIN_ORDER_VALUES.get(self.exchange_id, DEFAULT_TRADE_AMOUNT_USD)

    async def validate_exchange_limits_bulk(self, symbols: list[str]) -> dict[str, dict]:
        """
        ✨ НОВЫЙ МЕТОД: Массовая проверка лимитов для нескольких торговых пар.
        Полезно для инициализации и кэширования лимитов.

        Args:
            symbols: Список торговых пар для проверки

        Returns:
            dict: Словарь с лимитами для каждой пары
        """
        results = {}

        try:
            # Загружаем все рынки один раз
            markets = await self._safe_api_call(self.client.load_markets)

            for symbol in symbols:
                if symbol in markets:
                    market = markets[symbol]
                    limits = market.get('limits', {})

                    results[symbol] = {
                        'min_amount': limits.get('amount', {}).get('min', 0),
                        'min_cost': limits.get('cost', {}).get('min', 0),
                        'precision': market.get('precision', {}).get('amount', 8)
                    }
                else:
                    logger.warning(f"Пара {symbol} не найдена на {self.exchange_id}")
                    results[symbol] = None

        except Exception as e:
            logger.error(f"Ошибка при массовой проверке лимитов на {self.exchange_id}: {e}")

        return results

    async def get_dynamic_min_order_value(self, symbol: str) -> float:
        """
        НОВЫЙ метод: Получает актуальную минимальную стоимость ордера с биржи.
        Включает fallback на константы при недоступности API.
        """
        try:
            market_details = await self.get_market_details(symbol)
            if market_details and market_details.get('cost_min'):
                dynamic_min = float(market_details['cost_min'])
                # Добавляем % запас на всякий случай
                return dynamic_min * LIMIT_SAFETY_MULTIPLIER

        except Exception as e:
            logger.warning(f"Не удалось получить динамические лимиты для {symbol}: {e}")

        # Fallback на обновленные константы
        return EXCHANGE_MIN_ORDER_VALUES.get(self.exchange_id, DEFAULT_TRADE_AMOUNT_USD)

    async def validate_order_limits(self, symbol: str, amount: float, price: float) -> Tuple[bool, str]:
        """
        НОВЫЙ метод: Комплексная валидация лимитов перед отправкой ордера.
        """
        try:
            # Получаем актуальные лимиты
            details = await self.get_market_details(symbol)
            if not details:
                return False, f"Не удалось получить лимиты для {symbol}"

            # Проверяем минимальное количество
            min_amount = details.get('amount_min', 0)
            if min_amount > 0 and amount < min_amount:
                return False, f"Количество {amount:.6f} меньше минимума {min_amount:.6f}"

            # Проверяем минимальную стоимость
            order_cost = amount * price
            min_cost = details.get('cost_min', 0)
            if min_cost > 0 and order_cost < min_cost:
                return False, f"Стоимость ${order_cost:.2f} меньше минимума ${min_cost:.2f}"

            return True, "OK"

        except Exception as e:
            return False, f"Ошибка валидации: {str(e)}"

    async def get_balance(self) -> Dict[str, float]:
        """Получает баланс аккаунта."""
        try:
            logger.debug(f"Запрос баланса с биржи '{self.exchange_id.capitalize()}'...")

            # Проверяем соединение перед запросом баланса
            if not self.client.apiKey:
                raise Exception("API ключ не установлен")

            balance_data = await self._safe_api_call(self.client.fetch_balance)

            target_balance = balance_data.get('total', {})

            positive_balances = {
                asset: data for asset, data in target_balance.items() if data > 0
            }
            logger.info(
                f"Баланс с '{self.exchange_id.capitalize()}' успешно получен. Найдено активов: {len(positive_balances)}")
            return positive_balances


        except ccxt.AuthenticationError as e:
            API_ERRORS_TOTAL.labels(exchange_id=self.exchange_id, error_type="AuthenticationError").inc()
            logger.error(f"Ошибка аутентификации на '{self.exchange_id.capitalize()}': {e}")
            raise
        except ccxt.NetworkError as e:
            logger.error(f"Сетевая ошибка при обращении к '{self.exchange_id.capitalize()}': {e}")
            raise
        except Exception as e:
            logger.error(f"Ошибка при получении баланса с '{self.exchange_id.capitalize()}': {e}", exc_info=True)
            raise

    async def get_all_spot_assets(self) -> List[str]:
        """
        Использует централизованный кэш рынков из ServiceManager.
        Больше не вызывает load_markets() напрямую.
        """
        from src.services.service_manager import service_manager
        try:
            logger.debug(f"Получение спотовых активов с биржи '{self.exchange_id.capitalize()}' из кэша...")
            # 1. Получаем запись из кэша (это может быть кортеж или None)
            cache_entry = service_manager.markets_cache.get(self.exchange_id)

            # 2. Проверяем, что запись существует и является кортежем
            if not cache_entry or not isinstance(cache_entry, tuple):
                logger.warning(f"Кэш рынков для '{self.exchange_id.capitalize()}' пуст или имеет неверный формат.")
                return []

            # 3. Распаковываем кортеж, чтобы получить словарь рынков
            markets, _ = cache_entry  # Вторая переменная (timestamp) нам здесь не нужна

            if not markets:
                logger.warning(f"Кэш рынков для '{self.exchange_id.capitalize()}' пуст.")
                return []

            assets = {
                market_data[MARKET_FIELD_BASE]
                for market_data in markets.values()
                if (market_data.get(MARKET_FIELD_SPOT) and
                    market_data.get(MARKET_FIELD_QUOTE) == PRIMARY_QUOTE_CURRENCY and
                    market_data.get(MARKET_FIELD_BASE))
            }

            logger.debug(f"Найдено {len(assets)} спотовых активов в кэше для '{self.exchange_id.capitalize()}'.")
            return sorted(list(assets))
        except Exception as e:
            logger.error(f"Не удалось обработать кэш активов для '{self.exchange_id.capitalize()}': {e}",
                         exc_info=True)
            return []

    async def get_tickers(self, symbols: List[str]) -> Dict[str, float]:
        """
        Получает последние цены для списка торговых пар.

        Args:
            symbols (List[str]): Список пар, например ['BTC/USDT', 'ETH/USDT'].

        Returns:
            Dict[str, float]: Словарь, где ключ - пара, а значение - последняя цена.
        """
        if not symbols:
            return {}

        try:
            logger.debug(f"Запрос цен для {len(symbols)} пар с биржи '{self.exchange_id.capitalize()}'...")

            # Сначала загружаем рынки для проверки существования символов
            markets = await self._safe_api_call(self.client.load_markets)
            valid_symbols = [s for s in symbols if s in markets]

            if not valid_symbols:
                logger.warning(f"Ни один из запрошенных символов не найден на бирже: {symbols}")
                return {}

            if len(valid_symbols) != len(symbols):
                invalid_symbols = set(symbols) - set(valid_symbols)
                logger.debug(f"Не найдены символы: {invalid_symbols}")

            # Запрашиваем цены только для существующих символов
            tickers_data = await self._safe_api_call(self.client.fetch_tickers, valid_symbols)

            # Извлекаем только последнюю цену для каждой пары
            prices = {}
            for symbol, ticker in tickers_data.items():
                last_price = safe_get_numeric(ticker, 'last')
                if last_price > 0:
                    prices[symbol] = last_price
                else:
                    logger.debug(f"Некорректные данные или нулевая цена для {symbol}: {ticker}")

            logger.info(f"Цены успешно получены для {len(prices)} из {len(symbols)} запрошенных символов.")
            return prices

        except ccxt.NetworkError as e:
            logger.error(f"Сетевая ошибка при получении цен с '{self.exchange_id.capitalize()}': {e}")
            return {}
        except ccxt.ExchangeError as e:
            logger.warning(f"Ошибка биржи при получении цен с '{self.exchange_id.capitalize()}': {e}")
            return {}
        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении цен с '{self.exchange_id.capitalize()}': {e}")
            return {}

    async def test_connection(self) -> bool:
        """
        Тестирует соединение с биржей, используя основной и запасной публичные методы.
        """
        try:
            logger.debug(f"Тестирование соединения с '{self.exchange_id.capitalize()}' (метод: fetch_time)...")
            # 1. Основной, самый легковесный метод
            await self._safe_api_call(self.client.fetch_time)
            logger.info(f"Соединение с '{self.exchange_id.capitalize()}' успешно установлено.")
            return True

        except ccxt.NotSupported:
            # 2. Если fetch_time не поддерживается, пробуем запасной вариант
            logger.debug(f"fetch_time не поддерживается для {self.exchange_id}, пробуем fetch_ticker...")
            try:
                # fetch_ticker('BTC/USDT') - очень универсальный метод
                await self._safe_api_call(self.client.fetch_ticker, DEFAULT_FALLBACK_SYMBOL)
                logger.info(f"Соединение с '{self.exchange_id.capitalize()}' успешно установлено (через fallback).")
                return True
            except Exception as e:
                # Если и fallback не сработал, логируем финальную ошибку
                if isinstance(e, ccxt.AuthenticationError):
                    logger.critical(f"КРИТИЧЕСКАЯ ОШИБКА АУТЕНТИФИКАЦИИ на '{self.exchange_id.capitalize()}': {e}")
                    logger.critical("ПРОВЕРЬТЕ ПРАВИЛЬНОСТЬ API КЛЮЧЕЙ В .ENV ФАЙЛЕ.")
                else:
                    logger.error(f"Не удалось подключиться к '{self.exchange_id.capitalize()}' (fallback): {e}")
                return False

        except ccxt.AuthenticationError as auth_err:
            # 3. Отлавливаем ошибку аутентификации от основного метода
            logger.critical(f"КРИТИЧЕСКАЯ ОШИБКА АУТЕНТИФИКАЦИИ на '{self.exchange_id.capitalize()}': {auth_err}")
            logger.critical("ПРОВЕРЬТЕ ПРАВИЛЬНОСТЬ API КЛЮЧЕЙ В .ENV ФАЙЛЕ.")
            return False

        except Exception as e:
            # 4. Отлавливаем все остальные ошибки (сетевые и т.д.) от основного метода
            logger.error(f"Не удалось подключиться к '{self.exchange_id.capitalize()}': {e}")
            return False

    async def close(self):
        """
        ФИНАЛЬНАЯ ВЕРСИЯ: Надежно закрывает ccxt клиент,
        даже если он был только частично инициализирован.
        """
        # Проверяем, что клиент вообще был создан и еще не закрыт
        if self.client and hasattr(self.client, 'close') and callable(self.client.close):
            try:
                # ccxt.close() является корутиной, ее нужно вызывать с await
                logger.debug(f"Попытка закрыть соединение для '{self.exchange_id.capitalize()}'...")
                await self.client.close()
                logger.info(f"✅ Соединение с '{self.exchange_id.capitalize()}' корректно закрыто.")
            except Exception as e:
                logger.warning(f"⚠️ Ошибка при закрытии соединения с '{self.exchange_id.capitalize()}': {e}")
            finally:
                # В любом случае обнуляем ссылку
                self.client = None

    # async def close(self):
    #     """
    #     ФИНАЛЬНАЯ ВЕРСИЯ: Надежно закрывает ccxt клиент.
    #     Этот метод вызывается ServiceManager'ом при выключении приложения.
    #     """
    #     # Проверяем, что клиент вообще был создан и еще не закрыт
    #     if self.client and hasattr(self.client, 'close'):
    #         try:
    #             # Проверяем, является ли метод асинхронным
    #             if asyncio.iscoroutinefunction(self.client.close):
    #                 await self.client.close()
    #                 logger.debug(f"✅ Асинхронное соединение с '{self.exchange_id.capitalize()}' корректно закрыто.")
    #             # Если это не так, считаем его синхронным
    #             elif callable(self.client.close):
    #                 await self.client.close()
    #                 logger.debug(f"✅ Синхронное соединение с '{self.exchange_id.capitalize()}' закрыто.")
    #         except Exception as e:
    #             logger.warning(f"⚠️ Ошибка при закрытии соединения с '{self.exchange_id.capitalize()}': {e}")
    #         finally:
    #             # Обнуляем ссылку, чтобы избежать повторного использования
    #             self.client = None

