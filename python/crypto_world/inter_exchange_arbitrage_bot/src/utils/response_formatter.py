# inter_exchange_arbitrage_bot/src/utils/response_formatter.py
import re
from typing import Dict, Any, Optional, Tuple

from src.constants.assets_constants import PATTERN_IMAGES
from src.constants.emoji_constants import COIN_EMOJIS, CONFIDENCE_EMOJIS, TRADING_ACTION_EMOJIS, TIMEFRAME_EMOJIS, \
    PATTERN_EMOJIS, ANALYSIS_SECTION_EMOJIS, SENTIMENT_EMOJIS, TRADING_IMPACT_EMOJIS


class AIResponseFormatter:
    """
    Класс для красивого форматирования ответов AI с эмодзи и структурированным выводом.
    Следует принципу: промпты без эмодзи -> красивое форматирование в цикле.
    """

    @classmethod
    def get_coin_emoji(cls, coin_symbol: str) -> str:
        """Возвращает эмодзи для конкретной монеты из констант."""
        return COIN_EMOJIS.get(coin_symbol.upper(), '🪙')

    @classmethod
    def format_btc_direction_analysis(cls, raw_analysis: str) -> str:
        """
        Форматирует анализ направления BTC. Логика схожа с рыночной аналитикой.
        """
        if not raw_analysis:
            return "❌ Анализ по BTC недоступен"

        formatted_lines = []
        header = f"{cls.get_coin_emoji('BTC')} <b><u>Анализ направления Bitcoin</u></b>\n"
        formatted_lines.append(header)

        lines = raw_analysis.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            formatted_lines.append(cls._format_market_line(line))

        return '\n'.join(formatted_lines)

    @classmethod
    def format_coin_analysis(cls, raw_analysis: str, coin_symbol: str) -> str:
        """
        Форматирует анализ конкретной монеты с добавлением эмодзи и структуры.
        """
        if not raw_analysis:
            return f"❌ Анализ по {coin_symbol} недоступен"

        formatted_lines = []
        coin_emoji = cls.get_coin_emoji(coin_symbol)
        header = f"{coin_emoji} <b><u>Торговая аналитика по {coin_symbol}</u></b>\n"
        formatted_lines.append(header)

        lines = raw_analysis.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            formatted_lines.append(cls._format_analysis_line(line))

        return '\n'.join(formatted_lines)

    @classmethod
    def format_market_summary(cls, raw_summary: str) -> str:
        """
        Форматирует общую рыночную аналитику с эмодзи и структурой.
        """
        if not raw_summary:
            return "❌ Рыночная аналитика недоступна"

        formatted_lines = ["🌍 <b><u>Комплексная аналитика по рынку</u></b>\n"]
        lines = raw_summary.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            formatted_lines.append(cls._format_market_line(line))

        return '\n'.join(formatted_lines)

    @classmethod
    def format_news_item(cls, news_item: Dict[str, Any]) -> str:
        """
        Форматирует отдельную новость с эмодзи настроения и структурой.
        """
        sentiment = news_item.get('sentiment', 'Нейтрально')
        sentiment_emoji = SENTIMENT_EMOJIS.get(sentiment, '⚪')

        title = news_item.get('title_ru', 'Без заголовка')
        summary = news_item.get('summary_ru', 'Нет описания')
        source = news_item.get('source', 'Неизвестный источник')
        url = news_item.get('url', '')

        trading_impact = news_item.get('trading_impact', 'Низкий')
        impact_emoji = TRADING_IMPACT_EMOJIS.get(trading_impact, '💡')

        news_block = (
            f"{sentiment_emoji} {impact_emoji} <b>{title}</b>\n"
            f"<i>Источник: {source} | Тональность: {sentiment}</i>\n"
            f"{summary}\n"
        )

        if url:
            news_block += f"<a href='{url}'>📖 Читать полностью</a>\n"

        return news_block + "\n"

    @classmethod
    def format_trending_analysis(cls, raw_analysis: str) -> str:
        """
        Форматирует анализ трендовых монет с эмодзи и структурой.
        """
        if not raw_analysis:
            return "❌ Анализ трендов недоступен"

        formatted_lines = ["💎 <b><u>Аналитика по трендам</u></b>\n"]
        lines = raw_analysis.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            formatted_lines.append(cls._format_trending_line(line))
        return '\n'.join(formatted_lines)

    @classmethod
    def format_gainers_losers_analysis(cls, raw_analysis: str) -> str:
        """
        Форматирует анализ лидеров роста/падения с эмодзи.
        """
        if not raw_analysis:
            return "❌ Анализ лидеров рынка недоступен"

        formatted_lines = ["📈 <b><u>Аналитика по лидерам рынка</u></b>\n"]
        lines = raw_analysis.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            formatted_lines.append(cls._format_gainers_losers_line(line))
        return '\n'.join(formatted_lines)

    @classmethod
    def _format_analysis_line(cls, line: str) -> str:
        """
        Форматирует строку анализа с добавлением соответствующих эмодзи из констант.
        """
        for section, emoji in ANALYSIS_SECTION_EMOJIS.items():
            section_text = section.replace('_', ' ')
            if line.upper().startswith(section_text):
                return f"{emoji} <b>{line}</b>"

        for action, emoji in TRADING_ACTION_EMOJIS.items():
            if action in line.upper():
                return f"{emoji} {line}"

        for confidence, emoji in CONFIDENCE_EMOJIS.items():
            if confidence.upper() in line.upper():
                return f"{emoji} {line}"

        for timeframe, emoji in TIMEFRAME_EMOJIS.items():
            if timeframe in line:
                return f"{emoji} {line}"

        for pattern, emoji in PATTERN_EMOJIS.items():
            if pattern.lower() in line.lower():
                return f"{emoji} {line}"

        if any(indicator in line.upper() for indicator in ['RSI', 'MACD', 'EMA', 'ОБЪЁМ', 'BOLLINGER', 'ФИБОНАЧЧИ']):
            return f"📈 {line}"

        return line

    @classmethod
    def _format_market_line(cls, line: str) -> str:
        """
        Форматирует строку рыночного анализа.
        """
        line_upper = line.upper()
        if 'ОБЩИЙ РЕЖИМ:' in line_upper or 'ОБЩАЯ СТРАТЕГИЯ:' in line_upper:
            return f"🎯 <b>{line}</b>"
        if 'КРАТКОСРОЧНО' in line_upper:
            return f"⚡ {line}"
        if 'СРЕДНЕСРОЧНО' in line_upper:
            return f"⏰ {line}"
        if 'ДОЛГОСРОЧНО' in line_upper:
            return f"📅 {line}"
        if 'ЛУЧШИЕ ВОЗМОЖНОСТИ:' in line_upper or 'ВОЗМОЖНОСТИ:' in line_upper:
            return f"💎 <b>{line}</b>"
        if 'ИЗБЕГАТЬ:' in line_upper or 'РИСКИ:' in line_upper:
            return f"⚠️ <b>{line}</b>"

        return cls._format_analysis_line(line)

    @classmethod
    def _format_trending_line(cls, line: str) -> str:
        """
        Форматирует строку анализа трендов.
        """
        if 'ТОП-РЕКОМЕНДАЦИИ' in line.upper():
            return f"🏆 <b>{line}</b>"
        if 'ОБЩАЯ СТРАТЕГИЯ' in line.upper():
            return f"🎯 <b>{line}</b>"
        return cls._format_analysis_line(line)

    @classmethod
    def _format_gainers_losers_line(cls, line: str) -> str:
        """
        Форматирует строку анализа лидеров.
        """
        line_upper = line.upper()
        if 'ТОРГОВЛЯ ПО ТРЕНДУ' in line_upper:
            return f"🚀 <b>{line}</b>"
        if 'ВОЗМОЖНОСТИ РАЗВОРОТА' in line_upper:
            return f"🔄 <b>{line}</b>"
        if 'ОБЩАЯ ТАКТИКА' in line_upper:
            return f"🎯 <b>{line}</b>"
        return cls._format_analysis_line(line)

    @classmethod
    def find_pattern_image_path(cls, raw_analysis: str) -> Optional[str]:
        """
        Ищет в тексте упоминание паттерна и возвращает путь к его изображению.
        Улучшенная версия, устойчивая к разным формулировкам.
        """
        # ИСПРАВЛЕНИЕ: Regex теперь ищет "ПАТТЕРН:" и опционально "ДЛЯ ПОИСКА"
        match = re.search(r"(?:ГРАФИЧЕСКИЕ ПАТТЕРНЫ|ПАТТЕРН)(?: ДЛЯ ПОИСКА)?:\s*(.+)", raw_analysis, re.IGNORECASE)
        if not match:
            return None

        pattern_name_from_ai = match.group(1).strip()

        # Ищем точное совпадение в словаре констант
        for defined_pattern_name, image_path in PATTERN_IMAGES.items():
            if defined_pattern_name.lower() in pattern_name_from_ai.lower():
                return image_path
        return None

    @classmethod
    def format_analysis_with_image(cls, raw_analysis: str, coin_symbol: str) -> Tuple[str, Optional[str]]:
        """
        Форматирует анализ и дополнительно возвращает путь к изображению паттерна.
        """
        formatted_text = cls.format_coin_analysis(raw_analysis, coin_symbol)
        image_path = cls.find_pattern_image_path(raw_analysis)
        # ИСПРАВЛЕНИЕ: Убраны лишние скобки
        return formatted_text, image_path


