# telegram_bot_book/handlers/user_handlers.py

from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon_ru import LEXICON
from logger_config import logger
from services.file_handling import book

# Инициализируем роутер уровня модуля
router: Router = Router()


# Обработчик команды "/start".
# Отправляет приветственное сообщение и добавляет пользователя в базу данных, если он отсутствует.
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
        Handler for the "/start" command.

        Args:
            message (types.Message): The user's message object.

        Returns:
            None

        Sends a welcome message and adds the user to the database if they are not already present.
    """
    # Выводим апдейт в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))

    # Отправка приветственного сообщения, хранящегося в словаре LEXICON по ключу "/start".
    await message.answer(LEXICON[message.text])

    # Проверка наличия пользователя в базе данных.
    if message.from_user.id not in users_db:
        # Если пользователя нет в базе данных, добавляем его. Это происходит путем создания новой записи в базе данных.
        # Ключом записи является ID пользователя (извлекаемый из объекта сообщения), а значением - глубокая копия
        # шаблонных данных для новых пользователей. Глубокая копия создается для того, чтобы избежать ссылочных проблем,
        # когда изменения одного пользователя могут повлиять на других.
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# Этот хэндлер будет срабатывать на команду "/help"
# Будет отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    """
        Handler for the "/help" command.

        Args:
            message (types.Message): The user's message object.

        Returns:
            None

        Sends a message to the user with a list of available commands in the bot.
    """
    # Выводим апдейт в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))

    await message.answer(LEXICON[message.text])


# Обработчик команды "/beginning".
# Этот обработчик срабатывает при получении команды "/beginning" от пользователя. Он устанавливает текущую страницу
# пользователя в начало книги (стр. №1) и отправляет пользователю текст первой страницы книги с кнопками пагинации.
@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message) -> None:
    """
        Handler for the "/beginning" command.

        Args:
            message (types.Message): The user's message object.

        Returns:
            None

        This handler triggers upon receiving the "/beginning" command from the user. It sets the user's current page
        to the beginning of the book (page №1) and sends the user the text of the first page of the book with
        pagination buttons.
    """
    # Выводим апдейт в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))

    # Устанавливаем текущую страницу пользователя в начало книги (страница №1).
    users_db[message.from_user.id]['page'] = 1

    # Получаем текст первой страницы книги.
    text = book[users_db[message.from_user.id]['page']]

    # Отправляем текст вместе с кнопками пагинации.
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'))


# Обработчик команды "/continue".
# Этот обработчик срабатывает при получении команды "/continue" от пользователя. Он отправляет пользователю страницу
# книги, на которой пользователь остановился в процессе взаимодействия с ботом.

@router.message(Command(commands='continue'))
async def process_continue_command(message: Message) -> None:
    """
        Handler for the "/continue" command.

        Args:
            message (types.Message): The user's message object.

        Returns:
            None

        This handler triggers upon receiving the "/continue" command from the user. It sends the user the page of the
        book where the user left off during interaction with the bot.
    """
    # Выводим апдейт в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))

    # Получаем текст страницы книги, на которой остановился пользователь.
    text = book[users_db[message.from_user.id]['page']]

    # Отправляем текст вместе с кнопками пагинации.
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'))


# Обработчик команды "/bookmarks".
# Этот обработчик срабатывает при получении команды "/bookmarks" от пользователя. Он отправляет пользователю список
# сохраненных закладок, если они есть, или сообщение о том, что у пользователя нет закладок.
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message) -> None:
    """
        Handler for the "/bookmarks" command.

        Args:
            message (types.Message): The user's message object.

        Returns:
            None

        This handler triggers upon receiving the "/bookmarks" command from the user. It sends the user a list of saved
        bookmarks if they exist, or a message indicating that the user has no bookmarks.
    """
    # Выводим апдейт в терминал
    logger.info(message.model_dump_json(indent=4, exclude_none=True))

    # Проверяем, есть ли у пользователя сохраненные закладки.
    if users_db[message.from_user.id]["bookmarks"]:
        # Если закладки есть, отправляем сообщение с клавиатурой закладок.
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]["bookmarks"]))
    else:
        # Если закладок нет, отправляем сообщение о их отсутствии.
        await message.answer(text=LEXICON['no_bookmarks'])


# # Обработчик callback-запроса нажатия на кнопку "Вперед" или "Назад"
# @router.callback_query(F.data.one_of(['forward', 'backward']))
# async def process_pagination_press(callback: CallbackQuery) -> None:
#     """
#         Handler for the pagination buttons forward and backward.
#
#         This handler triggers when the user presses the "Forward" or "Backward" button in the pagination.
#         It retrieves the current page number of the user and adjusts it based on the button pressed.
#         Then it retrieves the text of the new page of the book, updates the user's current page in the database,
#         and sends an edited message with the new page and updated pagination keyboard.
#
#         Args:
#             callback (types.CallbackQuery): The callback query object.
#
#         Returns:
#             None
#     """
#     # Выводим апдейт в терминал
#     logger.info(callback.model_dump_json(indent=4, exclude_none=True))
#
#     # Получаем текущую страницу пользователя
#     page_num = users_db[callback.from_user.id]['page']
#
#     # Увеличиваем или уменьшаем номер страницы в зависимости от нажатой кнопки
#     if callback.data == 'forward':
#         page_num += 1
#     else:
#         page_num -= 1
#
#     # Получаем текст новой страницы книги
#     text = book[page_num]
#
#     # Обновляем текущую страницу пользователя в базе данных
#     users_db[callback.from_user.id]['page'] = page_num
#
#     # Отправляем отредактированное сообщение с новой страницей и обновленной клавиатурой пагинации
#     await callback.message.edit_text(
#         text=text,
#         reply_markup=pagination_keyboard_wrapper(page_num))
#
#     # Отвечаем на callback-запрос, чтобы скрыть часики на кнопке
#     await callback.answer()
# Обработчик callback-запроса 'backward'.
# Этот обработчик срабатывает при нажатии пользователем кнопки "Назад".
@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery) -> None:
    """
    Обработчик callback-запроса 'backward'.

    Args:
        callback (types.CallbackQuery): Объект callback-запроса.

    Returns:
        None

    Этот обработчик срабатывает при нажатии пользователем кнопки "Назад".
    Если текущая страница пользователя больше 1, уменьшает номер текущей страницы
    пользователя на 1 и отправляет сообщение с новой страницей книги и обновленной
    клавиатурой пагинации. В противном случае ничего не делает.
    """
    # Выводим апдейт в терминал
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))

    # Проверяем, что текущая страница пользователя больше 1.
    if users_db[callback.from_user.id]['page'] > 1:
        # Если условие выполняется, уменьшаем номер текущей страницы пользователя на 1.
        users_db[callback.from_user.id]['page'] -= 1
        # Получаем текст новой страницы книги.
        text = book[users_db[callback.from_user.id]['page']]
        # Отправляем отредактированное сообщение с новой страницей и обновленной клавиатурой пагинации.
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'))
    # Отвечаем на callback-запрос, чтобы скрыть часики на кнопке.
    await callback.answer()


