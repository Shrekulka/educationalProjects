# inter_exchange_arbitrage_bot/src/utils/api_error_handler.py

from functools import wraps
from typing import Callable

from aiogram.types import CallbackQuery

import src.core.state as app_state
from src.bot.keyboards import get_main_menu_inline_keyboard
from src.lexicon import LEXICON_RU
from src.utils.chat_actions import safe_edit_text
from src.utils.exceptions import APINotReadyError, APIConnectionError
from src.utils.logger import logger


def handle_api_errors(fallback_keyboard_func: Callable = get_main_menu_inline_keyboard):
    """
    УЛУЧШЕННАЯ ВЕРСИЯ: Все операции выполняются внутри try/except для максимальной безопасности.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            callback_or_message = args[0]
            message = getattr(callback_or_message, 'message', callback_or_message)

            try:
                # ИСПРАВЛЕНО: Проверка готовности теперь внутри try/except
                if not app_state.is_ready_event.is_set():
                    logger.info(
                        f"Действие заблокировано: приложение не готово. "
                        f"Пользователь {callback_or_message.from_user.id}, хендлер {func.__name__}"
                    )

                    if isinstance(callback_or_message, CallbackQuery):
                        await callback_or_message.answer(
                            text=LEXICON_RU.get('system_initializing_alert',
                                                'Пожалуйста, подождите, система готовится к работе...'),
                            show_alert=True
                        )
                    return

                # Выполняем основную логику хендлера
                return await func(*args, **kwargs)

            except APINotReadyError as e:
                logger.info(f"Хендлер {func.__name__}: API не готово. {e.progress_details}")

                if isinstance(callback_or_message, CallbackQuery):
                    await callback_or_message.answer("Система загружается, пожалуйста, подождите...", show_alert=True)

                # Формируем сообщение с прогрессом
                progress_text = "Пожалуйста, подождите несколько секунд и попробуйте снова."
                if hasattr(e, 'progress_details') and e.progress_details:
                    details = e.progress_details
                    progress_lines = [
                        "<b>Статус инициализации:</b>",
                        f" - Подключение к биржам: {details.get('healthy_services', 0)} / {details.get('total_services', 0)}",
                        f" - Кэширование пар: {details.get('caches_initialized', 0)} / {details.get('total_services', 0)}"
                    ]
                    progress_text = "\n".join(progress_lines)

                await safe_edit_text(
                    message=message,
                    text=f"⏳ <b>Система инициализируется...</b>\n\n{progress_text}",
                    reply_markup=fallback_keyboard_func()
                )

            except APIConnectionError as e:
                logger.warning(f"Хендлер {func.__name__}: ошибка подключения к API: {e}")

                if isinstance(callback_or_message, CallbackQuery):
                    await callback_or_message.answer(str(e), show_alert=True)

                await safe_edit_text(
                    message=message,
                    text="🔌 <b>Ошибка подключения!</b>\n\nНе удается связаться с сервером API. Пожалуйста, попробуйте позже.",
                    reply_markup=fallback_keyboard_func()
                )

            except Exception as e:
                # УЛУЧШЕНО: Более подробное логгирование
                logger.error(
                    f"Критическая ошибка в хендлере {func.__name__} "
                    f"(пользователь {callback_or_message.from_user.id}): {type(e).__name__}: {e}",
                    exc_info=True
                )

                if isinstance(callback_or_message, CallbackQuery):
                    await callback_or_message.answer("❌ Произошла внутренняя ошибка", show_alert=True)

                await safe_edit_text(
                    message=message,
                    text="💥 <b>Произошла непредвиденная ошибка.</b>\n\nАдминистратор уже уведомлен. Пожалуйста, попробуйте повторить действие позже.",
                    reply_markup=fallback_keyboard_func()
                )

        return wrapper

    return decorator

# # inter_exchange_arbitrage_bot/src/utils/api_error_handler.py
#
# from functools import wraps
# from typing import Callable
#
# from aiogram.types import CallbackQuery
#
# from src.bot.keyboards import get_main_menu_inline_keyboard
# from src.utils.chat_actions import safe_edit_text
# from src.utils.exceptions import APINotReadyError, APIConnectionError
# from src.utils.logger import logger
#
#
# def handle_api_errors(fallback_keyboard_func: Callable = get_main_menu_inline_keyboard):
#     """
#     Декоратор для единообразной обработки API ошибок в хендлерах Telegram.
#     """
#
#     def decorator(func: Callable) -> Callable:
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             # Предполагаем, что первый аргумент - это CallbackQuery или Message
#             callback_or_message = args[0]
#             # Получаем объект message, с которым будем работать
#             message = getattr(callback_or_message, 'message', callback_or_message)
#
#             try:
#                 # Пытаемся выполнить основную логику хендлера
#                 return await func(*args, **kwargs)
#             except APINotReadyError as e:
#                 logger.info(f"Действие заблокировано: API не готово. {e.progress_details}")
#                 if isinstance(callback_or_message, CallbackQuery):
#                     await callback_or_message.answer("Система загружается, пожалуйста, подождите...", show_alert=True)
#
#                 # Формируем сообщение с прогрессом
#                 progress_text = "Пожалуйста, подождите несколько секунд и попробуйте снова."
#                 if hasattr(e, 'progress_details') and e.progress_details:
#                     details = e.progress_details
#                     progress_lines = [
#                         "<b>Статус инициализации:</b>",
#                         f" - Подключение к биржам: {details.get('healthy_services', 0)} / {details.get('total_services', 0)}",
#                         f" - Кэширование пар: {details.get('caches_initialized', 0)} / {details.get('total_services', 0)}"
#                     ]
#                     progress_text = "\n".join(progress_lines)
#
#                 await safe_edit_text(
#                     message=message,
#                     text=f"⏳ <b>Система инициализируется...</b>\n\n{progress_text}",
#                     reply_markup=fallback_keyboard_func()
#                 )
#             except APIConnectionError as e:
#                 # Ошибка: API не отвечает (сервер выключен)
#                 if isinstance(callback_or_message, CallbackQuery):
#                     await callback_or_message.answer(str(e), show_alert=True)
#                 # Редактируем сообщение
#                 await safe_edit_text(
#                     message=message,
#                     text=f"🔌 <b>Ошибка подключения!</b>\n\n{e}",
#                     reply_markup=fallback_keyboard_func()
#                 )
#             except Exception as e:
#                 # Любая другая непредвиденная ошибка в хендлере
#                 logger.error(f"Неожиданная ошибка в хендлере {func.__name__}: {e}", exc_info=True)
#                 if isinstance(callback_or_message, CallbackQuery):
#                     await callback_or_message.answer("❌ Произошла внутренняя ошибка. Смотрите логи.", show_alert=True)
#
#         return wrapper
#
#     return decorator
