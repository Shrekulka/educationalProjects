from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from aiogram.types import InlineKeyboardMarkup  # импортируем клавиатуру
from aiogram.types import InlineKeyboardButton  # импортируем кнопку
from aiogram.dispatcher.filters import Text

# в этом файле создаем экземпляры нашего бота
bot = Bot(token=TOKEN)
# (storage = storage) - место, где будем хранить ответы от пользователя
dp = Dispatcher(bot)

# Заводим словарь для подсчета голосов
answ = dict()

# Книпки ссылки
# инициализируем класс клавиатуры
# (row_width=1) - прописываем ширину ряда(по две кнопки в ряд)
urlkb = InlineKeyboardMarkup(row_width=2)
# Создаем под каждую кнопку переменную
# (text='Ссылка', url='https://youtube.com') - записываем название этой кнопки и url - ссылка куда приведет эта кнопка
urlButton = InlineKeyboardButton(text='Ссылка', url='https://youtube.com')
# делаем вторую кнопку
urlButton2 = InlineKeyboardButton(text='Ссылка2', url='https://google.com')
# формируем список кнопок
x = [InlineKeyboardButton(text='Ссылка3', url='https://google.com'),
     InlineKeyboardButton(text='Ссылка4', url='https://google.com'),
     InlineKeyboardButton(text='Ссылка5', url='https://google.com')]
# методом add добавляем эти кнопки
# методом row(*x) добавляем список кнопок распаковывая его - вывод три кнопки подряд идущие
# ограничение ширины ряда (InlineKeyboardMarkup(row_width=2)) не распространяется на метод row; т.е. сколько передадим
# кнопок метод row попытается их добавить в один ряд
# 6-тая кнопка вывелась с новой строчки, т.к. метод row(*x) исчерпал весь лимит расположения кнопок в один ряд и метод
# insert не добавил кнопку в один ряд, как это обычно происходит
urlkb.add(urlButton, urlButton2).row(*x).insert(InlineKeyboardButton(text='Ссылка6', url='https://google.com'))


# пишем хендлер, что бы вызвать эту клавиатуру
@dp.message_handler(commands='ссылки')
async def url_command(message: types.Message):
    # отвечаем на комманду ссылки; отправкой этой клавиатуры - reply_markup=urlkb
    await message.answer('Ссылочки', reply_markup=urlkb)


# колбек кнопки
# создаем клавиатуру шириной в одну кнопку и сразу же добавляем через метод
# в поле text вводим текст, который будет отображаться на самой кнопке
# во второй параметр (callback_data=) передаем строку. Это строка отправляется незримо для пользователя нашему боту,
# которую мы и улавливаем специальным хендлером. Сюда мы можем передать данные на основе которых будет работать код
inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Нажми меня', callback_data='www'))


# пишем хендлер, что бы вызвать эту клавиатуру
@dp.message_handler(commands='Test')
async def test_command(message: types.Message):
    # отвечаем на комманду ссылки; отправкой этой клавиатуры - reply_markup=inkb
    await message.answer('Инлайн кнопка', reply_markup=inkb)


# пишем специальный хендлер, что бы поймать вот это событие - (callback_data='www')
# передаем то событие на кторое хендлер должен отриагировать (text='www')
@dp.callback_query_handlers(text='www')
# асинхронная ф-ция, в нее передаем анатацию типа (callback: types.CallbackQuery)
async def www_call(callback: types.CallbackQuery):
    # здесь отвечаем на нажатие кнопки - текст появляется в чате ввиде сплавающего окошка, которое потом исчезает
    # await callback.answer('Нажата инлайн кнопка') - текст появляется в чате ввиде сплавающего окошка, которое потом
    # исчезает
    # или вот так
    await callback.message.answer('Нажата инлайн кнопка')  # - теперь бот отправляет ответ в чат в виде сообщения
    await callback.answer()  # для await callback.message.answer('Нажата инлайн кнопка') автоматически подтверждаем  и
    # убраем часики
    # await callback.answer('Нажата инлайн кнопка', show_alert=True) - появится специальное всплывающее окно с
    # сообщением - Нажата инлайн кнопка, которое нужно будет подтвердить - в это сообщение вмещается до 200 символов


########################################################################################################################
# Для обработки нескольких инлайн кнопок

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='like', callback_data='like_1'),
                                             InlineKeyboardButton(text='dislike', callback_data='like_-1'))


@dp.message_handler(commands='Test')
async def test_command(message: types.Message):
    await message.answer('За видео про деплой бота', reply_markup=inkb)


@dp.callback_query_handlers(Text(startswith='like_'))
async def www_call(callback: types.CallbackQuery):
    # разбиваем по зазделителю ('_') берем по индексу 1 и это будет 1 или -1 и приводим к типу int
    res = int(callback.data.split('_')[1])

    # проверка, что бы пользователь не мог проголосовать несколько раз
    if f'{callback.from_user.id}' not in answ:
        answ[f'{callback.from_user.id}'] = res
        await callback.answer('Вы проголосовали')
    else:
        await callback.answer('Вы уже проголосовали', show_alert=True)


########################################################################################################################

# старт нашего поллинга (старт входа)
executor.start_polling(dp, skip_updates=True)
