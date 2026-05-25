# inter_exchange_arbitrage_bot/src/bot/logic/density_logic.py

import asyncio
import os
from collections import defaultdict
from typing import List

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from src.bot.keyboards.density_screener_keyboards import get_density_screener_menu_keyboard
from src.bot.logic.report_maps import DENSITY_ACTION_MAP
from src.constants.telegram_constants import TELEGRAM_CAPTION_MAX_LENGTH, TELEGRAM_MESSAGE_MAX_LENGTH
from src.core import state as app_state
from src.lexicon.lexicon_ru import LEXICON_RU
from src.models.screener_models import Density
from src.services.density_chart_service import DensityChartService
from src.strategies.enums import DensityAction
from src.utils.chat_actions import safe_edit_text
from src.utils.helpers import split_long_message, build_caption_and_remainder
from src.utils.logger import logger


async def show_density_screener_menu(message: Message, state: FSMContext):
    await state.clear()
    await safe_edit_text(
        message=message,
        text=LEXICON_RU['density_screener_menu_text'],
        reply_markup=get_density_screener_menu_keyboard()
    )


async def start_density_scan(message: Message, symbols_to_scan: List[str]):
    status_message = await message.answer(
        text=f"⏳ <b>Запускаю сканирование...</b>\nАнализирую <b>{len(symbols_to_scan)}</b> активов.")
    asyncio.create_task(run_density_scan_task(chat_id=message.chat.id, message_id=status_message.message_id,
                                              symbols_to_scan=symbols_to_scan))


def _format_price(price: float) -> str:
    return f"${price:,.4f}" if price < 1.0 else f"${price:,.2f}"


def generate_report_lines(symbol: str, densities: List[Density]) -> List[str]:
    """
    ✅ НОВАЯ ВЕРСИЯ: Генерирует отчет в виде списка строк.
    """
    lines = []
    lines.append(f"📈 <b>{symbol} - Анализ плотностей</b>")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━")

    stats_service = DensityChartService()
    stats = stats_service.get_stats(densities)
    action_info = DENSITY_ACTION_MAP.get(stats['action'], DENSITY_ACTION_MAP[DensityAction.NEUTRAL])

    lines.append(f"\n📊 <b>ОБЩАЯ СТАТИСТИКА:</b>")
    lines.append(f"┌ 💰 Общий объем: <code>${stats.get('total_volume_k', 0):,.0f}k</code>")
    lines.append(f"├ 🏦 Количество бирж: <code>{stats.get('exchanges_count', 0)}</code>")
    lines.append(
        f"├ 🟢 Поддержка: <code>${stats.get('support_k', 0):,.0f}k</code> (<code>{stats.get('support_count', 0)} ур.</code>)")
    lines.append(
        f"└ 🔴 Сопротивление: <code>${stats.get('resistance_k', 0):,.0f}k</code> (<code>{stats.get('resistance_count', 0)} ур.</code>)")

    lines.append(f"\n🎯 <b>РЕКОМЕНДАЦИЯ:</b>")
    lines.append(f"┌ {action_info['emoji']} <b>{action_info['text']}</b>")
    lines.append(f"└ <i>{action_info['description']}</i>")

    lines.append(f"\n📋 <b>ДЕТАЛИЗАЦИЯ ПО БИРЖАМ:</b>")

    grouped_by_exchange = defaultdict(list)
    for d in densities:
        grouped_by_exchange[d.exchange].append(d)

    sorted_exchanges = sorted(grouped_by_exchange.items(),
                              key=lambda x: sum(density_item.volume_usd for density_item in x[1]), reverse=True)

    for i, (exchange, dens) in enumerate(sorted_exchanges):
        exchange_total = sum(d.volume_usd for d in dens) / 1000
        is_last_exchange = (i == len(sorted_exchanges) - 1)
        lines.append(
            f"\n{'└' if is_last_exchange else '├'} 🏛️ <b>{exchange.upper()}</b> <code>(${exchange_total:,.0f}k)</code>")

        resistances = sorted([d for d in dens if d.density_type == 'resistance'],
                             key=lambda x: x.volume_usd, reverse=True)
        supports = sorted([d for d in dens if d.density_type == 'support'],
                          key=lambda x: x.volume_usd, reverse=True)

        prefix = "  " if is_last_exchange else "│ "

        if resistances and supports:
            # Сценарий 1: Есть и то, и другое
            lines.append(f"{prefix}┌ 🔴 <b>Сопротивления:</b>")
            for j, r in enumerate(resistances):
                lines.append(
                    f"{prefix}│ ├ <code>{_format_price(r.price)}</code> → <code>${r.volume_usd / 1000:.0f}k</code>")

            lines.append(f"{prefix}└ 🟢 <b>Поддержки:</b>")
            prefix_nested = "  " if is_last_exchange else "│ "
            for j, s in enumerate(supports):
                connector = "└" if j == len(supports) - 1 else "├"
                lines.append(
                    f"{prefix_nested}  {connector} <code>{_format_price(s.price)}</code> → <code>${s.volume_usd / 1000:.0f}k</code>")

        elif resistances:
            # Сценарий 2: Есть только сопротивления
            lines.append(f"{prefix}┌ 🔴 <b>Сопротивления:</b>")
            for j, r in enumerate(resistances):
                connector = "└" if j == len(resistances) - 1 else "├"
                lines.append(
                    f"{prefix}│ {connector} <code>{_format_price(r.price)}</code> → <code>${r.volume_usd / 1000:.0f}k</code>")
            lines.append(f"{prefix}└ 🟢 <b>Поддержки:</b> <i>нет</i>")

        elif supports:
            # Сценарий 3: Есть только поддержки
            lines.append(f"{prefix}┌ 🔴 <b>Сопротивления:</b> <i>нет</i>")
            lines.append(f"{prefix}└ 🟢 <b>Поддержки:</b>")
            prefix_nested = "  " if is_last_exchange else "│ "
            for j, s in enumerate(supports):
                connector = "└" if j == len(supports) - 1 else "├"
                lines.append(
                    f"{prefix_nested}  {connector} <code>{_format_price(s.price)}</code> → <code>${s.volume_usd / 1000:.0f}k</code>")
    return lines


