# callback_data_factory/keyboards/keyboard_utils.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.goods_callback_factory import GoodsCallbackFactory


# Создаем объект кнопки для категории 1 с применением фабрики коллбэков
button_1 = InlineKeyboardButton(
    text='Категория 1',                  # Текст кнопки
    callback_data=GoodsCallbackFactory(  # Указываем callback_data с помощью фабрики
        category_id=1,                   # Идентификатор категории 1
        subcategory_id=0,                # Идентификатор подкатегории (в данном случае не используется)
        item_id=0                        # Идентификатор товара (в данном случае не используется)
    ).pack())                            # Формируем callback_data и упаковываем его


# Создаем объект кнопки для категории 2 с применением фабрики коллбэков
button_2 = InlineKeyboardButton(
    text='Категория 2',                  # Текст кнопки
    callback_data=GoodsCallbackFactory(  # Указываем callback_data с помощью фабрики
        category_id=2,                   # Идентификатор категории 2
        subcategory_id=0,                # Идентификатор подкатегории (в данном случае не используется)
        item_id=0                        # Идентификатор товара (в данном случае не используется)
    ).pack())                            # Формируем callback_data и упаковываем его


# Создаем объект клавиатуры, добавляя в список списки с кнопками
markup = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])  # Формируем массив массивов кнопок

