# inter_exchange_arbitrage_bot/src/services/arbitrage_report_service.py

import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from sqlalchemy import select, and_, func

from src.core.database import async_session_factory
from src.models.arbitrage_attempt import ArbitrageAttempt
from src.models.arbitrage_attempt import ArbitrageStatus
from src.utils.logger import logger


class ArbitrageReportService:
    """Сервис для генерации отчетов по арбитражным сделкам."""

    async def log_arbitrage_attempt(
            self,
            user_id: int,
            symbol: str,
            coin: str,
            buy_exchange: str,
            sell_exchange: str,
            planned_amount: float,
            trade_value_usd: float,
            spread_percent: float,
            status: ArbitrageStatus,
            failure_reason: Optional[str] = None,
            balance_issues: Optional[Dict] = None,
            buy_price: Optional[float] = None,
            sell_price: Optional[float] = None,
            actual_profit_usd: Optional[float] = None
    ) -> bool:
        """Логирует попытку арбитража в базу данных с использованием Enum статуса."""
        try:
            async with async_session_factory() as session:
                attempt = ArbitrageAttempt(
                    user_id=user_id, symbol=symbol, coin=coin,
                    buy_exchange=buy_exchange, sell_exchange=sell_exchange,
                    planned_amount=planned_amount, trade_value_usd=trade_value_usd,
                    spread_percent=spread_percent, status=status, failure_reason=failure_reason,
                    balance_issues=json.dumps(balance_issues) if balance_issues else None,
                    buy_price=buy_price, sell_price=sell_price, actual_profit_usd=actual_profit_usd
                )
                session.add(attempt)
                await session.commit()
                logger.debug(f"Записана попытка арбитража со статусом {status.name} для {user_id}")
                return True
        except Exception as e:
            logger.error(f"Ошибка при логировании попытки арбитража: {e}", exc_info=True)
            return False

    async def get_summary_report(self, user_id: int, hours_back: int) -> Dict:
        """Собирает расширенную статистику по сделкам с учетом новых статусов."""
        report_data = {
            'period_hours': hours_back, 'total_attempts': 0,
            'successful_attempts': {'count': 0, 'profit': 0.0},
            'executed_unprofitable': {'count': 0, 'loss': 0.0},
            'failed_attempts': {'count': 0, 'reasons': defaultdict(int)}
        }
        # АРГУМЕНТАЦИЯ: Заменяем устаревший datetime.utcnow() на современный,
        # timezone-aware вызов datetime.now(timezone.utc). Это обеспечивает
        # корректное сравнение времени и соответствует новым стандартам Python.
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_back)
        try:
            async with async_session_factory() as session:
                stmt = select(
                    ArbitrageAttempt.status,
                    func.count().label('count'),
                    func.sum(ArbitrageAttempt.actual_profit_usd).label('total_profit'),
                    ArbitrageAttempt.failure_reason
                ).where(
                    and_(ArbitrageAttempt.user_id == user_id, ArbitrageAttempt.timestamp >= cutoff_time)
                ).group_by(ArbitrageAttempt.status, ArbitrageAttempt.failure_reason)

                results = await session.execute(stmt)

                for row in results.all():
                    status, count, total_profit, failure_reason = row
                    report_data['total_attempts'] += count

                    if status == ArbitrageStatus.FULLY_SUCCESSFUL:
                        report_data['successful_attempts']['count'] = count
                        report_data['successful_attempts']['profit'] = float(total_profit or 0.0)
                    elif status == ArbitrageStatus.EXECUTED_UNPROFITABLE:
                        report_data['executed_unprofitable']['count'] = count
                        report_data['executed_unprofitable']['loss'] = float(total_profit or 0.0)
                    elif status == ArbitrageStatus.EXECUTION_FAILED:
                        reason_key = failure_reason or 'unknown'
                        report_data['failed_attempts']['reasons'][reason_key] += count
                        report_data['failed_attempts']['count'] += count

                return report_data
        except Exception as e:
            logger.error(f"Ошибка при формировании расширенного отчета: {e}", exc_info=True)
            return report_data

    async def get_detailed_attempts_report(self, user_id: int, hours_back: int = 24) -> Dict:
        """
        ИСПРАВЛЕННАЯ ВЕРСИЯ: Собирает детальный отчет с учетом новой трехуровневой
        системы статусов (FULLY_SUCCESSFUL, EXECUTED_UNPROFITABLE, EXECUTION_FAILED).
        """
        # Структура данных теперь отражает три статуса
        report_data = {
            'successful': {},
            'executed_unprofitable': {},
            'failed': {},
            'period_hours': hours_back
        }

        # АРГУМЕНТАЦИЯ: Заменяем устаревший datetime.utcnow() на современный,
        # timezone-aware вызов datetime.now(timezone.utc). Это обеспечивает
        # корректное сравнение времени и соответствует новым стандартам Python.
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_back)
        try:
            async with async_session_factory() as session:
                stmt = select(ArbitrageAttempt).where(
                    and_(
                        ArbitrageAttempt.user_id == user_id,
                        ArbitrageAttempt.timestamp >= cutoff_time
                    )
                ).order_by(ArbitrageAttempt.timestamp.desc())

                result = await session.execute(stmt)
                attempts = result.scalars().all()

                # Группируем попытки по новым статусам
                successful_groups = defaultdict(lambda: defaultdict(list))
                unprofitable_groups = defaultdict(lambda: defaultdict(list))
                failed_groups = defaultdict(lambda: defaultdict(list))

                for attempt in attempts:
                    exchange_key = attempt.buy_exchange
                    coin_key = attempt.coin

                    if attempt.status == ArbitrageStatus.FULLY_SUCCESSFUL:
                        successful_groups[exchange_key][coin_key].append(attempt)
                    elif attempt.status == ArbitrageStatus.EXECUTED_UNPROFITABLE:
                        unprofitable_groups[exchange_key][coin_key].append(attempt)
                    else:
                        failed_groups[exchange_key][coin_key].append(attempt)

                report_data['successful'] = {
                    exchange: dict(coins) for exchange, coins in successful_groups.items()
                }
                report_data['executed_unprofitable'] = {
                    exchange: dict(coins) for exchange, coins in unprofitable_groups.items()
                }
                report_data['failed'] = {
                    exchange: dict(coins) for exchange, coins in failed_groups.items()
                }

                total_attempts = len(attempts)
                logger.debug(f"Детальный отчет для пользователя {user_id}: {total_attempts} попыток за {hours_back}ч")
                return report_data

        except Exception as e:
            logger.error(f"Ошибка при формировании детального отчета для {user_id}: {e}", exc_info=True)
            return report_data
