# inter_exchange_arbitrage_bot/src/services/notifier_service.py

import asyncio
from typing import Optional, Dict, Any

from aiogram.types import InlineKeyboardMarkup

import src.core.state as app_state
from src.bot.keyboards.scanner_keyboard import get_scanner_menu_keyboard
from src.constants.system_constants import SCANNER_STATUS_RUNNING
from src.constants.telegram_constants import (
    get_telegram_api_url, NOTIFICATION_UI_SYNC_DELAY_SECONDS
)
from src.core.config import config
from src.lexicon.lexicon_ru import LEXICON_RU
from src.services.scanner_state_service import get_scanner_state_from_db
from src.utils.logger import logger


class NotifierService:
    """
    Сервис для централизованной отправки уведомлений в Telegram ИСКЛЮЧИТЕЛЬНО через HTTP API.
    Не имеет зависимостей от экземпляра aiogram Bot.
    """

    def __init__(self):
        self.api_url = get_telegram_api_url(config.tg_bot.token)

    async def send_message(
            self,
            chat_id: int,
            text: str,
            reply_markup: Optional[InlineKeyboardMarkup] = None,
            parse_mode: str = "HTML"
    ) -> Optional[Dict[str, Any]]:
        """
        ИСПРАВЛЕНО: Использует глобальный экземпляр Bot из app_state.
        """
        try:
            # Проверяем, что бот был инициализирован
            if not app_state.bot_instance:
                logger.error("NotifierService: Глобальный экземпляр Bot не был создан.")
                return None

            # Используем глобального бота
            response = await app_state.bot_instance.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            logger.debug(f"Сообщение успешно отправлено пользователю {chat_id}")
            return response.model_dump()  # Возвращаем как словарь для совместимости

        except Exception as e:
            logger.error(f"Непредвиденная ошибка при отправке сообщения пользователю {chat_id}: {e}")
            return None

    async def edit_message(self, chat_id: int, message_id: int, text: str, reply_markup=None):
        """
        ИСПРАВЛЕНО: Использует глобальный экземпляр Bot из app_state.
        """
        try:
            # Проверяем, что бот был инициализирован
            if not app_state.bot_instance:
                logger.error("NotifierService: Глобальный экземпляр Bot не был создан.")
                return

            # Используем глобального бота
            await app_state.bot_instance.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Ошибка при редактировании сообщения {message_id}: {e}")

    async def notify_all_admins_about_scanner_state(self):
        """
        Формирует и рассылает всем администраторам актуальное состояние сканера.
        """
        try:
            await asyncio.sleep(NOTIFICATION_UI_SYNC_DELAY_SECONDS)
            is_running = await get_scanner_state_from_db() == SCANNER_STATUS_RUNNING
            status_text = LEXICON_RU['bot_status_active_full'] if is_running else LEXICON_RU['bot_status_stopped_full']
            menu_text = LEXICON_RU['bot_scanner_menu_text'].format(status=status_text)
            keyboard = get_scanner_menu_keyboard(is_running)

            for admin_id in config.tg_bot.admin_ids:
                await self.send_message(chat_id=admin_id, text=menu_text, reply_markup=keyboard)

            logger.info(LEXICON_RU['log_admins_notification_sent'])
        except Exception as e:
            logger.error(LEXICON_RU['log_admins_notification_error'].format(error=e))


