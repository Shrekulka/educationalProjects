# src/models/user_models.py

from sqlalchemy import BigInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class UserCoin(Base):
    """Модель для хранения избранных монет пользователя."""
    __tablename__ = 'user_coins'

    # Уникальный идентификатор записи (стандартно для всех таблиц)
    id: Mapped[int] = mapped_column(primary_key=True)

    # ID пользователя в Telegram. BigInteger, так как ID могут быть большими.
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)

    # Тикер монеты, например, 'BTC' или 'ETH'.
    coin_ticker: Mapped[str] = mapped_column(String(20))

    # Ограничение, которое не позволит добавить одну и ту же монету одному пользователю дважды.
    __table_args__ = (
        UniqueConstraint('user_id', 'coin_ticker', name='_user_coin_uc'),
    )

    def __repr__(self):
        return f"<UserCoin(user_id={self.user_id}, coin='{self.coin_ticker}')>"