# inter_exchange_arbitrage_bot/src/models/screener_models.py

from dataclasses import dataclass

@dataclass
class Density:
    """
    Структура для хранения информации о найденной плотности в биржевом стакане.
    Является общей моделью данных для сервисов скринера и отрисовки графиков.
    """
    symbol: str
    exchange: str
    price: float
    volume_usd: float
    density_type: str  # 'support' или 'resistance'
    distance_percent: float