# Функция для интеграции в существующую логику
def format_ai_analysis_response(raw_analysis: str, analysis_type: str, coin_symbol: str = None) -> str:
    """
    Универсальная функция для форматирования AI ответов.

    Args:
        raw_analysis: Сырой ответ от AI без эмодзи
        analysis_type: Тип анализа ('coin', 'btc_direction', 'market', 'trending', 'gainers_losers')
        coin_symbol: Символ монеты (для анализа конкретной монеты)

    Returns:
        Красиво отформатированный ответ с эмодзи
    """
    if analysis_type == 'btc_direction':
        return AIResponseFormatter.format_btc_direction_analysis(raw_analysis)
    elif analysis_type == 'coin' and coin_symbol:
        return AIResponseFormatter.format_coin_analysis(raw_analysis, coin_symbol)
    elif analysis_type == 'market':
        return AIResponseFormatter.format_market_summary(raw_analysis)
    elif analysis_type == 'trending':
        return AIResponseFormatter.format_trending_analysis(raw_analysis)
    elif analysis_type == 'gainers_losers':
        return AIResponseFormatter.format_gainers_losers_analysis(raw_analysis)
    else:
        # Базовое форматирование
        return f"💡 <b><u>AI Аналитика</u></b>\n\n{raw_analysis}"
