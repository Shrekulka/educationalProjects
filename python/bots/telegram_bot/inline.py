from config import TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import hashlib
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle

# в этом файле создаем экземпляры нашего бота
bot = Bot(token=TOKEN)

dp = Dispatcher(bot)

# Этот хендлер позваляет уловить обращение к боту
@dp.inline_handler()
# некое сбытие - query
async def inline_handler(query: types.InlineQuery):
    # в text попадает вводимый нами текст или "echo" - пока пользователь ничего не ввел
    text = query.query or "echo"
    # формируем ссылку
    link = 'https://ru.wikipedia.org/wiki/' + text
    # формируем идентификатор
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    # формируем, то что нужно отправить
    articles = [types.InlineQueryResultArticle(id=result_id, title='Статья Wikipedia: ', url=link,
                                               input_message_content=types.InputTextMessageContent(message_text=link))]
    # все это отправляем; cache_time = задержка от 1 до 60
    await query.answer(articles, cache_time=1, is_personal=True)


executor.start_polling(dp, skip_updates=True)
