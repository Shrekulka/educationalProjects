# inter_exchange_arbitrage_bot/src/bot/logic/recon_logic.py

import html
import re
from collections import defaultdict
from datetime import datetime, timezone
from typing import List, Dict, Optional

from src.bot.logic.report_maps import RISK_LEVEL_MAP, RSI_STATUS_MAP, MACD_SIGNAL_MAP
from src.constants.api_constants import BASE_URLS
from src.constants.telegram_constants import TELEGRAM_MESSAGE_MAX_LENGTH
from src.strategies import ArbitrageOpportunity
from src.strategies.enums import RiskLevel
from src.utils import logger
from src.utils.helpers import get_number_emoji


def _safe_html_escape(value, field_name="unknown") -> str:
    """
    Безопасное экранирование HTML с дополнительной защитой от некорректных тегов.
    """
    if value is None:
        return ""

    str_value = str(value)

    # Двойное экранирование для максимальной защиты
    escaped = html.escape(str_value, quote=True)

    # Дополнительная защита от "голых" тегов
    escaped = escaped.replace('<', '&lt;').replace('>', '&gt;')

    # Специальная защита от числовых тегов типа <30
    escaped = re.sub(r'<(\d+)', r'&lt;\1', escaped)

    return escaped


def _validate_html_content(content: str) -> str:
    """
    Финальная проверка HTML-блока на корректность тегов.
    """
    # Поиск подозрительных паттернов вида <число>
    suspicious_pattern = r'<\d+\s*[^>]*(?:>|$)'
    matches = re.findall(suspicious_pattern, content)

    if matches:
        logger.error(f"Обнаружены некорректные HTML-теги: {matches}")
        # Заменяем на безопасные сущности
        content = re.sub(suspicious_pattern, lambda m: html.escape(m.group(0)), content)

    # Изоляция ссылок - добавляем перенос строки после каждой ссылки
    content = re.sub(r'(</a>)(?!\s*\n)', r'\1\n', content)

    return content


def _split_report_into_messages(report_string: str) -> List[str]:
    """Разделяет длинный отчет на несколько сообщений, не разрывая блоки возможностей."""
    messages = []
    current_message = ""
    # Разделяем отчет на логические блоки (шапка, разделы, отдельные возможности)
    blocks = report_string.split('\n\n')

    for block in blocks:
        # Если добавление следующего блока превысит лимит, сохраняем текущее сообщение
        if len(current_message) + len(block) + 2 > TELEGRAM_MESSAGE_MAX_LENGTH:
            if current_message:
                # Добавляем разделитель в конец сообщения для изоляции
                messages.append(current_message.strip() + "\n\n" + "─" * 10)
            current_message = block
        else:
            # Собираем сообщение из блоков
            current_message = (current_message + "\n\n" + block) if current_message else block

    if current_message:
        messages.append(current_message.strip())

    logger.info(f"Итоговый отчет был разделен на {len(messages)} сообщений для отправки.")
    return messages if messages else [""]


def _format_report_header(opportunities: List[ArbitrageOpportunity], scan_duration: float) -> str:
    """Формирует шапку отчета со статистикой."""
    utc_time = datetime.now(timezone.utc).strftime("%H:%M UTC")
    header_lines = [
        f"🛰️ <b>АРБИТРАЖНАЯ РАЗВЕДКА</b> • {utc_time}",
        "",
        "📊 <b>Статистика сканирования:</b>"
    ]
    total_ops = len(opportunities)
    # Считаем только реальные, а не "фантомные" возможности
    real_ops = len([o for o in opportunities if not o.is_phantom])
    header_lines.append(f"├─ 🎯 Проанализировано: {total_ops} связок")
    header_lines.append(f"├─ ⚡ Найдено возможностей: {real_ops}")
    header_lines.append(f"├─ 🕐 Время анализа: {scan_duration:.1f} сек.")

    if real_ops > 0:
        # Находим лучшую возможность среди реальных
        best_opp = max((o for o in opportunities if not o.is_phantom), key=lambda o: o.roi_percent, default=None)
        if best_opp:
            # Используем безопасное экранирование для символа
            header_lines.append(
                f"└─ 🎪 Лучший ROI: {best_opp.roi_percent:.2f}% ({_safe_html_escape(best_opp.symbol, 'header_symbol')})")

    return "\n".join(header_lines)


