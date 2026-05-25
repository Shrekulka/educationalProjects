# inter_exchange_arbitrage_bot/src/bot/logic/news_logic.py

from typing import Dict, List, Optional, Any

from aiogram.types import FSInputFile
from aiogram.types import Message
from sqlalchemy import select

import src.core.state as app_state
from src.bot.keyboards.news_keyboards import get_news_menu_keyboard
from src.constants.emoji_constants import PRICE_CHANGE_EMOJIS
from src.constants.telegram_constants import (
    BLOCK_HEADER_TEMPLATE,
    SUB_BLOCK_HEADER_TEMPLATE,
    REPORT_BLOCK_SEPARATOR,
    SUB_BLOCK_SEPARATOR,
    TELEGRAM_MESSAGE_MAX_LENGTH, TELEGRAM_CAPTION_MAX_LENGTH
)
from src.core import async_session_factory
from src.lexicon.lexicon_ru import LEXICON_RU
from src.models import UserCoin
from src.services import scanner_api_service
from src.utils import logger
from src.utils.chat_actions import safe_edit_text
from src.utils.helpers import get_canonical_symbol
from src.utils.helpers import get_number_emoji, split_long_message
from src.utils.response_formatter import AIResponseFormatter, format_ai_analysis_response


async def format_and_send_news(message: Message, news_by_coin: Dict[str, List[Dict]], requested_coins: List[str],
                               block_counter: int) -> int:
    """
    Форматирует и отправляет новости с красивым форматированием и AI аналитикой.
    """
    news_to_process = news_by_coin.copy()

    # Обработка новостей по Bitcoin
    if 'BTC' in news_to_process:
        numbered_emoji = get_number_emoji(block_counter)
        header = BLOCK_HEADER_TEMPLATE.format(
            block_emoji="₿",
            numbered_emoji=numbered_emoji,
            title="Новости по Bitcoin (BTC)"
        )
        await message.answer(header)
        block_counter += 1

        await _send_coin_news_block(message, None, news_to_process.pop('BTC'))

        # AI аналитика по BTC с красивым форматированием (направление рынка)
        if app_state.ai_trade_advisor:
            try:
                # Получаем аналитику направления BTC (без торговых уровней)
                raw_analysis = await app_state.ai_trade_advisor.analyze_btc_trading_situation(
                    news_by_coin['BTC'], {}
                )

                # Форматирование уже происходит внутри AITradeAdvisorService
                for part in split_long_message(raw_analysis, TELEGRAM_MESSAGE_MAX_LENGTH):
                    await message.answer(part)

            except Exception as e:
                logger.error(f"Ошибка генерации аналитики для BTC: {e}")
                await message.answer("⚠️ Аналитика по BTC временно недоступна")

        await message.answer(REPORT_BLOCK_SEPARATOR)

    # Обработка выбранных монет
    selected_coins_news_found = any(
        coin.upper() in news_to_process for coin in requested_coins if coin.upper() != 'BTC'
    )

    if selected_coins_news_found:
        numbered_emoji = get_number_emoji(block_counter)
        header = BLOCK_HEADER_TEMPLATE.format(
            block_emoji="🪙",
            numbered_emoji=numbered_emoji,
            title="Выбранные монеты"
        )
        await message.answer(header)
        block_counter += 1

        first_coin_in_block = True
        for coin in sorted(requested_coins):
            coin_upper = coin.upper()
            if coin_upper == 'BTC':
                continue

            if coin_upper in news_to_process:
                if not first_coin_in_block:
                    await message.answer(SUB_BLOCK_SEPARATOR)
                first_coin_in_block = False

                sub_header = SUB_BLOCK_HEADER_TEMPLATE.format(title=f"Новости по {coin_upper}")
                await message.answer(sub_header)
                await _send_coin_news_block(message, None, news_to_process.pop(coin_upper))

                # AI аналитика по конкретной монете с торговыми уровнями
                # AI аналитика по конкретной монете с торговыми уровнями
                if app_state.ai_trade_advisor:
                    try:
                        # Получаем сырой анализ от сервиса (сервис больше не форматирует сам)
                        raw_analysis_text = await app_state.ai_trade_advisor.get_raw_coin_analysis(
                            news_by_coin[coin_upper], coin_upper
                        )

                        # Теперь вызываем наш новый умный форматтер
                        formatted_text, image_path = AIResponseFormatter.format_analysis_with_image(
                            raw_analysis_text, coin_upper
                        )

                        # Разделяем длинный текст (важно для подписи к фото)
                        text_parts = split_long_message(formatted_text, TELEGRAM_CAPTION_MAX_LENGTH)

                        if image_path:
                            # Если есть картинка, отправляем ее с подписью
                            await message.answer_photo(
                                photo=FSInputFile(image_path),
                                caption=text_parts[0]  # Первая часть текста как подпись
                            )
                            # Остальные части текста (если они есть) отправляем как обычные сообщения
                            if len(text_parts) > 1:
                                for part in text_parts[1:]:
                                    await message.answer(part)
                        else:
                            # Если картинки нет, работаем как раньше
                            for part in split_long_message(formatted_text, TELEGRAM_MESSAGE_MAX_LENGTH):
                                await message.answer(part)

                    except Exception as e:
                        logger.error(f"Ошибка генерации аналитики для {coin_upper}: {e}")
                        await message.answer(f"⚠️ Аналитика по {coin_upper} временно недоступна")

        await message.answer(REPORT_BLOCK_SEPARATOR)

    # Обработка общих новостей и рыночной аналитики
    market_summary = news_by_coin.get('market_summary', "")
    has_general_content = 'GENERAL' in news_to_process or (
            market_summary and market_summary != "Аналитика не была сгенерирована."
    )

    if has_general_content:
        numbered_emoji = get_number_emoji(block_counter)
        header = BLOCK_HEADER_TEMPLATE.format(
            block_emoji="🌍",
            numbered_emoji=numbered_emoji,
            title="Общие новости по рынку"
        )
        await message.answer(header)
        block_counter += 1

        if 'GENERAL' in news_to_process:
            await _send_coin_news_block(message, None, news_to_process.pop('GENERAL'))

        if market_summary and market_summary != "Аналитика не была сгенерирована.":
            # Форматируем рыночную аналитику с эмодзи
            formatted_summary = format_ai_analysis_response(
                raw_analysis=market_summary,
                analysis_type="market"
            )

            for part in split_long_message(formatted_summary, TELEGRAM_MESSAGE_MAX_LENGTH):
                await message.answer(part)

        await message.answer(REPORT_BLOCK_SEPARATOR)

    # Показываем какие монеты не найдены
    requested_set = {c.upper() for c in requested_coins}
    found_in_response = {k for k in news_by_coin.keys() if k != 'market_summary'}
    missing_coins = requested_set - found_in_response

    if missing_coins:
        await message.answer(
            f"ℹ️ Новостей по следующим монетам не найдено: <b>{', '.join(sorted(list(missing_coins)))}</b>"
        )

    return block_counter


