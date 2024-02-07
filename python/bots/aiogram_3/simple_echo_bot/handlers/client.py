# simple_echo_bot/handlers/client.py
import traceback

from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from create_bot import bot, dp


# @dp.message(Command(commands=["start"]))
async def process_start_command(message: Message) -> None:
    """Handler for the "/start" command.

        Args:
            message (Message): Incoming message object.

        Returns:
            None
    """
    try:
        # Выводим апдейт в терминал
        print(message.model_dump_json(indent=4, exclude_none=True))
        # Отправка приветственного сообщения с именем пользователя
        await bot.send_message(message.from_user.id, f"Hello, {message.from_user.first_name}!"
                                                     f" 👋\nMy name is Echo-bot!\nWrite me something")
        # Удаление команды /start из чата
        await message.delete()
    except Exception as e:
        # Получение детализированной информации об ошибке
        detailed_send_message_error = traceback.format_exc()
        # Отправка сообщения об ошибке
        await message.reply(f"An error occurred: {str(e)}\n{detailed_send_message_error}")


# Этот хэндлер будет срабатывать на команду "/help"
# @dp.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:
    """Handler for the "/help" command.

        Args:
            message (Message): Incoming message object.

        Returns:
            None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отправляет в чат сообщение
    await message.answer("Write me something and in response\nI will send you your message")

# Хендлер для стикеров
# @dp.message()
async def handle_sticker(message: Message) -> None:
    """Handler for stickers.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отправляет ответ на сообщение
    await message.reply("Here's your sticker")
    # Отправляет в чат сообщение
    await message.answer_sticker(sticker=message.sticker.file_id)

# Хендлер для фото
# @dp.message(F.photo)
async def handle_photo(message: Message) -> None:
    """Handler for photos.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply("Here's your photo")
    # Отправляем фотографию в чат
    await message.answer_photo(photo=message.photo[-1].file_id)

# Хендлер для видео
# @dp.message(F.video)
async def handle_video(message: Message) -> None:
    """Handler for videos.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply("Here's your video")
    # Отправляем видео в чат
    await message.answer_video(video=message.video.file_id)

# Хендлер для видео-заметок
# @dp.message(F.video_note)
async def handle_video_note(message: Message) -> None:
    """Handler for video notes.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply("Here's your video message")
    # Отправляем видео-заметку в чат
    await message.answer_video_note(video_note=message.video_note.file_id)

# Хендлер для аудиофайлов
# @dp.message(F.audio)
async def handle_audio(message: Message) -> None:
    """Handler for audio files.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply("Here's your audio")
    # Отправляем аудиофайл в чат
    await message.answer_audio(audio=message.audio.file_id)

# Хендлер для голосовых сообщений
# @dp.message(F.voice)
async def handle_voice(message: Message) -> None:
    """Handler for voice messages.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply("Here's your voice message")
    # Отправляем голосовое сообщение в чат
    await message.answer_voice(voice=message.voice.file_id)

# Хендлер для документов
# @dp.message(F.document)
async def handle_document(message: Message) -> None:
    """Handler for documents.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply("Here's your document")
    # Отправляем документ в чат
    await message.answer_document(document=message.document.file_id)

# Хендлер для местоположений
# @dp.message(F.location)
async def handle_location(message: Message) -> None:
    """Handler for locations.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply("Here's your location")
    # Отправляем местоположение в чат
    await message.answer_location(latitude=message.location.latitude, longitude=message.location.longitude)


# Хендлер для контактов
# @dp.message(F.contact)
async def handle_contact(message: Message) -> None:
    """Handler for contacts.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply("Here's your contact")
    # Отправляем контакт в чат
    await message.answer_contact(phone_number=message.contact.phone_number, first_name=message.contact.first_name)


# У aiogram есть готовый метод, который отправит в чат копию сообщения, не зависимо от типа контента (Audio, Video,
# Sticker, Animation, Document, Voice).
# @dp.message()
async def send_copy_message(message: Message) -> None:
    """
       Handler to send a copy of the message.

       Args:
           message (Message): Incoming message object.

       Returns:
           None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    try:
        # Отвечаем на сообщение
        await message.reply("Here is your response from the send_copy handler")
        # Отправляем копию сообщения в чат
        await message.send_copy(chat_id=message.chat.id)  # await message.copy_to(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="This type of update is not supported by the send_copy method")


# @dp.message()
async def handle_other_messages(message: Message) -> None:
    """Handler for text messages.

    Args:
        message (Message): Incoming message object.

    Returns:
        None
    """
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply(text=f"You wrote me such a message:\n{message.text}\nand I write you the same thing")


# Регистрация всех хэндлеров и передача их в файл bot_telegram
# @dp.message()
def register_handlers_client(dp: Dispatcher) -> None:
    """
        Register all handlers for the client part of the bot.

        Args:
            dp: The Dispatcher instance.
    """
    # Регистрируем хэндлеры
    dp.message.register(process_start_command, Command(commands='start'))
    dp.message.register(process_help_command, Command(commands='help'))
    dp.message.register(handle_sticker, F.sticker)
    dp.message.register(handle_photo, F.photo)
    dp.message.register(handle_video, F.video)
    dp.message.register(handle_video_note, F.video_note)
    dp.message.register(handle_audio, F.audio)
    dp.message.register(handle_voice, F.voice)
    dp.message.register(handle_document, F.document)
    dp.message.register(handle_location, F.location)
    dp.message.register(handle_contact, F.contact)
    dp.message.register(send_copy_message)
    dp.message.register(handle_other_messages)
