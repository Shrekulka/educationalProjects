# inter_exchange_arbitrage_bot/src/api/schemas.py

from pydantic import BaseModel, Field

from src.constants import DEFAULT_FALLBACK_SYMBOL, EXCHANGE_BYBIT
from src.constants.api_constants import (
    API_KEY_STATUS, API_KEY_HUMAN_STATUS, API_KEY_MESSAGE,
    API_KEY_EXCHANGE, API_KEY_SYMBOL, API_STATUS_VALUE_RUNNING, API_STATUS_VALUE_STOPPED
)


class ScannerStatusResponse(BaseModel):
    """Схема ответа для эндпоинта статуса сканера."""
    # Используем константу в 'alias', чтобы связать поле с ключом в JSON.
    machine_status: str = Field(
        ...,
        alias=API_KEY_STATUS,
        description=f"Текущий статус сканера ('{API_STATUS_VALUE_RUNNING}' или '{API_STATUS_VALUE_STOPPED}')",
        example=API_STATUS_VALUE_RUNNING
    )
    # Также добавляем alias здесь для явного определения контракта API.
    human_readable_status: str = Field(
        ...,
        alias=API_KEY_HUMAN_STATUS,
        description="Человекочитаемый статус",
        example="📈 В рынке!"
    )

    class Config:
        # Это позволяет Pydantic правильно сопоставлять псевдонимы (aliases) с полями модели.
        populate_by_name = True


class ScannerActionResponse(BaseModel):
    """Общая схема ответа для действий (запуск/остановка)."""
    # Явно указываем, что поле 'message' в Python соответствует ключу "message" в JSON.
    message: str = Field(
        ...,
        alias=API_KEY_MESSAGE,
        description="Сообщение о результате выполнения действия",
        example="Scanner started successfully."
    )

    class Config:
        populate_by_name = True


class PairActionRequest(BaseModel):
    """Схема для запросов на исключение/включение торговых пар."""
    # Явно указываем, что поле 'exchange' соответствует ключу "exchange".
    exchange: str = Field(
        ...,
        alias=API_KEY_EXCHANGE,
        description="ID биржи в нижнем регистре",
        example=EXCHANGE_BYBIT
    )
    # Явно указываем, что поле 'symbol' соответствует ключу "symbol".
    symbol: str = Field(
        ...,
        alias=API_KEY_SYMBOL,
        description="Торговый символ в верхнем регистре",
        example=DEFAULT_FALLBACK_SYMBOL
    )

    class Config:
        populate_by_name = True

# Схема для запроса на "Разведку"
class ReconnaissanceRequest(BaseModel):
    """Схема для запроса на запуск сканирования в режиме 'Разведка'."""
    chat_id: int = Field(..., description="ID чата для отправки обновлений прогресса.")
    message_id: int = Field(..., description="ID сообщения, которое нужно обновлять с прогрессом.")

    class Config:
        populate_by_name = True