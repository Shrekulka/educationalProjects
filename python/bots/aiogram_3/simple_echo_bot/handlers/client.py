# simple_echo_bot/handlers/client.py
import traceback

from aiogram import Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import Message, ChatMemberUpdated

from create_bot import bot
from logger import logger
from utils.client_utils import get_successful_payment_data, get_passport_data, get_invoice_data


########################################################################################################################
# 1) Хендлеры команд
########################################################################################################################
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


########################################################################################################################
# 2) Мультимедийные хендлеры (стикеры, фотографии, видео, аудио, голосовые сообщения и документы и т.д.)
########################################################################################################################
# Хендлер для стикеров
# @dp.message(F.sticker) или (F.content_type == 'sticker') или (F.content_type == ContentType.STICKER)
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
# @dp.message(F.photo) или (F.content_type == 'photo') или (F.content_type == ContentType.PHOTO)
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
# @dp.message(F.video) или (F.content_type == 'video') или (F.content_type == ContentType.VIDEO)
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
# @dp.message(F.video_note) или (F.content_type == 'video_note') или (F.content_type == ContentType.VIDEO_NOTE)
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
# @dp.message(F.audio) или (F.content_type == 'audio') или (F.content_type == ContentType.AUDIO)
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
# @dp.message(F.voice) или (F.content_type == 'voice') или (F.content_type == ContentType.VOICE)
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
# @dp.message(F.document) или (F.content_type == 'document') или (F.content_type == ContentType.DOCUMENT)
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
# @dp.message(F.location) или (F.content_type == 'location') или (F.content_type == ContentType.LOCATION)
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
# @dp.message(F.contact) или (F.content_type == 'contact') или (F.content_type == ContentType.CONTACT)
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


########################################################################################################################
# 3) Хендлеры для сообщений с различными условиями начала и окончания
########################################################################################################################
# Обработчик для текстовых сообщений с полным совпадением "Hello"
# @dp.message(F.text == 'Hello') или @dp.message(lambda message: message.text == 'Hello')
async def handle_exact_hello_message(message: Message):
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply("Here is your written word Hello")


# Обработчик для текстовых сообщений, начинающихся с "Hello"
# @dp.message(F.text.startswith('Hello')) или @dp.message(lambda message: message.text.startswith('Hello')
async def handle_starts_with_hello_message(message: Message):
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply(f"Here's your sentence that started with the word 'Hello':\n{message.text}")


# Обработчик для текстовых сообщений, не начинающихся с "Hello"
# @dp.message(~F.text.startswith('Hello')) или @dp.message(lambda message: not message.text.startswith('Hello')
async def handle_not_starts_with_hello_message(message: Message):
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply(f"Here's your sentence that doesn't start with 'Hello':\n{message.text}")


# Обработчик для текстовых сообщений, не заканчивающихся на "bot"
# @dp.message(~F.text.endswith('bot')) или @dp.message(lambda message: not message.text.endswith('bot')
async def handle_not_ends_with_bot_message(message: Message):
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply(f"Here's your sentence that doesn't end with 'bot':\n{message.text}")


# Хендлер, который будет пропускать только апдейты от пользователя с ID = 173901673
# @dp.message(F.from_user.id == 173901673)
# или @dp.message(lambda message: message.from_user.id == 173901673)
async def handle_specific_user(message: Message):
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply(f"The following message was sent from {message.from_user.id}:\n{message.text}")


# Хендлер, который будет пропускать только апдейты от админов из списка 193905674, 173901673, 144941561
# @dp.message(F.from_user.id.in_({193905674, 173901673, 144941561})
# или @dp.message(lambda message: message.from_user.id in {193905674, 173901673, 144941561})
async def handle_admins(message: Message):
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply(f"The following message was sent from an admin {message.from_user.id}: {message.text}")


# Хендлер, который будет пропускать апдейты любого типа, кроме фото, видео, аудио и документов
# @dp.message(~F.content_type.in_({ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT})
# или @dp.message(lambda message: not message.content_type in {ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO,
# ContentType.DOCUMENT}
async def handle_non_media(message: Message):
    # Выводим апдейт в терминал
    print(message.model_dump_json(indent=4, exclude_none=True))
    # Отвечаем на сообщение
    await message.reply(f"The following message was sent that is not a photo, video, audio or document: {message.text}")


