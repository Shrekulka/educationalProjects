# inter_exchange_arbitrage_bot/src/models/user_settings.py

from sqlalchemy import BigInteger, String, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base

class UserSetting(Base):
    """Модель для хранения индивидуальных настроек пользователя в формате ключ-значение."""
    __tablename__ = 'user_settings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)

    # Ключ настройки, например, 'trade_amount'
    key: Mapped[str] = mapped_column(String(50))

    # Значение настройки. Используем String, чтобы хранить любые типы данных.
    # Преобразование в нужный тип (float, int) будет происходить в коде.
    value: Mapped[str] = mapped_column(String(255))

    __table_args__ = (
        UniqueConstraint('user_id', 'key', name='_user_setting_uc'),
    )

    def __repr__(self):
        return f"<UserSetting(user_id={self.user_id}, key='{self.key}', value='{self.value}')>"