def _format_market_temperature(report_context: Dict) -> str:
    """Формирует блок рыночной температуры."""
    change_24h = report_context.get('market_cap_change_24h', 0.0)
    status_emoji = "🟢" if change_24h >= 0 else "🔴"
    status_text = "РАСТУЩИЙ РЫНОК" if change_24h >= 0 else "ПАДАЮЩИЙ РЫНОК"
    btc_dominance = report_context.get('btc_dominance', 0.0)

    temp_lines = [
        f"🌡️ <b>Рыночная температура:</b> {status_emoji} {status_text} ({change_24h:+.1f}% за 24ч)",
        f"└─ 🐂 Доминация BTC: {btc_dominance:.1f}%"
    ]
    return "\n".join(temp_lines)


def _format_analytical_summary(opportunities: List[ArbitrageOpportunity], context: Dict) -> str:
    """
    Формирует ДИНАМИЧЕСКИЙ блок с AI-рекомендациями,
    корректным завершением списков и двойными отступами между блоками.
    """
    if not opportunities:
        return ""

    # Фильтруем и сортируем возможности по категориям
    immediate = sorted([o for o in opportunities if o.ai_score >= 8.0 and not o.is_phantom], key=lambda x: x.ai_score,
                       reverse=True)
    watch = sorted([o for o in opportunities if 6.0 <= o.ai_score < 8.0 and not o.is_phantom], key=lambda x: x.ai_score,
                   reverse=True)
    avoid = sorted([o for o in opportunities if o.is_phantom or o.risk_level in [RiskLevel.HIGH, RiskLevel.EXTREME]],
                   key=lambda x: x.roi_percent, reverse=True)

    # --- Собираем основной блок ---
    main_block = ["📊 <b><u><i>АНАЛИТИЧЕСКИЙ БЛОК</i></u></b>",
                  "🎯 <b>БЫСТРЫЕ ДЕЙСТВИЯ (AI Рекомендации)</b>"]

    # --- Создаем каждый под-блок как отдельный список строк ---
    immediate_lines = []
    watch_lines = []
    radar_lines = []
    avoid_lines = []

    # --- Блок "НЕМЕДЛЕННО" ---
    immediate_list = immediate[:2]
    if immediate_list:
        immediate_lines.append("🚀 <b><u><i>НЕМЕДЛЕННО (следующие 15 минут):</i></u></b>")
        for i, opp in enumerate(immediate_list):
            prefix = "└─" if i == len(immediate_list) - 1 else "├─"
            immediate_lines.append(f"{prefix} ✅ {_safe_html_escape(opp.symbol)} - лучшее соотношение риск/доходность")

    # --- Блок "СЕГОДНЯ" ---
    watch_list = watch[:2]
    if watch_list:
        watch_lines.append("⏰ <b><u><i>СЕГОДНЯ (в течение 6 часов):</i></u></b>")
        for i, opp in enumerate(watch_list):
            prefix = "└─" if i == len(watch_list) - 1 else "├─"
            watch_lines.append(f"{prefix} 👁️ {_safe_html_escape(opp.symbol)} - наблюдать, готовиться к входу")

    # --- Блок "НА РАДАРЕ" ---
    radar_lines.append("📈 <b><u><i>НА РАДАРЕ (следующие дни):</i></u></b>")
    btc_dominance_change = context.get('btc_dominance_24h_percentage_change', 0.0)
    top_sectors = context.get('top_sectors')

    line1 = ""
    if btc_dominance_change < -0.2:
        line1 = "├─ 💎 <b>Large-cap альткоины</b> - набирают силу, возможен рост"
    elif btc_dominance_change > 0.2:
        line1 = "├─ 🪙 <b>Bitcoin (BTC)</b> - доминирует на рынке, осторожнее с альтами"
    else:
        line1 = "├─ ⚖️ <b>Рынок в равновесии</b> - следить за доминацией BTC"

    line2 = ""
    if top_sectors:
        line2 = f"└─ 🔥 <b>Горячий сектор:</b> {', '.join(top_sectors)} - много сигналов"
    else:
        line2 = "└─ 🔍 Нет ярко выраженного сектора-лидера"
    radar_lines.extend([line1, line2])

    # --- Блок "ИЗБЕГАТЬ" ---
    avoid_list = avoid[:3]
    if avoid_list:
        avoid_lines.append("❌ <b><u><i>ИЗБЕГАТЬ:</i></u></b>")
        for i, opp in enumerate(avoid_list):
            prefix = "└─" if i == len(avoid_list) - 1 else "├─"
            reason_text = opp.phantom_reason or "Высокий риск"
            avoid_lines.append(f"{prefix} 🚫 {_safe_html_escape(opp.symbol)} - {reason_text}")

    # --- Собираем все блоки вместе с двойными переносами строк ---
    all_blocks = [
        "\n".join(main_block),
        "\n".join(immediate_lines),
        "\n".join(watch_lines),
        "\n".join(radar_lines),
        "\n".join(avoid_lines)
    ]

    # Фильтруем пустые блоки и соединяем их через \n\n
    return "\n\n".join(filter(None, all_blocks))


