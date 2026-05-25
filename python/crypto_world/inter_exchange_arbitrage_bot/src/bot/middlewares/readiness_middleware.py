# src/bot/middlewares/readiness_middleware.py

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message

import src.core.state as app_state
from src.lexicon.lexicon_ru import LEXICON_RU
from src.utils.logger import logger


class ReadinessMiddleware(BaseMiddleware):
    """
    Middleware для проверки готовности приложения перед обработкой запросов.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # Проверяем готовность системы
        is_ready = app_state.is_ready_event.is_set()
        logger.debug(
            f"ReadinessMiddleware: система {'готова' if is_ready else 'НЕ готова'}, событие: {type(event).__name__}")

        # Если приложение еще не готово к работе
        if not is_ready:
            # Если это нажатие на кнопку (CallbackQuery)
            if isinstance(event, CallbackQuery):
                logger.info(
                    f"Блокируем CallbackQuery от пользователя {event.from_user.id}, data: {getattr(event, 'data', 'N/A')}")
                try:
                    alert_text = LEXICON_RU.get('system_initializing_alert', 'Система инициализируется, подождите...')
                    logger.debug(f"Отправляем alert: '{alert_text}'")

                    # ИСПРАВЛЕНИЕ: Дожидаемся выполнения alert
                    await event.answer(
                        text=alert_text,
                        show_alert=True
                    )
                    logger.info(f"✅ Alert успешно отправлен пользователю {event.from_user.id}")
                except Exception as e:
                    logger.error(f"❌ Ошибка при отправке alert пользователю {event.from_user.id}: {e}", exc_info=True)

                # Возвращаем None, чтобы остановить дальнейшую обработку
                return None

            # Если это обычное сообщение, можно отправить текстовый ответ
            elif isinstance(event, Message):
                try:
                    await event.answer(
                        text=LEXICON_RU.get('system_initializing_message',
                                            'Система инициализируется. Пожалуйста, подождите...')
                    )
                    logger.debug(f"Сообщение о инициализации отправлено пользователю {event.from_user.id}")
                except Exception as e:
                    logger.error(f"Ошибка при отправке сообщения: {e}")

                return None

            # Для других типов событий просто блокируем
            return None

        # Если приложение готово, передаем событие дальше
        return await handler(event, data)