# inter_exchange_arbitrage_bot/src/bot/logic/report_maps.py

"""
Словари-мапперы для преобразования логических состояний из enums.py
в красивый, форматированный текст с эмодзи для отчетов в Telegram.

Этот файл является "слоем представления" для аналитических данных.
Централизация логики отображения здесь позволяет:
- Легко изменять внешний вид отчетов без затрагивания бизнес-логики
- Добавлять многоязычную поддержку
- Быстро адаптировать стиль под разные типы сообщений
- Поддерживать консистентность визуального оформления

Принцип использования:
1. В стратегиях используйте только Enum'ы для логики
2. В отчетах используйте эти мапперы для красивого отображения
"""

from src.strategies.enums import (
    OpportunityType, RiskLevel, MACDSignal, RSIStatus,
    BollingerBandStatus, MarketTrend, ExchangeStatus,
    OrderType, ArbitrageStatus, DensityAction
)

# ============================================================================
# МАППЕРЫ ДЛЯ ОСНОВНЫХ КАТЕГОРИЙ
# ============================================================================

OPPORTUNITY_TYPE_MAP = {
    OpportunityType.HIGH_PROFIT: {
        "text": "Высокоприбыльная",
        "emoji": "💎",
        "full": "💎 Высокоприбыльная",
        "color": "🟢",
        "priority": 1
    },
    OpportunityType.LOW_PROFIT: {
        "text": "Низкоприбыльная",
        "emoji": "📈",
        "full": "📈 Низкоприбыльная",
        "color": "🟡",
        "priority": 2
    },
    OpportunityType.PHANTOM_ROI: {
        "text": "Аномальный ROI",
        "emoji": "⚠️",
        "full": "⚠️ Аномальный ROI",
        "color": "🟠",
        "priority": 3
    },
    OpportunityType.PHANTOM_LIQUIDITY: {
        "text": "Низкая ликвидность",
        "emoji": "🌊",
        "full": "🌊 Низкая ликвидность",
        "color": "🔵",
        "priority": 4
    },
    OpportunityType.PHANTOM_LIMITS: {
        "text": "Ниже лимитов биржи",
        "emoji": "🚫",
        "full": "🚫 Ниже лимитов биржи",
        "color": "🔴",
        "priority": 5
    }
}

RISK_LEVEL_MAP = {
    RiskLevel.LOW: {
        "text": "НИЗКИЙ",
        "emoji": "🟢",
        "full": "🟢 НИЗКИЙ",
        "description": "Безопасная сделка",
        "color_hex": "#00FF00",
        "weight": 1
    },
    RiskLevel.MEDIUM: {
        "text": "СРЕДНИЙ",
        "emoji": "🟡",
        "full": "🟡 СРЕДНИЙ",
        "description": "Требует осторожности",
        "color_hex": "#FFFF00",
        "weight": 2
    },
    RiskLevel.HIGH: {
        "text": "ВЫСОКИЙ",
        "emoji": "🔴",
        "full": "🔴 ВЫСОКИЙ",
        "description": "Потенциально опасно",
        "color_hex": "#FF0000",
        "weight": 3
    },
    RiskLevel.EXTREME: {
        "text": "ЭКСТРЕМАЛЬНЫЙ",
        "emoji": "⚫",
        "full": "⚫ ЭКСТРЕМАЛЬНЫЙ",
        "description": "Крайне высокий риск",
        "color_hex": "#000000",
        "weight": 4
    },
    RiskLevel.UNDEFINED: {
        "text": "НЕ ОПРЕДЕЛЕН",
        "emoji": "⚪",
        "full": "⚪ НЕ ОПРЕДЕЛЕН",
        "description": "Невозможно оценить",
        "color_hex": "#FFFFFF",
        "weight": 0
    }
}

# ============================================================================
# МАППЕРЫ ДЛЯ ТЕХНИЧЕСКИХ ИНДИКАТОРОВ
# ============================================================================

