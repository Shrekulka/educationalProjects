# src/bot/logic/menu_logic.py

from aiogram.types import Message, User

from src.bot.keyboards import get_main_menu_inline_keyboard
from src.bot.logic.greeting_logic import get_dynamic_greeting
from src.lexicon.lexicon_ru import LEXICON_RU


async def show_main_menu(message: Message, user: User, edit: bool = False):
    """
    Универсальная функция для отображения главного меню с умным динамическим приветствием
    и информативным основным текстом.
    """
    # 1. Получаем умное приветствие (эта часть не меняется).
    dynamic_greeting = get_dynamic_greeting(user.id)

    # 2. Собираем финальный текст из двух частей.
    greeting_part = f"👋 {dynamic_greeting}, {user.first_name}!\n\n"
    main_text_part = LEXICON_RU['main_menu_greeting']

    text = greeting_part + main_text_part

    # 3. Получаем клавиатуру.
    keyboard = get_main_menu_inline_keyboard()

    # 4. Логика отправки/редактирования сообщения остается прежней.
    if edit:
        try:
            # Сравниваем, чтобы не отправлять лишний запрос, если текст не изменился
            if message.text != text:
                await message.edit_text(text, reply_markup=keyboard)
        except Exception:
            pass
    else:
        await message.answer(text, reply_markup=keyboard)