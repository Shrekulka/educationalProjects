# inter_exchange_arbitrage_bot/src/services/data_enricher_service.py

import asyncio
import html
import random
from collections import defaultdict
from typing import List, Dict, Optional, Set

import httpx
import numpy as np
import pandas as pd

from src.constants.trading_constants import ENRICHMENT_CONFIG, TRENDING_FALLBACK_TOKENS

try:
    import talib

    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False

from src.constants.api_constants import (
    CMC_PRO_API_BASE_URL, CMC_QUOTES_LATEST_ENDPOINT, CMC_GLOBAL_METRICS_LATEST, CMC_FEAR_AND_GREED_LATEST,
    CMC_TRENDING_TOKENS_LATEST, CMC_CRYPTO_INFO_ENDPOINT, CRYPTOPANIC_API_BASE_URL, ENRICHER_HTTP_TIMEOUT,
    CMC_LISTINGS_LATEST_ENDPOINT
)
from src.constants.telegram_constants import SPARKLINE_CHARS
from src.core.config import config
from src.strategies.arbitrage_strategy import ArbitrageOpportunity
from src.strategies.enums import RiskLevel, MACDSignal, RSIStatus
from src.utils.logger import logger


class DataEnricherService:
    def __init__(self):
        """Инициализирует HTTP-клиент для внешних API."""
        self.http_client = httpx.AsyncClient(timeout=ENRICHER_HTTP_TIMEOUT)

    async def enrich_opportunities(self, opportunities: List[ArbitrageOpportunity], services: Dict) -> List[
        ArbitrageOpportunity]:
        """Главный метод, оркестрирующий процесс обогащения данных."""
        if not opportunities:
            return []

        tickers = list(set([opp.coin for opp in opportunities]))
        logger.info(f"Начинаем обогащение данных для {len(tickers)} уникальных тикеров")

        cmc_data_task = self._fetch_cmc_data(tickers)
        news_data_task = self._fetch_news_data(tickers)
        trending_task = self._fetch_trending_tokens()
        info_task = self._fetch_crypto_info(tickers)

        results = await asyncio.gather(
            cmc_data_task, news_data_task, trending_task, info_task,
            return_exceptions=True
        )

        cmc_data = results[0] if isinstance(results[0], dict) else {}
        news_data = results[1] if isinstance(results[1], dict) else {}
        trending_set = results[2] if isinstance(results[2], set) else set()
        info_data = results[3] if isinstance(results[3], dict) else {}

        # --- ШАГ 2: Обогащаем каждую возможность ---
        enrichment_tasks = [
            self._enrich_single_opportunity(opp, services, cmc_data, news_data, trending_set, info_data)
            for opp in opportunities
        ]
        enriched_opportunities = await asyncio.gather(*enrichment_tasks, return_exceptions=True)

        return [opp for opp in enriched_opportunities if isinstance(opp, ArbitrageOpportunity)]

    async def _enrich_single_opportunity(self, opp: ArbitrageOpportunity, services: Dict, cmc_data: Dict,
                                         news_data: Dict, trending_set: Set, info_data: Dict) -> ArbitrageOpportunity:
        """Обогащает один объект ArbitrageOpportunity."""
        try:
            # ✅ ИСПРАВЛЕНИЕ: Универсальная обработка данных CMC
            if opp.coin in cmc_data:
                raw_coin_data = cmc_data[opp.coin]

                # Проверяем, что мы получили от API - список или словарь
                if isinstance(raw_coin_data, list):
                    # Если список, берем первый элемент
                    coin_info = raw_coin_data[0] if raw_coin_data else {}
                    logger.debug(f"CMC API вернул список для {opp.coin}, взят первый элемент")
                elif isinstance(raw_coin_data, dict):
                    # Если словарь, используем как есть
                    coin_info = raw_coin_data
                else:
                    logger.warning(f"Неожиданный тип данных CMC для {opp.coin}: {type(raw_coin_data)}")
                    coin_info = {}

                # Теперь безопасно извлекаем данные
                if coin_info and isinstance(coin_info, dict):
                    quote_data = coin_info.get('quote', {}).get('USD', {})
                    opp.cmc_slug = html.escape(str(coin_info.get('slug', ''))) if coin_info.get('slug') else None
                    opp.market_data.price = quote_data.get('price', 0)
                    opp.market_data.price_24h_change = quote_data.get('percent_change_24h', 0)
                    opp.market_data.volume_24h_usd = quote_data.get('volume_24h', 0)
                    opp.market_data.market_cap_usd = quote_data.get('market_cap', 0)
                    opp.market_data.listings_count = coin_info.get('num_market_pairs', 0)
                    logger.debug(f"Успешно обогащен {opp.coin} данными CMC")
                else:
                    logger.warning(f"Пустые или некорректные данные CMC для {opp.coin}")

            # ✅ ИСПРАВЛЕНИЕ: Безопасная обработка данных info
            if opp.coin in info_data:
                raw_info_data = info_data[opp.coin]
                if isinstance(raw_info_data, list):
                    info_item = raw_info_data[0] if raw_info_data else {}
                elif isinstance(raw_info_data, dict):
                    info_item = raw_info_data
                else:
                    info_item = {}

                raw_tags = info_item.get('tags', []) if isinstance(info_item, dict) else []
                opp.tags = [html.escape(str(tag)) for tag in raw_tags if tag]

            # Остальная логика остается без изменений
            if opp.coin in trending_set:
                opp.is_trending = True

            if opp.coin in news_data:
                opp.drivers = news_data[opp.coin][:ENRICHMENT_CONFIG['API_LIMITS']['NEWS_TOP_N']]

            # Технический анализ
            service = services.get(opp.buy_exchange_id)
            if not service: return opp

            if service and service.client.has['fetchOHLCV']:
                ta_config = ENRICHMENT_CONFIG['TECHNICAL_ANALYSIS']
                try:
                    ohlcv = await service.client.fetch_ohlcv(opp.symbol, timeframe=ta_config['OHLCV_TIMEFRAME'],
                                                             limit=ta_config['OHLCV_LIMIT'])
                    if ohlcv and len(ohlcv) >= ta_config['MIN_OHLCV_RECORDS']:
                        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                        if not df.empty:
                            self._calculate_technical_indicators(opp, df)
                except Exception as e:
                    logger.debug(f"Не удалось получить OHLCV для {opp.symbol} на {opp.buy_exchange_id}: {e}")
            else:
                logger.debug(
                    f"Пропуск теханализа для {opp.symbol} на {opp.buy_exchange_id}: fetchOHLCV не поддерживается.")

            # Расчет производных метрик
            opp.liquidity_usd = opp.buy_analysis.available_liquidity_usd if opp.buy_analysis else 0
            opp.execution_time_seconds = self._estimate_execution_time(opp)
            opp.ai_score = self._calculate_ai_score(opp)
            opp.risk_level = self._determine_risk_level(opp)
            opp.potential_reason, opp.action_recommendation = self._generate_recommendations(opp)

            return opp

        except Exception as e:
            logger.error(f"Ошибка обогащения {opp.symbol}: {type(e).__name__} - {e}")
            return opp

    def _estimate_execution_time(self, opp: ArbitrageOpportunity) -> float:
        """Примерная оценка времени исполнения в секундах."""
        base_time = 30.0  # Базовое время
        if opp.market_data.market_cap_usd > 1_000_000_000:
            base_time -= 10  # large-cap обычно быстрее
        if opp.market_data.listings_count < 5:
            base_time += 20  # мало листингов, возможны задержки
        return base_time + random.uniform(0, 15)  # Добавляем случайности

    def _generate_recommendations(self, opp: ArbitrageOpportunity) -> (Optional[str], Optional[str]):
        """Генерирует осмысленные текстовые рекомендации."""
        potential = []
        action = "👁️ НАБЛЮДАТЬ"  # Рекомендация по умолчанию

        # --- Анализ для action_recommendation ---
        if opp.is_phantom:
            action = f"❌ ИЗБЕГАТЬ. Причина: {opp.phantom_reason}"
        elif opp.ai_score >= 8.0:
            if opp.roi_percent > 0.5:  # Если ROI хороший
                action = "✅ ИСПОЛНЯТЬ АРБИТРАЖ. Сигнал высокого качества."
            else:  # Если ROI очень низкий
                action = "✅ ИСПОЛНЯТЬ АРБИТРАЖ. Сигнал чистый, но ROI невысокий."
        elif 6.0 <= opp.ai_score < 8.0:
            action = "🎯 РАССМОТРЕТЬ АРБИТРАЖ."
            if opp.technical_analysis.volume_spike_ratio > 1.5:
                action += f" Наблюдается всплеск объема (🔥{int((opp.technical_analysis.volume_spike_ratio - 1) * 100)}%), что подтверждает интерес к активу."
            elif opp.technical_analysis.rsi_status == RSIStatus.OVERSOLD:
                action += " Актив в зоне перепроданности, возможен скорый отскок цены вверх."

        # --- Анализ для potential_reason (если он не был задан ранее) ---
        if not opp.potential_reason:
            if opp.technical_analysis.volume_spike_ratio > 2.0:
                potential.append("аномальный всплеск объема")
            if opp.technical_analysis.rsi_status == RSIStatus.OVERSOLD:
                potential.append("сильная перепроданность")
            if opp.is_trending:
                potential.append("монета в трендах")

            reason_text = ", ".join(potential).capitalize() if potential else None
        else:
            reason_text = opp.potential_reason

        return reason_text, action

    def _calculate_rsi(self, prices: pd.Series, length: int = 14) -> float:
        """Вычисляет RSI вручную."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50.0

    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
        """Вычисляет MACD вручную."""
        exp1 = prices.ewm(span=fast).mean()
        exp2 = prices.ewm(span=slow).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=signal).mean()
        return macd_line.iloc[-1], signal_line.iloc[-1]

    def _calculate_technical_indicators(self, opp: ArbitrageOpportunity, df: pd.DataFrame):
        """Вычисляет все технические индикаторы и тренды."""
        ta_config = ENRICHMENT_CONFIG['TECHNICAL_ANALYSIS']
        try:
            close_prices = df['close']

            # RSI
            if HAS_TALIB:
                rsi_values = talib.RSI(close_prices.values, timeperiod=ta_config['RSI_LENGTH'])
                rsi_value = rsi_values[-1] if not np.isnan(rsi_values[-1]) else 50.0
            else:
                rsi_value = self._calculate_rsi(close_prices, ta_config['RSI_LENGTH'])

            opp.technical_analysis.rsi_14 = rsi_value
            if rsi_value > ta_config['RSI_CRITICAL_OVERBOUGHT']:
                opp.technical_analysis.rsi_status = RSIStatus.CRITICAL_OVERBOUGHT
            elif rsi_value > ta_config['RSI_OVERBOUGHT']:
                opp.technical_analysis.rsi_status = RSIStatus.OVERBOUGHT
            elif rsi_value < ta_config['RSI_OVERSOLD']:
                opp.technical_analysis.rsi_status = RSIStatus.OVERSOLD
            else:
                opp.technical_analysis.rsi_status = RSIStatus.HEALTHY

            # MACD
            if HAS_TALIB:
                macd_line, signal_line, _ = talib.MACD(close_prices.values, fastperiod=ta_config['MACD_FAST'],
                                                       slowperiod=ta_config['MACD_SLOW'],
                                                       signalperiod=ta_config['MACD_SIGNAL'])
                macd_val, signal_val = macd_line[-1], signal_line[-1]
            else:
                macd_val, signal_val = self._calculate_macd(close_prices, ta_config['MACD_FAST'],
                                                            ta_config['MACD_SLOW'], ta_config['MACD_SIGNAL'])

            if not pd.isna(macd_val) and not pd.isna(signal_val):
                if macd_val > signal_val:
                    opp.technical_analysis.macd_signal = MACDSignal.BULLISH
                else:
                    opp.technical_analysis.macd_signal = MACDSignal.BEARISH

            # Спарклайн (график тренда)
            prices = df['close'].tail(ta_config['SPARKLINE_PERIOD']).tolist()
            min_p, max_p = min(prices), max(prices)
            sparkline = ""
            if max_p > min_p:
                for p in prices:
                    idx = int((p - min_p) / (max_p - min_p) * (len(SPARKLINE_CHARS) - 1))
                    sparkline += SPARKLINE_CHARS[idx]
            opp.technical_analysis.price_trend_sparkline = sparkline

            # Всплеск объема
            avg_volume = df['volume'].rolling(window=ta_config['VOLUME_SPIKE_WINDOW']).mean().iloc[-1]
            last_hour_volume = df['volume'].iloc[-1]
            if avg_volume > 0:
                opp.technical_analysis.volume_spike_ratio = last_hour_volume / avg_volume
        except Exception as e:
            logger.error(f"Ошибка вычисления техиндикаторов для {opp.symbol}: {e}")

    async def _fetch_cmc_data(self, tickers: List[str]) -> Dict:
        """Получает данные от CoinMarketCap."""
        if not config.news_apis.coinmarketcap or not tickers:
            return {}

        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': config.news_apis.coinmarketcap}
        params = {'symbol': ','.join(tickers[:ENRICHMENT_CONFIG['API_LIMITS']['CMC_MAX_SYMBOLS']])}
        url = f"{CMC_PRO_API_BASE_URL}{CMC_QUOTES_LATEST_ENDPOINT}"

        try:
            response = await self.http_client.get(url, headers=headers, params=params)
            response.raise_for_status()

            raw_data = response.json().get('data', {})
            logger.debug(f"Получены данные CMC для {len(raw_data)} символов")

            # ✅ ИСПРАВЛЕНИЕ: Нормализация данных
            normalized_data = {}
            for symbol, data_value in raw_data.items():
                try:
                    if isinstance(data_value, list):
                        # API иногда возвращает массив объектов
                        normalized_data[symbol] = data_value[0] if data_value else {}
                        logger.debug(f"Нормализован список для {symbol}")
                    elif isinstance(data_value, dict):
                        # Обычный случай - объект
                        normalized_data[symbol] = data_value
                    else:
                        logger.warning(f"Неожиданный тип данных CMC для {symbol}: {type(data_value)}")
                        normalized_data[symbol] = {}
                except Exception as e:
                    logger.error(f"Ошибка нормализации данных для {symbol}: {e}")
                    normalized_data[symbol] = {}

            return normalized_data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP ошибка CoinMarketCap API: {e.response.status_code}")
            if e.response.status_code == 429:
                logger.warning("Достигнут лимит запросов CMC API")
            return {}
        except httpx.TimeoutException:
            logger.error("Таймаут запроса к CoinMarketCap API")
            return {}
        except Exception as e:
            logger.error(f"Неожиданная ошибка при запросе к CoinMarketCap: {type(e).__name__} - {e}")
            return {}

    async def _fetch_news_data(self, tickers: List[str]) -> Dict:
        """Получает новости от CryptoPanic, разбивая запрос на части."""
        if not config.news_apis.cryptopanic or not tickers: return {}
        all_news = defaultdict(list)
        chunk_size = ENRICHMENT_CONFIG['API_LIMITS']['CRYPTOPANIC_MAX_CURRENCIES_PER_REQUEST']
        tasks = []
        for i in range(0, len(tickers), chunk_size):
            chunk = tickers[i:i + chunk_size]
            params = {'auth_token': config.news_apis.cryptopanic, 'currencies': ','.join(chunk), 'public': 'true'}
            tasks.append(self.http_client.get(CRYPTOPANIC_API_BASE_URL, params=params))

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for result in responses:
            if isinstance(result, httpx.Response) and result.status_code == 200:
                for post in result.json().get('results', []):
                    if post.get('currencies'):
                        for currency in post['currencies']:
                            all_news[currency['code']].append({
                                'title': post.get('title', 'Без заголовка'),
                                'url': post.get('url'),
                                'source': post.get('source', {}).get('title', 'Неизвестный источник')
                            })
        return all_news

    async def _fetch_global_metrics(self) -> Dict:
        """Получает глобальные метрики рынка от CoinMarketCap."""
        if not config.news_apis.coinmarketcap: return {}
        url = f"{CMC_PRO_API_BASE_URL}{CMC_GLOBAL_METRICS_LATEST}"
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': config.news_apis.coinmarketcap}
        try:
            response = await self.http_client.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get('data', {})
        except Exception as e:
            logger.error(f"Ошибка при запросе глобальных метрик CMC: {e}")
            return {}

    async def _fetch_fear_and_greed_index(self) -> Dict:
        """Получает индекс страха и жадности от CoinMarketCap."""
        if not config.news_apis.coinmarketcap: return {}
        url = f"{CMC_PRO_API_BASE_URL}{CMC_FEAR_AND_GREED_LATEST}"
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': config.news_apis.coinmarketcap}
        try:
            response = await self.http_client.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get('data', {})
        except Exception as e:
            logger.error(f"Ошибка при запросе Fear & Greed Index: {e}")
            return {}

    async def _fetch_trending_tokens(self) -> Set[str]:
        """
        Получает список трендовых токенов с обработкой 403 ошибки и использованием Fallback-стратегии.
        """
        if not config.news_apis.coinmarketcap:
            return set()

        url = f"{CMC_PRO_API_BASE_URL}{CMC_TRENDING_TOKENS_LATEST}"
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': config.news_apis.coinmarketcap}

        try:
            response = await self.http_client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json().get('data', [])
            trending_symbols = {item['symbol'] for item in data}
            logger.info(f"Успешно получено {len(trending_symbols)} трендовых токенов через Pro API.")
            return trending_symbols

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                logger.warning(
                    "Доступ к эндпоинту трендов запрещен (403 Forbidden). Используется резервный список популярных токенов.")
                return TRENDING_FALLBACK_TOKENS
            else:
                logger.error(
                    f"HTTP ошибка при запросе трендовых токенов: {e.response.status_code}. Используется резервный список.")
                return TRENDING_FALLBACK_TOKENS

        except Exception as e:
            logger.error(f"Неожиданная ошибка при запросе трендовых токенов: {e}. Используется резервный список.")
            return TRENDING_FALLBACK_TOKENS

    async def _fetch_crypto_info(self, tickers: List[str]) -> Dict:
        """Получает метаданные (теги) для списка криптовалют."""
        if not config.news_apis.coinmarketcap or not tickers:
            return {}

        url = f"{CMC_PRO_API_BASE_URL}{CMC_CRYPTO_INFO_ENDPOINT}"
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': config.news_apis.coinmarketcap}
        params = {'symbol': ','.join(tickers), 'aux': 'tags'}

        try:
            response = await self.http_client.get(url, headers=headers, params=params)
            response.raise_for_status()
            raw_data = response.json().get('data', {})

            # ✅ ИСПРАВЛЕНИЕ: Универсальная обработка ответа API
            info_data = {}
            for symbol, data_value in raw_data.items():
                try:
                    if isinstance(data_value, list):
                        # API вернул массив - берем первый элемент
                        info_data[symbol] = data_value[0] if data_value else {}
                        logger.debug(f"Извлечен первый элемент из массива для {symbol}")
                    elif isinstance(data_value, dict):
                        # API вернул объект - используем как есть
                        info_data[symbol] = data_value
                    else:
                        logger.warning(f"Неожиданный тип данных для {symbol}: {type(data_value)}")
                        info_data[symbol] = {}
                except Exception as e:
                    logger.error(f"Ошибка обработки данных для {symbol}: {e}")
                    info_data[symbol] = {}

            logger.info(f"Успешно получены метаданные для {len(info_data)} монет")
            return info_data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP ошибка при запросе метаданных: {e.response.status_code} - {e.response.text}")
            return {}
        except Exception as e:
            logger.error(f"Неожиданная ошибка при запросе метаданных: {e}")
            return {}

    async def enrich_report_context(self) -> Dict:
        """
        Собирает все данные, необходимые для 'шапки' отчета.
        """
        logger.info("Сбор данных для контекста отчета (глобальные метрики)...")
        metrics_task = self._fetch_global_metrics()
        fng_task = self._fetch_fear_and_greed_index()

        results = await asyncio.gather(metrics_task, fng_task, return_exceptions=True)

        global_metrics = results[0] if not isinstance(results[0], Exception) else {}
        fng_index = results[1] if not isinstance(results[1], Exception) else {}

        # Обработка и возврат структурированных данных
        quote = global_metrics.get('quote', {}).get('USD', {})

        return {
            'btc_dominance': global_metrics.get('btc_dominance', 0.0),
            'market_cap_change_24h': quote.get('total_market_cap_yesterday_percentage_change', 0.0),
            'fear_greed_value': fng_index.get('value', 0),
            'fear_greed_classification': fng_index.get('value_classification', "Нейтрально")
        }

    def _calculate_ai_score(self, opp: ArbitrageOpportunity) -> float:
        """Рассчитывает AI-оценку на основе собранных данных."""
        rules = ENRICHMENT_CONFIG['AI_SCORE_RULES']
        score = rules['BASE_SCORE']
        if opp.technical_analysis.macd_signal == MACDSignal.BULLISH: score += rules['WEIGHTS']['MACD_BULLISH']
        if opp.technical_analysis.rsi_status == RSIStatus.HEALTHY: score += rules['WEIGHTS']['RSI_HEALTHY']
        if opp.technical_analysis.rsi_status == RSIStatus.OVERSOLD: score += rules['WEIGHTS']['RSI_OVERSOLD']
        if opp.technical_analysis.rsi_status == RSIStatus.CRITICAL_OVERBOUGHT: score += rules['WEIGHTS'][
            'RSI_CRITICAL_OVERBOUGHT']
        if opp.technical_analysis.volume_spike_ratio > rules['THRESHOLDS']['VOLUME_SPIKE_HIGH']: score += \
            rules['WEIGHTS']['VOLUME_SPIKE_HIGH']
        if opp.market_data.market_cap_usd > rules['THRESHOLDS']['MCAP_LARGE']:
            score += rules['WEIGHTS']['MCAP_LARGE']
        elif 0 < opp.market_data.market_cap_usd < rules['THRESHOLDS']['MCAP_NANO']:
            score += rules['WEIGHTS']['MCAP_NANO']
        return max(rules['MIN_SCORE'], min(rules['MAX_SCORE'], round(score, 1)))

    def _determine_risk_level(self, opp: ArbitrageOpportunity) -> RiskLevel:
        """Определяет уровень риска."""
        rules = ENRICHMENT_CONFIG['RISK_LEVEL_RULES']
        risk_score = 0
        if 0 < opp.market_data.market_cap_usd < rules['THRESHOLDS']['MCAP_MICRO']: risk_score += rules['POINTS'][
            'MCAP_MICRO']
        if opp.technical_analysis.rsi_status == RSIStatus.OVERBOUGHT: risk_score += rules['POINTS']['RSI_OVERBOUGHT']
        if opp.technical_analysis.rsi_status == RSIStatus.CRITICAL_OVERBOUGHT: risk_score += rules['POINTS'][
            'RSI_CRITICAL_OVERBOUGHT']
        if opp.technical_analysis.volume_spike_ratio > rules['THRESHOLDS']['VOLUME_SPIKE_EXTREME']: risk_score += \
            rules['POINTS']['VOLUME_SPIKE_EXTREME']
        if 0 < opp.market_data.listings_count < rules['THRESHOLDS']['LOW_LISTINGS']: risk_score += rules['POINTS'][
            'LOW_LISTINGS']
        if risk_score >= rules['THRESHOLDS']['EXTREME_RISK']: return RiskLevel.EXTREME
        if risk_score >= rules['THRESHOLDS']['HIGH_RISK']: return RiskLevel.HIGH
        if risk_score >= rules['THRESHOLDS']['MEDIUM_RISK']: return RiskLevel.MEDIUM
        return RiskLevel.LOW

    async def get_top_coins_by_market_cap(self, limit: int) -> List[str]:
        """
        Получает список тикеров топ-N монет по капитализации с CoinMarketCap.
        """
        if not config.news_apis.coinmarketcap:
            logger.warning("CMC API ключ не настроен, не могу получить топ монет.")
            return []

        url = f"{CMC_PRO_API_BASE_URL}{CMC_LISTINGS_LATEST_ENDPOINT}"
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': config.news_apis.coinmarketcap}
        params = {'limit': limit, 'sort': 'market_cap', 'convert': 'USD'}

        try:
            response = await self.http_client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json().get('data', [])

            top_symbols = [item['symbol'] for item in data if 'symbol' in item]
            logger.info(f"Успешно получено топ-{len(top_symbols)} монет по капитализации с CMC.")
            return top_symbols

        except Exception as e:
            logger.error(f"Ошибка при запросе топ монет с CMC: {e}")
            return []


# Глобальный экземпляр
data_enricher = DataEnricherService()

# import asyncio
# from collections import defaultdict
# from typing import List, Dict
# import pandas_ta as ta
# import httpx
# import pandas as pd
#
# from src.constants.api_constants import (
#     CMC_PRO_API_BASE_URL, CMC_QUOTES_LATEST_ENDPOINT,
#     CRYPTOPANIC_API_BASE_URL, ENRICHER_HTTP_TIMEOUT
# )
# from src.constants.telegram_constants import SPARKLINE_CHARS
# from src.constants.trading_constants import ENRICHMENT_CONFIG
# from src.core.config import config
# from src.strategies.arbitrage_strategy import ArbitrageOpportunity
# from src.strategies.enums import RiskLevel, MACDSignal, RSIStatus
# from src.utils.logger import logger
#
#
# class DataEnricherService:
#     def __init__(self):
#         """Инициализирует HTTP-клиент для внешних API."""
#         self.http_client = httpx.AsyncClient(timeout=ENRICHER_HTTP_TIMEOUT)
#
#     async def enrich_opportunities(self, opportunities: List[ArbitrageOpportunity], services: Dict) -> List[
#         ArbitrageOpportunity]:
#         """Главный метод, оркестрирующий процесс обогащения данных."""
#         if not opportunities:
#             return []
#
#         tickers = list(set([opp.coin for opp in opportunities]))
#
#         cmc_data_task = self._fetch_cmc_data(tickers)
#         news_data_task = self._fetch_news_data(tickers)
#
#         cmc_data, news_data = await asyncio.gather(cmc_data_task, news_data_task, return_exceptions=True)
#
#         cmc_data = cmc_data if isinstance(cmc_data, dict) else {}
#         news_data = news_data if isinstance(news_data, dict) else {}
#
#         enrichment_tasks = [self._enrich_single_opportunity(opp, services, cmc_data, news_data) for opp in
#                             opportunities]
#         enriched_opportunities = await asyncio.gather(*enrichment_tasks, return_exceptions=True)
#
#         return [opp for opp in enriched_opportunities if isinstance(opp, ArbitrageOpportunity)]
#
#     async def _enrich_single_opportunity(self, opp: ArbitrageOpportunity, services: Dict, cmc_data: Dict,
#                                          news_data: Dict) -> ArbitrageOpportunity:
#         """Обогащает один объект ArbitrageOpportunity."""
#         try:
#             if opp.coin in cmc_data:
#                 coin_data = cmc_data[opp.coin]['quote']['USD']
#                 opp.market_data.price = coin_data.get('price', 0)
#                 opp.market_data.price_24h_change = coin_data.get('percent_change_24h', 0)
#                 opp.market_data.volume_24h_usd = coin_data.get('volume_24h', 0)
#                 opp.market_data.market_cap_usd = coin_data.get('market_cap', 0)
#                 opp.listings_count = cmc_data[opp.coin].get('num_market_pairs', 0)
#
#             if opp.coin in news_data:
#                 opp.drivers = news_data[opp.coin][:ENRICHMENT_CONFIG['API_LIMITS']['NEWS_TOP_N']]
#
#             service = services.get(opp.buy_exchange_id)
#             if not service: return opp
#
#             # Проверяем, поддерживает ли биржа получение исторических данных
#             if service.client.has['fetchOHLCV']:
#                 ta_config = ENRICHMENT_CONFIG['TECHNICAL_ANALYSIS']
#                 ohlcv = await service.client.fetch_ohlcv(opp.symbol, timeframe=ta_config['OHLCV_TIMEFRAME'],
#                                                          limit=ta_config['OHLCV_LIMIT'])
#                 if ohlcv and len(ohlcv) >= ta_config['MIN_OHLCV_RECORDS']:
#                     df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
#                     if not df.empty:
#                         self._calculate_technical_indicators(opp, df)
#             else:
#                 # Если биржа не поддерживает OHLCV (как Yobit), просто логируем это и пропускаем теханализ
#                 logger.debug(
#                     f"Пропуск теханализа для {opp.symbol} на {opp.buy_exchange_id}: fetchOHLCV не поддерживается.")
#
#             opp.ai_score = self._calculate_ai_score(opp)
#             opp.risk_level = self._determine_risk_level(opp)
#
#             return opp
#         except Exception as e:
#             logger.error(f"Ошибка обогащения {opp.symbol}: {type(e).__name__} - {e}")
#             return opp
#
#     def _calculate_technical_indicators(self, opp: ArbitrageOpportunity, df: pd.DataFrame):
#         """Вычисляет все технические индикаторы и тренды из констант."""
#         ta_config = ENRICHMENT_CONFIG['TECHNICAL_ANALYSIS']
#
#         rsi_value = df.ta.rsi(length=ta_config['RSI_LENGTH']).iloc[-1]
#         if pd.notna(rsi_value):
#             opp.technical_analysis.rsi_14 = rsi_value
#             if rsi_value > ta_config['RSI_CRITICAL_OVERBOUGHT']:
#                 opp.technical_analysis.rsi_status = RSIStatus.CRITICAL_OVERBOUGHT
#             elif rsi_value > ta_config['RSI_OVERBOUGHT']:
#                 opp.technical_analysis.rsi_status = RSIStatus.OVERBOUGHT
#             elif rsi_value < ta_config['RSI_OVERSOLD']:
#                 opp.technical_analysis.rsi_status = RSIStatus.OVERSOLD
#             else:
#                 opp.technical_analysis.rsi_status = RSIStatus.HEALTHY
#
#         macd = df.ta.macd(fast=ta_config['MACD_FAST'], slow=ta_config['MACD_SLOW'], signal=ta_config['MACD_SIGNAL'])
#         if macd is not None and not macd.empty:
#             if macd[f'MACD_{ta_config["MACD_FAST"]}_{ta_config["MACD_SLOW"]}_{ta_config["MACD_SIGNAL"]}'].iloc[-1] > \
#                     macd[f'MACDs_{ta_config["MACD_FAST"]}_{ta_config["MACD_SLOW"]}_{ta_config["MACD_SIGNAL"]}'].iloc[
#                         -1]:
#                 opp.technical_analysis.macd_signal = MACDSignal.BULLISH
#             else:
#                 opp.technical_analysis.macd_signal = MACDSignal.BEARISH
#
#         prices = df['close'].tail(ta_config['SPARKLINE_PERIOD']).tolist()
#         min_p, max_p = min(prices), max(prices)
#         sparkline = ""
#         for p in prices:
#             if max_p > min_p:
#                 idx = int((p - min_p) / (max_p - min_p) * (len(SPARKLINE_CHARS) - 1))
#                 sparkline += SPARKLINE_CHARS[idx]
#         opp.technical_analysis.price_trend_sparkline = sparkline
#
#         avg_volume = df['volume'].rolling(window=ta_config['VOLUME_SPIKE_WINDOW']).mean().iloc[-1]
#         last_hour_volume = df['volume'].iloc[-1]
#         if avg_volume > 0: opp.technical_analysis.volume_spike_ratio = last_hour_volume / avg_volume
#
#     async def _fetch_cmc_data(self, tickers: List[str]) -> Dict:
#         if not config.coinmarketcap_api_key or not tickers: return {}
#         headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': config.coinmarketcap_api_key}
#         params = {'symbol': ','.join(tickers[:ENRICHMENT_CONFIG['API_LIMITS']['CMC_MAX_SYMBOLS']])}
#         url = f"{CMC_PRO_API_BASE_URL}{CMC_QUOTES_LATEST_ENDPOINT}"
#         try:
#             response = await self.http_client.get(url, headers=headers, params=params)
#             response.raise_for_status()
#             return response.json().get('data', {})
#         except httpx.HTTPStatusError as e:
#             logger.error(f"Ошибка API CoinMarketCap: {e.response.status_code} - {e.response.text}")
#             return {}
#         except Exception as e:
#             logger.error(f"Неожиданная ошибка при запросе к CoinMarketCap: {e}")
#             return {}
#
#     async def _fetch_news_data(self, tickers: List[str]) -> Dict:
#         if not config.cryptopanic_api_key or not tickers: return {}
#         params = {'auth_token': config.cryptopanic_api_key, 'currencies': ','.join(tickers), 'public': 'true'}
#         try:
#             response = await self.http_client.get(CRYPTOPANIC_API_BASE_URL, params=params)
#             response.raise_for_status()
#             news = defaultdict(list)
#             for post in response.json()['results']:
#                 if post.get('currencies'):
#                     for currency in post['currencies']:
#                         news[currency['code']].append(post['title'])
#             return news
#         except Exception as e:
#             logger.error(f"Ошибка запроса к CryptoPanic: {e}")
#             return {}
#
#     def _calculate_ai_score(self, opp: ArbitrageOpportunity) -> float:
#         rules = ENRICHMENT_CONFIG['AI_SCORE_RULES']
#         score = rules['BASE_SCORE']
#         if opp.technical_analysis.macd_signal == MACDSignal.BULLISH: score += rules['WEIGHTS']['MACD_BULLISH']
#         if opp.technical_analysis.rsi_status == RSIStatus.HEALTHY: score += rules['WEIGHTS']['RSI_HEALTHY']
#         if opp.technical_analysis.rsi_status == RSIStatus.OVERSOLD: score += rules['WEIGHTS']['RSI_OVERSOLD']
#         if opp.technical_analysis.rsi_status == RSIStatus.CRITICAL_OVERBOUGHT: score += rules['WEIGHTS'][
#             'RSI_CRITICAL_OVERBOUGHT']
#         if opp.technical_analysis.volume_spike_ratio > rules['THRESHOLDS']['VOLUME_SPIKE_HIGH']: score += \
#             rules['WEIGHTS']['VOLUME_SPIKE_HIGH']
#         if opp.market_data.market_cap_usd > rules['THRESHOLDS']['MCAP_LARGE']:
#             score += rules['WEIGHTS']['MCAP_LARGE']
#         elif 0 < opp.market_data.market_cap_usd < rules['THRESHOLDS']['MCAP_NANO']:
#             score += rules['WEIGHTS']['MCAP_NANO']
#         return max(rules['MIN_SCORE'], min(rules['MAX_SCORE'], round(score, 1)))
#
#     def _determine_risk_level(self, opp: ArbitrageOpportunity) -> RiskLevel:
#         rules = ENRICHMENT_CONFIG['RISK_LEVEL_RULES']
#         risk_score = 0
#         if 0 < opp.market_data.market_cap_usd < rules['THRESHOLDS'][
#             'MCAP_MICRO']: risk_score += rules['POINTS']['MCAP_MICRO']
#         if opp.technical_analysis.rsi_status == RSIStatus.OVERBOUGHT: risk_score += rules['POINTS']['RSI_OVERBOUGHT']
#         if opp.technical_analysis.rsi_status == RSIStatus.CRITICAL_OVERBOUGHT: risk_score += rules['POINTS'][
#             'RSI_CRITICAL_OVERBOUGHT']
#         if opp.technical_analysis.volume_spike_ratio > rules['THRESHOLDS']['VOLUME_SPIKE_EXTREME']: risk_score += \
#             rules['POINTS']['VOLUME_SPIKE_EXTREME']
#         if 0 < opp.market_data.listings_count < rules['THRESHOLDS']['LOW_LISTINGS']: risk_score += \
#             rules['POINTS']['LOW_LISTINGS']
#
#         if risk_score >= rules['THRESHOLDS']['EXTREME_RISK']: return RiskLevel.EXTREME
#         if risk_score >= rules['THRESHOLDS']['HIGH_RISK']: return RiskLevel.HIGH
#         if risk_score >= rules['THRESHOLDS']['MEDIUM_RISK']: return RiskLevel.MEDIUM
#         return RiskLevel.LOW
#
#
# data_enricher = DataEnricherService()