########################################################################################################################
# 4) Комбинация различных хендлеров
########################################################################################################################
# Комбинированнный хэндлер будет срабатывать на тип контента "invoice", "passport_data" или "successful_payment"
# @dp.message(F.content_type.in_({'invoice', 'passport_data', 'successful_payment'})) или
# @dp.message(F.content_type.in_({ContentType.INVOICE, ContentType.PASSPORT_DATA, ContentType.SUCCESSFUL_PAYMENT}))
async def process_send_vovite(message: Message) -> None:
    """
        Handler for processing different types of messages: "invoice", "passport_data", "successful_payment".

        Args:
            message (Message): Incoming message object.

        Returns:
            None
    """
    # Если тип контента сообщения - 'invoice'
    if message.content_type == ContentType.INVOICE:  # if message.content_type == 'invoice'
        # Получаем данные о счете
        invoice_data = await get_invoice_data(message)
        # Отправляем данные о счете в чат
        await message.answer(text=f"Here's your invoice data: {invoice_data}")

    # Если тип контента сообщения - 'passport_data'
    elif message.content_type == ContentType.PASSPORT_DATA:  # elif message.content_type == 'passport_data':
        # Получаем данные паспорта
        passport_data = await get_passport_data(message)
        # Отправляем данные паспорта в чат
        await message.answer(text=f"Here's your passport data: {passport_data}")

    # Если тип контента сообщения - 'successful_payment'
    elif message.content_type == ContentType.SUCCESSFUL_PAYMENT:  # elif message.content_type == 'successful_payment':
        # Получаем данные об успешной оплате
        payment_data = await get_successful_payment_data(message)
        # Отправляем данные об успешной оплате в чат
        await message.answer(text=f"Here's your payment data: {payment_data}")


########################################################################################################################
# 5) Универсальный хендлер для отправки копий сообщений, не зависимо от типа контента
########################################################################################################################
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


########################################################################################################################
# 6) Хендлер для всех текстовых сообщений
########################################################################################################################
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


########################################################################################################################
# 7) Хендлеры для блокировки/разблокировки бота
########################################################################################################################
# Иногда возникает необходимость делать рассылку по пользователям, которые когда-либо запускали бота. Рекламную или с
# оповещением об изменении графика работы, или с полезной инфомацией, не суть. Мы где-то в базе данных сохраняли всех
# пользователей, когда они отправляли команду /start и теперь хотим их о чем-то оповестить. Но часть пользователей затем
# могла заблокировать бота и отправка сообщений таким пользователям приведет к ошибке. Бот из-за нее, скорее всего, не
# упадет, но нагрузка на ресурсы будет, если мы каждый раз будем пытаться отправлять таким пользователям сообщения.
# Правильнее вести учет статуса пользователей бота. То есть пришел апдейт от пользователя с командой /start - добавили
# пользователя в базу данных с пометкой Active, пришел апдейт о том, что пользователь заблокировал бота - поменяли ему
# статус на Inactive, разблокировал пользователь бота - снова Active и так далее. А когда делаем рассылку - смотрим на
# статус пользователя и пропускаем тех, кто Inactive. Уверен, идея понятна.

# Этот хэндлер будет срабатывать на блокировку бота пользователем
# @dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated) -> None:
    """
        Handler triggered when a user blocks the bot.

        Args:
            event (ChatMemberUpdated): Incoming chat member update event.

        Returns:
            None
    """
    logger.info(f"User {event.from_user.id} blocked the bot")


# Этот хэндлер будет срабатывать на разблокировку бота пользователем
# @dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def process_user_unblocked_bot(event: ChatMemberUpdated) -> None:
    """
    Handler triggered when a user unblocks the bot.

    Args:
        event (ChatMemberUpdated): The event of chat member update.

    Returns:
        None
    """
    logger.info(f"User {event.from_user.id} unblocked the bot")
    await bot.send_message(chat_id=event.from_user.id, text=f"{event.from_user.first_name}, Welcome back!")


########################################################################################################################
# 8) Хендлеры для
########################################################################################################################