# def format_full_report_caption(symbol: str, densities: List[Density]) -> str:
#     """
#     ✅ УЛУЧШЕННАЯ ВЕРСИЯ: Создает красивый структурированный текстовый отчет.
#     """
#     lines = []
#     lines.append(f"📈 <b>{symbol} - Анализ плотностей</b>")
#     lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━")
#
#     stats_service = DensityChartService()
#     stats = stats_service.get_stats(densities)
#
#     action_info = DENSITY_ACTION_MAP.get(stats['action'], DENSITY_ACTION_MAP[DensityAction.NEUTRAL])
#
#     lines.append(f"\n📊 <b>ОБЩАЯ СТАТИСТИКА:</b>")
#     lines.append(f"┌ 💰 Общий объем: <code>${stats.get('total_volume_k', 0):,.0f}k</code>")
#     lines.append(f"├ 🏦 Количество бирж: <code>{stats.get('exchanges_count', 0)}</code>")
#     lines.append(
#         f"├ 🟢 Поддержка: <code>${stats.get('support_k', 0):,.0f}k</code> (<code>{stats.get('support_count', 0)} ур.</code>)")
#     lines.append(
#         f"└ 🔴 Сопротивление: <code>${stats.get('resistance_k', 0):,.0f}k</code> (<code>{stats.get('resistance_count', 0)} ур.</code>)")
#
#     lines.append(f"\n🎯 <b>РЕКОМЕНДАЦИЯ:</b>")
#     lines.append(f"┌ {action_info['emoji']} <b>{action_info['text']}</b>")
#     lines.append(f"└ <i>{action_info['description']}</i>")
#
#     lines.append(f"\n📋 <b>ДЕТАЛИЗАЦИЯ ПО БИРЖАМ:</b>")
#     grouped_by_exchange = defaultdict(list)
#     for d in densities:
#         grouped_by_exchange[d.exchange].append(d)
#
#     # Сортируем биржи по общему объему (убывание)
#     sorted_exchanges = sorted(grouped_by_exchange.items(),
#                               key=lambda x: sum(density_item.volume_usd for density_item in x[1]), reverse=True)
#
#     for i, (exchange, dens) in enumerate(sorted_exchanges):
#         exchange_total = sum(d.volume_usd for d in dens) / 1000
#         is_last_exchange = (i == len(sorted_exchanges) - 1)
#
#         # Заголовок биржи с рамкой
#         lines.append(
#             f"\n{'└' if is_last_exchange else '├'} 🏛️ <b>{exchange.upper()}</b> <code>(${exchange_total:,.0f}k)</code>")
#
#         # Группируем по типам
#         resistances = sorted([d for d in dens if d.density_type == 'resistance'],
#                              key=lambda x: x.volume_usd, reverse=True)
#         supports = sorted([d for d in dens if d.density_type == 'support'],
#                           key=lambda x: x.volume_usd, reverse=True)
#
#         prefix = "  " if is_last_exchange else "│ "
#
#         # Сопротивления
#         if resistances:
#             lines.append(f"{prefix}┌ 🔴 <b>Сопротивления:</b>")
#             for j, resistance in enumerate(resistances):
#                 price_str = _format_price(resistance.price)
#                 volume_str = f"${resistance.volume_usd / 1000:.0f}k"
#                 is_last_resistance = (j == len(resistances) - 1) and not supports
#                 connector = "└" if is_last_resistance else "├"
#                 lines.append(f"{prefix}│ {connector} <code>{price_str}</code> → <code>{volume_str}</code>")
#
#         # Поддержки
#         if supports:
#             lines.append(f"{prefix}└ 🟢 <b>Поддержки:</b>")
#             for j, support in enumerate(supports):
#                 price_str = _format_price(support.price)
#                 volume_str = f"${support.volume_usd / 1000:.0f}k"
#                 is_last_support = (j == len(supports) - 1)
#                 connector = "└" if is_last_support else "├"
#                 lines.append(f"{prefix}  {connector} <code>{price_str}</code> → <code>{volume_str}</code>")
#
#     full_text = "\n".join(lines)
#
#     if len(full_text) > TELEGRAM_MESSAGE_MAX_LENGTH:
#         # Динамически вычисляем точку среза, чтобы итоговое сообщение
#         # вместе с суффиксом не превысило лимит.
#         cutoff_point = TELEGRAM_MESSAGE_MAX_LENGTH - len(TRUNCATION_SUFFIX)
#         return full_text[:cutoff_point] + TRUNCATION_SUFFIX
#     else:
#         return full_text


