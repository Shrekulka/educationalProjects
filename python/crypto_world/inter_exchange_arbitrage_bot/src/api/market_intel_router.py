# inter_exchange_arbitrage_bot/src/api/market_intel_router.py

from fastapi import APIRouter, HTTPException, status
import src.core.state as app_state
from src.constants.api_constants import API_PREFIX_INTEL, API_TAG_INTEL

from src.utils.logger import logger



intel_router = APIRouter(prefix=API_PREFIX_INTEL, tags=[API_TAG_INTEL])


@intel_router.get("/summary")
async def get_market_intelligence_summary():
    """
    Возвращает сводку рыночной аналитики: тренды, лидеры роста и падения.
    """
    if not app_state.market_intel_service:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Сервис аналитики не готов.")

    try:
        trending = await app_state.market_intel_service.get_trending_coins()
        gainers_losers = await app_state.market_intel_service.get_top_gainers_losers()

        return {
            "status": "success",
            "data": {
                "trending": trending,
                "gainers": gainers_losers.get("gainers", []),
                "losers": gainers_losers.get("losers", [])
            }
        }
    except Exception as e:
        logger.error(f"Ошибка в эндпоинте /intel/summary: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))