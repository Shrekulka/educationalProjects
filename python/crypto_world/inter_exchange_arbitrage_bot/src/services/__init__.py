# inter_exchange_arbitrage_bot/src/services/__init__.py
from .data_enricher_service import DataEnricherService
from .exchange_service import ExchangeService
from .balance_service import BalanceService
from .notifier_service import NotifierService
from .report_formatter import ReportFormatter
from .arbitrage_report_service import ArbitrageReportService
from .scanner_api_service import (
    get_scanner_status,
    start_scanner,
    stop_scanner,
)
from .service_manager import ServiceManager, service_manager, managed_services
from .scanner_state_service import get_scanner_state_from_db, set_scanner_state_in_db

# __all__ определяет публичный API пакета 'services'
# Это то, что будет импортировано при `from src.services import *`
__all__ = [
    # --- Основные классы-сервисы ---
    'ExchangeService',
    'BalanceService',
    'NotifierService',
    'ServiceManager',
    'ReportFormatter',
    'ArbitrageReportService',
    'DataEnricherService',

    # --- Функции для взаимодействия с API сканера ---
    'get_scanner_status',
    'start_scanner',
    'stop_scanner',

    # --- Функции для работы с состоянием сканера в БД ---
    'get_scanner_state_from_db',
    'set_scanner_state_in_db',

    # --- Глобальные экземпляры и утилиты ---
    'service_manager',   # Экземпляр-одиночка для управления сервисами
    'managed_services',  # Контекстный менеджер для удобной работы с сервисами
]