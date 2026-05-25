# inter_exchange_arbitrage_bot/src/api/middleware.py

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

import src.core.state as app_state


async def check_readiness_middleware(request: Request, call_next):
    """
    Проверяет готовность приложения для API запросов, кроме системных.

    Это middleware перехватывает все входящие запросы. Если сервисы
    приложения еще не полностью инициализированы (событие is_ready_event
    не установлено), оно возвращает ответ 503 Service Unavailable,
    предотвращая выполнение эндпоинтов с неинициализированными зависимостями.
    """
    # Пропускаем системные эндпоинты (например, /health) и документацию,
    # чтобы они всегда были доступны для мониторинга и отладки.
    if request.url.path.startswith("/system/") or request.url.path in ["/docs", "/openapi.json"]:
        return await call_next(request)

    # Главная проверка: если событие готовности не установлено...
    if not app_state.is_ready_event.is_set():
        # ...немедленно возвращаем ответ с кодом 503.
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "Service Unavailable",
                "message": "Приложение еще инициализируется. Попробуйте позже."
            }
        )

    # Если система готова, передаем запрос дальше на обработку в роутеры.
    return await call_next(request)