def _format_final_summary(
        symbols_to_scan: List[str],
        found_symbols: List[str],
        skipped_symbols: List[str],
        scan_highlights: List[tuple]) -> str:
    """
    Формирует красивый и информативный итоговый отчет о сканировании.
    """
    lines = [
        "🛡️ <b>Отчет Скринера Плотности</b> 🛡️",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"  • Всего в задании: <b>{len(symbols_to_scan)}</b> активов",
        f"  • Найдено с плотностями: <b>{len(found_symbols)}</b> ✅",
        f"  • Пропущено (нет плотностей): <b>{len(skipped_symbols)}</b> ℹ️"
    ]

    if scan_highlights:
        lines.append("\n🔥 <b>Ключевые Находки:</b>")
        scan_highlights.sort(key=lambda x: x[0], reverse=True)
        emojis = ["🥇", "🥈", "🥉"]
        for i, (total_volume, count, symbol) in enumerate(scan_highlights[:3]):
            emoji = emojis[i] if i < len(emojis) else "🔹"
            lines.append(f"{emoji} <code>{symbol}</code>: Объем <b>${total_volume / 1000:,.0f}k</b> ({count} ур.)")

    if skipped_symbols:
        lines.append("\n📋 <b>Пропущенные Активы:</b>")
        skipped_display = [f"<code>{s.split('/')[0]}</code>" for s in skipped_symbols[:10]]
        line = ", ".join(skipped_display)
        if len(skipped_symbols) > 10:
            line += f", и еще {len(skipped_symbols) - 10}..."
        lines.append(line)

    lines.append("\n💡 <b>Что дальше?</b>")
    lines.append("<i>Проанализируйте графики ключевых находок или запустите новый скан!</i>")

    return "\n".join(lines)


async def run_density_scan_task(chat_id: int, message_id: int, symbols_to_scan: List[str]):
    sent_items_count = 0
    found_symbols = []
    skipped_symbols = []
    scan_highlights = []
    try:
        density_screener = app_state.density_screener_service
        chart_service = app_state.density_chart_service

        if not density_screener or not chart_service:
            raise ValueError("Один из сервисов (Screener или Chart) не был инициализирован.")

        await app_state.bot_instance.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text=f"🔍 <b>Сканирование запущено</b>...")

        density_results = await density_screener.scan_for_densities(symbols_to_scan)

        try:
            await app_state.bot_instance.delete_message(chat_id, message_id)
        except TelegramBadRequest as e:
            logger.debug(f"Не удалось удалить сообщение {message_id}: {e}")
        except Exception:
            logger.warning(f"Неожиданная ошибка при удалении сообщения {message_id}", exc_info=True)

        await app_state.bot_instance.send_message(
            chat_id=chat_id,
            text=f"✅ <b>Анализ завершен!</b> Найдено плотностей для <b>{len(density_results)} из {len(symbols_to_scan)}</b> активов. Формирую отчеты...")

        for symbol in symbols_to_scan:
            data = density_results.get(symbol)
            if data:
                found_symbols.append(symbol)
                densities = data.get('densities', [])
                total_volume = sum(d.volume_usd for d in densities)
                scan_highlights.append((total_volume, len(densities), symbol))
                try:
                    logger.info(f"[{symbol}] НАЧАЛО ОБРАБОТКИ. Плотности: {len(data.get('densities', []))}.")

                    image_path = chart_service.create_multi_block_image(
                        symbol, data['densities'], data['mid_price'])

                    report_lines = generate_report_lines(symbol, data['densities'])
                    full_text = "\n".join(report_lines)

                    if image_path:
                        photo = FSInputFile(image_path)
                        if len(full_text) <= TELEGRAM_CAPTION_MAX_LENGTH:
                            await app_state.bot_instance.send_photo(
                                chat_id=chat_id, photo=photo, caption=full_text)
                        else:
                            logger.warning(
                                f"Подпись для {symbol} слишком длинная ({len(full_text)}). Разбиваю на части.")

                            # Используем новую безопасную функцию
                            caption_part, remainder_text = build_caption_and_remainder(report_lines,
                                                                                       TELEGRAM_CAPTION_MAX_LENGTH)

                            await app_state.bot_instance.send_photo(
                                chat_id=chat_id, photo=photo, caption=caption_part)

                            if remainder_text:
                                text_chunks = split_long_message(remainder_text, TELEGRAM_MESSAGE_MAX_LENGTH)
                                for chunk in text_chunks:
                                    await app_state.bot_instance.send_message(chat_id=chat_id, text=chunk)
                                    await asyncio.sleep(0.3)
                        if os.path.exists(image_path):
                            os.remove(image_path)
                    else:
                        text_chunks = split_long_message(full_text, TELEGRAM_MESSAGE_MAX_LENGTH)
                        for chunk in text_chunks:
                            await app_state.bot_instance.send_message(chat_id=chat_id, text=chunk)
                            await asyncio.sleep(0.3)
                    sent_items_count += 1
                except TelegramBadRequest:
                    logger.critical(f"[{symbol}] НЕУДАЧА! Ошибка API Telegram при отправке отчета.", exc_info=True)
                    await app_state.bot_instance.send_message(
                        chat_id=chat_id,
                        text=f"❗️ Произошла ошибка API при отправке отчета по <b>{symbol}</b>. Возможно, неверный формат.")
                except Exception:
                    logger.critical(f"[{symbol}] НЕУДАЧА! Ошибка при обработке актива.", exc_info=True)
                    await app_state.bot_instance.send_message(
                        chat_id=chat_id,
                        text=f"❗️ Произошла ошибка при обработке <b>{symbol}</b>.")
            else:
                skipped_symbols.append(symbol)
                logger.info(f"[{symbol}] Данные отсутствуют в результатах, отправляю уведомление о пропуске.")
                await app_state.bot_instance.send_message(
                    chat_id=chat_id,
                    text=f"ℹ️ Для <b>{symbol}</b> не найдено плотностей, соответствующих вашим критериям.")
                sent_items_count += 1
            await asyncio.sleep(0.5)
    except Exception:
        logger.critical(f"Критическая ошибка в главном цикле сканирования!", exc_info=True)
    finally:
        final_summary = _format_final_summary(
            symbols_to_scan=symbols_to_scan,
            found_symbols=found_symbols,
            skipped_symbols=skipped_symbols,
            scan_highlights=scan_highlights
        )
        await app_state.bot_instance.send_message(
            chat_id=chat_id, text=final_summary,
            reply_markup=get_density_screener_menu_keyboard())

