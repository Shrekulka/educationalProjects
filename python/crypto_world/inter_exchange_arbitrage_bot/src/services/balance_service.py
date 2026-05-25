# inter_exchange_arbitrage_bot/src/services/balance_service.py

import asyncio
import datetime
import html
from typing import List, Dict, Set, Tuple

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

import src.core.state as app_state
from src.bot.keyboards.scanner_keyboard import get_scanner_menu_keyboard
from src.constants.api_constants import INSUFFICIENT_FUNDS_WARNING_INTERVAL_MINUTES
from src.constants.telegram_constants import TELEGRAM_MESSAGE_MAX_LENGTH
from src.constants.trading_constants import (
    DEFAULT_FALLBACK_SYMBOL, DEFAULT_TRADE_AMOUNT_USD, EXCHANGE_MIN_ORDER_VALUES,
    MIN_API_LIMIT_THRESHOLD, MIN_API_LIMIT_THRESHOLD_YOBIT, MINIMUM_QUANTITY_THRESHOLD,
    MINIMUM_VALUE_THRESHOLD, PRIMARY_QUOTE_CURRENCY, STABLE_COINS, STABLECOIN_PRICE,
    TRADE_AMOUNT_SAFETY_MARGIN, MIN_EXCHANGES_FOR_ARBITRAGE, MIN_SELL_VALUE_RATIO, MIN_BUY_CAPABLE_EXCHANGES
)
from src.core.config import config
from src.core.database import async_session_factory
from src.models.system_models import SystemState
from src.models.user_models import UserCoin
from src.services.scanner_state_service import get_scanner_state_from_db
from src.services.service_manager import service_manager
from src.utils.helpers import get_number_emoji
from src.utils.logger import logger


