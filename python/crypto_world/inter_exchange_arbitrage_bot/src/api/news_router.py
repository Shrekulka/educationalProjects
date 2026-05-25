# inter_exchange_arbitrage_bot/src/api/news_router.py
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, validator
import src.core.state as app_state

from src.api.dependencies import get_api_key
from src.constants.api_constants import API_PREFIX_NEWS, API_TAG_NEWS
from src.utils.helpers import get_canonical_symbol
from src.utils.logger import logger

news_router = APIRouter(prefix=API_PREFIX_NEWS, tags=[API_TAG_NEWS])


class NewsRequest(BaseModel):
    mode: Optional[str] = None  # Например, 'top10' или 'favorites'
    coins: Optional[List[str]] = None  # Список монет теперь тоже необязателен

    @validator('mode')
    def validate_mode(cls, v):
        """Валидирует режим запроса новостей."""
        if v is not None and v not in ['top10', 'favorites', 'custom']:
            raise ValueError("Режим должен быть одним из: 'top10', 'favorites', 'custom'")
        return v

    @validator('coins')
    def validate_coins(cls, v, values):
        """Валидирует список монет и нормализует их символы."""
        mode = values.get('mode')

        # Если режим 'custom', список монет обязателен
        if mode == 'custom' and (not v or len(v) == 0):
            raise ValueError("Для режима 'custom' необходимо указать список монет")

        # Нормализуем символы монет, если они предоставлены
        if v:
            try:
                normalized_coins = [get_canonical_symbol(coin) for coin in v]
                return normalized_coins
            except Exception as e:
                logger.warning(f"Ошибка нормализации символов монет {v}: {e}")
                return v  # Возвращаем оригинал в случае ошибки

        return v


@news_router.post("/get", dependencies=[Depends(get_api_key)])
async def get_news_endpoint(request: NewsRequest):
    """
    Получает новости по монетам в зависимости от выбранного режима.

    Поддерживаемые режимы:
    - 'top10': Топ-10 монет по капитализации
    - 'favorites': Пользовательские избранные монеты (только при вызове из бота)
    - 'custom': Пользовательский список монет
    - None: Использует переданный список coins или возвращает ошибку
    """
    if not app_state.news_aggregator_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервис новостей не готов."
        )

    coins_to_process = []

    try:
        if request.mode == 'top10':
            # Логика определения топ-10 теперь на бэкенде
            api_coins = await app_state.market_intel_service.get_top_coin_symbols(10)
            if not api_coins:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Не удалось получить список топ-монет"
                )
            coins_to_process = api_coins

        elif request.mode == 'custom' or (request.mode is None and request.coins):
            # Используем переданный список монет (уже нормализованный валидатором)
            coins_to_process = request.coins or []

        elif request.mode == 'favorites':
            # Этот режим должен использоваться только ботом с предварительно полученным списком
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Режим 'favorites' предназначен только для внутреннего использования ботом"
            )
        else:
            # Если не указан ни режим, ни монеты
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходимо указать режим или список монет"
            )

        if not coins_to_process:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Список монет для обработки пуст"
            )

        # Получаем новости
        news_data = await app_state.news_aggregator_service.get_aggregated_news(coins_to_process)

        return {
            "status": "success",
            "data": news_data,
            "count": len(news_data),
            "processed_coins": coins_to_process
        }

    except HTTPException:
        # Пробрасываем HTTP исключения как есть
        raise
    except Exception as e:
        logger.error(f"Ошибка в эндпоинте /news/get: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при обработке новостей"
        )