# # inter_exchange_arbitrage_bot/src/bot/logic/density_logic.py
#
# import asyncio
# import os
# from collections import defaultdict
# from typing import List
#
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, FSInputFile
#
# from src.bot.keyboards import get_main_menu_inline_keyboard
# from src.bot.keyboards.density_screener_keyboards import get_density_screener_menu_keyboard
# from src.core import state as app_state
# from src.models.screener_models import Density
# from src.services.density_chart_service import DensityChartService  # Важно - импорт остается
# from src.utils import logger
# from src.utils.chat_actions import safe_edit_text
# from src.constants.trading_constants import DENSITY_CHART_CONFIG
#
#
# async def show_density_screener_menu(message: Message, state: FSMContext):
#     """Отображает главное меню скринера плотностей."""
#     await state.clear()
#     await safe_edit_text(
#         message=message,
#         text="🛡️ <b>Скринер плотностей</b>\n\nВыберите, какие активы вы хотите просканировать:",
#         reply_markup=get_density_screener_menu_keyboard()
#     )
#
#
# async def start_density_scan(message: Message, symbols_to_scan: List[str]):
#     """Запускает фоновую задачу сканирования."""
#     status_message = await message.answer(
#         text=f"⏳ <b>Запускаю сканирование...</b>\nАнализирую <b>{len(symbols_to_scan)}</b> активов.",
#     )
#     asyncio.create_task(run_density_scan_task(
#         chat_id=message.chat.id,
#         message_id=status_message.message_id,
#         symbols_to_scan=symbols_to_scan
#     ))
#
#
# def format_text_schema(symbol: str, densities: List[Density], mid_price: float) -> str:
#     """
#     ✅ НОВАЯ ФУНКЦИЯ: Генерирует красивый и читаемый ТЕКСТОВЫЙ отчет для >10 уровней.
#     """
#     lines = []
#     lines.append(f"📊 <b>{symbol} — Схема уровней</b>\n<i>(>10 уровней, показан текст)</i>\n")
#
#     # --- Статистика ---
#     stats_service = DensityChartService()  # Используем хелпер из сервиса
#     stats = stats_service._get_stats(densities)
#     lines.append("<b><u>Статистика:</u></b>")
#     lines.append(f"  - <b>Объем:</b> ${stats['total_volume_k']:,.0f}k на {stats['exchanges_count']} биржах")
#     lines.append(f"  - 🟢 <b>Поддержка:</b> ${stats['support_k']:,.0f}k ({stats['support_count']} ур.)")
#     lines.append(f"  - 🔴 <b>Сопротивление:</b> ${stats['resistance_k']:,.0f}k ({stats['resistance_count']} ур.)")
#     lines.append(f"  - <b>Баланс:</b> {stats['balance']}\n")
#
#     # --- Разбивка по биржам ---
#     lines.append("<b><u>Подробная разбивка:</u></b>")
#
#     grouped_by_exchange = defaultdict(list)
#     for d in densities: grouped_by_exchange[d.exchange].append(d)
#     sorted_exchanges = sorted(grouped_by_exchange.items(), key=lambda x: sum(d.volume_usd for d in x[1]), reverse=True)
#
#     for exchange, dens in sorted_exchanges:
#         exchange_total = sum(d.volume_usd for d in dens) / 1000
#         lines.append(f"\n<b>{exchange.upper()} (${exchange_total:,.0f}k):</b>")
#
#         resistances = sorted([d for d in dens if d.density_type == 'resistance'], key=lambda x: x.volume_usd,
#                              reverse=True)[:3]
#         supports = sorted([d for d in dens if d.density_type == 'support'], key=lambda x: x.volume_usd, reverse=True)[
#                    :3]
#
#         if resistances:
#             res_text = ", ".join([f"${d.price:,.4f}→${d.volume_usd / 1000:.0f}k" for d in resistances])
#             lines.append(f"  🔴 {res_text}")
#         if supports:
#             sup_text = ", ".join([f"${d.price:,.4f}→${d.volume_usd / 1000:.0f}k" for d in supports])
#             lines.append(f"  🟢 {sup_text}")
#
#     return "\n".join(lines)
#
#
# async def run_density_scan_task(chat_id: int, message_id: int, symbols_to_scan: List[str]):
#     sent_items_count = 0
#     total_found = 0
#     try:
#         # --- 1. Подготовка и сканирование (без изменений) ---
#         if not app_state.density_screener_service: raise ValueError("Сервис не инициализирован.")
#         await app_state.bot_instance.edit_message_text(chat_id=chat_id, message_id=message_id,
#                                                        text=f"🔍 <b>Сканирование запущено</b>...")
#         density_results = await app_state.density_screener_service.scan_for_densities(symbols_to_scan)
#         try:
#             await app_state.bot_instance.delete_message(chat_id, message_id)
#         except:
#             pass
#         if not density_results:
#             await app_state.bot_instance.send_message(chat_id=chat_id,
#                                                       text="🛡️ <b>Сканирование завершено.</b> Значимых плотностей не найдено.",
#                                                       reply_markup=get_main_menu_inline_keyboard())
#             return
#
#         # --- 2. Сортировка и обработка ---
#         chart_service = DensityChartService()
#         sorted_results = sorted(density_results.items(),
#                                 key=lambda item: sum(d.volume_usd for d in item[1]['densities']), reverse=True)
#         total_found = len(sorted_results)
#         await app_state.bot_instance.send_message(chat_id=chat_id,
#                                                   text=f"✅ <b>Анализ завершен!</b> Найдено плотностей для <b>{total_found}</b> активов. Формирую отчеты...")
#
#         for symbol, data in sorted_results:
#             densities, mid_price = data['densities'], data['mid_price']
#             level_count = len(densities)
#
#             # --- 3. ✅ Ключевая логика выбора режима ---
#             # Если уровней 10 или меньше, генерируем КАРТИНКУ
#             if level_count <= DENSITY_CHART_CONFIG['COMPACT_CHART_THRESHOLD']:
#                 try:
#                     # Вызываем новый метод, который создает целостную картинку
#                     image_path = chart_service.create_final_image(symbol, densities, mid_price)
#                     if image_path:
#                         photo = FSInputFile(image_path)
#                         # Отправляем фото БЕЗ caption, вся информация уже на нем
#                         await app_state.bot_instance.send_photo(chat_id=chat_id, photo=photo, caption="")
#                         if os.path.exists(image_path): os.remove(image_path)
#                         sent_items_count += 1
#                     else:  # Если картинка не создалась
#                         raise ValueError("Image generation failed")
#                 except Exception as e:
#                     logger.error(f"Ошибка создания изображения для {symbol}, отправка текста: {e}")
#                     # В случае ошибки отправляем красивый текстовый отчет
#                     text_report = format_text_schema(symbol, densities, mid_price)
#                     await app_state.bot_instance.send_message(chat_id=chat_id, text=text_report)
#                     sent_items_count += 1
#             # Если уровней БОЛЬШЕ 10, генерируем красивый ТЕКСТ
#             else:
#                 text_report = format_text_schema(symbol, densities, mid_price)
#                 await app_state.bot_instance.send_message(chat_id=chat_id, text=text_report)
#                 sent_items_count += 1
#
#             await asyncio.sleep(0.5)
#
#     except Exception as e:
#         logger.error(f"Критическая ошибка в задаче сканирования: {e}", exc_info=True)
#     finally:
#         # --- Финальный отчет ---
#         if total_found > 0:
#             final_summary = (f"📈 <b>Итоговый отчет сканирования</b>\n\n"
#                              f"  • Найдено для: <b>{total_found}</b> активов\n"
#                              f"  • Отправлено отчетов: <b>{sent_items_count}</b>")
#             await app_state.bot_instance.send_message(chat_id=chat_id, text=final_summary,
#                                                       reply_markup=get_main_menu_inline_keyboard())