class BalanceService:
    """
    Централизованный сервис для всех операций с балансами пользователя.
    Является единой точкой входа для получения, анализа и форматирования данных о балансах.
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.prices: Dict[str, float] = {}
        self._initialized = False

    async def initialize(self):
        """
        Упрощенная инициализация - ServiceManager уже управляет сервисами.
        """
        if self._initialized:
            return

        # Убеждаемся, что ServiceManager инициализирован
        await service_manager.initialize()
        self._initialized = True
        logger.info(f"BalanceService инициализирован для пользователя {self.user_id}")

    async def get_all_balances(self) -> Dict[str, Dict[str, float]]:
        """
        ОПТИМИЗИРОВАННАЯ версия: использует ServiceManager напрямую.
        # """
        # await self.initialize()
        return await service_manager.get_all_balances()

    @property
    def validated_services(self) -> Dict:
        """
        Свойство для обратной совместимости.
        Возвращает здоровые сервисы из ServiceManager.
        """
        # Возвращаем future, чтобы сохранить интерфейс
        return service_manager.services

    async def send_warning_with_antispam(self, warning_message: str):
        """
        Отправляет предупреждение о балансах ВСЕМ администраторам с защитой от спама.
        """
        warning_key = 'last_balance_warning_ts'
        now = datetime.datetime.now(datetime.timezone.utc)
        async with async_session_factory() as session:
            stmt_get = select(SystemState.value).where(SystemState.key == warning_key)
            last_warning_ts_str = (await session.execute(stmt_get)).scalar_one_or_none()

            should_send = False
            if not last_warning_ts_str:
                should_send = True
            else:
                last_warning_ts = datetime.datetime.fromisoformat(last_warning_ts_str)
                minutes_passed = (now - last_warning_ts).total_seconds() / 60
                if minutes_passed > INSUFFICIENT_FUNDS_WARNING_INTERVAL_MINUTES:
                    should_send = True

            if should_send:
                logger.info("📨 Отправка предупреждения о балансах всем администраторам")
                is_running = await get_scanner_state_from_db() == 'running'
                keyboard = get_scanner_menu_keyboard(is_running=is_running)

                for admin_id in config.tg_bot.admin_ids:
                    # Используем глобальный notifier_service, так как он инициализируется один раз
                    await app_state.notifier_service.send_message(
                        admin_id, text=warning_message, reply_markup=keyboard
                    )

                stmt_set = insert(SystemState).values(key=warning_key, value=now.isoformat())
                stmt_set = stmt_set.on_conflict_do_update(
                    index_elements=['key'], set_={'value': stmt_set.excluded.value}
                )
                await session.execute(stmt_set)
                await session.commit()

    async def get_healthy_services(self) -> Dict:
        """Возвращает здоровые сервисы."""
        await self.initialize()
        return await service_manager.get_healthy_services()

    async def _fetch_prices(self, assets: Set[str]):
        """
        ПОЛНОСТЬЮ ПЕРЕРАБОТАННАЯ ВЕРСИЯ: Динамически запрашивает цены
        у каждой биржи только для тех активов, которые на ней есть.
        """
        await self.initialize()
        healthy_services = await service_manager.get_healthy_services()
        if not healthy_services:
            return

        # Шаг 1: Создаем задачи для получения рынков с каждой биржи параллельно.
        # Это нужно, чтобы знать, какие монеты где торгуются.
        market_tasks = [service.client.load_markets() for service in healthy_services.values()]
        market_results = await asyncio.gather(*market_tasks, return_exceptions=True)

        # Шаг 2: Группируем монеты по биржам.
        # a. Создаем словарь: { 'binance': {'BTC', 'ETH'}, 'bybit': {'SOL', 'BTC'} }
        exchange_to_assets: Dict[str, Set[str]] = {}
        service_list = list(healthy_services.values())  # Сохраняем порядок

        for i, markets in enumerate(market_results):
            service = service_list[i]
            exchange_id = service.exchange_id
            exchange_to_assets[exchange_id] = set()

            if isinstance(markets, dict):
                # b. Для каждой биржи находим, какие из НАШИХ активов на ней торгуются.
                for asset in assets:
                    symbol = f"{asset}/{PRIMARY_QUOTE_CURRENCY}"
                    if symbol in markets:
                        exchange_to_assets[exchange_id].add(asset)

        # Шаг 3: Создаем задачи для получения цен с каждой биржи параллельно.
        price_tasks = []
        exchange_ids = []

        for exchange_id, exchange_assets in exchange_to_assets.items():
            if exchange_assets:
                service = healthy_services[exchange_id]
                # Формируем список пар для запроса (например, ['BTC/USDT', 'ETH/USDT'])
                symbols_to_fetch = [f"{asset}/{PRIMARY_QUOTE_CURRENCY}" for asset in exchange_assets]
                logger.debug(f"Запрос цен для {len(symbols_to_fetch)} пар с биржи '{exchange_id}'...")

                # Добавляем задачу в список
                price_tasks.append(service.get_tickers(symbols_to_fetch))
                exchange_ids.append(exchange_id)

        # Шаг 4: Выполняем все запросы цен и собираем результаты.
        if price_tasks:
            all_prices_results = await asyncio.gather(*price_tasks, return_exceptions=True)
        else:
            all_prices_results = []

        # Шаг 5: Объединяем все полученные цены в один словарь.
        final_prices: Dict[str, float] = {}

        for i, price_dict in enumerate(all_prices_results):
            exchange_id = exchange_ids[i] if i < len(exchange_ids) else "unknown"

            if isinstance(price_dict, Exception):
                logger.error(f"Ошибка получения цен с {exchange_id}: {price_dict}")
                continue

            if isinstance(price_dict, dict):
                symbols_received = len(price_dict)
                logger.info(f"Цены успешно получены для {symbols_received} символов с биржи '{exchange_id}'.")
                final_prices.update(price_dict)

        # Добавляем стейблкоины, как и раньше.
        for asset in assets:
            if asset.upper() in STABLE_COINS:
                final_prices[f"{asset}/{PRIMARY_QUOTE_CURRENCY}"] = STABLECOIN_PRICE

        # Обновляем кэш цен в сервисе.
        self.prices = final_prices
        total_assets = len(assets)
        prices_found = sum(1 for asset in assets if f"{asset}/{PRIMARY_QUOTE_CURRENCY}" in final_prices)

        logger.info(f"Итоговый сбор цен: найдено {prices_found} из {total_assets} уникальных активов.")

        # Логируем отсутствующие цены для отладки
        missing_assets = [asset for asset in assets
                          if f"{asset}/{PRIMARY_QUOTE_CURRENCY}" not in final_prices
                          and asset.upper() not in STABLE_COINS]

        if missing_assets:
            logger.warning(
                f"Не найдены цены для {len(missing_assets)} активов: {missing_assets[:10]}{'...' if len(missing_assets) > 10 else ''}")

    def _calculate_usd_value(self, asset: str, quantity: float) -> float:
        """Вычисляет USD стоимость актива."""
        if asset.upper() in STABLE_COINS:
            return float(quantity)

        price = self.prices.get(f"{asset}/{PRIMARY_QUOTE_CURRENCY}", 0.0)
        return float(quantity) * float(price)

    async def generate_report_messages(self, mode: str) -> Tuple[List[str], str]:
        """
        ФИНАЛЬНАЯ ВЕРСИЯ: Создает стильный и корректно отформатированный отчет.
        """
        raw_balances = await self.get_all_balances()
        if not raw_balances:
            return ["❌ Не удалось подключиться ни к одной бирже."], mode

        async with async_session_factory() as session:
            stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == self.user_id)
            tracked_coins = set((await session.execute(stmt)).scalars().all())

        if mode == 'tracked' and not tracked_coins:
            return ["📋 У вас нет отслеживаемых монет."], mode

        all_user_assets = set()
        for balances in raw_balances.values():
            all_user_assets.update(balances.keys())
        await self._fetch_prices(all_user_assets)

        total_portfolio_value = 0
        exchange_reports = []

        def get_asset_emoji(asset: str, value_in_usd: float) -> str:
            asset_upper = asset.upper()
            crypto_emojis = {
                'BTC': '₿', 'ETH': 'Ξ', 'BNB': '🔶', 'ADA': '💙', 'DOT': '🔴',
                'LINK': '🔗', 'UNI': '🦄', 'LTC': '🔹', 'XRP': '💧', 'DOGE': '🐕',
                'SHIB': '🐶', 'PEPE': '🐸', 'FLOKI': '🐕‍🦺', 'BONK': '🏓'
            }
            if asset_upper in crypto_emojis: return crypto_emojis[asset_upper]
            if asset_upper in STABLE_COINS: return '💵'
            if value_in_usd == -1: return '🌍'
            if value_in_usd >= 1000: return '💎'
            if value_in_usd >= 100: return '🟢'
            if value_in_usd >= 10: return '🟡'
            return '🟠'

        for exchange_id, balance_data in sorted(raw_balances.items()):
            assets_to_process = {asset: amount for asset, amount in balance_data.items()
                                 if mode == 'all' or asset in tracked_coins}
            if not assets_to_process: continue

            exchange_total_value = 0
            crypto_lines, fiat_lines = [], []

            for asset, quantity in sorted(assets_to_process.items()):
                if quantity < MINIMUM_QUANTITY_THRESHOLD: continue

                safe_asset_name = html.escape(asset)
                usd_value = self._calculate_usd_value(asset, quantity)

                if quantity >= 1000000:
                    qty_display = f"{quantity / 1000000:.2f}M"
                elif quantity >= 1000:
                    qty_display = f"{quantity / 1000:.2f}K"
                else:
                    qty_display = f"{quantity:,.8f}".rstrip('0').rstrip('.')

                if usd_value >= MINIMUM_VALUE_THRESHOLD:
                    # Это крипто-актив с ценой. Вызываем emoji с реальной стоимостью.
                    asset_emoji = get_asset_emoji(asset, usd_value)
                    exchange_total_value += usd_value
                    line = f"{asset_emoji} <b>{safe_asset_name}</b> <code>{qty_display}</code> → <b>${usd_value:,.2f}</b>"
                    crypto_lines.append((line, usd_value))
                else:
                    # Это фиат или актив без цены. Вызываем emoji со специальным флагом -1.0.
                    asset_emoji = get_asset_emoji(asset, -1.0)
                    line = f"{asset_emoji} <b>{safe_asset_name}</b> <code>{qty_display}</code> → <i>н/д</i>"
                    fiat_lines.append((line, -1.0))

            all_lines = []
            if crypto_lines:
                crypto_lines.sort(key=lambda x: x[1], reverse=True)
                all_lines.extend(crypto_lines)
            if fiat_lines:
                if crypto_lines: all_lines.append(("", -2))
                all_lines.extend(fiat_lines)

            if all_lines:
                exchange_reports.append({
                    'name': exchange_id.capitalize(), 'total': exchange_total_value,
                    'lines': [line[0] for line in all_lines], 'crypto_count': len(crypto_lines),
                    'fiat_count': len(fiat_lines)
                })
                total_portfolio_value += exchange_total_value

        if not exchange_reports:
            return ["📭 На ваших биржах нет активов для отображения."], mode

        final_report_lines = [
            "┏━━━━━━━━━━━━━━━━━━━━━━┓",
            "┃ 💰 <b>КРИПТОПОРТФЕЛЬ</b>                                    ┃",
            "┗━━━━━━━━━━━━━━━━━━━━━━┛",
            "",
            f"💎 <b>Общая стоимость:</b> <code>${total_portfolio_value:,.2f}</code>",
            "",
            "<i><u>Легенда иконок:</u></i>",
            "💎 - &gt; $1000 | 🟢 - &gt; $100 | 🟡 - &gt; $10",
            "🟠 - &lt; $10   | 💵 - Стейблкоины",
            "🌍 - Фиат / Нет данных о цене"
        ]

        exchange_reports.sort(key=lambda x: x['total'], reverse=True)

        for i, report in enumerate(exchange_reports, 1):
            emoji_num = get_number_emoji(i)

            # --- ИЗМЕНЕНИЕ 2: Добавлены поясняющие слова к статистике ---
            stats_parts = []
            if report['crypto_count'] > 0:
                stats_parts.append(f"Крипто: 🪙 {report['crypto_count']}")
            if report['fiat_count'] > 0:
                stats_parts.append(f"Фиат: 🌍 {report['fiat_count']}")
            stats_text = " | ".join(stats_parts)

            final_report_lines.extend([
                "", "━━━━━━━━━━━━━━━━━━━━━━",
                f"{emoji_num} <b>{report['name']}</b> • <code>${report['total']:,.2f}</code>",
                f"<i>{stats_text}</i>", ""
            ])

            # --- ИЗМЕНЕНИЕ 3: Логика для символа └─ на последнем элементе ---
            num_lines = len(report['lines'])
            for idx, line_text in enumerate(report['lines']):
                is_last = (idx == num_lines - 1)
                prefix = "└─" if is_last else "├─"

                if line_text == "":
                    # Для разделителя фиата всегда используем ├─, если он не последний
                    final_report_lines.append(f"{prefix} <i>Фиатные валюты:</i>")
                else:
                    final_report_lines.append(f"{prefix} {line_text}")

        final_report_lines.extend([
            "", "━━━━━━━━━━━━━━━━━━━━━━",
            f"📊 <i>Отчет создан: {self._get_current_time()}</i>"
        ])

        return self._split_message(final_report_lines), mode

    def _get_current_time(self) -> str:
        """Возвращает текущее время в красивом формате."""
        from datetime import datetime
        import pytz

        # Используем киевское время из логов
        tz = pytz.timezone('Europe/Kiev')
        now = datetime.now(tz)
        return now.strftime("%H:%M %d.%m.%y")

    def _split_message(self, lines: List[str]) -> List[str]:
        """Разделяет длинный отчет на несколько сообщений."""
        if not lines: return []
        messages, current_message = [], ""
        for line in lines:
            if len(current_message) + len(line) + 1 > TELEGRAM_MESSAGE_MAX_LENGTH:
                messages.append(current_message)
                current_message = line
            else:
                current_message += ("\n" if current_message else "") + line
        if current_message: messages.append(current_message)
        return messages

    async def get_all_min_order_limits(self) -> Dict[str, float]:
        """
        ✨ ИСПРАВЛЕННАЯ ВЕРСИЯ с фильтрацией некорректных лимитов.
        """
        await self.initialize()

        if not self.validated_services:
            logger.warning("Нет активных сервисов для получения лимитов")
            return {}

        # Создаем задачи для параллельного выполнения
        limit_tasks = []
        exchange_names = []

        for ex_id, service in self.validated_services.items():
            task = service.get_reliable_min_order_value(DEFAULT_FALLBACK_SYMBOL)
            limit_tasks.append(task)
            exchange_names.append(ex_id)

        # Выполняем все запросы параллельно
        try:
            results = await asyncio.gather(*limit_tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Критическая ошибка при получении лимитов: {e}")
            return {
                ex_id: EXCHANGE_MIN_ORDER_VALUES.get(ex_id, DEFAULT_TRADE_AMOUNT_USD)
                for ex_id in exchange_names
            }

        # Обрабатываем результаты
        limits = {}
        for ex_id, result in zip(exchange_names, results):
            if isinstance(result, BaseException):
                # Используем fallback при ошибке
                fallback = EXCHANGE_MIN_ORDER_VALUES.get(ex_id, DEFAULT_TRADE_AMOUNT_USD)
                limits[ex_id] = fallback
                logger.warning(f"Fallback лимит для {ex_id}: ${fallback:.2f} (ошибка: {type(result).__name__})")
            else:
                try:
                    limit_value = float(result)

                    # 🔧 ИСПРАВЛЕНИЕ: Фильтруем некорректные значения
                    if limit_value <= 0:
                        fallback = EXCHANGE_MIN_ORDER_VALUES.get(ex_id, DEFAULT_TRADE_AMOUNT_USD)
                        limits[ex_id] = fallback
                        logger.warning(
                            f"Некорректный лимит для {ex_id}: {limit_value:.2f}. Использую fallback: ${fallback:.2f}")
                    else:
                        limits[ex_id] = limit_value
                        logger.info(f"Актуальный лимит для {ex_id}: ${limit_value:.2f}")

                except (ValueError, TypeError) as e:
                    fallback = EXCHANGE_MIN_ORDER_VALUES.get(ex_id, DEFAULT_TRADE_AMOUNT_USD)
                    limits[ex_id] = fallback
                    logger.warning(
                        f"Ошибка преобразования лимита для {ex_id}: {e}. Использую fallback: ${fallback:.2f}")

        return limits

    def calculate_safe_trade_limits(self, all_balances: Dict, min_limits: Dict[str, float]) -> dict:
        """
        УЛУЧШЕННАЯ ВЕРСИЯ: Анализирует все биржи и возвращает структурированный отчет
        вместо остановки на первой проблеме.

        Returns:
            dict: {
                'min_trade_amount': float,
                'max_trade_amount': float,
                'sufficient_exchanges': [{'exchange': str, 'balance': float}],
                'insufficient_exchanges': [{'exchange': str, 'current': float, 'required': float, 'shortage': float}]
            }
        """
        logger.debug(f"🔍 Входные лимиты для анализа: {min_limits}")

        # Шаг 1: Валидация лимитов
        valid_limits = {}
        for exchange_id, limit in min_limits.items():
            min_threshold = MIN_API_LIMIT_THRESHOLD_YOBIT if exchange_id == 'yobit' else MIN_API_LIMIT_THRESHOLD
            if limit >= min_threshold:
                valid_limits[exchange_id] = limit
            else:
                fallback = EXCHANGE_MIN_ORDER_VALUES.get(exchange_id, DEFAULT_TRADE_AMOUNT_USD)
                valid_limits[exchange_id] = fallback
                logger.warning(f"🔧 {exchange_id}: некорректный лимит ${limit:.4f} заменен на fallback ${fallback:.2f}")

        # Шаг 2: Расчет минимальной суммы (логика остается прежней)
        min_amount = max(valid_limits.values()) if valid_limits else DEFAULT_TRADE_AMOUNT_USD
        logger.info(f"📊 Минимальная сумма для торговли: ${min_amount:.2f}")

        # Шаг 3: Разделяем биржи на категории
        sufficient_exchanges = []
        insufficient_exchanges = []
        usdt_balances = []

        for exchange_id in valid_limits.keys():
            balances = all_balances.get(exchange_id, {})
            usdt_balance = balances.get(PRIMARY_QUOTE_CURRENCY, 0.0)
            required_with_margin = min_amount / TRADE_AMOUNT_SAFETY_MARGIN

            if usdt_balance >= required_with_margin:
                # Биржа готова к торговле
                sufficient_exchanges.append({
                    'exchange': exchange_id,
                    'balance': usdt_balance
                })
                usdt_balances.append(usdt_balance)
                logger.debug(f"✅ {exchange_id}: готов (${usdt_balance:.2f} >= ${required_with_margin:.2f})")
            else:
                # Биржа имеет недостаток средств
                shortage = required_with_margin - usdt_balance
                insufficient_exchanges.append({
                    'exchange': exchange_id,
                    'current': usdt_balance,
                    'required': required_with_margin,
                    'shortage': shortage
                })
                logger.debug(f"❌ {exchange_id}: недостаток ${shortage:.2f}")

        # Шаг 4: Расчет максимальной суммы для готовых бирж
        safe_max = 0.0
        if usdt_balances:
            raw_max = min(usdt_balances)
            safe_max = raw_max * TRADE_AMOUNT_SAFETY_MARGIN

        logger.info(
            f"📊 Анализ завершен: готовых бирж {len(sufficient_exchanges)}, проблемных {len(insufficient_exchanges)}")

        # Возвращаем структурированный отчет вместо ошибки
        return {
            'min_trade_amount': min_amount,
            'max_trade_amount': safe_max,
            'sufficient_exchanges': sufficient_exchanges,
            'insufficient_exchanges': insufficient_exchanges
        }

    async def _analyze_sell_capabilities(self, all_balances: Dict, tracked_coins: List[str], min_limits: Dict) -> Dict:
        """
        Анализирует наличие отслеживаемых монет на биржах для возможности их продажи.
        Возвращает список монет, которые реально можно продать.
        """
        sellable_coins = set()

        for coin in tracked_coins:
            coin_is_sellable_somewhere = False
            for exchange_id, balances in all_balances.items():
                coin_balance = balances.get(coin, 0.0)

                # Используем грубую оценку, чтобы понять, есть ли значимое количество монеты
                # Минимальный лимит ордера / 10 (чтобы отсечь совсем пыль)
                min_sell_value_threshold = min_limits.get(exchange_id, DEFAULT_TRADE_AMOUNT_USD) * MIN_SELL_VALUE_RATIO

                # Приблизительная стоимость монет на балансе
                approximate_value = coin_balance * STABLECOIN_PRICE  # Используем 1.0 для скорости

                if approximate_value > min_sell_value_threshold:
                    coin_is_sellable_somewhere = True
                    break  # Нашли монету на одной бирже, переходим к следующей

            if coin_is_sellable_somewhere:
                sellable_coins.add(coin)

        return {
            'sellable_coins_list': sorted(list(sellable_coins)),
            'all_tracked_coins': tracked_coins,
            'unavailable_for_sell': sorted(list(set(tracked_coins) - sellable_coins))
        }

    async def perform_pre_flight_check(self, trade_amount: float, tracked_coins: List[str]) -> dict:
        """
        Выполняет полную пред-полетную проверку с детализированным сообщением об ошибке.
        """
        min_limits = await self.get_all_min_order_limits()
        all_balances = await self.get_all_balances()

        if not all_balances:
            return {'can_trade': False, 'warning_message': 'Не удалось получить балансы.', 'balances': {}}

        # 1. Анализ USDT для ПОКУПКИ
        buy_capable = []
        insufficient_exchanges_details = []  # Собираем детали для сообщения

        for exchange_id, balances in all_balances.items():
            usdt_balance = balances.get(PRIMARY_QUOTE_CURRENCY, 0.0)
            # Рассчитываем, сколько реально нужно USDT с учетом всех лимитов и запаса
            min_limit_for_exchange = min_limits.get(exchange_id, DEFAULT_TRADE_AMOUNT_USD)
            actually_required_amount = max(trade_amount, min_limit_for_exchange)
            required_usdt_with_margin = actually_required_amount / TRADE_AMOUNT_SAFETY_MARGIN

            if usdt_balance >= required_usdt_with_margin:
                buy_capable.append(exchange_id)
            else:
                shortage = required_usdt_with_margin - usdt_balance
                insufficient_exchanges_details.append({
                    'exchange': exchange_id,
                    'shortage': shortage
                })

        # 2. Анализ МОНЕТ для ПРОДАЖИ
        sell_analysis = await self._analyze_sell_capabilities(all_balances, tracked_coins, min_limits)

        # 3. Формирование результата
        can_buy = len(buy_capable) >= MIN_BUY_CAPABLE_EXCHANGES
        can_sell = len(sell_analysis['sellable_coins_list']) > 0
        enough_exchanges = len(all_balances) >= MIN_EXCHANGES_FOR_ARBITRAGE

        can_trade = can_buy and can_sell and enough_exchanges

        warning_message = ""
        if insufficient_exchanges_details:
            problem_details = [
                f"• {problem['exchange'].capitalize()}: нехватка ${problem['shortage']:.2f}"
                for problem in insufficient_exchanges_details
            ]
            warning_message = (
                    f"⚠️ <b>Следующие биржи не могут быть использованы для ПОКУПКИ:</b>\n" +
                    "\n".join(problem_details) +
                    f"\n\n<i>Они все еще могут участвовать в сделках в роли продавца.</i>"
            )

        if not can_sell and can_buy:  # Добавляем вторую часть, если нужно
            warning_message += ("\n\n🚨 <b>КРИТИЧНО:</b> На балансах нет ни одной из отслеживаемых монет для продажи. "
                                "Арбитраж невозможен.")

        return {
            'can_trade': can_trade,
            'buy_capable_exchanges': buy_capable,
            'sell_capability_info': sell_analysis,
            'warning_message': warning_message.strip(),
            'balances': all_balances
        }
