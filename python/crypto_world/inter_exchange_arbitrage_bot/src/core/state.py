# inter_exchange_arbitrage_bot/src/core/state.py

import asyncio
from typing import Optional, TYPE_CHECKING

import httpx
from aiogram import Bot
import aiohttp

# Этот блок выполняется только во время статической проверки типов, но не при запуске программы.
if TYPE_CHECKING:
    from src.services import (
        BalanceService, NotifierService, ArbitrageReportService,
        DataEnricherService
    )
    from src.services.density_screener_service import DensityScreenerService
    from src.services.density_chart_service import DensityChartService
    from src.services.news_aggregator_service import NewsAggregatorService
    from src.services.market_intelligence_service import MarketIntelligenceService
    from src.services.ai_trade_advisor_service import AITradeAdvisorService
    from src.services.proxy_manager import ProxyManager


# Этот файл хранит глобальное, изменяемое состояние API.

# --- Сервисы, которые будут инициализированы при запуске ---
balance_service: Optional['BalanceService'] = None
notifier_service: Optional['NotifierService'] = None
report_service: Optional['ArbitrageReportService'] = None
density_screener_service: Optional['DensityScreenerService'] = None
density_chart_service: Optional['DensityChartService'] = None
aiohttp_session: Optional[aiohttp.ClientSession] = None
bot_instance: Optional[Bot] = None

# --- Управление фоновыми задачами (Tasks) ---
# Для чего это нужно: Хранение ссылок на ключевые фоновые задачи (например, запуск бота или
# инициализация сервисов) позволяет корректно управлять ими: проверять их состояние
# и, что самое важное, безопасно отменять их при завершении работы приложения.
bot_task: Optional[asyncio.Task] = None
services_init_task: Optional[asyncio.Task] = None
# Задача для конкретной операции "Разведки"
services_task: Optional[asyncio.Task] = None
# Хранилище для самой задачи разведки +++
recon_task: Optional[asyncio.Task] = None

# --- Главный флаг готовности всего приложения ---
is_ready_event = asyncio.Event()

# Блокировка для предотвращения одновременного запуска ресурсоемкой операции "Разведки" из API-эндпоинта /reconnaissance.
reconnaissance_lock = asyncio.Lock()
# Блокировка для предотвращения конфликта между ручной разведкой и фоновым обновлением кэша
cache_refresh_lock = asyncio.Lock()

news_aggregator_service: Optional['NewsAggregatorService'] = None

# --- HTTP клиенты ---
# Основной клиент для ВНЕШНИХ запросов (API -> Groq, Binance, NewsAPI и т.д.)
httpx_session: Optional[httpx.AsyncClient] = None
# Отдельный клиент для ВНУТРЕННИХ запросов (бот -> свой API)

internal_httpx_session: Optional[httpx.AsyncClient] = None
market_intel_service: Optional['MarketIntelligenceService'] = None
data_enricher: Optional['DataEnricherService'] = None
ai_trade_advisor: Optional['AITradeAdvisorService'] = None
proxy_manager: Optional['ProxyManager'] = None