async def process_forward_press(callback: CallbackQuery) -> None:
    """
        Обработчик callback-запроса 'forward'.

        Args:
            callback (types.CallbackQuery): Объект callback-запроса.

        Returns:
            None

        Этот обработчик срабатывает при нажатии пользователем кнопки "Вперед".
        Если текущая страница пользователя меньше общего количества страниц книги,
        увеличивает номер текущей страницы пользователя на 1 и отправляет сообщение
        с новой страницей книги и обновленной клавиатурой пагинации.
        В противном случае ничего не делает.
    """
    # Проверяем, что текущая страница пользователя меньше общего количества страниц книги.
    if users_db[callback.from_user.id]['page'] < len(book):
        # Если условие выполняется, увеличиваем номер текущей страницы пользователя на 1.
        users_db[callback.from_user.id]['page'] += 1
        # Получаем текст новой страницы книги.
        text = book[users_db[callback.from_user.id]['page']]
        # Отправляем отредактированное сообщение с новой страницей и обновленной клавиатурой пагинации.
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'))
    # Отвечаем на callback-запрос, чтобы скрыть часики на кнопке.
    await callback.answer()


# Обработчик callback-запроса нажатия на кнопку с номером текущей страницы.
# Этот обработчик срабатывает при нажатии пользователем кнопки с номером текущей страницы книги.
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery) -> None:
    """
        Handler for the callback query of pressing the button with the current page number.

        Args:
            callback (types.CallbackQuery): The callback query object.

        Returns:
            None

        This handler triggers when the user presses the button with the current page number of the book.
        It adds the current page of the book to the user's bookmarks and responds to the callback query with a message
        confirming the successful addition of the page to the bookmarks.
    """
    # Выводим апдейт в терминал
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))

    # Добавляем текущую страницу книги в закладки пользователя.
    users_db[callback.from_user.id]['bookmarks'].add(users_db[callback.from_user.id]['page'])

    # Отвечаем на callback-запрос сообщением об успешном добавлении страницы в закладки.
    await callback.answer('Страница добавлена в закладки!')