RSI_STATUS_MAP = {
    RSIStatus.OVERSOLD: {
        "text": "Перепроданность",
        "emoji": "🧊",
        "full": "🧊 Перепроданность",
        "signal": "BUY",
        "strength": "strong",
        "description": "RSI < 30, возможен отскок"
    },
    RSIStatus.HEALTHY: {
        "text": "Нейтрально",
        "emoji": "🟢",
        "full": "🟢 Нейтрально",
        "signal": "HOLD",
        "strength": "neutral",
        "description": "RSI 30-70, нормальное состояние"
    },
    RSIStatus.OVERBOUGHT: {
        "text": "Перекупленность",
        "emoji": "🔥",
        "full": "🔥 Перекупленность",
        "signal": "SELL",
        "strength": "medium",
        "description": "RSI > 70, возможна коррекция"
    },
    RSIStatus.CRITICAL_OVERBOUGHT: {
        "text": "Крит. перекупленность",
        "emoji": "🚨",
        "full": "🚨 Критическая перекупленность",
        "signal": "STRONG_SELL",
        "strength": "critical",
        "description": "RSI > 90, высока вероятность падения"
    }
}

MACD_SIGNAL_MAP = {
    MACDSignal.BULLISH: {
        "text": "Бычий",
        "emoji": "📈",
        "full": "📈 Бычий сигнал",
        "arrow": "↗️",
        "trend": "up",
        "description": "MACD выше сигнальной линии"
    },
    MACDSignal.BEARISH: {
        "text": "Медвежий",
        "emoji": "📉",
        "full": "📉 Медвежий сигнал",
        "arrow": "↘️",
        "trend": "down",
        "description": "MACD ниже сигнальной линии"
    },
    MACDSignal.NEUTRAL: {
        "text": "Флэт",
        "emoji": "➡️",
        "full": "➡️ Нейтральный сигнал",
        "arrow": "→",
        "trend": "sideways",
        "description": "MACD около сигнальной линии"
    }
}

BOLLINGER_BAND_MAP = {
    BollingerBandStatus.ABOVE_UPPER: {
        "text": "Выше верхней",
        "emoji": "⬆️",
        "full": "⬆️ Выше верхней полосы",
        "signal": "OVERBOUGHT",
        "description": "Цена пробила верхнюю полосу Боллинджера"
    },
    BollingerBandStatus.BELOW_LOWER: {
        "text": "Ниже нижней",
        "emoji": "⬇️",
        "full": "⬇️ Ниже нижней полосы",
        "signal": "OVERSOLD",
        "description": "Цена пробила нижнюю полосу Боллинджера"
    },
    BollingerBandStatus.INSIDE_BANDS: {
        "text": "Внутри полос",
        "emoji": "↔️",
        "full": "↔️ Внутри полос",
        "signal": "NORMAL",
        "description": "Цена находится между полосами"
    },
    BollingerBandStatus.ON_MIDDLE_BAND: {
        "text": "На средней линии",
        "emoji": "🎯",
        "full": "🎯 На средней линии",
        "signal": "EQUILIBRIUM",
        "description": "Цена на уровне среднего значения"
    }
}

# ============================================================================
# МАППЕРЫ ДЛЯ ТРЕНДОВ И ГРАФИКОВ
# ============================================================================

