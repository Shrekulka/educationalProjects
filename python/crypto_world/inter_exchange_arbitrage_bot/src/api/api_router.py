# inter_exchange_arbitrage_bot/src/api/api_router.py

import asyncio

from fastapi import APIRouter, HTTPException, status, Depends

import src.core.state as app_state
from src.api.dependencies import get_api_key
from src.api.schemas import ScannerStatusResponse, ScannerActionResponse, ReconnaissanceRequest
from src.constants.api_constants import (
    API_PREFIX_SCANNER, API_TAG_SCANNER, API_KEY_STATUS, API_KEY_HUMAN_STATUS, API_KEY_MESSAGE,
    SCHEDULER_JOB_ID_ARBITRAGE
)
from src.constants.system_constants import SCANNER_STATUS_RUNNING, SCANNER_STATUS_STOPPED
from src.core.scheduler import scheduler
from src.lexicon.lexicon_ru import LEXICON_RU
from src.services.reconnaissance_service import run_reconnaissance_task
from src.services.scanner_state_service import get_scanner_state_from_db, set_scanner_state_in_db
from src.utils.logger import logger

api_router = APIRouter(prefix=API_PREFIX_SCANNER, tags=[API_TAG_SCANNER])


@api_router.get("/status", response_model=ScannerStatusResponse)
async def get_scanner_status_endpoint():
    current_status = await get_scanner_state_from_db()
    status_text_key = f'status_{current_status}'
    human_readable_status = LEXICON_RU.get(status_text_key, current_status)
    return {API_KEY_STATUS: current_status, API_KEY_HUMAN_STATUS: human_readable_status}


@api_router.post("/start", response_model=ScannerActionResponse, dependencies=[Depends(get_api_key)])
async def start_scanner_endpoint():
    """
    Надежный запуск сканера с проверками и откатом состояния.
    """
    job = scheduler.get_job(SCHEDULER_JOB_ID_ARBITRAGE)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=LEXICON_RU['job_not_found'])

    await set_scanner_state_in_db(SCANNER_STATUS_RUNNING)

    try:
        if not job.next_run_time:
            scheduler.resume_job(SCHEDULER_JOB_ID_ARBITRAGE)
            logger.info(LEXICON_RU['log_scheduler_resumed'])
        else:
            logger.info(LEXICON_RU['log_scheduler_already_active'])
    except Exception as e:
        logger.error(LEXICON_RU['log_scheduler_resume_error'].format(error=e))
        await set_scanner_state_in_db(SCANNER_STATUS_STOPPED)  # ОТКАТ СОСТОЯНИЯ
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=LEXICON_RU['api_error_scheduler_start']
        )

    logger.info(LEXICON_RU['log_started_api'])
    # ИСПОЛЬЗУЕМ СЕРВИС ИЗ ГЛОБАЛЬНОГО СОСТОЯНИЯ
    if app_state.notifier_service:
        asyncio.create_task(app_state.notifier_service.notify_all_admins_about_scanner_state())

    return {API_KEY_MESSAGE: LEXICON_RU['scanner_started']}


@api_router.post("/stop", response_model=ScannerActionResponse, dependencies=[Depends(get_api_key)])
async def stop_scanner_endpoint():
    """
    Надежная остановка сканера.
    """
    job = scheduler.get_job(SCHEDULER_JOB_ID_ARBITRAGE)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=LEXICON_RU['job_not_found'])

    await set_scanner_state_in_db(SCANNER_STATUS_STOPPED)

    try:
        if job.next_run_time:
            scheduler.pause_job(SCHEDULER_JOB_ID_ARBITRAGE)
            logger.info(LEXICON_RU['log_scheduler_paused'])
        else:
            logger.info(LEXICON_RU['log_scheduler_already_paused'])
    except Exception as e:
        # Здесь откат не нужен, так как мы и так хотели остановить. Просто логируем.
        logger.error(LEXICON_RU['log_scheduler_pause_error'].format(error=e))

    logger.info(LEXICON_RU['log_stopped_api'])
    # ИСПОЛЬЗУЕМ СЕРВИС ИЗ ГЛОБАЛЬНОГО СОСТОЯНИЯ
    if app_state.notifier_service:
        asyncio.create_task(app_state.notifier_service.notify_all_admins_about_scanner_state())

    return {API_KEY_MESSAGE: LEXICON_RU['scanner_stopped']}


@api_router.post("/reconnaissance", dependencies=[Depends(get_api_key)])
async def run_reconnaissance_endpoint(request: ReconnaissanceRequest):
    """
    ✅ ПРАВИЛЬНАЯ ВЕРСИЯ: Создает и запускает задачу разведки в фоновом режиме,
    сохраняя на нее ссылку в глобальном состоянии для управления (например, отмены).
    """
    # Проверяем, не запущена ли уже аналогичная задача
    if app_state.recon_task and not app_state.recon_task.done():
        logger.warning(LEXICON_RU['log_recon_already_running'])
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=LEXICON_RU['recon_already_running_user_message']
        )

    # Создаем фоновую задачу и сохраняем ссылку на нее
    app_state.recon_task = asyncio.create_task(run_reconnaissance_task(request))

    # МГНОВЕННО возвращаем статус, не дожидаясь завершения задачи
    return {"status": "reconnaissance_started"}


@api_router.get("/reconnaissance/status")
async def get_recon_status():
    if app_state.recon_task:
        return {"status": "running" if not app_state.recon_task.done() else "completed"}
    return {"status": "idle"}