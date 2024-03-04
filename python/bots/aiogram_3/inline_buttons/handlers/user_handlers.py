# inline_buttons/handlers/user_handlers.py

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.keyboards import keyboard
from lexicon.data import DATA
from lexicon.lexicon_ru import LEXICON_RU
from logger_config import logger

# Создание объекта маршрутизатора для обработки сообщений
router = Router()


# Этот хэндлер будет срабатывать на команду "/start" и отправлять в чат клавиатуру c url-кнопками
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
        Handler for the "/start" command.

        When receiving the "/start" command, sends a message with a keyboard
        containing URL buttons.

        Parameters:
            message (Message): The message object.

        Returns:
            None
    """
    # Вывод информации о сообщении в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))
    # Формируем текст сообщения, используя строку из словаря лексикона для команды "/start"
    # Метод .format() используется для подстановки значений переменных из словаря DATA в строку сообщения
    # group_name: значение переменной "group_name" из словаря DATA
    # user_id: значение переменной "user_id" из словаря DATA
    # channel_name: значение переменной "channel_name" из словаря DATA
    self_text = LEXICON_RU["/start"].format(group_name=DATA["group_name"], user_id=DATA["user_id"],
                                            channel_name=DATA["channel_name"])
    # Отправляем ответное сообщение пользователю
    # text: текст сообщения, который мы сформировали ранее
    # reply_markup: клавиатура, которую мы хотим прикрепить к сообщению
    # resize_keyboard: указываем, что размер клавиатуры должен быть изменен (True)
    await message.answer(text=self_text, reply_markup=keyboard, resize_keyboard=True)