########################################################################################################################
# Регистрация всех хэндлеров и передача их в файл bot_telegram
def register_handlers_client(dp: Dispatcher) -> None:
    """
        Register all handlers for the client part of the bot.

        Args:
            dp: The Dispatcher instance.
    """
    # 1) Хендлеры команд
    dp.message.register(process_start_command, Command(commands='start'))  # Обработка команды "/start"
    dp.message.register(process_help_command, Command(commands='help'))  # Обработка команды "/help"
    ####################################################################################################################
    # 2) Мультимедийные хендлеры (стикеры, фотографии, видео, аудио, голосовые сообщения и документы и т.д.)
    dp.message.register(handle_sticker, F.sticker)  # Обработка стикеров
    # (F.sticker) или (F.content_type == 'sticker') или (F.content_type == ContentType.STICKER)
    dp.message.register(handle_photo, F.photo)  # Обработка фотографий
    # (F.photo) или (F.content_type == 'photo') или (F.content_type == ContentType.PHOTO)
    dp.message.register(handle_video, F.video)  # Обработка видео
    # (F.video) или (F.content_type == 'video') или (F.content_type == ContentType.VIDEO)
    dp.message.register(handle_video_note, F.video_note)  # Обработка видео-заметок
    # (F.video_note) или (F.content_type == 'video_note') или (F.content_type == ContentType.VIDEO_NOTE)
    dp.message.register(handle_audio, F.audio)  # Обработка аудиосообщений
    # (F.audio) или (F.content_type == 'audio') или (F.content_type == ContentType.AUDIO)
    dp.message.register(handle_voice, F.voice)  # Обработка голосовых сообщений
    # (F.voice) или (F.content_type == 'voice') или (F.content_type == ContentType.VOICE)
    dp.message.register(handle_document, F.document)  # Обработка документов
    # (F.document) или (F.content_type == 'document') или (F.content_type == ContentType.DOCUMENT)
    dp.message.register(handle_location, F.location)  # Обработка местоположений
    # (F.location) или (F.content_type == 'location') или (F.content_type == ContentType.LOCATION)
    dp.message.register(handle_contact, F.contact)  # Обработка контактов
    # (F.contact) или (F.content_type == 'contact') или (F.content_type == ContentType.CONTACT)
    ####################################################################################################################
    # 3)  Хендлеры для сообщений с различными условиями начала и окончания
    dp.message.register(handle_exact_hello_message, F.text == 'Hello')  # Хендлер для текстовых сообщений,
    # начинающихся с "Hello"
    # или (lambda message: message.text == 'Hello')
    dp.message.register(handle_starts_with_hello_message, F.text.startswith('Hello'))  # Хендлер для текстовых
    # сообщений, начинающихся с "Hello"
    # или (lambda message: message.text.startswith('Hello')
    dp.message.register(handle_not_starts_with_hello_message, ~F.text.startswith('Hello'))  # Хендлер для текстовых
    # сообщений, не начинающихся с "Hello"
    # или (lambda message: not message.text.startswith('Hello')
    dp.message.register(handle_not_ends_with_bot_message, ~F.text.endswith('bot'))  # Обработчик для текстовых
    # сообщений,не заканчивающихся на "bot"
    # или (lambda message: not message.text.endswith('bot')
    dp.message.register(handle_specific_user, F.from_user.id == 173901673)  # Хендлер, который будет пропускать только
    # апдейты от пользователя с ID = 173901673
    # или (lambda message: message.from_user.id == 173901673)
    dp.message.register(handle_admins, F.from_user.id.in_({193905674, 173901673, 144941561}))  # Хендлер, который
    # будет пропускать только апдейты от админов из списка 193905674, 173901673, 144941561
    # или @ dp.message(lambda message: message.from_user.id in {193905674, 173901673, 144941561})
    dp.message.register(handle_non_media, ~F.content_type.in_({ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO,
                                                               ContentType.DOCUMENT}))  # Хендлер, который будет
    # пропускать апдейты любого типа, кроме фото, видео, аудио и документов
    # или @dp.message(lambda message: not message.content_type in {ContentType.PHOTO, ContentType.VIDEO,
    # ContentType.AUDIO, ContentType.DOCUMENT}

    ####################################################################################################################
    # 4) Комбинация различных хендлеров
    dp.message.register(process_send_vovite, (F.content_type.in_({'invoice', 'passport_data', 'successful_payment'})))
    # Обработка комбинированных сообщений о счетах, данным паспортов или успешных платежах
    # или (F.content_type.in_({ContentType.INVOICE, ContentType.PASSPORT_DATA, ContentType.SUCCESSFUL_PAYMENT}))
    ####################################################################################################################
    # 5) Универсальный хендлер для отправки копий сообщений, не зависимо от типа контента
    dp.message.register(send_copy_message)  # Отправка копии сообщения
    ####################################################################################################################
    # 6) Хендлер для всех текстовых сообщений
    dp.message.register(handle_other_messages)  # Обработка прочих текстовых сообщений
    ####################################################################################################################
    # 7) Хендлеры для блокировки/разблокировки бота
    dp.message.register(process_user_blocked_bot, ChatMemberUpdatedFilter(member_status_changed=KICKED))  # Обработчик
    # для события изменения статуса участника чата, когда участник заблокировал бота.
    dp.message.register(process_user_unblocked_bot, ChatMemberUpdatedFilter(member_status_changed=MEMBER))  # Обработчик
    # для события изменения статуса участника чата, когда участник разблокировал бота.
    ####################################################################################################################