MARKET_TREND_MAP = {
    MarketTrend.STABLE_GROWTH: {
        "sparkline": "▁▂▃▄▅▆▇█",
        "description": "Стабильный рост",
        "emoji": "📈",
        "full": "📈 Стабильный рост",
        "direction": "bullish",
        "volatility": "low",
        "recommendation": "HOLD/BUY"
    },
    MarketTrend.ACCELERATING_GROWTH: {
        "sparkline": "▁▁▂▃▅▇█",
        "description": "Ускоряющийся рост",
        "emoji": "🚀",
        "full": "🚀 Ускоряющийся рост",
        "direction": "strong_bullish",
        "volatility": "medium",
        "recommendation": "BUY"
    },
    MarketTrend.GROWTH_WITH_SLOWDOWN: {
        "sparkline": "▂▃▅▆▇▆▅",
        "description": "Рост с замедлением",
        "emoji": "📊",
        "full": "📊 Рост с замедлением",
        "direction": "weakening_bullish",
        "volatility": "medium",
        "recommendation": "CAUTION"
    },
    MarketTrend.CONSOLIDATION: {
        "sparkline": "▃▄▃▄▄▃▄",
        "description": "Боковик/Флэт",
        "emoji": "➡️",
        "full": "➡️ Консолидация",
        "direction": "sideways",
        "volatility": "low",
        "recommendation": "HOLD"
    },
    MarketTrend.STABLE_DECLINE: {
        "sparkline": "█▇▆▅▄▃▂",
        "description": "Плавное падение",
        "emoji": "📉",
        "full": "📉 Стабильное снижение",
        "direction": "bearish",
        "volatility": "low",
        "recommendation": "SELL"
    },
    MarketTrend.SHARP_FALL: {
        "sparkline": "▇▆▄▃▂▁▁",
        "description": "Падающий нож",
        "emoji": "🩸",
        "full": "🩸 Резкое падение",
        "direction": "strong_bearish",
        "volatility": "high",
        "recommendation": "AVOID"
    },
    MarketTrend.PUMP_AND_DUMP: {
        "sparkline": "▁▂▅█▇▄▁",
        "description": "Памп и дамп",
        "emoji": "⚠️",
        "full": "⚠️ Памп и дамп",
        "direction": "manipulation",
        "volatility": "extreme",
        "recommendation": "AVOID"
    },
    MarketTrend.REBOUND: {
        "sparkline": "█▃▁▂▄▆▇",
        "description": "Отскок после падения",
        "emoji": "♻️",
        "full": "♻️ Отскок",
        "direction": "recovery",
        "volatility": "high",
        "recommendation": "CAUTIOUS_BUY"
    }
}

# ============================================================================
# МАППЕРЫ ДЛЯ СИСТЕМНЫХ СТАТУСОВ
# ============================================================================

EXCHANGE_STATUS_MAP = {
    ExchangeStatus.ACTIVE: {
        "text": "Активна",
        "emoji": "🟢",
        "full": "🟢 Биржа работает",
        "description": "Все системы функционируют нормально"
    },
    ExchangeStatus.MAINTENANCE: {
        "text": "Техобслуживание",
        "emoji": "🟡",
        "full": "🟡 Техническое обслуживание",
        "description": "Плановые работы, торговля ограничена"
    },
    ExchangeStatus.DEGRADED: {
        "text": "Частичные проблемы",
        "emoji": "🟠",
        "full": "🟠 Частичные проблемы",
        "description": "Возможны задержки в выполнении ордеров"
    },
    ExchangeStatus.OFFLINE: {
        "text": "Недоступна",
        "emoji": "🔴",
        "full": "🔴 Биржа недоступна",
        "description": "Торговля временно невозможна"
    }
}

ORDER_TYPE_MAP = {
    OrderType.MARKET: {
        "text": "Рыночный",
        "emoji": "⚡",
        "full": "⚡ Рыночный ордер",
        "description": "Исполняется немедленно по рыночной цене"
    },
    OrderType.LIMIT: {
        "text": "Лимитный",
        "emoji": "🎯",
        "full": "🎯 Лимитный ордер",
        "description": "Исполняется при достижении указанной цены"
    },
    OrderType.STOP_LOSS: {
        "text": "Стоп-лосс",
        "emoji": "🛑",
        "full": "🛑 Стоп-лосс",
        "description": "Ограничение убытков при неблагоприятном движении"
    },
    OrderType.TAKE_PROFIT: {
        "text": "Тейк-профит",
        "emoji": "💰",
        "full": "💰 Тейк-профит",
        "description": "Фиксация прибыли при достижении цели"
    }
}

