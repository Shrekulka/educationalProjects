# inter_exchange_arbitrage_bot/src/services/reconnaissance_service.py

import asyncio
import re
import time
from collections import defaultdict

import aiogram.exceptions

import src.core.state as app_state
from src.api.schemas import ReconnaissanceRequest
from src.bot.keyboards.scanner_keyboard import get_cancel_keyboard, get_scanner_menu_keyboard
from src.bot.logic.recon_logic import format_reconnaissance_report
from src.bot.logic.settings_logic import get_user_settings
from src.constants.telegram_constants import SPINNER_CHARS
from src.constants.trading_constants import STABLE_COINS
from src.core.config import config
from src.lexicon.lexicon_ru import LEXICON_RU
from src.services import service_manager, scanner_api_service
from src.services.data_enricher_service import data_enricher
from src.strategies.arbitrage_strategy import ArbitrageStrategy
from src.utils.helpers import create_progress_bar
from src.utils.logger import logger
from src.utils.metrics import RECON_DURATION_SECONDS


async def run_reconnaissance_task(request: ReconnaissanceRequest):
    """
    ФИНАЛЬНАЯ ВЕРСИЯ: Выполняет полный цикл разведки, включая сбор данных,
    анализ, обогащение и отправку итогового отчета в Telegram.
    Эта задача является полностью самодостаточной.
    """
    callback_chat_id = request.chat_id
    callback_message_id = request.message_id
    start_time = time.monotonic()
    opportunities = []  # Инициализируем на случай раннего выхода

    try:
        # --- Шаг 0: Валидация и подготовка ---
        if not config.tg_bot.admin_ids:
            logger.error(LEXICON_RU['api_error_no_admins'])
            await _send_error_message(callback_chat_id, callback_message_id,
                                      "❌ <b>Ошибка конфигурации:</b> Не настроены ID администраторов")
            return

        user_id = config.tg_bot.admin_ids[0]
        _, profit_threshold = await get_user_settings(user_id)
        spinner_index = 0

        async def progress_callback(progress_status: str, current: int = -1, total: int = -1):
            nonlocal spinner_index
            spinner = SPINNER_CHARS[spinner_index % len(SPINNER_CHARS)]
            spinner_index += 1
            header = f"🛰️ <b>Идет разведка...</b> {spinner} <u>Операция может занять несколько минут</u>\n\n"
            progress_lines = []
            if current >= 0 and total > 0:
                percentage = (current / total) * 100
                bar = create_progress_bar(current, total)
                progress_lines.append(f"{bar} {percentage:.1f}%")
                progress_lines.append(f"\n<i>Анализ активов: {current} из {total}</i>\n")
            progress_lines.append(f"<i>{progress_status}</i>")
            progress_update_text = header + "\n".join(progress_lines)
            try:
                await app_state.notifier_service.edit_message(
                    chat_id=callback_chat_id,
                    message_id=callback_message_id,
                    text=progress_update_text,
                    reply_markup=get_cancel_keyboard()
                )
            except Exception as e_progress:
                logger.warning(LEXICON_RU['log_recon_progress_update_failed'].format(e_progress=e_progress))

        # --- Шаг 1: Проверка сервисов и сбор активов ---
        await progress_callback("Проверка доступности бирж...")
        healthy_services = await service_manager.get_healthy_services()
        if not healthy_services:
            await _send_error_message(callback_chat_id, callback_message_id,
                                      "❌ <b>Нет доступных бирж.</b> Проверьте API ключи и подключение.")
            return

        await progress_callback("Сбор всех торгуемых активов...")
        all_assets = service_manager.get_all_spot_assets_from_cache()
        if not all_assets:
            await _send_error_message(callback_chat_id, callback_message_id,
                                      "❌ <b>Активы не найдены.</b> Не удалось получить список торговых пар.")
            return

        coins_to_scan = sorted([coin for coin in all_assets if coin not in STABLE_COINS])
        await progress_callback(f"Найдено {len(coins_to_scan)} активов для анализа.")

        if not app_state.balance_service:
            await _send_error_message(callback_chat_id, callback_message_id,
                                      "❌ <b>Внутренняя ошибка:</b> Сервис балансов недоступен.")
            return

        # --- Шаг 2: Запуск основной стратегии сканирования ---
        strategy = ArbitrageStrategy(
            user_id=user_id,
            validated_services=healthy_services,
            profit_threshold=profit_threshold,
            initial_balances={},
            buy_capable_exchanges=list(healthy_services.keys()),
            notifier=app_state.notifier_service,
            report_service=app_state.report_service,
            tracked_coins_to_scan=coins_to_scan,
            progress_callback=progress_callback
        )

        logger.info("Начинаем основное сканирование арбитражных возможностей...")
        opportunities = await strategy.run_reconnaissance_scan()
        logger.info(f"✅ Сканирование завершено, найдено {len(opportunities)} потенциальных возможностей")

        # --- Шаг 3: Сбор контекста и формирование отчета ---
        await progress_callback("Сбор рыночной аналитики...")
        report_context = await data_enricher.enrich_report_context()

        # Анализ секторов для динамических рекомендаций
        if opportunities:
            sector_counter = defaultdict(int)
            real_opportunities = [opp for opp in opportunities if not opp.is_phantom]
            for opp in real_opportunities:
                if opp.tags:
                    for tag in opp.tags:
                        sector_counter[tag.capitalize()] += 1
            if sector_counter:
                top_sectors = sorted(sector_counter.items(), key=lambda item: item[1], reverse=True)
                report_context['top_sectors'] = [sector[0] for sector in top_sectors[:2]]

        scan_duration = time.monotonic() - start_time
        await progress_callback("Формирование итогового отчета...")
        await asyncio.sleep(1.0)

        is_running = await scanner_api_service.get_scanner_status()
        final_keyboard = get_scanner_menu_keyboard(is_running)

        logger.info(f"Начинаем формирование отчета для {len(opportunities)} возможностей")
        report_messages = format_reconnaissance_report(opportunities, scan_duration, report_context)

        # --- Шаг 4: Отправка отчета пользователю ---
        for i, message_text in enumerate(report_messages):
            is_last_message = (i == len(report_messages) - 1)
            reply_markup = final_keyboard if is_last_message else None
            try:
                if i == 0:
                    await app_state.bot_instance.edit_message_text(
                        chat_id=callback_chat_id, message_id=callback_message_id,
                        text=message_text, reply_markup=reply_markup
                    )
                    logger.info("✅ Первое сообщение отчета успешно отправлено (отредактировано)")
                else:
                    await app_state.bot_instance.send_message(
                        chat_id=callback_chat_id, text=message_text, reply_markup=reply_markup
                    )
                    logger.info(f"✅ Сообщение отчета #{i + 1} успешно отправлено")
            except aiogram.exceptions.TelegramBadRequest as e:
                logger.warning(f"Ошибка парсинга HTML в сообщении #{i + 1}: {e}. Попытка отправки без форматирования.")
                logger.debug(
                    f"--- НАЧАЛО ПРОБЛЕМНОГО БЛОКА HTML (Сообщение #{i + 1}) ---\n{message_text}\n--- КОНЕЦ ПРОБЛЕМНОГО БЛОКА HTML ---")
                try:
                    raw_text = re.sub(r'<[^>]+>', '', message_text)  # Убираем все HTML теги
                    if i == 0:
                        await app_state.bot_instance.edit_message_text(
                            chat_id=callback_chat_id, message_id=callback_message_id,
                            text=raw_text, reply_markup=reply_markup
                        )
                    else:
                        await app_state.bot_instance.send_message(
                            chat_id=callback_chat_id, text=raw_text, reply_markup=reply_markup
                        )
                    logger.info(f"✅ Сообщение #{i + 1} успешно отправлено в fallback-режиме (без HTML).")
                except Exception as fallback_e:
                    logger.error(f"Критическая ошибка при отправке fallback-сообщения #{i + 1}: {fallback_e}")
            except Exception as send_e:
                logger.error(f"Неожиданная ошибка при отправке сообщения #{i + 1}: {send_e}")

        logger.info(
            f"🎯 Разведка успешно завершена! Отправлено {len(report_messages)} сообщений за {scan_duration:.1f} сек")

    except asyncio.CancelledError:
        logger.info("Задача разведки была отменена пользователем.")
        try:
            is_running_status = await scanner_api_service.get_scanner_status()
            await asyncio.sleep(0.5)  # Даем время на обработку
            await app_state.notifier_service.edit_message(
                chat_id=callback_chat_id, message_id=callback_message_id,
                text="❌ <b>Разведка отменена.</b>",
                reply_markup=get_scanner_menu_keyboard(is_running_status)
            )
        except Exception as e:
            logger.error(f"Ошибка при обновлении сообщения об отмене: {e}")
        raise  # Важно перевыбросить исключение

    except Exception as e:
        logger.error(LEXICON_RU['log_recon_endpoint_error'].format(e=e), exc_info=True)
        await _send_error_message(callback_chat_id, callback_message_id,
                                  LEXICON_RU['recon_critical_error_user_message'])

    finally:
        # Очистка и запись метрик
        app_state.recon_task = None
        duration = time.monotonic() - start_time
        RECON_DURATION_SECONDS.set(duration)
        logger.info(f"Фоновая задача разведки завершена за {duration:.2f} сек.")


async def _send_error_message(chat_id: int, message_id: int, error_text: str):
    """Вспомогательная функция для отправки сообщений об ошибке."""
    try:
        is_running_status = await scanner_api_service.get_scanner_status()
        await app_state.notifier_service.edit_message(
            chat_id=chat_id,
            message_id=message_id,
            text=error_text,
            reply_markup=get_scanner_menu_keyboard(is_running_status)
        )
        logger.info(f"✅ Сообщение об ошибке отправлено: {error_text[:50]}...")
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение об ошибке: {e}")
