# inter_exchange_arbitrage_bot/src/models/system_models.py

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base


class SystemState(Base):
    """Модель для хранения глобальных состояний системы."""
    __tablename__ = 'system_states'

    # Ключ состояния, например, 'scanner_status'. Уникальный.
    key: Mapped[str] = mapped_column(String(50), primary_key=True)

    # Значение состояния, например, 'running' или 'stopped'.
    value: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"<SystemState(key='{self.key}', value='{self.value}')>"