ARBITRAGE_STATUS_MAP = {
    ArbitrageStatus.PENDING: {
        "text": "Ожидает",
        "emoji": "⏳",
        "full": "⏳ Ожидает выполнения",
        "color": "🟡"
    },
    ArbitrageStatus.IN_PROGRESS: {
        "text": "Выполняется",
        "emoji": "⚙️",
        "full": "⚙️ В процессе выполнения",
        "color": "🔵"
    },
    ArbitrageStatus.COMPLETED: {
        "text": "Завершена",
        "emoji": "✅",
        "full": "✅ Успешно завершена",
        "color": "🟢"
    },
    ArbitrageStatus.FAILED: {
        "text": "Неудачно",
        "emoji": "❌",
        "full": "❌ Не удалось выполнить",
        "color": "🔴"
    },
    ArbitrageStatus.CANCELLED: {
        "text": "Отменена",
        "emoji": "🚫",
        "full": "🚫 Отменена пользователем",
        "color": "⚪"
    },
    ArbitrageStatus.TIMEOUT: {
        "text": "Таймаут",
        "emoji": "⏰",
        "full": "⏰ Истекло время ожидания",
        "color": "🟠"
    }
}


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ УДОБНОЙ РАБОТЫ С МАППЕРАМИ
# ============================================================================

def get_opportunity_display(opportunity_type: OpportunityType, format_type: str = "full") -> str:
    """
    Получить отформатированное представление типа возможности.

    Args:
        opportunity_type: Тип возможности из Enum
        format_type: Тип форматирования ("text", "emoji", "full")

    Returns:
        Отформатированная строка
    """
    mapping = OPPORTUNITY_TYPE_MAP.get(opportunity_type, {})
    return mapping.get(format_type, "Неизвестно")


def get_risk_display(risk_level: RiskLevel, format_type: str = "full") -> str:
    """
    Получить отформатированное представление уровня риска.
    """
    mapping = RISK_LEVEL_MAP.get(risk_level, {})
    return mapping.get(format_type, "Неизвестно")


def get_trend_sparkline(market_trend: MarketTrend) -> str:
    """
    Получить sparkline график для тренда.
    """
    mapping = MARKET_TREND_MAP.get(market_trend, {})
    return mapping.get("sparkline", "▄▄▄▄▄▄▄")


def format_technical_analysis(rsi_status: RSIStatus, macd_signal: MACDSignal,
                              bollinger_status: BollingerBandStatus) -> str:
    """
    Создать сводку технического анализа.
    """
    rsi_info = RSI_STATUS_MAP.get(rsi_status, {})
    macd_info = MACD_SIGNAL_MAP.get(macd_signal, {})
    bollinger_info = BOLLINGER_BAND_MAP.get(bollinger_status, {})

    return f"""📊 **Технический анализ:**
RSI: {rsi_info.get('full', 'Н/Д')}
MACD: {macd_info.get('full', 'Н/Д')}  
Боллинджер: {bollinger_info.get('full', 'Н/Д')}"""


# ============================================================================
# КОНСТАНТЫ ДЛЯ БЫСТРОГО ДОСТУПА К ЧАСТО ИСПОЛЬЗУЕМЫМ ЗНАЧЕНИЯМ
# ============================================================================

# Эмодзи для быстрого доступа
EMOJI = {
    "profit_high": "💎",
    "profit_low": "📈",
    "risk_low": "🟢",
    "risk_high": "🔴",
    "trend_up": "📈",
    "trend_down": "📉",
    "warning": "⚠️",
    "success": "✅",
    "error": "❌",
    "loading": "⏳"
}

# Цвета для различных состояний
COLORS = {
    "green": "🟢",
    "yellow": "🟡",
    "red": "🔴",
    "blue": "🔵",
    "orange": "🟠",
    "black": "⚫",
    "white": "⚪"
}

# ============================================================================
# МАППЕРЫ ДЛЯ СКРИНЕРА ПЛОТНОСТЕЙ
# ============================================================================

DENSITY_ACTION_MAP = {
    DensityAction.CONSIDER_LONG: {
        "text": "Рассмотреть LONG",
        "emoji": "🟢",
        "description": "Сильная поддержка, возможен рост цены."
    },
    DensityAction.CONSIDER_SHORT: {
        "text": "Рассмотреть SHORT",
        "emoji": "🔴",
        "description": "Сильное сопротивление, возможно падение цены."
    },
    DensityAction.WAIT_AND_WATCH: {
        "text": "Ждать и наблюдать",
        "emoji": "🟡",
        "description": "Силы покупателей и продавцов сбалансированы."
    },
    DensityAction.NEUTRAL: {
        "text": "Нейтрально",
        "emoji": "⚪️",
        "description": "Нет данных для формирования вывода."
    }
}