# src/services/report_formatter.py

import json
from collections import defaultdict
from typing import Dict, List

from src.constants.telegram_constants import (
    TELEGRAM_MESSAGE_MAX_LENGTH, REPORT_SECTION_SEPARATOR_CHAR,
    REPORT_SECTION_SEPARATOR_LENGTH, REPORT_DATE_FORMAT, DEFAULT_REPORT_PERIOD_HOURS
)
from src.lexicon.lexicon_ru import LEXICON_RU
from src.models.arbitrage_attempt import ArbitrageAttempt
from src.utils.logger import logger


class ReportFormatter:
    """
    Класс-утилита для преобразования данных об арбитражных сделках в готовые для отправки HTML-сообщения.
    """

    @staticmethod
    def format_summary_report(report_data: Dict) -> str:
        """
        Создает сводный (агрегированный) текстовый отчет по сделкам.

        Args:
            report_data: Словарь с агрегированными данными из ArbitrageReportService.

        Returns:
            Готовое к отправке HTML-сообщение в виде одной строки.
        """
        # --- Извлечение данных ---
        # Получаем период отчета или используем значение по умолчанию.
        period = report_data.get('period_hours', DEFAULT_REPORT_PERIOD_HOURS)
        total_attempts = report_data.get('total_attempts', 0)

        # Безопасно извлекаем данные по каждой категории сделок.
        successful = report_data.get('successful_attempts', {})
        unprofitable = report_data.get('executed_unprofitable', {})
        failed = report_data.get('failed_attempts', {})

        # Распаковываем данные из словарей для удобства.
        successful_count, successful_profit = successful.get('count', 0), successful.get('profit', 0.0)
        unprofitable_count, unprofitable_loss = unprofitable.get('count', 0), unprofitable.get('loss', 0.0)
        failed_count, failure_reasons = failed.get('count', 0), failed.get('reasons', {})

        # --- Расчет итоговых метрик ---
        # Чистый финансовый результат = вся прибыль минус все убытки.
        net_profit = successful_profit + unprofitable_loss

        # --- Сборка сообщения ---
        # Начинаем с заголовка из лексикона.
        lines = [LEXICON_RU['report_summary_title'].format(period=period)]

        # Определяем текст и эмодзи в зависимости от того, прибыль это или убыток.
        if net_profit >= 0:
            profit_label = LEXICON_RU['report_summary_profit_label']
            profit_emoji = LEXICON_RU['report_summary_profit_emoji']
            formatted_value = f"+${net_profit:,.2f}"
        else:
            profit_label = LEXICON_RU['report_summary_loss_label']
            profit_emoji = LEXICON_RU['report_summary_loss_emoji']
            formatted_value = f"${abs(net_profit):,.2f}"

        # Добавляем строку с общим результатом.
        lines.append(f"{profit_emoji} <b>{profit_label}:</b> <code>{formatted_value}</code>")
        lines.append(LEXICON_RU['report_summary_total_attempts'].format(total_attempts=total_attempts))

        # Добавляем блок с детализацией по категориям.
        lines.append(LEXICON_RU['report_summary_details_header'])
        lines.append(
            LEXICON_RU['report_summary_successful_line'].format(count=successful_count, profit=successful_profit))
        lines.append(LEXICON_RU['report_summary_unprofitable_line'].format(count=unprofitable_count,
                                                                           loss=abs(unprofitable_loss)))
        lines.append(LEXICON_RU['report_summary_failed_line'].format(count=failed_count))

        # Если были неудачные сделки, добавляем статистику по причинам.
        if failure_reasons:
            lines.append(LEXICON_RU['report_summary_failure_reasons_header'])
            # Сортируем причины по популярности для лучшей читаемости.
            sorted_reasons = sorted(failure_reasons.items(), key=lambda item: item[1], reverse=True)
            for reason, count in sorted_reasons:
                # Преобразуем "some_reason" в "Some reason" для красоты.
                reason_text = reason.replace('_', ' ').capitalize()
                lines.append(f"     - {reason_text}: {count}")

        # Объединяем все строки в одно сообщение.
        return "\n".join(lines)

    @staticmethod
    def _split_report_into_messages(lines: List[str]) -> List[str]:
        """
        Разделяет длинный отчет на несколько сообщений, чтобы не превысить лимит Telegram.
        """
        if not lines: return []
        messages, current_message = [], ""
        for line in lines:
            # Проверяем, поместится ли следующая строка в текущее сообщение.
            if len(current_message) + len(line) + 1 > TELEGRAM_MESSAGE_MAX_LENGTH:
                # Если нет, сохраняем текущее сообщение и начинаем новое.
                messages.append(current_message)
                current_message = line
            else:
                # Если да, добавляем строку к текущему сообщению.
                current_message += ("\n" if current_message else "") + line
        # Не забываем сохранить последнее собранное сообщение.
        if current_message: messages.append(current_message)
        return messages

    @staticmethod
    def _format_executed_attempt(attempt: ArbitrageAttempt) -> str:
        """
        Форматирует одну технически исполненную сделку (прибыльную или убыточную).

        Args:
            attempt: Объект ArbitrageAttempt из базы данных.

        Returns:
            Готовая HTML-строка для детального отчета.
        """
        try:
            # Безопасно извлекаем фактический финансовый результат.
            profit_or_loss = float(attempt.actual_profit_usd or 0.0)

            # Выбираем правильные иконку, текст и формат значения.
            if profit_or_loss >= 0:
                result_label, result_value = LEXICON_RU['report_item_profit_label'], f"+${profit_or_loss:,.2f}"
                icon = LEXICON_RU['report_item_profit_icon']
            else:
                result_label, result_value = LEXICON_RU['report_item_loss_label'], f"-${abs(profit_or_loss):,.2f}"
                icon = LEXICON_RU['report_item_loss_icon']

            # Собираем финальную строку, подставляя все данные в шаблон из лексикона.
            return LEXICON_RU['report_item_executed_template'].format(
                icon=icon, coin=attempt.coin, timestamp=attempt.timestamp.strftime(REPORT_DATE_FORMAT),
                route=f"{attempt.buy_exchange.capitalize()} → {attempt.sell_exchange.capitalize()}",
                trade_value=float(attempt.trade_value_usd), spread=float(attempt.spread_percent),
                result_label=result_label, result_value=result_value
            )
        except (TypeError, ValueError) as e:
            logger.warning(f"Не удалось отформатировать исполненную сделку ID {attempt.id}: {e}")
            return f"  ⚪️ <b>{attempt.coin}</b> - Ошибка форматирования"

    @staticmethod
    def _format_failed_attempt(attempt: ArbitrageAttempt) -> str:
        """
        Форматирует одну технически НЕ исполненную сделку.

        Args:
            attempt: Объект ArbitrageAttempt из базы данных.

        Returns:
            Готовая HTML-строка для детального отчета.
        """
        # Формируем ключ для поиска перевода причины в лексиконе.
        reason_key = f"failure_reason_{attempt.failure_reason or 'unknown'}"
        # Получаем перевод или, если его нет, форматируем ключ по умолчанию.
        reason_text = LEXICON_RU.get(reason_key, (attempt.failure_reason or 'unknown').replace('_', ' ').capitalize())

        # Собираем основную часть сообщения из шаблона.
        lines = [
            LEXICON_RU['report_item_failed_template'].format(
                coin=attempt.coin, timestamp=attempt.timestamp.strftime(REPORT_DATE_FORMAT),
                route=f"{attempt.buy_exchange.capitalize()} → {attempt.sell_exchange.capitalize()}",
                spread=float(attempt.spread_percent), reason=reason_text
            )
        ]

        # Если причина - нехватка баланса, добавляем подробности.
        if attempt.failure_reason == 'insufficient_balance' and attempt.balance_issues:
            try:
                # Парсим JSON с деталями о нехватке средств.
                issues = json.loads(attempt.balance_issues)
                for ex, details in issues.items():
                    lines.append(LEXICON_RU['report_item_balance_issue_line'].format(
                        exchange=ex.capitalize(),
                        currency=details.get('currency', LEXICON_RU['report_item_unknown_currency']),
                        needed=details.get('needed', 0),
                        available=details.get('available', 0)
                    ))
            except (json.JSONDecodeError, TypeError):
                # Игнорируем ошибки, если JSON некорректен.
                pass
        return "\n".join(lines)

    @staticmethod
    def format_detailed_arbitrage_report(report_data: Dict) -> List[str]:
        """
        Создает детальный текстовый отчет по всем типам сделок.

        Args:
            report_data: Словарь с данными из ArbitrageReportService.get_detailed_attempts_report.

        Returns:
            Список сообщений, готовых к отправке (уже разделены по лимиту длины).
        """
        # Извлекаем данные, используя значения по умолчанию.
        period = report_data.get('period_hours', DEFAULT_REPORT_PERIOD_HOURS)
        successful_data = report_data.get('successful', {})
        unprofitable_data = report_data.get('executed_unprofitable', {})
        failed_data = report_data.get('failed', {})

        # Если данных нет, возвращаем короткое сообщение.
        if not successful_data and not unprofitable_data and not failed_data:
            return [LEXICON_RU['report_detailed_title'].format(period=period) + LEXICON_RU['report_no_data']]

        # Начинаем отчет с заголовка.
        lines = [LEXICON_RU['report_detailed_title'].format(period=period)]

        # Преобразуем вложенные словари в плоские списки для удобства.
        all_successful = [att for ex in successful_data.values() for coin in ex.values() for att in coin]
        all_unprofitable = [att for ex in unprofitable_data.values() for coin in ex.values() for att in coin]
        all_failed = [att for ex in failed_data.values() for coin in ex.values() for att in coin]

        # Сортируем все сделки по времени от новых к старым.
        all_successful.sort(key=lambda x: x.timestamp, reverse=True)
        all_unprofitable.sort(key=lambda x: x.timestamp, reverse=True)
        all_failed.sort(key=lambda x: x.timestamp, reverse=True)

        # Собираем разделитель из констант.
        separator = f"\n{REPORT_SECTION_SEPARATOR_CHAR * REPORT_SECTION_SEPARATOR_LENGTH}\n"

        # Формируем блок для успешных сделок.
        if all_successful:
            total_profit = sum(float(a.actual_profit_usd or 0.0) for a in all_successful)
            lines.append(
                LEXICON_RU['report_detailed_successful_header'].format(count=len(all_successful), profit=total_profit))
            for attempt in all_successful:
                lines.append(ReportFormatter._format_executed_attempt(attempt))

        # Формируем блок для убыточных, но исполненных сделок.
        if all_unprofitable:
            total_loss = sum(float(a.actual_profit_usd or 0.0) for a in all_unprofitable)
            lines.append(separator)
            lines.append(LEXICON_RU['report_detailed_unprofitable_header'].format(count=len(all_unprofitable),
                                                                                  loss=abs(total_loss)))
            for attempt in all_unprofitable:
                lines.append(ReportFormatter._format_executed_attempt(attempt))

        # Формируем блок для неисполненных сделок.
        if all_failed:
            reason_counts = defaultdict(int)
            for a in all_failed: reason_counts[a.failure_reason or 'unknown'] += 1
            top_reasons = sorted(reason_counts.items(), key=lambda item: item[1], reverse=True)
            reason_summary = ", ".join([f"{reason.replace('_', ' ')} ({count})" for reason, count in top_reasons])

            lines.append(separator)
            lines.append(LEXICON_RU['report_detailed_failed_header'].format(count=len(all_failed),
                                                                            reasons_summary=reason_summary))
            for attempt in all_failed:
                lines.append(ReportFormatter._format_failed_attempt(attempt))

        # Разделяем длинный отчет на несколько сообщений.
        return ReportFormatter._split_report_into_messages(lines)