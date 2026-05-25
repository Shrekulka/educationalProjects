# inter_exchange_arbitrage_bot/src/services/scanner_state_service.py

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.constants.system_constants import (SYSTEM_STATE_SCANNER_STATUS, SCANNER_STATUS_STOPPED, SCANNER_STATUS_RUNNING)
from src.core.database import async_session_factory
from src.models.system_models import SystemState


async def get_scanner_state_from_db() -> str:
    """
    Получает состояние сканера из БД.

    Если запись о состоянии отсутствует, создает ее со значением по умолчанию ('stopped').
    """
    async with async_session_factory() as session:
        stmt = select(SystemState.value).where(SystemState.key == SYSTEM_STATE_SCANNER_STATUS)
        status = (await session.execute(stmt)).scalar_one_or_none()

        # Если статус в БД еще не задан (например, первый запуск).
        if status is None:
            stmt_insert = insert(SystemState).values(
                key=SYSTEM_STATE_SCANNER_STATUS,
                value=SCANNER_STATUS_STOPPED
            ).on_conflict_do_nothing()

            await session.execute(stmt_insert)
            await session.commit()
            # Возвращаем статус по умолчанию.
            return SCANNER_STATUS_STOPPED

        # Если статус найден, возвращаем его.
        return status


async def set_scanner_state_in_db(status: str):
    """
    Сохраняет (обновляет) состояние сканера в БД.
    """
    # Валидация входных данных, чтобы в БД не попал мусор
    if status not in [SCANNER_STATUS_RUNNING, SCANNER_STATUS_STOPPED]:
        raise ValueError(f"Недопустимый статус сканера: {status}")

    async with async_session_factory() as session:
        # Она атомарно вставит запись, если ее нет, или обновит, если она есть.
        stmt = insert(SystemState).values(key=SYSTEM_STATE_SCANNER_STATUS, value=status)
        stmt = stmt.on_conflict_do_update(
            index_elements=['key'],
            set_={'value': stmt.excluded.value}
        )
        await session.execute(stmt)
        await session.commit()
