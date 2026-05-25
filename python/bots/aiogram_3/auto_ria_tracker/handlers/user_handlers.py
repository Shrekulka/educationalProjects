# auto_ria_tracker/handlers/user_handlers.py

from typing import Union
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.main_kb import markup_main, markup_settings
from lexicon.lexicon_ru import LEXICON_RU, ALLOWED_MODELS
from database import db
from utils.handlers_utils import (
    handle_setting_update,
    handle_monitoring,
    safe_edit_message,
    format_settings_message, parse_yes_no
)

# Инициализируем роутер
router = Router()


# Класс состояний
class ModelStates(StatesGroup):
    """State group for model selection process"""
    waiting_for_model = State()


@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
    Handle the /start command by sending a welcome message and initializing user settings.

    This function processes the incoming /start command, retrieves the user's settings from the database,
    and sends a welcome message along with the main keyboard markup.

    Args:
        message (Message): The incoming message object containing information about the /start command.

    Returns:
        None: Sends a welcome message along with the main keyboard markup to the user.
    """
    # Получаем ID чата
    chat_id = message.chat.id
    # Загружаем настройки пользователя из базы данных
    db.get_user_settings(message.from_user.id)
    # Отправляем приветственное сообщение с клавиатурой
    await message.answer(text=LEXICON_RU["/start"], reply_markup=markup_main)


@router.message(Command("help"))
@router.callback_query(lambda c: c.data == "help")
async def process_help(interface: Union[CallbackQuery, Message]) -> None:
    """
    Processes the /help command and the "help" callback query.

    This function handles both user messages containing the "/help" command
    and button clicks (callback queries) with the "help" identifier.
    It responds with a predefined help message and displays the main keyboard.

    Args:
        interface (Union[CallbackQuery, Message]): The user's input,
            either as a text command or a button interaction.

    Returns:
        None: This function does not return anything explicitly.
              It sends a response message with the main keyboard.
    """
    # Получаем текст сообщения помощи из словаря локализации
    text = LEXICON_RU["/help"]

    # Проверяем, является ли интерфейс объектом CallbackQuery (запрос нажатия кнопки)
    if isinstance(interface, CallbackQuery):
        # Редактируем существующее сообщение, заменяя его на текст помощи с основной клавиатурой
        await safe_edit_message(interface, text=text, reply_markup=markup_main)
        await interface.answer()
    else:
        # Если это обычное текстовое сообщение, отправляем ответ с текстом помощи и клавиатурой
        await interface.answer(text=text, reply_markup=markup_main)


@router.message(Command("settings"))
@router.callback_query(lambda c: c.data == "view_settings")
async def process_settings(interface: Union[CallbackQuery, Message]) -> None:
    """
    Processes the /settings command and the 'view_settings' callback query.

    This function handles user interactions related to settings.
    It retrieves the user's settings from the database, formats them,
    and displays them with the settings keyboard.

    Args:
        interface (Union[CallbackQuery, Message]): The incoming user interaction,
            either a command message or a callback query.

    Returns:
        None: This function does not return anything explicitly.
              It sends a response with the user's settings and an interactive keyboard.
    """
    # Загружаем настройки пользователя
    settings = db.get_user_settings(interface.from_user.id)
    # Форматируем сообщение с настройками
    text = await format_settings_message(settings)

    # Проверяем тип интерфейса
    if isinstance(interface, CallbackQuery):
        # Если это callback query, редактируем существующее сообщение
        await safe_edit_message(interface, text=text, reply_markup=markup_settings)
        # Завершаем callback
        await interface.answer()
    else:
        # Если это обычное сообщение, отправляем новое
        await interface.answer(text=text, reply_markup=markup_settings)


@router.message(Command("monitoring_started"))
@router.callback_query(lambda c: c.data == "start_monitoring")
async def process_start_monitoring(interface: Union[CallbackQuery, Message], car_service) -> None:
    """
    Handles the start monitoring callback.

    This function processes the start monitoring command and callback,
    initiating the monitoring process if not already started.

    Args:
        interface (Union[CallbackQuery, Message]): Incoming interaction object,
            which could be either a callback query or a message.
        car_service (Any): Car service instance used for starting the monitoring process.

    Returns:
        None: This function does not return anything explicitly,
              but sends a response message based on the monitoring status.
    """
    # Если входящий объект — это callback-запрос
    if isinstance(interface, CallbackQuery):
        # Обрабатываем мониторинг через callback
        await handle_monitoring(interface, car_service, "start")
    # Если входящий объект — это сообщение
    else:
        # Пытаемся запустить мониторинг
        success = car_service.start_monitoring()
        # Если мониторинг успешно начался
        if success:
            await interface.answer(text=LEXICON_RU["/monitoring_started"], reply_markup=markup_main)
        # Если мониторинг уже был начат
        else:
            await interface.answer(text=LEXICON_RU["monitoring_already_start"], reply_markup=markup_main)


@router.message(Command("monitoring_stopped"))
@router.callback_query(lambda c: c.data == "stop_monitoring")
async def process_stop_monitoring(interface: Union[CallbackQuery, Message], car_service) -> None:
    """
    Handles the stop monitoring callback.

    This function processes the stop monitoring command and callback,
    stopping the monitoring process if it was previously started.

    Args:
        interface (Union[CallbackQuery, Message]): Incoming interaction object,
            which could be either a callback query or a message.
        car_service (Any): Car service instance used for stopping the monitoring process.

    Returns:
        None: This function does not return anything explicitly,
              but sends a response message based on the monitoring status.
    """
    # Если входящий объект — это callback-запрос
    if isinstance(interface, CallbackQuery):
        # Обрабатываем остановку мониторинга через callback
        await handle_monitoring(interface, car_service, "stop")
    # Если входящий объект — это сообщение
    else:
        # Пытаемся остановить мониторинг
        success = car_service.stop_monitoring()
        # Если мониторинг успешно остановлен
        if success:
            await interface.answer(text=LEXICON_RU["/monitoring_stopped"], reply_markup=markup_main)
        # Если мониторинг уже был остановлен
        else:
            await interface.answer(text=LEXICON_RU["monitoring_already_stop"], reply_markup=markup_main)


@router.message(Command("set_import"))
@router.callback_query(lambda c: c.data.startswith("set_import:"))
async def process_import_setting(interface: Union[CallbackQuery, Message]) -> None:
    """
    Handler for setting import status.

    This handler processes commands and callback queries related to setting the import status.
    The import setting indicates whether the car is imported from the USA.

    Args:
        interface (Union[CallbackQuery, Message]): The incoming interface object,
            which can be either a callback query or a message.

    Returns:
        None: The function does not return any values, but sends a message with the updated setting.
    """
    # Если входящий объект — это callback-запрос
    if isinstance(interface, CallbackQuery):
        # Обработка через кнопки (извлекаем тип и значение из данных callback)
        setting_type, value = interface.data.split(":")
        # Устанавливаем новое значение в зависимости от значения кнопки
        new_value = value == "yes"
        # Обновляем настройку импорта
        await handle_setting_update(interface, "import", new_value)
    else:
        # Если входящий объект — это сообщение (обрабатываем команду)
        parts = interface.text.split(maxsplit=1)
        if len(parts) < 2:
            # Если значение не указано, запрашиваем его
            await interface.answer(text=LEXICON_RU["set_import_usage"], reply_markup=markup_settings)
            return
        # Парсим значение из команды (указанное в lexicon_ru.py)
        value = parse_yes_no(parts[1])
        # Если значение неверное, сообщаем об ошибке
        if value is None:
            await interface.answer(text=LEXICON_RU["invalid_value"], reply_markup=markup_settings)
            return
        # Обновляем настройку импорта с выбранным значением
        await handle_setting_update(interface, "import", value)


@router.message(Command("set_accident"))
@router.callback_query(lambda c: c.data.startswith("set_accident:"))
async def process_accident_setting(interface: Union[CallbackQuery, Message]) -> None:
    """
    Handler for setting accident status.

    This handler processes commands and callback queries related to setting the accident status of a car.
    The setting indicates whether the car has been in an accident.

    Args:
        interface (Union[CallbackQuery, Message]): The incoming interface object,
            which can be either a callback query or a message.

    Returns:
        None: The function does not return any values, but sends a message with the updated setting.
    """
    # Если входящий объект — это callback-запрос
    if isinstance(interface, CallbackQuery):
        # Обработка через кнопки (извлекаем тип и значение из данных callback)
        setting_type, value = interface.data.split(":")
        # Устанавливаем новое значение в зависимости от значения кнопки
        new_value = value == "yes"
        # Обновляем настройку аварии
        await handle_setting_update(interface, "accident", new_value)
    else:
        # Если входящий объект — это сообщение (обрабатываем команду)
        parts = interface.text.split(maxsplit=1)
        if len(parts) < 2:
            # Если значение не указано, запрашиваем его
            await interface.answer(text=LEXICON_RU["set_accident_usage"],reply_markup=markup_settings)
            return
        # Парсим значение из команды (указанное в lexicon_ru.py)
        value = parse_yes_no(parts[1])
        # Если значение неверное, сообщаем об ошибке
        if value is None:
            await interface.answer(text=LEXICON_RU["invalid_value"], reply_markup=markup_settings)
            return
        # Обновляем настройку аварии с выбранным значением
        await handle_setting_update(interface, "accident", value)


@router.callback_query(lambda c: c.data == "set_model")
@router.message(Command("set_model"))
async def process_set_model(interface: Union[CallbackQuery, Message], state: FSMContext) -> None:
    """
    Handle the setting of a car model (specifically for Toyota) through both callback query and command.

    This function handles both the callback query triggered by the user selecting the "set_model" option
    and the message command where the user specifies the model they want to set.

    Args:
        interface (Union[CallbackQuery, Message]): The incoming interface object, which can be either a callback query
            or a message containing the user's input.
        state (FSMContext): The finite state machine context used for managing the state of the user interaction.

    Returns:
        None: The function does not return any value, but updates the state or sends responses to the user as needed.
    """
    # Если это callback запрос
    if isinstance(interface, CallbackQuery):
        # Редактируем сообщение с выбором модели
        await safe_edit_message(interface, text=LEXICON_RU["choose_model"], reply_markup=markup_settings)
        # Устанавливаем состояние ожидания модели
        await state.set_state(ModelStates.waiting_for_model)
        # Отправляем предупреждение
        await interface.answer(text=LEXICON_RU["model_example"], show_alert=True)
    else:
        # Разделяем текст сообщения
        parts = interface.text.split(maxsplit=1)
        # Если нет второго слова (модели)
        if len(parts) < 2:
            # Запрашиваем модель
            await interface.answer(text=LEXICON_RU["choose_model"], reply_markup=markup_settings)
            # Устанавливаем состояние ожидания модели
            await state.set_state(ModelStates.waiting_for_model)
            return
        # Обрабатываем введенную модель
        await handle_model_input(interface, parts[1].strip(), state)


@router.message(ModelStates.waiting_for_model)
async def handle_model_input(message: Message, state: FSMContext) -> None:
    """
    Handle the user's input for car model selection.

    This function processes the model input from the user, checks if it is an allowed model,
    and updates the model setting accordingly. If the model is invalid, it informs the user.

    Args:
        message (Message): The message containing the car model name provided by the user.
        state (FSMContext): The finite state machine context used for managing the state of the user interaction.

    Returns:
        None: Updates the model setting or informs the user if the input model is invalid.
    """
    # Получаем текст модели в нижнем регистре
    model = message.text.strip().lower()
    # Если модель разрешена
    if model in ALLOWED_MODELS:
        # Обновляем настройку модели
        await handle_setting_update(message, "model", model.capitalize(), state)
    else:
        # Сообщаем об ошибке
        await message.answer(text=LEXICON_RU["invalid_model"], reply_markup=markup_settings)


@router.callback_query(lambda c: c.data == "back_to_main")
async def process_back_button(callback: CallbackQuery) -> None:
    """
    Handle the "Back to main menu" callback.

    This function processes the callback triggered when the user presses the "Back to main menu" button.
    It updates the message with the main menu text and markup, effectively returning the user to the main menu.

    Args:
        callback (CallbackQuery): The callback query object containing the data triggered by the user's interaction.

    Returns:
        None: The function does not return any value, but it updates the message and terminates the callback.
    """
    # Отправляем сообщение с главного меню
    await safe_edit_message(callback, text=LEXICON_RU["/start"], reply_markup=markup_main)
    # Завершаем callback
    await callback.answer()


@router.message()
async def process_other_messages(message: Message) -> None:
    """
    Handle any unrecognized messages.

    This function processes messages that do not match any predefined commands or expected inputs. It responds
    with an error message, notifying the user that the command was not recognized, and provides the main menu.

    Args:
        message (Message): The incoming message object containing the user's text.

    Returns:
        None: The function does not return any value but sends an error message and the main menu markup.
    """
    # Сообщаем, что команда не распознана
    await message.answer(text=LEXICON_RU["no_command"], reply_markup=markup_main)
