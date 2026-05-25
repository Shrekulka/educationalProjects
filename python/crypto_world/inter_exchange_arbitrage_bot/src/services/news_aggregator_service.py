# inter_exchange_arbitrage_bot/src/services/news_aggregator_service.py

import asyncio
import html
import time
from typing import List, Dict, Set

from src.constants.api_constants import FALLBACK_NEWS_LIMIT
from src.services.enhanced_ai_processor_service import EnhancedAIProcessorService
from src.services.market_data_service import MarketDataService
from src.services.market_intelligence_service import MarketIntelligenceService
from src.services.news_service import NewsService
from src.utils.logger import logger


class NewsAggregatorService:
    def __init__(self, news_service: NewsService, ai_service: EnhancedAIProcessorService,
                 market_data_service: MarketDataService, market_intel_service: MarketIntelligenceService):
        self.news_service = news_service
        self.ai_service = ai_service
        self.market_data_service = market_data_service
        self.market_intel_service = market_intel_service
        self.seen_urls: Set[str] = set()

    async def get_aggregated_news(self, coins: List[str]):
        target_coins_set = {c.upper() for c in coins}
        target_coins_set.add("BTC")

        logger.info(f"Агрегатор: запрашиваю сырые новости и рыночные данные для {target_coins_set}...")

        news_task = self.news_service.fetch_all_raw_news_by_source(target_coins_set)
        market_data_task = self.market_data_service.get_assets_market_data(target_coins_set)
        events_task = self.market_intel_service.get_coingecko_events(target_coins_set)

        logger.debug("Агрегатор: Начинаю параллельный сбор данных от всех источников (gather)...")
        gather_start_time = time.time()
        results = await asyncio.gather(news_task, market_data_task, events_task, return_exceptions=True)
        gather_time = time.time() - gather_start_time
        logger.debug(f"Агрегатор: Параллельный сбор данных ЗАВЕРШЕН за {gather_time:.2f} сек.")

        raw_news_by_source = results[0] if isinstance(results[0], dict) else {}
        market_data = results[1] if isinstance(results[1], dict) else {}
        events = results[2] if isinstance(results[2], list) else []

        if events:
            raw_news_by_source["CoinGeckoEvents"] = events

        active_sources = [name for name, news_list in raw_news_by_source.items() if news_list]
        logger.info(
            f"Получены новости от {len(active_sources)} API: {', '.join(active_sources) or 'Нет активных источников'}")

        raw_news = [item for news_list in raw_news_by_source.values() for item in news_list]
        unique_news = self._deduplicate(raw_news)

        logger.info(f"Агрегатор: Всего уникальных новостей для обработки AI: {len(unique_news)}.")

        if not unique_news:
            return {"news": [], "market_summary": "Нет новостей для анализа."}

        try:
            logger.info(f"Передача {len(unique_news)} новостей в AI для комплексного анализа...")

            ai_result = await self.ai_service.process_news_batch(unique_news, comprehensive_mode=True)

            all_processed_data = ai_result.get("news", [])
            market_summary = ai_result.get("market_summary", "Аналитика не была сгенерирована.")

            logger.info(f"AI успешно обработал {len(all_processed_data)} новостей и сгенерировал аналитику.")

            final_news = self._merge_news_data(all_processed_data, unique_news, market_data)

            return {"news": final_news, "market_summary": market_summary}

        except Exception as e:
            logger.error(f"Агрегатор: критическая ошибка обработки AI ({e}). Возвращаем базовый формат.", exc_info=True)
            fallback_news = [self._format_fallback(n) for n in unique_news[:FALLBACK_NEWS_LIMIT]]
            return {"news": fallback_news, "summary": "Аналитика временно недоступна из-за ошибки AI."}

    def _deduplicate(self, news_list: List[Dict]) -> List[Dict]:
        """Убирает дубликаты новостей по URL."""
        unique_list = []
        self.seen_urls.clear()
        for item in news_list:
            url = item.get('url')
            if url and url not in self.seen_urls:
                unique_list.append(item)
                self.seen_urls.add(url)
        return unique_list

    def _merge_news_data(self, processed_list: List[Dict], original_list: List[Dict], market_data: Dict) -> List[Dict]:
        """Объединяет данные от AI, исходные новости и рыночные данные."""
        final_news = []
        sentiment_map = {
            'Очень позитивно': '🚀', 'Позитивно': '🟢', 'Нейтрально': '⚪️',
            'Негативно': '🔴', 'Очень негативно': '🔥'
        }
        for processed_item in processed_list:
            try:
                coin_symbol = processed_item.get('coin', 'GENERAL').upper()
                if coin_symbol == 'IGNORE':
                    continue

                # AI возвращает ID, который является индексом в оригинальном списке
                original_index = int(processed_item['id'])
                original_news = original_list[original_index]

                final_item = {
                    'coin': coin_symbol,
                    'title_ru': html.escape(processed_item.get('title_ru', '')),
                    'summary_ru': html.escape(processed_item.get('summary_ru', '')),
                    'sentiment': processed_item.get('sentiment', 'Нейтрально'),
                    'sentiment_emoji': sentiment_map.get(processed_item.get('sentiment'), '⚪️'),
                    'url': original_news.get('url'),
                    'source': original_news.get('source'),
                    'image_url': original_news.get('image_url'),
                    'market_data': market_data.get(coin_symbol)
                }
                final_news.append(final_item)
            except (IndexError, KeyError, ValueError, TypeError) as e:
                logger.warning(f"Не удалось смержить новость с ID {processed_item.get('id')}: {e}")

        final_news.sort(key=lambda x: (x['coin'] != 'BTC', x['coin'] != 'GENERAL'))
        return final_news

    def _format_fallback(self, news_item: Dict) -> Dict:
        """Создает базовый объект новости, если AI не сработал."""
        return {
            'coin': 'N/A',
            'title_ru': html.escape(news_item.get('title', 'Без заголовка')),
            'summary_ru': html.escape(news_item.get('body', 'Нет описания')[:250] + '...'),
            'sentiment': 'Нейтрально', 'sentiment_emoji': '⚪️',
            'source': news_item.get('source', 'Неизвестный источник'),
            'url': news_item.get('url'), 'image_url': news_item.get('image_url'),
            'market_data': None
        }