def _format_risk_and_market_summary(opportunities: List[ArbitrageOpportunity], context: Dict) -> str:
    """Формирует сводку по рыночной ситуации и общему риску."""
    lines = ["", "🌡️ <b><u><i>РЫНОЧНАЯ СИТУАЦИЯ</i></u></b>", "🌊 <b><u><i>Рыночные течения:</i></u></b>"]

    fng_value = context.get('fear_greed_value', 0)
    fng_class = _safe_html_escape(context.get('fear_greed_classification', "Н/Д")).upper()

    lines.append("├─ 📈 <b>Основной тренд:</b> Бычий (среднесрочный)")
    lines.append("├─ 🎢 <b>Волатильность:</b> Умеренная (хорошо для арбитража)")
    lines.append(f"├─ 😱 <b>Fear & Greed:</b> {fng_value} ({fng_class})")

    # Выводим горячие секторы и сюда для наглядности
    top_sectors = context.get('top_sectors')
    if top_sectors:
        lines.append(f"└─ 🔥 <b>Hottest sectors:</b> {', '.join(top_sectors)}")
    else:
        lines.append("└─ 🔥 <b>Hottest sectors:</b> Данные отсутствуют")

    risk_counts = defaultdict(int)
    for opp in opportunities:
        if not opp.is_phantom:
            risk_counts[opp.risk_level] += 1

    lines.extend([
        "", "⚖️ <b><u><i>Риск-профиль дня:</i></u></b>",
        f"├─ 🟢 <b>Низкий риск:</b> {risk_counts[RiskLevel.LOW]} сигнала(ов)",
        f"├─ 🟡 <b>Средний риск:</b> {risk_counts[RiskLevel.MEDIUM]} сигнала(ов)",
        f"├─ 🔴 <b>Высокий риск:</b> {risk_counts[RiskLevel.HIGH]} сигнала(ов)",
        f"└─ ⚫ <b>Экстремальный:</b> {risk_counts[RiskLevel.EXTREME]} сигнала(ов)"
    ])

    recommendation = "<b>НЕЙТРАЛЬНАЯ</b> торговля. Рынок в балансе."
    if fng_value > 70:
        recommendation = "<b>ОСТОРОЖНАЯ</b> торговля. Рынок перегрет, не поддавайтесь жадности."
    elif fng_value < 30:
        recommendation = "<b>УМЕРЕННО АГРЕССИВНАЯ</b> торговля. На страхе рынка можно найти хорошие возможности."

    lines.extend(["", f"🎯 <b><u><i>Общая рекомендация:</i></u></b> \n{recommendation}"])

    return "\n".join(lines)


