# callback_data_factory/handlers/user_handlers.py

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from filters.goods_callback_factory import GoodsCallbackFactory
from keyboards.keyboard_utils import markup
from logger_config import logger

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер будет срабатывать на команду /start и отправлять пользователю сообщение с клавиатурой
@router.message(CommandStart())                     # Декоратор, указывающий на команду /start
async def process_start_command(message: Message):  # Асинхронная функция-обработчик
    await message.answer(                           # Отправляем ответное сообщение
        text='Вот такая клавиатура',                # Текст сообщения
        reply_markup=markup)                        # Клавиатура, переданная как параметр ответного сообщения


# Этот хэндлер будет срабатывать на нажатие любой инлайн кнопки и распечатывать апдейт в терминал
# Декоратор с фильтром, указывающий на обработчик нажатия кнопок, отфильтрованных с помощью GoodsCallbackFactory
@router.callback_query(GoodsCallbackFactory.filter())
# Асинхронная функция-обработчик с параметрами callback и callback_data
async def process_category_press(callback: CallbackQuery, callback_data: GoodsCallbackFactory):
    await callback.message.answer(text=callback_data.pack())  # Отправляем ответное сообщение с данными из callback_data
    await callback.answer()                               # Отправка подтверждения обработки нажатия кнопки пользователю


# Ну, а если мы хотим поймать только нажатие на первую кнопку ("Категория 1"), то нам в очередной раз может помочь
# магический фильтр и хэндлер может быть таким:
@router.callback_query(GoodsCallbackFactory.filter(F.category_id == 1))
async def process_category_press(callback: CallbackQuery,
                                 callback_data: GoodsCallbackFactory):
    await callback.message.answer(text=callback_data.pack())  # Отправляем ответное сообщение с данными из callback_data
    await callback.answer()                               # Отправка подтверждения обработки нажатия кнопки пользователю


# Есть удобные способы извлечения данных из callback_data. Будем принимать нажатие на любую кнопку. А пользователю мы
# отправим форматированный текст с данными, извлеченными из callback_data.

# Этот хэндлер будет срабатывать на нажатие любой инлайн кнопки и отправлять в чат форматированный ответ с данными
# из callback_data
# Декоратор с фильтром, указывающий на обработчик нажатия кнопок, отфильтрованных с помощью GoodsCallbackFactory
@router.callback_query(GoodsCallbackFactory.filter())
# Асинхронная функция-обработчик с параметрами callback и callback_data
async def process_category_press(callback: CallbackQuery, callback_data: GoodsCallbackFactory):
    await callback.message.answer(                                      # Отправляем ответное сообщение
        text=f'Категория товаров: {callback_data.category_id}\n'        # Текст с информацией о категории товаров
             f'Подкатегория товаров: {callback_data.subcategory_id}\n'  # Текст с информацией о подкатегории товаров
             f'Товар: {callback_data.item_id}')                         # Текст с информацией о товаре
    await callback.answer()                               # Отправка подтверждения обработки нажатия кнопки пользователю


# Отличие между двумя хэндлерами заключается в том, что первый хэндлер использует фильтр, определенный с помощью
# GoodsCallbackFactory.filter(), который фильтрует callback_data, чтобы хэндлер реагировал только на определенные типы
# callback_data, соответствующие указанным критериям. Второй хэндлер не использует фильтр и реагирует на все
# callback_data без ограничений.


# Этот хэндлер будет срабатывать на нажатие любой инлайн кнопки и распечатывать апдейт в терминал
@router.callback_query()                                          # Декоратор, указывающий на обработчик нажатия кнопок
async def process_any_inline_button_press(callback: CallbackQuery):     # Асинхронная функция-обработчик
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))  # Вывод информации об апдейте в терминал
    await callback.answer()                               # Отправка подтверждения обработки нажатия кнопки пользователю
