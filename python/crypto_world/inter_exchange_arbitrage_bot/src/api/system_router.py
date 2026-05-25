# inter_exchange_arbitrage_bot/src/api/system_router.py
import asyncio

from fastapi import APIRouter, HTTPException, Depends, status

import src.core.state as app_state
from src.api.dependencies import get_api_key
from src.api.schemas import PairActionRequest
from src.constants.api_constants import (
    API_KEY_MESSAGE, API_KEY_SERVICES_READY, API_KEY_HEALTHY_SERVICES, HEALTH_STATUS_DEGRADED,
    HEALTH_STATUS_HEALTHY, API_KEY_STATUS, API_KEY_TOTAL_SERVICES, API_KEY_SERVICE_DETAILS,
    SERVICE_STATUS_HEALTHY, SERVICE_STATUS_UNHEALTHY, API_KEY_READY_FOR_ARBITRAGE, API_KEY_HUMAN_REPORT,
    API_KEY_ASSETS, API_KEY_SOURCES, API_STATUS_VALUE_SUCCESS, API_KEY_EXCLUDED_PAIRS, API_KEY_TOTAL_COUNT,
    BALANCE_MODE_TRACKED, BALANCE_MODE_ALL, API_KEY_REPORT_TEXT, API_KEY_MODE, API_KEY_SERVICES_INITIALIZED,
    API_KEY_CACHES_INITIALIZED, API_TAG_SYSTEM, API_TAG_ADMIN, API_TAG_BOT_FACING
)
from src.constants.trading_constants import MIN_EXCHANGES_FOR_ARBITRAGE, ADMIN_EXCLUSION_REASON_MANUAL
from src.lexicon.lexicon_ru import LEXICON_RU
from src.services.dynamic_pairs_manager import dynamic_pairs_manager
from src.services.service_manager import service_manager
from src.utils.helpers import get_configured_exchanges
from src.utils.logger import logger

system_router = APIRouter(tags=[API_TAG_SYSTEM])


@system_router.get("/")
async def root():
    return {
        API_KEY_MESSAGE: LEXICON_RU['api_is_running'],
        API_KEY_SERVICES_READY: service_manager.is_ready_for_arbitrage,
        API_KEY_HEALTHY_SERVICES: len(service_manager.healthy_services)
    }


@system_router.get("/health")
async def health_check():
    """Полностью исправленная функция health_check."""
    is_fully_ready = app_state.is_ready_event.is_set()

    healthy_services_set = await service_manager.get_healthy_services()
    all_service_keys = sorted(service_manager.services.keys())
    healthy_count = len(healthy_services_set)
    total_count = len(all_service_keys)

    is_ready_for_arbitrage = is_fully_ready and service_manager.is_ready_for_arbitrage

    is_degraded = healthy_count < MIN_EXCHANGES_FOR_ARBITRAGE or not is_fully_ready
    machine_status = HEALTH_STATUS_DEGRADED if is_degraded else HEALTH_STATUS_HEALTHY

    human_status_key = 'health_status_degraded' if is_degraded else 'health_status_ok'
    human_status_text = LEXICON_RU[human_status_key]

    readiness_key = 'ready_for_arbitrage_true' if is_ready_for_arbitrage else 'ready_for_arbitrage_false'
    readiness_text = LEXICON_RU[readiness_key]

    service_details_lines = []
    for service_name in all_service_keys:
        is_service_healthy = service_name in healthy_services_set
        service_status_key = 'service_healthy' if is_service_healthy else 'service_unhealthy'
        line = LEXICON_RU['health_check_service_line'].format(
            service_name=service_name,
            service_status=LEXICON_RU[service_status_key]
        )
        service_details_lines.append(line)

    human_readable_report = (
            LEXICON_RU['health_check_title'] +
            LEXICON_RU['health_check_summary'].format(status=human_status_text) +
            LEXICON_RU['health_check_services_count'].format(healthy_count=healthy_count, total_count=total_count) +
            LEXICON_RU['health_check_details_title'] + "".join(service_details_lines) +
            LEXICON_RU['health_check_readiness'].format(is_ready=readiness_text)
    )

    return {
        API_KEY_STATUS: machine_status,
        API_KEY_TOTAL_SERVICES: total_count,
        API_KEY_HEALTHY_SERVICES: healthy_count,
        API_KEY_SERVICE_DETAILS: {
            exchange_id: SERVICE_STATUS_HEALTHY if exchange_id in healthy_services_set else SERVICE_STATUS_UNHEALTHY
            for exchange_id in all_service_keys
        },
        API_KEY_READY_FOR_ARBITRAGE: is_ready_for_arbitrage,
        API_KEY_HUMAN_REPORT: human_readable_report
    }


@system_router.get("/health/progress", tags=["System"])
async def health_check_progress():
    """
    Возвращает детализированный статус инициализации для отображения пользователю.
    """
    # DynamicPairsManager может быть еще не инициализирован, проверяем это
    cache_stats = dynamic_pairs_manager.get_cache_stats()
    # Считаем, сколько бирж уже имеют проинициализированный кэш
    initialized_caches = sum(1 for data in cache_stats.values() if data.get('total_pairs', 0) > 0)

    return {
        API_KEY_SERVICES_INITIALIZED: service_manager._initialized,
        API_KEY_HEALTHY_SERVICES: len(service_manager.healthy_services),
        API_KEY_TOTAL_SERVICES: len(get_configured_exchanges()),
        API_KEY_CACHES_INITIALIZED: initialized_caches,
    }