def _format_exchange_url(exchange_id: str, symbol: str) -> Optional[str]:
    """Безопасно формирует URL для торговой пары на бирже."""
    base_url = BASE_URLS.get(exchange_id)
    if not base_url or '/' not in symbol:
        return None
    try:
        base, quote = symbol.split('/', 1)
        return base_url.format(base=base, quote=quote)
    except (ValueError, KeyError) as e:
        logger.warning(f"Не удалось отформатировать URL для биржи '{exchange_id}' и символа '{symbol}': {e}")
        return None


def _format_opportunity_block(opp: ArbitrageOpportunity, index: int) -> str:
    """
    ✅ ИСПРАВЛЕННАЯ ВЕРСИЯ: Форматирует блок возможности с изолированной ссылкой
    и тотальным экранированием всех динамических данных.
    """
    logger.debug(f"Начинаю форматирование блока для {opp.symbol} [{index}]")
    try:
        emoji_num = get_number_emoji(index + 1)
        risk_color = RISK_LEVEL_MAP.get(opp.risk_level, {}).get("emoji", "⚪️")

        # --- ИСПРАВЛЕНИЕ: Создаем простые названия бирж без HTML-ссылок для маршрута ---
        buy_exchange_simple = _safe_html_escape(opp.buy_exchange_id.capitalize(), 'buy_exchange')
        sell_exchange_simple = _safe_html_escape(opp.sell_exchange_id.capitalize(), 'sell_exchange')

        # Создаем простой заголовок без ссылок
        safe_symbol = f"<b>{_safe_html_escape(opp.symbol, 'symbol')}</b>"
        header = f'{risk_color} {emoji_num} {safe_symbol} │ <b>ROI: {opp.roi_percent:.2f}%</b> │ ⭐ <b>AI Score: {opp.ai_score}/10</b>'
        lines = [header]

        # Добавляем ссылку как отдельный элемент с усиленной изоляцией
        if opp.cmc_slug:
            coin_url = f"{BASE_URLS.get('coinmarketcap', '')}{opp.cmc_slug}/"
            lines.append(f"   ├─ 🔗 <b>Подробнее:</b> <a href='{coin_url}'>На CoinMarketCap</a>")

        # ✅ ГЛАВНОЕ ИСПРАВЛЕНИЕ: Маршрут БЕЗ HTML-ссылок на одной строке
        lines.append(f"   ├─ 🔄 <b>Маршрут:</b> {buy_exchange_simple} ➔ {sell_exchange_simple}")
        lines.append(
            f"   ├─ 💹 <b>Цены:</b> Купить по ~${opp.effective_buy_price:,.4f}, Продать по ~${opp.effective_sell_price:,.4f}")
        lines.append(
            f"   ├─ 💰 <b>Потенциал:</b> Объем до <b>${opp.max_volume_usd:,.0f}</b> ➔ Профит <b>~${opp.potential_profit_usd:,.0f}</b>")

        price_change_str = f"+{opp.market_data.price_24h_change:.1f}% 📈" if opp.market_data.price_24h_change >= 0 else f"{opp.market_data.price_24h_change:.1f}% 📉"
        lines.append(f"   ├─ 📊 <b>Рынок:</b> ${opp.market_data.price:,.4f} │ <b>24ч:</b> {price_change_str}")

        if opp.market_data.market_cap_usd > 0:
            lines.append(
                f"   ├─ 🏢 <b>Размер:</b> MCap: ${opp.market_data.market_cap_usd:,.0f} │ Листинги: {opp.market_data.listings_count}+ бирж")

        if opp.tags:
            tags_text = ', '.join([t.capitalize() for t in opp.tags[:3]])
            lines.append(f"   ├─ 🏷️ <b>Категория:</b> {_safe_html_escape(tags_text, 'tags')}")

        if opp.technical_analysis.rsi_14 > 0:
            rsi_info = RSI_STATUS_MAP.get(opp.technical_analysis.rsi_status, {}).get("full", "Н/Д")
            macd_arrow = MACD_SIGNAL_MAP.get(opp.technical_analysis.macd_signal, {}).get("arrow", "➡️")
            macd_text = MACD_SIGNAL_MAP.get(opp.technical_analysis.macd_signal, {}).get("text", "Н/Д")
            lines.append(
                f"   ├─ 🎯 <b>Тех. анализ:</b> RSI({int(opp.technical_analysis.rsi_14)},{_safe_html_escape(rsi_info, 'rsi')}) │ MACD({macd_arrow}{_safe_html_escape(macd_text, 'macd')})")

        safe_sparkline = _safe_html_escape(opp.technical_analysis.price_trend_sparkline, f"sparkline[{index}]")
        if safe_sparkline:
            lines.append(f"   ├─ 📈 <b>Тренд (8ч):</b> {safe_sparkline}")

        if opp.market_data.volume_24h_usd > 0:
            vol_spike_str = f"│ Всплеск: ✅<b>+{int((opp.technical_analysis.volume_spike_ratio - 1) * 100)}%</b>🔥" if opp.technical_analysis.volume_spike_ratio > 1.5 else ""
            lines.append(f"   ├─ 🌊 <b>Объем (24ч):</b> ${opp.market_data.volume_24h_usd:,.0f} {vol_spike_str}")

        if opp.is_trending:
            lines.append("   ├─ 📱 <b>Социум:</b> 🔥 <b>В ТРЕНДАХ CoinMarketCap!</b>")

        last_line_prefix = "   └─"
        if opp.is_phantom and opp.phantom_reason:
            reason_text = opp.phantom_reason or "Неизвестная аномалия"
            lines.append(f"{last_line_prefix} 🚨 <b>Предупреждение:</b> {reason_text}")
        elif opp.action_recommendation:
            lines.append(
                f"{last_line_prefix} 💡 <b>Рекомендация:</b> {_safe_html_escape(opp.action_recommendation, 'action_recommendation')}")

        final_block = "\n".join(lines)
        return _validate_html_content(final_block)

    except Exception as e:
        logger.error(f"Ошибка форматирования блока для {opp.symbol}: {e}", exc_info=True)
        return f"⚠️ Ошибка форматирования для {_safe_html_escape(opp.symbol, 'error_symbol')}"