# # inter_exchange_arbitrage_bot/src/bot/logic/density_logic.py
#
# import asyncio
# import os
# from collections import defaultdict
# from typing import List
#
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, FSInputFile
#
# from src.bot.keyboards import get_main_menu_inline_keyboard
# from src.bot.keyboards.density_screener_keyboards import get_density_screener_menu_keyboard
# from src.core import state as app_state
# from src.models.screener_models import Density
# from src.services.density_chart_service import DensityChartService
# from src.utils import logger
# from src.utils.chat_actions import safe_edit_text
#
#
# async def show_density_screener_menu(message: Message, state: FSMContext):
#     """
#     Отображает главное меню скринера плотностей.
#     """
#     await state.clear()
#     await safe_edit_text(
#         message=message,
#         text="🛡️ <b>Скринер плотностей</b>\n\nВыберите, какие активы вы хотите просканировать на наличие крупных лимитных заявок (стен):",
#         reply_markup=get_density_screener_menu_keyboard()
#     )
#
#
# async def start_density_scan(message: Message, symbols_to_scan: List[str]):
#     """
#     Запускает фоновую задачу сканирования для указанного списка символов.
#     """
#     # Отправляем временное "статусное" сообщение
#     status_message = await message.answer(
#         text=f"⏳ <b>Запускаю сканирование...</b>\n\nАнализирую <b>{len(symbols_to_scan)}</b> активов. Это может занять некоторое время.",
#         reply_markup=None
#     )
#
#     # Создаем и запускаем фоновую задачу
#     asyncio.create_task(run_density_scan_task(
#         chat_id=message.chat.id,
#         message_id=status_message.message_id,
#         symbols_to_scan=symbols_to_scan  # ✅ Передаем список
#     ))
#
#
# def format_density_caption(symbol: str, densities: List[Density], mid_price: float) -> str:
#     """
#     Улучшенная версия: Формирует более информативное и красивое текстовое резюме для графика.
#     """
#     if not densities:
#         return f"Для <b>{symbol}</b> не найдено значимых плотностей."
#
#     # Группируем плотности по бирже
#     grouped_by_exchange = defaultdict(lambda: {'support': [], 'resistance': []})
#     for d in densities:
#         grouped_by_exchange[d.exchange][d.density_type].append(d)
#
#     # Базовая статистика
#     total_support_usd = sum(d.volume_usd for d in densities if d.density_type == 'support')
#     total_resistance_usd = sum(d.volume_usd for d in densities if d.density_type == 'resistance')
#     total_exchanges = len(grouped_by_exchange)
#     total_levels = len(densities)
#     total_volume = total_support_usd + total_resistance_usd
#
#     # Самые крупные уровни
#     strongest_support = max([d for d in densities if d.density_type == 'support'],
#                             key=lambda x: x.volume_usd, default=None)
#     strongest_resistance = max([d for d in densities if d.density_type == 'resistance'],
#                                key=lambda x: x.volume_usd, default=None)
#
#     # АДАПТИВНАЯ СТРУКТУРА в зависимости от объема данных
#     is_compact_mode = total_levels > 8 or total_exchanges > 4
#
#     caption_lines = [
#         f"📊 <b>{symbol}</b> • ${mid_price:,.4f}",
#         f"💰 <b>${total_volume / 1000:,.0f}k</b> на <b>{total_exchanges}</b> биржах"
#     ]
#
#     if not is_compact_mode:
#         # Подробный режим для небольшого объема данных
#         caption_lines.extend([
#             "",
#             "📈 <b>Распределение:</b>",
#             f"  🟢 Поддержка: <b>${total_support_usd / 1000:,.0f}k</b> ({sum(1 for d in densities if d.density_type == 'support')} ур.)",
#             f"  🔴 Сопротивление: <b>${total_resistance_usd / 1000:,.0f}k</b> ({sum(1 for d in densities if d.density_type == 'resistance')} уровней)",
#             ""
#         ])
#
#     # Выделяем самые важные уровни
#     if strongest_support or strongest_resistance:
#         caption_lines.append("⭐ <b>Ключевые уровни:</b>")
#
#         if strongest_support:
#             distance = abs(strongest_support.price - mid_price) / mid_price * 100
#             caption_lines.append(
#                 f"  🟢 <b>Сильнейшая поддержка:</b> "
#                 f"<code>${strongest_support.price:.4f}</code> "
#                 f"(${strongest_support.volume_usd / 1000:.0f}k на {strongest_support.exchange.title()}) "
#                 f"[-{distance:.1f}%]"
#             )
#
#         if strongest_resistance:
#             distance = abs(strongest_resistance.price - mid_price) / mid_price * 100
#             caption_lines.append(
#                 f"  🔴 <b>Сильнейшее сопротивление:</b> "
#                 f"<code>${strongest_resistance.price:.4f}</code> "
#                 f"(${strongest_resistance.volume_usd / 1000:.0f}k на {strongest_resistance.exchange.title()}) "
#                 f"[+{distance:.1f}%]"
#             )
#         caption_lines.append("")
#
#     # Детали по биржам (топ-3 самых активных)
#     sorted_exchanges = sorted(grouped_by_exchange.items(),
#                               key=lambda x: sum(d.volume_usd for d in x[1]['support'] + x[1]['resistance']),
#                               reverse=True)[:3]
#
#     if len(sorted_exchanges) > 1:
#         caption_lines.append("🏪 <b>Детали по ключевым биржам:</b>")
#
#         for exchange, data in sorted_exchanges:
#             supports = sorted(data['support'], key=lambda x: x.volume_usd, reverse=True)[:2]
#             resistances = sorted(data['resistance'], key=lambda x: x.volume_usd, reverse=True)[:2]
#
#             if supports or resistances:
#                 exchange_total = sum(d.volume_usd for d in supports + resistances)
#                 caption_lines.append(f"  <b>• {exchange.title()}</b> (${exchange_total / 1000:.0f}k):")
#
#                 if resistances:
#                     for d in resistances:
#                         caption_lines.append(f"     🔴 <code>${d.price:.4f}</code> → ${d.volume_usd / 1000:.0f}k")
#
#                 if supports:
#                     for d in supports:
#                         caption_lines.append(f"     🟢 <code>${d.price:.4f}</code> → ${d.volume_usd / 1000:.0f}k")
#         caption_lines.append("")
#
#     # Итоговый анализ
#     support_strength = "сильная" if total_support_usd > total_resistance_usd * 1.5 else \
#         "слабая" if total_support_usd < total_resistance_usd * 0.5 else "умеренная"
#
#     resistance_strength = "сильное" if total_resistance_usd > total_support_usd * 1.5 else \
#         "слабое" if total_resistance_usd < total_support_usd * 0.5 else "умеренное"
#
#     caption_lines.extend([
#         "🔍 <b>Краткий анализ:</b>",
#         f"  Поддержка: <b>{support_strength}</b>",
#         f"  Сопротивление: <b>{resistance_strength}</b>"
#     ])
#
#     # Добавляем рекомендации на основе соотношения
#     ratio = total_support_usd / total_resistance_usd if total_resistance_usd > 0 else float('inf')
#     if ratio > 2:
#         caption_lines.append("  📊 <i>Преобладает поддержка - потенциал роста</i>")
#     elif ratio < 0.5:
#         caption_lines.append("  📊 <i>Преобладает сопротивление - давление продаж</i>")
#     else:
#         caption_lines.append("  📊 <i>Сбалансированная ситуация</i>")
#
#     return "\n".join(caption_lines)
#
#
# async def run_density_scan_task(chat_id: int, message_id: int, symbols_to_scan: List[str]):
#     """
#     Улучшенная версия: Более информативные сообщения о прогрессе и результатах.
#     """
#     sent_charts_count = 0
#     total_found = 0
#     processing_errors = 0
#
#     try:
#         if not app_state.density_screener_service:
#             raise ValueError("Сервис скринера плотностей не инициализирован.")
#
#         if not symbols_to_scan:
#             await app_state.bot_instance.edit_message_text(
#                 chat_id=chat_id, message_id=message_id,
#                 text="⚠️ <b>Внимание!</b>\n\nСписок монет для сканирования пуст. Пожалуйста, выберите активы для анализа.",
#                 reply_markup=get_main_menu_inline_keyboard()
#             )
#             return
#
#         # Улучшенное сообщение о начале сканирования
#         progress_text = (
#             f"🔍 <b>Сканирование запущено</b>\n\n"
#             f"📋 Анализируем: <b>{len(symbols_to_scan)}</b> активов\n"
#             f"⏱ Примерное время: ~{len(symbols_to_scan) * 2} сек\n"
#             f"🔄 Получаем данные с бирж..."
#         )
#
#         try:
#             await app_state.bot_instance.edit_message_text(
#                 chat_id=chat_id, message_id=message_id, text=progress_text
#             )
#         except Exception:
#             pass
#
#         density_results = await app_state.density_screener_service.scan_for_densities(symbols_to_scan)
#
#         # Удаляем сообщение о прогрессе
#         try:
#             await app_state.bot_instance.delete_message(chat_id, message_id)
#         except Exception:
#             pass
#
#         if not density_results:
#             no_results_text = (
#                 f"🛡️ <b>Сканирование завершено</b>\n\n"
#                 f"📊 Проанализировано: <b>{len(symbols_to_scan)}</b> активов\n"
#                 f"📈 Найдено плотностей: <b>0</b>\n\n"
#                 f"💡 <i>Возможные причины:</i>\n"
#                 f"• Низкая активность рынка\n"
#                 f"• Все крупные заявки находятся далеко от цены\n"
#                 f"• Технические проблемы с получением данных"
#             )
#             await app_state.bot_instance.send_message(
#                 chat_id=chat_id,
#                 text=no_results_text,
#                 reply_markup=get_main_menu_inline_keyboard()
#             )
#             return
#
#         chart_service = DensityChartService()
#         sorted_results = sorted(density_results.items(),
#                                 key=lambda item: sum(d.volume_usd for d in item[1]['densities']), reverse=True)
#
#         total_found = len(sorted_results)
#         total_volume_found = sum(sum(d.volume_usd for d in data['densities']) for _, data in sorted_results)
#
#         # Отправляем краткую сводку перед графиками
#         summary_text = (
#             f"✅ <b>Анализ завершен!</b>\n\n"
#             f"📊 Найдено плотностей для <b>{total_found}</b> активов\n"
#             f"💰 Общий объем: <b>${total_volume_found / 1000000:.1f}M</b>\n"
#             f"📈 Отправляю графики..."
#         )
#
#         try:
#             await app_state.bot_instance.send_message(chat_id=chat_id, text=summary_text)
#         except Exception as e:
#             logger.error(f"Не удалось отправить сводку: {e}")
#
#         # Обрабатываем результаты и создаем графики
#         for i, (symbol, data) in enumerate(sorted_results):
#             try:
#                 chart_path = chart_service.create_density_chart(symbol, data['densities'], data['mid_price'])
#
#                 if chart_path:
#                     try:
#                         photo = FSInputFile(chart_path)
#                         caption_text = format_density_caption(symbol, data['densities'], data['mid_price'])
#
#                         await app_state.bot_instance.send_photo(
#                             chat_id=chat_id,
#                             photo=photo,
#                             caption=caption_text,
#                             reply_markup=None
#                         )
#                         sent_charts_count += 1
#
#                         # Пауза для соблюдения rate-лимитов
#                         await asyncio.sleep(0.3)
#                     except Exception as e:
#                         logger.error(f"Ошибка отправки графика {symbol}: {e}")
#                         processing_errors += 1
#                     finally:
#                         if os.path.exists(chart_path):
#                             os.remove(chart_path)
#                 else:
#                     processing_errors += 1
#
#             except Exception as e:
#                 logger.error(f"Ошибка обработки {symbol}: {e}")
#                 processing_errors += 1
#
#     except Exception as e:
#         logger.error(f"Критическая ошибка в фоновой задаче сканирования плотностей: {e}", exc_info=True)
#         try:
#             error_text = (
#                 f"❌ <b>Ошибка сканирования</b>\n\n"
#                 f"Произошла техническая ошибка при анализе плотностей.\n"
#                 f"Попробуйте повторить сканирование через несколько минут.\n\n"
#                 f"<i>Если проблема повторяется, обратитесь к администратору.</i>"
#             )
#             await app_state.bot_instance.send_message(
#                 chat_id=chat_id,
#                 text=error_text,
#                 reply_markup=get_main_menu_inline_keyboard()
#             )
#         except Exception as notify_e:
#             logger.error(f"Не удалось уведомить пользователя об ошибке: {notify_e}")
#
#     finally:
#         # Отправляем детальный итоговый отчет
#         if total_found > 0:
#             success_rate = ((sent_charts_count / total_found) * 100) if total_found > 0 else 0
#
#             final_summary = (
#                 f"📈 <b>Итоговый отчет сканирования</b>\n\n"
#                 f"🎯 <b>Результаты:</b>\n"
#                 f"  • Проанализировано: <b>{len(symbols_to_scan)}</b> активов\n"
#                 f"  • Найдено плотностей: <b>{total_found}</b> активов\n"
#                 f"  • Успешно обработано: <b>{sent_charts_count}</b> графиков\n"
#                 f"  • Успешность: <b>{success_rate:.0f}%</b>\n"
#             )
#
#             if processing_errors > 0:
#                 final_summary += f"  • Ошибок обработки: <b>{processing_errors}</b>\n"
#
#             final_summary += f"\n💡 <i>Все графики показывают крупные заявки в пределах ±2% от текущей цены</i>"
#
#             if sent_charts_count < total_found:
#                 final_summary += f"\n\n⚠️ <i>Некоторые графики не созданы из-за технических ошибок</i>"
#
#         else:
#             final_summary = (
#                 f"📊 <b>Сканирование завершено</b>\n\n"
#                 f"Проанализировано <b>{len(symbols_to_scan)}</b> активов.\n"
#                 f"Значимых плотностей не обнаружено.\n\n"
#                 f"💡 <i>Попробуйте повторить анализ позже или выберите другие активы</i>"
#             )
#
#         try:
#             await app_state.bot_instance.send_message(
#                 chat_id=chat_id,
#                 text=final_summary,
#                 reply_markup=get_main_menu_inline_keyboard()
#             )
#         except Exception as e:
#             logger.error(f"Не удалось отправить финальный отчет: {e}")