async def _send_coin_news_block(message: Message, header: Optional[str], news_list: List[Dict]):
    """
    Отправляет блок новостей по монете с красивым форматированием.
    """
    if not news_list:
        return

    full_text = ""
    if header:
        full_text += f"<b><u>{header}</u></b>\n"

    # Добавляем рыночные данные если есть
    market_data = news_list[0].get('market_data')
    if market_data:
        price = market_data.get('price_usd', 0)
        change = market_data.get('change_24h', 0)
        change_emoji = PRICE_CHANGE_EMOJIS['UP'] if change >= 0 else PRICE_CHANGE_EMOJIS['DOWN']
        full_text += f"<i>Цена: ${price:,.2f}  |  24ч: {change_emoji} {change:+.2f}%</i>\n\n"
    elif header:
        full_text += "\n"

    # Форматируем каждую новость с помощью форматтера
    for news in news_list:
        formatted_news = AIResponseFormatter.format_news_item(news)
        full_text += formatted_news

    if not full_text.strip():
        return

    # Отправляем блоки сообщений
    for part in split_long_message(full_text, TELEGRAM_MESSAGE_MAX_LENGTH):
        await message.answer(part, disable_web_page_preview=True)


async def format_and_send_market_intel(message: Message, intel_data: Dict, block_counter: int) -> int:
    """
    Форматирует и отправляет рыночную аналитику с красивым оформлением.
    """
    try:
        # Блок трендовых монет
        if trending := intel_data.get('trending'):
            numbered_emoji = get_number_emoji(block_counter)
            header = BLOCK_HEADER_TEMPLATE.format(
                block_emoji="💎",
                numbered_emoji=numbered_emoji,
                title="В тренде"
            )
            block_counter += 1

            lines = [header]
            for i, coin in enumerate(trending[:7], 1):
                coin_emoji = AIResponseFormatter.get_coin_emoji(coin['symbol'])
                lines.append(
                    f"  {get_number_emoji(i)} {coin_emoji} {coin['name']} (<b>${coin['symbol'].upper()}</b>) - Rank: #{coin['market_cap_rank']}"
                )

            await message.answer("\n".join(lines))

            # AI аналитика по трендам
            if app_state.ai_trade_advisor:
                try:
                    raw_analysis = await app_state.ai_trade_advisor.analyze_trending_trading_opportunities(trending)
                    # Форматирование уже происходит в сервисе
                    for part in split_long_message(raw_analysis, TELEGRAM_MESSAGE_MAX_LENGTH):
                        await message.answer(part)
                except Exception as e:
                    logger.error(f"Ошибка генерации аналитики по трендам: {e}")
                    await message.answer("⚠️ Аналитика по трендам временно недоступна")

            await message.answer(REPORT_BLOCK_SEPARATOR)

        # Блок лидеров роста и падения
        if intel_data.get('gainers') or intel_data.get('losers'):
            numbered_emoji = get_number_emoji(block_counter)
            header = BLOCK_HEADER_TEMPLATE.format(
                block_emoji="📈",
                numbered_emoji=numbered_emoji,
                title="Лидеры роста и падения"
            )
            block_counter += 1

            lines = [header]

            if gainers := intel_data.get('gainers'):
                lines.append("\n" + SUB_BLOCK_HEADER_TEMPLATE.format(title="🚀 Рост:"))
                for g in gainers:
                    coin_emoji = AIResponseFormatter.get_coin_emoji(g['symbol'])
                    lines.append(
                        f"    🟢 {coin_emoji} {g['name']} (<b>${g['symbol'].upper()}</b>): <b>+{g['change_24h']:.2f}%</b>")

            if losers := intel_data.get('losers'):
                lines.append("\n" + SUB_BLOCK_HEADER_TEMPLATE.format(title="📉 Падение:"))
                for l in losers:
                    coin_emoji = AIResponseFormatter.get_coin_emoji(l['symbol'])
                    lines.append(
                        f"    🔴 {coin_emoji} {l['name']} (<b>${l['symbol'].upper()}</b>): <b>{l['change_24h']:.2f}%</b>")

            await message.answer("\n".join(lines))

            # AI аналитика по лидерам
            if app_state.ai_trade_advisor:
                try:
                    raw_analysis = await app_state.ai_trade_advisor.analyze_gainers_losers_opportunities(intel_data)
                    # Форматирование уже происходит в сервисе
                    for part in split_long_message(raw_analysis, TELEGRAM_MESSAGE_MAX_LENGTH):
                        await message.answer(part)
                except Exception as e:
                    logger.error(f"Ошибка генерации аналитики по лидерам рынка: {e}")
                    await message.answer("⚠️ Аналитика по лидерам рынка временно недоступна")

    except Exception as e:
        logger.error(f"Ошибка форматирования рыночной аналитики: {e}")
        await message.answer("⚠️ Не удалось отобразить рыночную аналитику.")

    return block_counter


