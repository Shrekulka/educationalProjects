# inter_exchange_arbitrage_bot/src/bot/keyboards/pagination_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_pagination_keyboard(
        current_page: int,
        total_pages: int,
        callback_prefix: str
) -> InlineKeyboardMarkup:
    """
    Создает универсальную клавиатуру пагинации.

    Args:
        current_page: Текущая страница (начиная с 0)
        total_pages: Общее количество страниц
        callback_prefix: Уникальный префикс для callback_data кнопок

    Returns:
        InlineKeyboardMarkup: Готовая клавиатура с кнопками пагинации
    """
    builder = InlineKeyboardBuilder()

    pagination_buttons = []

    # Кнопка "Назад" (если не первая страница)
    if current_page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"{callback_prefix}:{current_page - 1}"
            )
        )

    # Индикатор текущей страницы (если страниц больше одной)
    if total_pages > 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text=f"{current_page + 1}/{total_pages}",
                callback_data="noop"  # неактивная кнопка
            )
        )

    # Кнопка "Вперед" (если не последняя страница)
    if current_page < total_pages - 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"{callback_prefix}:{current_page + 1}"
            )
        )

    # Добавляем кнопки в одну строку
    if pagination_buttons:
        builder.row(*pagination_buttons)

    return builder.as_markup()