# Обработчик callback-запроса нажатия на кнопку с закладкой из списка закладок.
# Этот обработчик срабатывает при нажатии пользователем кнопки с закладкой из списка закладок.
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery) -> None:
    """
        Handler for the callback query of pressing the button with a bookmark from the list of bookmarks.

        Args:
            callback (types.CallbackQuery): The callback query object.

        Returns:
            None

        This handler triggers when the user presses the button with a bookmark from the list of bookmarks.
        It retrieves the text of the book page by the bookmark number, updates the user's current page in the database,
        and sends a message with the text of the book page and the pagination keyboard.
    """
    # Выводим апдейт в терминал
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))

    # Получаем текст страницы книги по номеру закладки.
    text = book[int(callback.data)]

    # Обновляем текущую страницу пользователя в базе данных.
    users_db[callback.from_user.id]['page'] = int(callback.data)

    # Отправляем сообщение с текстом страницы книги и клавиатурой пагинации.
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'))

    # Отвечаем на callback-запрос.
    await callback.answer()


# Обработчик callback-запроса нажатия на кнопку "редактировать" под списком закладок.
# Этот обработчик срабатывает при нажатии пользователем кнопки "редактировать" под списком закладок.
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery) -> None:
    """
        Handler for the callback query of pressing the "edit" button below the list of bookmarks.

        Args:
            callback (types.CallbackQuery): The callback query object.

        Returns:
            None

        This handler triggers when the user presses the "edit" button below the list of bookmarks.
        It sends a message with the text "edit" and a keyboard for editing bookmarks.
    """
    # Выводим апдейт в терминал
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))

    # Отправляем сообщение с текстом "редактировать" и клавиатурой для редактирования закладок.
    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks'],
        reply_markup=create_edit_keyboard(
            *users_db[callback.from_user.id]["bookmarks"]))

    # Отвечаем на callback-запрос.
    await callback.answer()


# Обработчик callback-запроса нажатия на кнопку "отменить" во время работы со списком закладок
# (просмотр и редактирование). Этот обработчик срабатывает при нажатии пользователем кнопки "отменить" во время работы
# со списком закладок (просмотр и редактирование).
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery) -> None:
    """
        Handler for the callback query of pressing the "cancel" button while working with the list of bookmarks.

        Args:
            callback (types.CallbackQuery): The callback query object.

        Returns:
            None

        This handler triggers when the user presses the "cancel" button while working with the list of bookmarks
        (viewing and editing). It edits the message, sending the text "continue reading".
    """
    # Выводим апдейт в терминал
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))

    # Редактируем сообщение, отправляя текст "продолжить чтение".
    await callback.message.edit_text(text=LEXICON['cancel_text'])

    # Отвечаем на callback-запрос.
    await callback.answer()


# Обработчик callback-запроса нажатия на кнопку закладки для удаления из списка закладок.
# Этот обработчик срабатывает при нажатии пользователем кнопки с закладкой для удаления из списка закладок.
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery) -> None:
    """
        Handler for the callback query of pressing the bookmark button to remove it from the list of bookmarks.

        Args:
            callback (types.CallbackQuery): The callback query object.

        Returns:
            None

        This handler triggers when the user presses the button with a bookmark to remove it from the list of bookmarks.
        It removes the page number from the set of bookmarks of the current user.
        After removal, it checks for remaining bookmarks for the user. If there are any, it edits the message with
        bookmarks, sending a keyboard with the remaining bookmarks. If there are no more bookmarks, it replaces the
        message with "You don't have any bookmarks yet".
    """
    # Выводим апдейт в терминал
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))

    # Удаляем номер страницы из множества закладок текущего пользователя.
    users_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))

    # Вызываем обработчик для редактирования закладок
    await process_edit_press(callback)