async def get_user_favorite_coins(user_id: int) -> list[str]:
    """
    Получает список избранных монет пользователя.
    """
    try:
        async with async_session_factory() as session:
            stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == user_id)
            result = await session.execute(stmt)
            raw_coins = result.scalars().all()

            normalized_coins = [get_canonical_symbol(coin) for coin in raw_coins]
            return normalized_coins
    except Exception as e:
        logger.error(f"Ошибка получения избранных монет для пользователя {user_id}: {e}")
        return []


async def send_error_and_return_to_menu(message: Message, error_text: str):
    """
    Отправляет сообщение об ошибке и возвращает в меню новостей.
    """
    await safe_edit_text(message, error_text, reply_markup=None)
    await message.answer(LEXICON_RU['news_menu_header'], reply_markup=get_news_menu_keyboard())


async def process_news_response(message: Message, api_response: Optional[Dict]):
    """
    Обрабатывает ответ API и отправляет отформатированные новости с аналитикой.
    """
    try:
        block_counter = 1
        response_data = api_response.get("data")

        if not isinstance(response_data, dict):
            await send_error_and_return_to_menu(
                message,
                "🤷‍♂️ Новости не найдены или API вернуло некорректный ответ."
            )
            return

        news_data = response_data.get("news", [])
        market_summary = response_data.get("market_summary", "")
        coins_requested = api_response.get("processed_coins", [])

        if not news_data and not market_summary:
            await message.answer("🤷‍♂️ Новости по вашему запросу не найдены.")
        else:
            # Группируем новости по монетам
            news_by_coin: Dict[str, Any] = {'market_summary': market_summary}
            for item in news_data:
                coin = item.get('coin', 'GENERAL').upper()
                if coin not in news_by_coin:
                    news_by_coin[coin] = []
                news_by_coin[coin].append(item)

            # Отправляем отформатированные новости
            block_counter = await format_and_send_news(message, news_by_coin, coins_requested, block_counter)

        # Добавляем рыночную аналитику
        market_intel_data = await scanner_api_service.get_market_intel_from_api() or {}
        if market_intel_data:
            await format_and_send_market_intel(message, market_intel_data, block_counter)

    except Exception as e:
        logger.error(f"Критическая ошибка при отображении новостей: {e}", exc_info=True)
        await message.answer("⚠️ Произошла критическая ошибка при отображении новостей.")
    finally:
        await message.answer(LEXICON_RU['news_menu_header'], reply_markup=get_news_menu_keyboard())