# inter_exchange_arbitrage_bot/src/bot/logic/recon_logic.py

def get_glossary() -> str:
    """
    ✅ ФИНАЛЬНАЯ ВЕРСИЯ: Возвращает полный, красивый и HTML-безопасный глоссарий.
    """
    return """
💡 <b>Глоссарий и расшифровка терминов отчета</b>

<i>Здесь объясняется каждое поле, которое вы видите в карточке арбитражной связки.</i>

────────────────────

📋 <b><u>ОСНОВНЫЕ МЕТРИКИ</u></b>

🔹 <b>ROI (Return On Investment):</b>
Чистый процент прибыли от сделки <u>после</u> вычета всех комиссий бирж. Это главный показатель эффективности связки.

🔹 <b>AI Score (Оценка ИИ):</b>
Комплексная оценка качества сигнала от 1 до 10. Учитывает более 15 факторов: риск, ликвидность, теханализ, волатильность и другие.
    • <code>8.0 - 10</code>: 🔥 Очень высокий, надежный сигнал.
    • <code>6.0 - 7.9</code>: 🟡 Хороший сигнал, стоит наблюдать.
    • <code>&lt; 6.0</code>: ❄️ Низкий, требует тщательного анализа.

🗺️ <b><u>ДЕТАЛИ СДЕЛКИ</u></b>

🔹 <b>Подробнее:</b>
Прямая ссылка на страницу монеты на <b>CoinMarketCap</b>. Позволяет быстро изучить детальные графики, новости и официальные ссылки на проект.

🔹 <b>Маршрут:</b>
<u>Направление сделки.</u> Показывает, на какой бирже нужно <b>купить</b> (первая) и сразу же <b>продать</b> (вторая) актив для получения прибыли.

🔹 <b>Цены:</b>
Это не просто лучшая цена, а <u>эффективная средняя цена</u> исполнения ордера на весь объем с учетом глубины стакана (проскальзывания).

🔹 <b>Потенциал:</b>
    • <code>Объем до $...</code>: Максимальная сумма в USD, на которую можно войти в сделку с учетом ликвидности в стаканах обеих бирж.
    • <code>Профит ~$...</code>: Примерная чистая прибыль в USD при сделке на максимальный объем.

📈 <b><u>РЫНОЧНЫЕ ДАННЫЕ</u></b>

🔹 <b>Рынок:</b>
<u>Общие данные по монете.</u> 
    • Первая цифра (<code>$0.6964</code>) — это средняя цена на всех биржах (для контекста).
    • Вторая часть (<code>-5.0% 📉</code>) — её процентное изменение за последние 24 часа.

🔹 <b>Размер:</b>
    • <code>MCap</code>: Общая рыночная капитализация монеты. Показывает "вес" и стабильность актива на рынке.
    • <code>Листинги</code>: Приблизительное количество бирж, где торгуется монета. Большое число говорит о популярности и доступности.

🔹 <b>Категория:</b>
<u>Сектор и особенности актива.</u> Теги, которые описывают суть проекта и помогают быстро понять, с чем вы имеете дело.
    • <i>Например:</i> <code>Layer-2, Gaming, DeFi</code> говорят о сфере деятельности монеты.
    • <i>Например:</i> <code>Binance-labs-portfolio</code> указывает на то, какие крупные фонды вложились в проект.

⚙️ <b><u>ТЕХНИЧЕСКИЙ АНАЛИЗ</u></b>

🔹 <b>RSI (Индекс относительной силы):</b>
Индикатор импульса, показывающий перекупленность или перепроданность актива.
    • <code>&lt;30 (🧊)</code>: <b>Перепроданность.</b> Цена слишком сильно упала, возможен скорый отскок вверх.
    • <code>&gt;70 (🔥)</code>: <b>Перекупленность.</b> Цена слишком сильно выросла, возможна скорая коррекция вниз.

🔹 <b>MACD (Схождение/расхождение скользящих средних):</b>
Индикатор, показывающий направление и силу текущего тренда.
    • <code>↗️ Бычий</code>: Тренд на повышение.
    • <code>↘️ Медвежий</code>: Тренд на понижение.

🔹 <b>Тренд (8ч):</b>
Мини-график, визуально отображающий динамику цены за последние 8 часов. Позволяет быстро оценить текущий импульс.

🔹 <b>Объем (24ч) и Всплеск:</b>
    • <code>Объем</code>: Общая сумма сделок с активом за сутки (как на CMC).
    • <code>Всплеск 🔥</code>: <b><u>Ключевой индикатор!</u></b> Показывает, на сколько % объем торгов за <b>последний час</b> был выше <b>среднего часового</b> объема за сутки. Значение +132% означает резкий, аномальный интерес к монете прямо сейчас.

📱 <b><u>СОЦИАЛЬНЫЙ ФОН</u></b>

🔹 <b>Социум:</b>
Показывает, если монета находится в "трендах" на крупных платформах (например, <code>🔥 В ТРЕНДАХ CoinMarketCap!</code>). Говорит о высоком интересе со стороны сообщества, что может привести к волатильности.

🤖 <b><u>ИТОГОВЫЙ ВЕРДИКТ</u></b>

🔹 <b>Рекомендация / Предупреждение:</b>
Прямой вывод бота на основе всех собранных данных.
    • <code>✅ ИСПОЛНЯТЬ</code>: Сигнал высокого качества, можно входить в сделку.
    • <code>🎯 РАССМОТРЕТЬ</code>: Сигнал хороший, но требует дополнительного внимания к рынку.
    • <code>🚨 Предупреждение</code>: Сделка не рекомендуется из-за высокого риска, аномального ROI или низкой прибыли.
"""