@system_router.get("/assets", tags=["Bot Facing"])
async def get_all_assets_for_bot():
    """
    Эндпоинт для бота: собирает все уникальные спотовые активы
    со всех 'здоровых' бирж.
    """
    try:
        # Получаем только здоровые сервисы
        healthy_services = await service_manager.get_healthy_services()
        if not healthy_services:
            return {API_KEY_ASSETS: [], API_KEY_SOURCES: []}

        # Параллельно запрашиваем активы
        asset_tasks = [service.get_all_spot_assets() for service in healthy_services.values()]
        results = await asyncio.gather(*asset_tasks, return_exceptions=True)

        all_assets = set()
        successful_sources = []

        # Собираем все активы в одно множество и отслеживаем успешные источники
        for exchange_id, result in zip(healthy_services.keys(), results):
            if isinstance(result, list):
                all_assets.update(result)
                successful_sources.append(exchange_id)
            else:
                logger.warning(LEXICON_RU['log_assets_fetch_failed'].format(exchange_id=exchange_id))
        return {
            API_KEY_ASSETS: sorted(list(all_assets)),
            API_KEY_SOURCES: successful_sources
        }
    except Exception as e:
        logger.error(LEXICON_RU['log_assets_endpoint_error'].format(e=e), exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=LEXICON_RU['api_error_asset_collection'])


# ====== ЗАЩИЩЕННЫЕ АДМИНИСТРАТИВНЫЕ ЭНДПОИНТЫ ======

@system_router.get("/admin/cache-stats", tags=[API_TAG_ADMIN], dependencies=[Depends(get_api_key)])
async def get_cache_stats_endpoint():
    """
    Возвращает актуальную статистику кэша торговых пар
    из работающего экземпляра DynamicPairsManager.
    """
    stats = dynamic_pairs_manager.get_cache_stats()
    if not stats:
        return {API_KEY_MESSAGE: LEXICON_RU['cache_is_empty']}
    return stats


@system_router.post("/admin/exclude-pair", tags=[API_TAG_ADMIN], dependencies=[Depends(get_api_key)])
async def exclude_pair_endpoint(request: PairActionRequest):
    """
    Добавляет торговую пару в административный список исключений.
    """
    try:
        dynamic_pairs_manager.add_admin_exclusion(request.exchange, request.symbol, ADMIN_EXCLUSION_REASON_MANUAL)
        return {API_KEY_STATUS: API_STATUS_VALUE_SUCCESS,
                API_KEY_MESSAGE: LEXICON_RU['api_msg_pair_excluded'].format(symbol=request.symbol,
                                                                            exchange=request.exchange)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@system_router.get("/admin/excluded-pairs", tags=[API_TAG_ADMIN], dependencies=[Depends(get_api_key)])
async def get_excluded_pairs_endpoint():
    """Возвращает список пар, исключенных администратором."""
    try:
        excluded_pairs = dynamic_pairs_manager.get_admin_excluded_pairs()
        return {
            API_KEY_STATUS: API_STATUS_VALUE_SUCCESS,
            API_KEY_EXCLUDED_PAIRS: excluded_pairs,
            API_KEY_TOTAL_COUNT: sum(len(symbols) for symbols in excluded_pairs.values())
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@system_router.post("/admin/include-pair", tags=[API_TAG_ADMIN], dependencies=[Depends(get_api_key)])
async def include_pair_endpoint(request: PairActionRequest):
    """
    Удаляет торговую пару из административного списка исключений.
    """
    try:
        dynamic_pairs_manager.remove_admin_exclusion(request.exchange, request.symbol)
        return {API_KEY_STATUS: API_STATUS_VALUE_SUCCESS,
                API_KEY_MESSAGE: LEXICON_RU['api_msg_pair_included'].format(symbol=request.symbol,
                                                                            exchange=request.exchange)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@system_router.get("/balances/{mode}", tags=[API_TAG_BOT_FACING])
async def get_balances_for_bot(mode: str):
    """Эндпоинт для бота - получение отчета о балансах через единый BalanceService."""
    # Импортируем здесь, чтобы избежать циклических зависимостей
    if app_state.balance_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=LEXICON_RU['api_error_balance_service_not_ready'])

    if mode not in [BALANCE_MODE_TRACKED, BALANCE_MODE_ALL]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=LEXICON_RU['api_error_invalid_balance_mode'])
    try:
        messages, final_mode = await app_state.balance_service.generate_report_messages(mode)
        full_report_text = "\n\n".join(messages)

        return {
            API_KEY_REPORT_TEXT: full_report_text,
            API_KEY_MODE: final_mode
        }
    except Exception as e:
        logger.error(LEXICON_RU['log_balance_report_error'].format(e=e), exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=LEXICON_RU['api_error_report_generation'])


@system_router.get("/coins/top", tags=[API_TAG_BOT_FACING])
async def get_top_coins(limit: int = 10):
    """
    Возвращает список тикеров топ-N монет по рыночной капитализации.
    """
    # АРГУМЕНТАЦИЯ: Обращаемся к market_intel_service, так как именно он
    # отвечает за всю логику работы с CoinGecko. Это устраняет дублирование
    # и делает архитектуру консистентной.
    if not app_state.market_intel_service:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Сервис рыночной аналитики не готов.")
    try:
        # Используем уже существующий и протестированный метод
        top_coins = await app_state.market_intel_service.get_top_coin_symbols(limit)
        return {"status": "success", "coins": top_coins}
    except Exception as e:
        logger.error(f"Ошибка при получении топ монет: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Не удалось получить список топ монет.")