# # inter_exchange_arbitrage_bot/src/bot/logic/news_logic.py
#
# import html
# from typing import List, Dict, Optional, Any
#
# import src.core.state as app_state
# from aiogram.types import Message
# from sqlalchemy import select
# from src.bot.keyboards.news_keyboards import get_news_menu_keyboard
# from src.constants.telegram_constants import TELEGRAM_MESSAGE_MAX_LENGTH, SUB_BLOCK_HEADER_TEMPLATE, \
#     BLOCK_HEADER_TEMPLATE, REPORT_BLOCK_SEPARATOR, AI_ANALYSIS_TEMPLATE, SUB_BLOCK_SEPARATOR
# from src.core.database import async_session_factory
# from src.lexicon import LEXICON_RU
# from src.models.user_models import UserCoin
# from src.services import scanner_api_service
# from src.utils import logger
# from src.utils.chat_actions import safe_edit_text  # Импорт safe_edit_text
# from src.utils.helpers import split_long_message, get_canonical_symbol, get_number_emoji
#
#
# async def format_and_send_news(message: Message, news_by_coin: Dict[str, List[Dict]], requested_coins: List[str],
#                                block_counter: int) -> int:
#     """
#     ФИНАЛЬНАЯ ВЕРСИЯ: Форматирует и отправляет новостные блоки с улучшенной стилизацией и отступами.
#     """
#     news_to_process = news_by_coin.copy()
#
#     # --- БЛОК №1: Новости по Bitcoin ---
#     if 'BTC' in news_to_process:
#         numbered_emoji = get_number_emoji(block_counter)
#         header = BLOCK_HEADER_TEMPLATE.format(block_emoji="₿", numbered_emoji=numbered_emoji,
#                                               title="Новости по Bitcoin (BTC)")
#         await message.answer(header)
#         block_counter += 1
#
#         await _send_coin_news_block(message, None, news_to_process.pop('BTC'))
#
#         if app_state.ai_trade_advisor:
#             try:
#                 analysis = await app_state.ai_trade_advisor.analyze_coin_trading_opportunity(news_by_coin['BTC'], 'BTC')
#                 formatted_analysis = AI_ANALYSIS_TEMPLATE.format(title="Торговая аналитика по BTC", analysis=analysis)
#                 for part in split_long_message(formatted_analysis, TELEGRAM_MESSAGE_MAX_LENGTH):
#                     await message.answer(part)
#             except Exception as e:
#                 logger.error(f"Ошибка генерации аналитики для BTC: {e}")
#
#         await message.answer(REPORT_BLOCK_SEPARATOR)
#
#     # --- БЛОК №2: Новости по Выбранным монетам ---
#     selected_coins_news_found = any(
#         coin.upper() in news_to_process for coin in requested_coins if coin.upper() != 'BTC')
#
#     if selected_coins_news_found:
#         numbered_emoji = get_number_emoji(block_counter)
#         header = BLOCK_HEADER_TEMPLATE.format(block_emoji="🪙", numbered_emoji=numbered_emoji, title="Выбранные монеты")
#         await message.answer(header)
#         block_counter += 1
#
#         first_coin_in_block = True
#         for coin in sorted(requested_coins):
#             coin_upper = coin.upper()
#             if coin_upper == 'BTC': continue
#
#             if coin_upper in news_to_process:
#                 # ✅ ИСПРАВЛЕНИЕ: Добавляем разделитель между монетами
#                 if not first_coin_in_block:
#                     await message.answer(SUB_BLOCK_SEPARATOR)
#                 first_coin_in_block = False
#
#                 sub_header = SUB_BLOCK_HEADER_TEMPLATE.format(title=f"Новости по {coin_upper}")
#                 await message.answer(sub_header)
#                 await _send_coin_news_block(message, None, news_to_process.pop(coin_upper))
#
#                 if app_state.ai_trade_advisor:
#                     try:
#                         analysis = await app_state.ai_trade_advisor.analyze_coin_trading_opportunity(
#                             news_by_coin[coin_upper], coin_upper)
#                         formatted_analysis = AI_ANALYSIS_TEMPLATE.format(title=f"Торговая аналитика по {coin_upper}",
#                                                                          analysis=analysis)
#                         for part in split_long_message(formatted_analysis, TELEGRAM_MESSAGE_MAX_LENGTH):
#                             await message.answer(part)
#                     except Exception as e:
#                         logger.error(f"Ошибка генерации аналитики для {coin_upper}: {e}")
#
#         await message.answer(REPORT_BLOCK_SEPARATOR)
#
#     # --- БЛОК №3: Общие новости и аналитика по рынку ---
#     market_summary = news_by_coin.get('market_summary', "")
#     has_general_content = 'GENERAL' in news_to_process or (
#             market_summary and market_summary != "Аналитика не была сгенерирована.")
#
#     if has_general_content:
#         numbered_emoji = get_number_emoji(block_counter)
#         header = BLOCK_HEADER_TEMPLATE.format(block_emoji="🌍", numbered_emoji=numbered_emoji,
#                                               title="Общие новости по рынку")
#         await message.answer(header)
#         block_counter += 1
#
#         if 'GENERAL' in news_to_process:
#             await _send_coin_news_block(message, None, news_to_process.pop('GENERAL'))
#
#         if market_summary and market_summary != "Аналитика не была сгенерирована.":
#             formatted_summary = AI_ANALYSIS_TEMPLATE.format(title="Комплексная аналитика по рынку",
#                                                             analysis=market_summary)
#             for part in split_long_message(formatted_summary, TELEGRAM_MESSAGE_MAX_LENGTH):
#                 await message.answer(part)
#
#         await message.answer(REPORT_BLOCK_SEPARATOR)
#
#     requested_set = {c.upper() for c in requested_coins}
#     found_in_response = {k for k in news_by_coin.keys() if k != 'market_summary'}
#     missing_coins = requested_set - found_in_response
#     if missing_coins:
#         await message.answer(
#             f"ℹ️ Новостей по следующим монетам не найдено: <b>{', '.join(sorted(list(missing_coins)))}</b>")
#
#     return block_counter
#
#
# async def _send_coin_news_block(message: Message, header: Optional[str], news_list: List[Dict]):
#     if not news_list: return
#     full_text = ""
#     if header: full_text += f"<b><u>{header}</u></b>\n"
#     market_data = news_list[0].get('market_data')
#     if market_data:
#         price = market_data.get('price_usd', 0)
#         change = market_data.get('change_24h', 0)
#         change_emoji = "📈" if change >= 0 else "📉"
#         full_text += f"<i>Цена: ${price:,.2f}  |  24ч: {change_emoji} {change:+.2f}%</i>\n\n"
#     elif header:
#         full_text += "\n"
#     for news in news_list:
#         sentiment_emoji = news.get('sentiment_emoji', '⚪️')
#         sentiment_text = news.get('sentiment', 'Нейтрально')
#         title = news.get('title_ru', 'Без заголовка')
#         summary = news.get('summary_ru', 'Нет описания')
#         source = html.escape(news.get('source', 'Неизвестный источник'))
#         url = news.get('url')
#         news_block = (f"{sentiment_emoji} <b>{title}</b>\n"
#                       f"<i>Источник: {source} | Тональность: {sentiment_text}</i>\n"
#                       f"{summary}\n"
#                       f"<a href='{url}'>Читать полностью</a>\n\n")
#         full_text += news_block
#     if not full_text.strip(): return
#     for part in split_long_message(full_text, TELEGRAM_MESSAGE_MAX_LENGTH):
#         await message.answer(part, disable_web_page_preview=True)
#
#
# async def format_and_send_market_intel(message: Message, intel_data: Dict, block_counter: int) -> int:
#     """
#     ФИНАЛЬНАЯ ВЕРСИЯ: Форматирует и отправляет блоки рыночной аналитики с исправленными отступами.
#     """
#     try:
#         # --- БЛОК №4: Тренды ---
#         if trending := intel_data.get('trending'):
#             numbered_emoji = get_number_emoji(block_counter)
#             header = BLOCK_HEADER_TEMPLATE.format(block_emoji="💎", numbered_emoji=numbered_emoji, title="В тренде")
#             block_counter += 1
#
#             # ✅ ИСПРАВЛЕНИЕ: Собираем все в одно сообщение для корректных отступов
#             lines = [header]
#             for i, coin in enumerate(trending[:7], 1):
#                 lines.append(
#                     f"  {get_number_emoji(i)} {coin['name']} (<b>${coin['symbol'].upper()}</b>) - Rank: #{coin['market_cap_rank']}")
#
#             await message.answer("\n".join(lines))
#
#             if app_state.ai_trade_advisor:
#                 try:
#                     analysis = await app_state.ai_trade_advisor.analyze_trending_trading_opportunities(trending)
#                     formatted_analysis = AI_ANALYSIS_TEMPLATE.format(title="Аналитика по трендам", analysis=analysis)
#                     for part in split_long_message(formatted_analysis, TELEGRAM_MESSAGE_MAX_LENGTH):
#                         await message.answer(part)
#                 except Exception as e:
#                     logger.error(f"Ошибка генерации аналитики по трендам: {e}")
#             await message.answer(REPORT_BLOCK_SEPARATOR)
#
#         # --- БЛОК №5: Лидеры роста и падения ---
#         if intel_data.get('gainers') or intel_data.get('losers'):
#             numbered_emoji = get_number_emoji(block_counter)
#             header = BLOCK_HEADER_TEMPLATE.format(block_emoji="📈", numbered_emoji=numbered_emoji,
#                                                   title="Лидеры роста и падения")
#             block_counter += 1
#
#             # ✅ ИСПРАВЛЕНИЕ: Собираем все в одно сообщение
#             lines = [header]
#             if gainers := intel_data.get('gainers'):
#                 lines.append("\n" + SUB_BLOCK_HEADER_TEMPLATE.format(title="Рост:"))
#                 for g in gainers:
#                     lines.append(f"    🟢 {g['name']} (<b>${g['symbol'].upper()}</b>): <b>+{g['change_24h']:.2f}%</b>")
#             if losers := intel_data.get('losers'):
#                 lines.append("\n" + SUB_BLOCK_HEADER_TEMPLATE.format(title="Падение:"))
#                 for l in losers:
#                     lines.append(f"    🔴 {l['name']} (<b>${l['symbol'].upper()}</b>): <b>{l['change_24h']:.2f}%</b>")
#
#             await message.answer("\n".join(lines))
#
#             if app_state.ai_trade_advisor:
#                 try:
#                     analysis = await app_state.ai_trade_advisor.analyze_gainers_losers_opportunities(intel_data)
#                     formatted_analysis = AI_ANALYSIS_TEMPLATE.format(title="Аналитика по лидерам рынка",
#                                                                      analysis=analysis)
#                     for part in split_long_message(formatted_analysis, TELEGRAM_MESSAGE_MAX_LENGTH):
#                         await message.answer(part)
#                 except Exception as e:
#                     logger.error(f"Ошибка генерации аналитики по лидерам рынка: {e}")
#     except Exception as e:
#         logger.error(f"Ошибка форматирования рыночной аналитики: {e}")
#         await message.answer("⚠️ Не удалось отобразить рыночную аналитику.")
#
#     return block_counter
#
#
# async def get_user_favorite_coins(user_id: int) -> list[str]:
#     """Получает нормализованный список избранных монет пользователя."""
#     try:
#         async with async_session_factory() as session:
#             stmt = select(UserCoin.coin_ticker).where(UserCoin.user_id == user_id)
#             result = await session.execute(stmt)
#             raw_coins = result.scalars().all()
#
#             normalized_coins = [get_canonical_symbol(coin) for coin in raw_coins]
#             return normalized_coins
#     except Exception as e:
#         logger.error(f"Ошибка получения избранных монет для пользователя {user_id}: {e}")
#         return []
#
#
# async def send_error_and_return_to_menu(message: Message, error_text: str):
#     """
#     ИСПРАВЛЕНО: Использует единое имя переменной 'message'.
#     Отправляет сообщение об ошибке, редактируя текущее сообщение,
#     и возвращает в меню новостей.
#     """
#     # Редактируем переданное сообщение с ошибкой
#     await safe_edit_text(message, error_text, reply_markup=None)
#     # Отправляем новое сообщение с меню новостей
#     await message.answer(LEXICON_RU['news_menu_header'], reply_markup=get_news_menu_keyboard())
#
#
# async def process_news_response(message: Message, api_response: Optional[Dict]):
#     """
#     ФИНАЛЬНАЯ ВЕРСИЯ: Главная функция-дирижер, управляющая нумерацией и последовательностью вывода.
#     """
#     try:
#         block_counter = 1
#         response_data = api_response.get("data")
#         if not isinstance(response_data, dict):
#             await send_error_and_return_to_menu(message, "🤷‍♂️ Новости не найдены или API вернуло некорректный ответ.")
#             return
#
#         news_data = response_data.get("news", [])
#         market_summary = response_data.get("market_summary", "")
#         coins_requested = api_response.get("processed_coins", [])
#
#         if not news_data and not market_summary:
#             await message.answer("🤷‍♂️ Новости по вашему запросу не найдены.")
#         else:
#             news_by_coin: Dict[str, Any] = {'market_summary': market_summary}
#             for item in news_data:
#                 coin = item.get('coin', 'GENERAL').upper()
#                 if coin not in news_by_coin:
#                     news_by_coin[coin] = []
#                 news_by_coin[coin].append(item)
#             block_counter = await format_and_send_news(message, news_by_coin, coins_requested, block_counter)
#
#         market_intel_data = await scanner_api_service.get_market_intel_from_api() or {}
#         if market_intel_data:
#             await format_and_send_market_intel(message, market_intel_data, block_counter)
#
#     except Exception as e:
#         logger.error(f"Критическая ошибка при отображении новостей: {e}", exc_info=True)
#         await message.answer("⚠️ Произошла критическая ошибка при отображении новостей.")
#     finally:
#         await message.answer(LEXICON_RU['news_menu_header'], reply_markup=get_news_menu_keyboard())
#