# def get_glossary() -> str:
#     """Возвращает текстовый блок с глоссарием."""
#     return """
# 💡 <b>Глоссарий и расшифровка терминов:</b>
#
# - <b>ROI:</b> Чистая доходность арбитражной связки в % после комиссий.
# - <b>AI Score:</b> Комплексная оценка качества сигнала от 1 до 10.
# - <b>MCap:</b> Рыночная капитализация. Показывает общий размер актива.
# - <b>Листинги:</b> Приблизительное количество бирж, где торгуется монета.
# - <b>RSI:</b> Индикатор силы тренда. &lt;30 (🧊) - перепроданность, &gt;70 (🔥) - перекупленность.
# - <b>MACD:</b> Индикатор направления и силы тренда. ↗️ - бычий, ↘️ - медвежий.
# - <b>Тренд(8ч):</b> Визуальное отображение динамики цены за последние 8 часов.
# - <b>Всплеск объема:</b> На сколько текущий часовой объем превышает средний.
# """


def format_reconnaissance_report(opportunities: List[ArbitrageOpportunity], scan_duration: float,
                                 report_context: Dict) -> List[str]:
    """
    ✅ ОБНОВЛЕННАЯ ВЕРСИЯ: Основная функция, которая собирает отчет из всех блоков, включая аналитический.
    """
    if not opportunities:
        return ["🛰️ Результаты рыночной разведки 🛰️\n\n❌ Связок не найдено."]

    try:
        # Категоризация для детальных блоков
        immediate = sorted([o for o in opportunities if o.ai_score >= 8.0 and not o.is_phantom],
                           key=lambda x: x.ai_score, reverse=True)
        watch = sorted([o for o in opportunities if 6.0 <= o.ai_score < 8.0 and not o.is_phantom],
                       key=lambda x: x.ai_score, reverse=True)
        phantoms = sorted([o for o in opportunities if o.is_phantom], key=lambda x: x.roi_percent, reverse=True)

        report_parts = [
            _format_report_header(opportunities, scan_duration),
            _format_market_temperature(report_context)
        ]
        separator = "─" * 20

        # Добавляем детальные блоки с возможностями
        if immediate:
            report_parts.append(separator)
            report_parts.append("🎯 <b>РАЗДЕЛ 1: ГОТОВЫЕ АРБИТРАЖНЫЕ СВЯЗКИ</b>\n"
                                "<i>(Высокая оценка AI, низкий риск, готовы к исполнению)</i>")
            for i, opp in enumerate(immediate):
                report_parts.append(_format_opportunity_block(opp, i))

        if watch:
            report_parts.append(separator)
            report_parts.append("👀 <b>РАЗДЕЛ 2: СВЯЗКИ ДЛЯ НАБЛЮДЕНИЯ</b>\n"
                                "<i>(Хороший потенциал, но требуют внимания к рыночным условиям)</i>")
            for i, opp in enumerate(watch):
                report_parts.append(_format_opportunity_block(opp, i))

        if phantoms:
            report_parts.append(separator)
            report_parts.append("👻 <b>РАЗДЕЛ 3: АНОМАЛЬНЫЕ СИГНАЛЫ</b>\n"
                                "<i>(Подозрительные связки, требующие тщательной проверки)</i>")
            for i, opp in enumerate(phantoms):
                report_parts.append(_format_opportunity_block(opp, i))

        # ✅ ИНТЕГРАЦИЯ: Добавляем аналитические блоки в конец отчета
        report_parts.append(separator)
        report_parts.append(_format_analytical_summary(opportunities, report_context))
        report_parts.append(_format_risk_and_market_summary(opportunities, report_context))

        report_parts.append(separator)
        report_parts.append(get_glossary())

        full_report_string = "\n\n".join(report_parts)

        # Валидация перед отправкой:
        full_report_string = _validate_html_content(full_report_string)

        return _split_report_into_messages(full_report_string)

    except Exception as e:
        logger.error(f"Критическая ошибка форматирования отчета: {e}", exc_info=True)
        return ["❌ Ошибка генерации отчета"]