# # inter_exchange_arbitrage_bot/src/services/notifier_service.py
#
# import asyncio
# from typing import Optional, Dict, Any
#
# from aiogram.types import InlineKeyboardMarkup
#
# import src.core.state as app_state
# from src.bot.keyboards.scanner_keyboard import get_scanner_menu_keyboard
# from src.constants.system_constants import SCANNER_STATUS_RUNNING
# from src.constants.telegram_constants import (
#     get_telegram_api_url, NOTIFICATION_UI_SYNC_DELAY_SECONDS
# )
# from src.core.config import config
# from src.lexicon.lexicon_ru import LEXICON_RU
# from src.services.scanner_state_service import get_scanner_state_from_db
# from src.utils.logger import logger
#
#
# class NotifierService:
#     """
#     Сервис для централизованной отправки уведомлений в Telegram ИСКЛЮЧИТЕЛЬНО через HTTP API.
#     Не имеет зависимостей от экземпляра aiogram Bot.
#     """
#
#     def __init__(self):
#         self.api_url = get_telegram_api_url(config.tg_bot.token)
#
#     async def edit_message(self, chat_id: int, message_id: int, text: str, reply_markup=None):
#         """
#         ИСПРАВЛЕНО: Пробрасывает исключения вместо их поглощения.
#         Это позволяет вызывающему коду корректно обрабатывать ошибки Telegram API.
#         """
#         try:
#             # Проверяем, что бот был инициализирован
#             if not app_state.bot_instance:
#                 logger.error("NotifierService: Глобальный экземпляр Bot не был создан.")
#                 raise RuntimeError("Бот не инициализирован")
#
#             # Используем глобального бота
#             await app_state.bot_instance.edit_message_text(
#                 chat_id=chat_id,
#                 message_id=message_id,
#                 text=text,
#                 reply_markup=reply_markup,
#                 parse_mode="HTML"
#             )
#             logger.debug(f"NotifierService: сообщение {message_id} отредактировано для пользователя {chat_id}")
#
#         except Exception as e:
#             # ИСПРАВЛЕНО: Логируем на уровне DEBUG и пробрасываем исключение
#             # чтобы вызывающий код мог обработать специфичные ошибки Telegram
#             logger.debug(
#                 f"NotifierService: ошибка редактирования сообщения {message_id} для {chat_id}: {type(e).__name__}: {e}")
#             raise  # Пробрасываем исключение для обработки на верхнем уровне
#
#     async def send_message(
#             self,
#             chat_id: int,
#             text: str,
#             reply_markup: Optional[InlineKeyboardMarkup] = None,
#             parse_mode: str = "HTML"
#     ) -> Optional[Dict[str, Any]]:
#         """
#         ИСПРАВЛЕНО: Использует глобальный экземпляр Bot из app_state.
#         """
#         try:
#             # Проверяем, что бот был инициализирован
#             if not app_state.bot_instance:
#                 logger.error("NotifierService: Глобальный экземпляр Bot не был создан.")
#                 return None
#
#             # Используем глобального бота
#             response = await app_state.bot_instance.send_message(
#                 chat_id=chat_id,
#                 text=text,
#                 reply_markup=reply_markup,
#                 parse_mode=parse_mode
#             )
#             logger.debug(f"NotifierService: сообщение успешно отправлено пользователю {chat_id}")
#             return response.model_dump()  # Возвращаем как словарь для совместимости
#
#         except Exception as e:
#             logger.error(
#                 f"NotifierService: критическая ошибка при отправке сообщения пользователю {chat_id}: {type(e).__name__}: {e}")
#             # ВАЖНО: В отличие от edit_message, здесь мы НЕ пробрасываем исключение,
#             # а возвращаем None, так как вызывающий код ожидает Optional[Dict]
#             return None
#
#     async def notify_all_admins_about_scanner_state(self):
#         """
#         Формирует и рассылает всем администраторам актуальное состояние сканера.
#         """
#         try:
#             await asyncio.sleep(NOTIFICATION_UI_SYNC_DELAY_SECONDS)
#             is_running = await get_scanner_state_from_db() == SCANNER_STATUS_RUNNING
#             status_text = LEXICON_RU['bot_status_active_full'] if is_running else LEXICON_RU['bot_status_stopped_full']
#             menu_text = LEXICON_RU['bot_scanner_menu_text'].format(status=status_text)
#             keyboard = get_scanner_menu_keyboard(is_running)
#
#             for admin_id in config.tg_bot.admin_ids:
#                 await self.send_message(chat_id=admin_id, text=menu_text, reply_markup=keyboard)
#
#             logger.info(LEXICON_RU['log_admins_notification_sent'])
#         except Exception as e:
#             logger.error(LEXICON_RU['log_admins_notification_error'].format(error=e))
