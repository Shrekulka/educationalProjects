# inter_exchange_arbitrage_bot/src/bot/handlers/scanner_handlers.py
import asyncio

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

import src.core.state as app_state
from src.bot.filters.admin_filter import AdminFilter
from src.bot.keyboards import get_scanner_menu_keyboard, get_main_menu_inline_keyboard
from src.bot.keyboards.scanner_keyboard import get_cancel_keyboard
from src.lexicon import LEXICON_RU
from src.services import scanner_api_service
from src.utils import logger
from src.utils.api_error_handler import handle_api_errors
from src.utils.chat_actions import show_typing_status, safe_edit_text

router = Router()


@router.callback_query(F.data == "show_scanner_menu", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)
async def show_scanner_menu(callback: CallbackQuery):
    """Показывает меню управления сканером с корректной обработкой ошибок."""
    # Это немедленно убирает "часики" с кнопки и предотвращает ошибку "query is too old".
    await callback.answer()

    # Теперь, когда мы уже ответили, можно выполнять долгую операцию
    is_running = await scanner_api_service.get_scanner_status()
    status_text = LEXICON_RU['bot_status_active_full'] if is_running else LEXICON_RU['bot_status_stopped_full']

    menu_text = LEXICON_RU['bot_scanner_menu_text'].format(status=status_text)

    # Попытка отредактировать сообщение
    await safe_edit_text(
        message=callback.message,
        text=menu_text,
        reply_markup=get_scanner_menu_keyboard(is_running)
    )


@router.callback_query(F.data == "start_scanner", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)  # <-- ПРИМЕНЯЕМ
async def start_scanner_api(callback: CallbackQuery, bot: Bot):
    """Запускает сканер через API."""
    async with show_typing_status(chat_id=callback.from_user.id, bot=bot):
        current_status = await scanner_api_service.get_scanner_status()
        if current_status:
            await callback.answer(LEXICON_RU['bot_scanner_already_running'], show_alert=True)
            await show_scanner_menu(callback)
            return

        success = await scanner_api_service.start_scanner()

    if success:
        await asyncio.sleep(1)
        verification_status = await scanner_api_service.get_scanner_status()
        if verification_status:
            await callback.answer(LEXICON_RU['bot_scanner_start_success'], show_alert=True)
        else:
            await callback.answer(LEXICON_RU['bot_scanner_status_not_changed_warning'], show_alert=True)
    else:
        await callback.answer(LEXICON_RU['bot_scanner_start_fail_api'], show_alert=True)

    await show_scanner_menu(callback)


@router.callback_query(F.data == "stop_scanner", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)  # <-- ПРИМЕНЯЕМ
async def stop_scanner_api(callback: CallbackQuery, bot: Bot):
    """Останавливает сканер через API."""
    async with show_typing_status(chat_id=callback.from_user.id, bot=bot):
        current_status = await scanner_api_service.get_scanner_status()
        if not current_status:
            await callback.answer("ℹ️ Сканер уже остановлен!", show_alert=True)
            await show_scanner_menu(callback)
            return

        success = await scanner_api_service.stop_scanner()

    if success:
        await asyncio.sleep(1)
        verification_status = await scanner_api_service.get_scanner_status()
        if not verification_status:
            await callback.answer("⏹️ Сканер успешно остановлен!", show_alert=True)
        else:
            await callback.answer("⚠️ Команда отправлена, но статус не изменился.", show_alert=True)
    else:
        await callback.answer("❌ Не удалось остановить сканер.", show_alert=True)

    await show_scanner_menu(callback)


@router.callback_query(F.data == "check_scanner_status", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)
async def check_scanner_status(callback: CallbackQuery):
    """Проверяет текущий статус сканера."""
    is_running = await scanner_api_service.get_scanner_status()
    status_message = "🟢 Сканер активен и работает" if is_running else "🔴 Сканер остановлен"
    await callback.answer(f"Статус: {status_message}", show_alert=True)


@router.callback_query(F.data == "recon_scanner", AdminFilter())
@handle_api_errors(fallback_keyboard_func=get_main_menu_inline_keyboard)
async def recon_scanner_handler(callback: CallbackQuery):
    """
    ✅ ПРАВИЛЬНАЯ ВЕРСИЯ: Инициирует запуск разведки через API и обновляет
    сообщение для пользователя, показывая статус подготовки.
    """
    await callback.answer("🛰️ Запускаю полную разведку рынка...")

    # Отправляем или редактируем сообщение, чтобы показать пользователю, что процесс начался
    status_message = await callback.message.answer(
        text="🛰️ <b>Подготовка к разведке...</b>\n\n<i>Инициализирую сканирование...</i>",
        reply_markup=get_cancel_keyboard()  # Сразу даем кнопку отмены
    )

    # Вызываем API, которое запустит фоновую задачу и сразу вернет ответ.
    # Мы не ждем здесь результат сканирования.
    api_response = await scanner_api_service.request_reconnaissance_scan(
        chat_id=callback.from_user.id,
        message_id=status_message.message_id
    )

    # Проверяем только то, что API приняло нашу команду
    if not api_response or api_response.get("status") != "reconnaissance_started":
        # Если API не смогло даже запустить задачу, сообщаем об этом
        is_running = await scanner_api_service.get_scanner_status()
        await safe_edit_text(
            message=status_message,
            text="❌ <b>Не удалось запустить разведку.</b>\n\nСервер API не смог принять команду. Проверьте логи.",
            reply_markup=get_scanner_menu_keyboard(is_running)
        )
        return

    # На этом работа хендлера ЗАКОНЧЕНА.
    # Дальнейшие обновления сообщения и отправка отчета будут выполнены
    # фоновой задачей `run_reconnaissance_task`.
    logger.info("Команда на разведку успешно передана в API, хендлер завершает работу.")


@router.callback_query(F.data == "cancel_recon", AdminFilter())
async def cancel_recon_handler(callback: CallbackQuery):
    """
    ИСПРАВЛЕННАЯ ВЕРСИЯ: Находит и отменяет фоновую задачу разведки.
    Убрано промежуточное сообщение, чтобы избежать конфликта с финальным обновлением.
    """
    logger.info("Пользователь запросил отмену разведки.")

    # Проверяем, есть ли активная задача для отмены
    if app_state.recon_task and not app_state.recon_task.done():
        # Отменяем задачу
        app_state.recon_task.cancel()

        # Показываем quick ответ пользователю без изменения сообщения
        await callback.answer("Отменяю разведку...", show_alert=False)

        # НЕ ОБНОВЛЯЕМ СООБЩЕНИЕ ЗДЕСЬ - это сделает блок CancelledError в reconnaissance_service.py
        # Финальное сообщение "❌ Разведка отменена." появится автоматически через ~0.5 сек

    else:
        # Если задачи нет (уже завершилась или была ошибка)
        await callback.answer("Задача уже завершена или не была запущена.", show_alert=True)
        # Обновляем меню, чтобы убрать кнопку "Отмена"
        is_running = await scanner_api_service.get_scanner_status()
        await callback.message.edit_text(
            text="Сканер готов к работе.",
            reply_markup=get_scanner_menu_keyboard(is_running)
        )
