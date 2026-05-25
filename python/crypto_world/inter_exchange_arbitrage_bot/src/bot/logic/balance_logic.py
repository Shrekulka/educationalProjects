# inter_exchange_arbitrage_bot/src/bot/logic/balance_logic.py

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from src.bot.keyboards import get_balance_menu_keyboard
from src.constants import TELEGRAM_MESSAGE_MAX_LENGTH
from src.services import scanner_api_service
from src.utils.chat_actions import show_typing_status


async def process_and_send_balance(callback: CallbackQuery, mode: str, bot: Bot):
    """
    НОВАЯ ВЕРСИЯ: Получает данные через API, а не напрямую от сервисов.
    """
    await callback.answer()

    async with show_typing_status(chat_id=callback.from_user.id, bot=bot):
        try:
            await callback.message.edit_text(
                f"⏳ Запрашиваю отчет о балансах через API ({'все активы' if mode == 'all' else 'избранные'})...",
                reply_markup=None
            )
        except TelegramBadRequest:
            pass

        # Получаем данные через API
        report_text, final_mode = await scanner_api_service.get_balances_from_api(mode)

        if not report_text:
            await callback.message.edit_text(
                "❌ Не удалось получить отчет о балансах. Попробуйте позже.",
                reply_markup=get_balance_menu_keyboard(mode)
            )
            return

        # # Разбиваем длинный текст на части (логика из BalanceService)
        # MAX_MESSAGE_LENGTH = 4000  # Telegram лимит ~4096

        if len(report_text) <= TELEGRAM_MESSAGE_MAX_LENGTH:
            messages = [report_text]
        else:
            # Простое разбиение по строкам
            lines = report_text.split('\n')
            messages = []
            current_chunk = ""

            for line in lines:
                if len(current_chunk + line + "\n") <= TELEGRAM_MESSAGE_MAX_LENGTH:
                    current_chunk += line + "\n"
                else:
                    if current_chunk:
                        messages.append(current_chunk.strip())
                    current_chunk = line + "\n"

            if current_chunk:
                messages.append(current_chunk.strip())

        # Удаляем временное сообщение
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass

        # Отправляем все части
        for i, text_chunk in enumerate(messages):
            is_last = (i == len(messages) - 1)
            reply_markup = get_balance_menu_keyboard(final_mode or mode) if is_last else None

            await bot.send_message(
                chat_id=callback.from_user.id,
                text=text_chunk,
                reply_markup=reply_markup
            )
