# inter_exchange_arbitrage_bot/src/bot/logic/admin_logic.py

from typing import Dict, Any

from src.constants.telegram_constants import CACHE_STATS_PREVIEW_LIMIT
from src.lexicon import LEXICON_RU


def format_cache_stats_report(stats: Dict[str, Any]) -> str:
    """
    Формирует текстовый отчет по статистике кэша торговых пар.

    Args:
        stats: Словарь со статистикой, полученный от API.

    Returns:
        Готовая к отправке строка с HTML-форматированием.
    """
    report_lines = [LEXICON_RU['cache_stats_header']]

    for exchange, data in stats.items():
        report_lines.append(LEXICON_RU['admin_report_exchange_header'].format(exchange=exchange.capitalize()))
        report_lines.append(LEXICON_RU['admin_report_active_line'].format(count=data.get('active_pairs', 0)))

        temp_list = data.get('temp_unavailable_list', [])
        report_lines.append(LEXICON_RU['admin_report_temp_unavailable_line'].format(count=len(temp_list)))
        if temp_list:
            preview_limit = CACHE_STATS_PREVIEW_LIMIT
            pairs_to_show = ", ".join([f"<code>{p}</code>" for p in temp_list[:preview_limit]])
            preview_line = f"{pairs_to_show}{'...' if len(temp_list) > preview_limit else ''}"
            report_lines.append(LEXICON_RU['admin_report_pairs_preview_line'].format(pairs_preview=preview_line))

        excluded_list = data.get('admin_excluded_list', [])
        report_lines.append(LEXICON_RU['admin_report_admin_excluded_line'].format(count=len(excluded_list)))
        if excluded_list:
            preview_limit = CACHE_STATS_PREVIEW_LIMIT
            pairs_to_show = ", ".join([f"<code>{p}</code>" for p in excluded_list[:preview_limit]])
            preview_line = f"{pairs_to_show}{'...' if len(excluded_list) > preview_limit else ''}"
            report_lines.append(LEXICON_RU['admin_report_pairs_preview_line'].format(pairs_preview=preview_line))

    return "\n".join(report_lines)
