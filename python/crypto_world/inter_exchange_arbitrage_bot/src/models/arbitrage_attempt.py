# inter_exchange_arbitrage_bot/src/models/arbitrage_attempt.py
import enum
from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime, Numeric, Text, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


# Создаем Enum для статусов
class ArbitrageStatus(enum.Enum):
    EXECUTION_FAILED = "execution_failed"
    EXECUTED_UNPROFITABLE = "executed_unprofitable"
    FULLY_SUCCESSFUL = "fully_successful"


class ArbitrageAttempt(Base):
    __tablename__ = 'arbitrage_attempts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    symbol: Mapped[str] = mapped_column(String(20))
    coin: Mapped[str] = mapped_column(String(10))
    buy_exchange: Mapped[str] = mapped_column(String(20))
    sell_exchange: Mapped[str] = mapped_column(String(20))
    planned_amount: Mapped[float] = mapped_column(Numeric(18, 8))
    trade_value_usd: Mapped[float] = mapped_column(Numeric(12, 2))
    spread_percent: Mapped[float] = mapped_column(Numeric(8, 4))
    status: Mapped[ArbitrageStatus] = mapped_column(Enum(ArbitrageStatus), default=ArbitrageStatus.EXECUTION_FAILED,
                                                    index=True)
    failure_reason: Mapped[str] = mapped_column(String(100), nullable=True)
    balance_issues: Mapped[str] = mapped_column(Text, nullable=True)
    buy_price: Mapped[float] = mapped_column(Numeric(18, 8), nullable=True)
    sell_price: Mapped[float] = mapped_column(Numeric(18, 8), nullable=True)
    actual_profit_usd: Mapped[float] = mapped_column(Numeric(12, 4), nullable=True)
