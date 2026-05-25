# inter_exchange_arbitrage_bot/src/services/ai_trade_advisor_service.py

from typing import List, Dict, Any, Optional

from src.constants.prompts import (
    COIN_ANALYSIS_PROMPT,
    BTC_ANALYSIS_PROMPT,
    TRENDING_ANALYSIS_PROMPT,
    GAINERS_LOSERS_ANALYSIS_PROMPT,
    MARKET_SUMMARY_PROMPT,
    RISK_ASSESSMENT_PROMPT
)
from src.services.enhanced_ai_processor_service import EnhancedAIProcessorService
from src.utils import logger
from src.utils.helpers import clean_html_for_telegram
from src.utils.response_formatter import format_ai_analysis_response


class AITradeAdvisorService:
    """
    Сервис для генерации торговых рекомендаций с красивым форматированием ответов.
    Принцип: промпты без эмодзи -> AI обработка -> красивое форматирование в цикле.
    """

    def __init__(self, ai_processor: EnhancedAIProcessorService):
        self.ai_processor = ai_processor

    async def _generate_trading_insights(
            self,
            prompt_template: str,
            analysis_type: str,
            coin_symbol: Optional[str] = None,
            return_raw: bool = False,
            **kwargs
    ) -> str:
        """
        Универсальный метод генерации торговых советов.
        Может возвращать либо отформатированный, либо сырой ответ.
        """
        if not kwargs:
            return "Недостаточно данных для формирования торговых рекомендаций."

        try:
            # --- ИСПРАВЛЕНИЕ НАЧАЛО ---
            # Создаем словарь для форматирования, который будет включать ВСЕ нужные переменные.
            # Копируем kwargs, чтобы не изменять исходный словарь.
            format_args = kwargs.copy()
            # Добавляем coin_symbol в этот словарь, если он нужен для промпта.
            # Это решает проблему KeyError.
            if '{coin_symbol}' in prompt_template:
                format_args['coin_symbol'] = coin_symbol

            # 1. Формируем промпт, используя наш новый, полный словарь аргументов.
            formatted_prompt = prompt_template.format(**format_args)
            # --- ИСПРАВЛЕНИЕ КОНЕЦ ---

            # 2. Получаем сырой ответ от AI
            raw_response = await self.ai_processor.generate_text_insight(formatted_prompt)

            if not raw_response or not raw_response.strip():
                logger.warning(f"AI вернул пустой ответ для {analysis_type}")
                return "AI временно недоступен. Попробуйте позже."

            # 3. Проверяем, нужно ли возвращать сырой ответ
            if return_raw:
                return raw_response

            # 4. Красиво форматируем ответ с эмодзи
            formatted_response = format_ai_analysis_response(
                raw_analysis=raw_response,
                analysis_type=analysis_type,
                coin_symbol=coin_symbol
            )

            # 5. Очищаем HTML для Telegram
            cleaned_response = clean_html_for_telegram(formatted_response)
            return cleaned_response

        except KeyError as e:
            logger.critical(
                f"Критическая ошибка форматирования промпта для '{analysis_type}': не найден ключ {e}. Проверьте передаваемые аргументы!")
            return f"Ошибка конфигурации промпта: отсутствует ключ {e}."
        except Exception as e:
            logger.error(f"Ошибка при генерации торговых советов ({analysis_type}): {e}", exc_info=True)
            return "Аналитика временно недоступна из-за внутренней ошибки."

    async def get_raw_coin_analysis(self, news_list: List[Dict], coin_symbol: str) -> str:
        """
        Получает СЫРОЙ, неотформатированный анализ по конкретной монете.
        """
        if not news_list:
            return f"По {coin_symbol} недостаточно новостей для формирования торговых рекомендаций."

        return await self._generate_trading_insights(
            prompt_template=COIN_ANALYSIS_PROMPT,
            analysis_type="coin",
            coin_symbol=coin_symbol,
            return_raw=True,
            news_data=str(news_list)
        )

    async def analyze_btc_trading_situation(self, btc_news: List[Dict], market_intel: Dict) -> str:
        """
        Анализ направления Bitcoin и влияния на альткоины.
        """
        combined_data = {
            "bitcoin_news": btc_news,
            "market_context": market_intel
        }

        return await self._generate_trading_insights(
            prompt_template=BTC_ANALYSIS_PROMPT,
            analysis_type="btc_direction",
            coin_symbol="BTC",
            data=str(combined_data)
        )

    async def analyze_coin_trading_opportunity(self, news_list: List[Dict], coin_symbol: str) -> str:
        """
        Анализ торговых возможностей по конкретной монете с форматированием.
        """
        if not news_list:
            return self._format_no_data_response(
                f"По {coin_symbol} недостаточно новостей для формирования торговых рекомендаций.")

        # ИСПРАВЛЕНИЕ: Мы должны передавать coin_symbol в kwargs для форматирования.
        return await self._generate_trading_insights(
            prompt_template=COIN_ANALYSIS_PROMPT,
            analysis_type="coin",
            coin_symbol=coin_symbol,
            news_data=str(news_list),
            # coin_symbol=coin_symbol # <-- Эта строка здесь не нужна, она дублируется
        )

    async def analyze_trending_trading_opportunities(self, trending_data: List[Dict]) -> str:
        """
        Анализ торговых возможностей по трендовым монетам.
        """
        if not trending_data:
            return self._format_no_data_response("Нет данных по трендовым монетам для анализа.")

        return await self._generate_trading_insights(
            prompt_template=TRENDING_ANALYSIS_PROMPT,
            analysis_type="trending",
            data=str(trending_data)
        )

    async def analyze_gainers_losers_opportunities(self, gainers_losers_data: Dict) -> str:
        """
        Анализ возможностей по лидерам роста/падения.
        """
        if not gainers_losers_data.get('gainers') and not gainers_losers_data.get('losers'):
            return self._format_no_data_response("Нет данных по лидерам роста/падения для анализа.")

        return await self._generate_trading_insights(
            prompt_template=GAINERS_LOSERS_ANALYSIS_PROMPT,
            analysis_type="gainers_losers",
            data=str(gainers_losers_data)
        )

    async def get_market_summary_analysis(self, market_data: Dict) -> str:
        """
        Получение краткой рыночной сводки.
        """
        if not market_data:
            return self._format_no_data_response("Нет рыночных данных для анализа.")

        return await self._generate_trading_insights(
            prompt_template=MARKET_SUMMARY_PROMPT,
            analysis_type="market",
            data=str(market_data)
        )

    async def assess_market_risks(self, risk_data: Dict) -> str:
        """
        Оценка рыночных рисков.
        """
        if not risk_data:
            return self._format_no_data_response("Нет данных для оценки рисков.")

        return await self._generate_trading_insights(
            prompt_template=RISK_ASSESSMENT_PROMPT,
            analysis_type="market",
            data=str(risk_data)
        )

    def _format_no_data_response(self, message: str) -> str:
        """
        Форматирует ответ, когда нет данных для анализа.
        """
        return f"ℹ️ <b>Информация</b>\n\n{message}"

    async def get_service_status(self) -> Dict[str, Any]:
        """
        Получение статуса сервиса.
        """
        return {
            "service": "AITradeAdvisorService",
            "status": "active",
            "ai_processor": type(self.ai_processor).__name__,
            "formatting_enabled": True
        }
