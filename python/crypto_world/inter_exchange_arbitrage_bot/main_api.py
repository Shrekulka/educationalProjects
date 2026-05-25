# inter_exchange_arbitrage_bot/main_api.py

import asyncio
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

import src.core.state as app_state
from src.api.api_router import api_router
from src.api.market_intel_router import intel_router
from src.api.middleware import check_readiness_middleware
from src.api.news_router import news_router
from src.api.system_router import system_router
from src.utils.app_lifecycle import (initialize_app_services, shutdown_application)
from src.utils.logger import logger


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Управляет жизненным циклом приложения. Инициализация бота перенесена в app_lifecycle.py.
    """
    logger.info("Application lifespan: startup sequence initiated.")

    app_state.httpx_session = httpx.AsyncClient()
    app_state.internal_httpx_session = httpx.AsyncClient()

    logger.info("API сервер запущен, инициализация сервисов и бота стартует в фоне...")
    app_state.services_init_task = asyncio.create_task(initialize_app_services())

    try:
        yield
    finally:
        logger.info("Application lifespan: shutdown sequence initiated...")
        await shutdown_application()


app = FastAPI(title="Trading Bot API", lifespan=lifespan)
app.middleware("http")(check_readiness_middleware)

app.include_router(system_router)
app.include_router(api_router)
app.include_router(news_router)
app.include_router(intel_router)
