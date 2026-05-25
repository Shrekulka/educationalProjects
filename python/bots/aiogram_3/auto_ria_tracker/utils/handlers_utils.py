# auto_ria_tracker/utils/handlers_utils.py

from typing import Union, Optional
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.main_kb import markup_settings, markup_main
from database.database import db
from logger_config import logger


async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup=None):
    """
    Safely edits a message by updating its text and reply_markup.

    This function catches the `TelegramBadRequest` exception and prevents the error "message is not modified"
    from causing the process to fail. If a different Telegram error occurs, it is re-raised.

    Args:
        callback (CallbackQuery): The callback query that triggered the message edit.
        text (str): The new text to update the message with.
        reply_markup: The new keyboard markup to update the message with (optional).

    Raises:
        TelegramBadRequest: If an error occurs while editing the message, except for "message is not modified".
    """
    try:
        # Попытка обновить текст и клавиатуру сообщения
        await callback.message.edit_text(text=text, reply_markup=reply_markup)
    except TelegramBadRequest as e:
        # Проверка, что ошибка не связана с тем, что сообщение не изменено
        if "message is not modified" not in str(e):
            raise


async def format_settings_message(settings: dict) -> str:
    """
    Formats the settings message for the user.

    The settings message includes details about the user's car preferences, such as whether they want to
    import cars from the USA and whether they are interested in cars with accidents. This message is constructed
    using the LEXICON_RU dictionary for translation.

    Args:
        settings (dict): A dictionary containing the user's settings, including 'model', 'import_usa', and 'accident'.

    Returns:
        str: A formatted string containing the user's settings in a readable format.
    """
    # Получаем текстовые значения для import_usa и accident, используя LEXICON_RU
    import_usa_text = LEXICON_RU["yes" if settings['import_usa'] else "no"][0]
    accident_text = LEXICON_RU["yes" if settings['accident'] else "no"][0]

    # Формирование строки с настройками через словарь
    return LEXICON_RU["/settings"].format(model=settings['model'], import_usa_text=import_usa_text, accident_text=accident_text)


async def handle_setting_update(interface: Union[CallbackQuery, Message], setting_name: str, new_value,
                                state: FSMContext = None) -> None:
    """
    Handles updating a specific user setting and sending appropriate feedback based on whether the setting
    has been changed or not.

    This function processes both command and callback interactions, updating user settings in the database
    and sending a response message to the user. If the setting value has changed, it updates the value in the
    database and notifies the user with a confirmation message. If the setting has not changed, it informs
    the user that the setting remains the same.

    Args:
        interface (Union[CallbackQuery, Message]): The incoming interaction object, which can either be a
            callback query (from a button press) or a message (from a command).
        setting_name (str): The name of the setting to be updated. It indicates which setting is being changed
            (e.g., "import" for import status, "model" for car model, etc.).
        new_value (bool): The new value for the setting (True/False) indicating the updated status of the setting
            (e.g., Yes/No).
        state (FSMContext, optional): The state of the finite state machine (FSM) context. If provided, the state
            will be cleared after processing the setting update.

    Returns:
        None: This function doesn't return any values explicitly but sends a response message to the user
              based on the update result.

    Notes:
        - If the setting is successfully updated, a message will be sent to inform the user of the change,
          and if the setting is related to the model, the response will also include the model name.
        - If the setting value remains unchanged, a message will notify the user that no update occurred.
        - The function supports both callback queries (from inline buttons) and regular messages (from commands).
    """

    # Получаем ID пользователя из интерфейса (callback-запрос или сообщение)
    user_id = interface.from_user.id
    # Получаем текущие настройки пользователя из базы данных
    settings = db.get_user_settings(user_id)

    # Определяем имя настройки в базе данных и ключи для сообщений
    db_setting_name = 'import_usa' if setting_name == 'import' else setting_name

    # Если обновляется модель, используем специальный ключ для значений
    if setting_name == "model":
        value_key = "model_updated"
    # Формируем ключ для значения в зависимости от того, "yes" или "no"
    else:
        value_key = f"{setting_name}_{'yes' if new_value else 'no'}"

    # Ключ для сообщения, если значение не изменилось
    unchanged_key = f"{db_setting_name}_setting_unchanged"

    # Проверяем, изменилось ли значение
    if settings.get(db_setting_name) != new_value:
        # Если значение изменилось, обновляем настройку в базе данных
        db.update_user_settings(user_id, **{db_setting_name: new_value})
        # Обновляем настройки пользователя после изменения
        settings = db.get_user_settings(user_id)
        # Формируем текст сообщения с обновленными настройками
        text = await format_settings_message(settings)

        # Если входящий запрос — это callback-запрос
        if isinstance(interface, CallbackQuery):
            await safe_edit_message(interface, text, markup_settings)
            # Если обновляется модель, отправляем сообщение с названием модели
            if setting_name == "model":
                await interface.answer(LEXICON_RU[value_key].format(model=new_value))
            else:
                await interface.answer(LEXICON_RU[value_key])
        # Если входящий запрос — это сообщение
        else:
            if setting_name == "model":
                await interface.answer(f"{LEXICON_RU[value_key].format(model=new_value)}\n\n{text}",
                                       reply_markup=markup_settings)
            else:
                await interface.answer(f"{LEXICON_RU[value_key]}\n\n{text}", reply_markup=markup_settings)

        # Если передан state, очищаем состояние FSM
        if state:
            await state.clear()
    # Если значение не изменилось
    else:
        if isinstance(interface, CallbackQuery):
            await interface.answer(LEXICON_RU[unchanged_key])
        else:
            await interface.answer(LEXICON_RU[unchanged_key], reply_markup=markup_settings)


async def handle_monitoring(callback: CallbackQuery, car_service, action: str) -> None:
    """
    Handles the start or stop of monitoring for a specific user.

    This function attempts to start or stop the monitoring service based on the provided action. If the action is
    successful, it sends a response to the user with the status of the monitoring. If the monitoring is already in
    the desired state, it informs the user that no action is necessary.

    Args:
        callback (CallbackQuery): The callback query that triggered the monitoring action.
        car_service: The car service that handles the monitoring actions.
        action (str): The action to perform, either "start" or "stop".

    Returns:
        None
    """
    logger.info(f"Attempting to {action} monitoring for user {callback.from_user.id}")

    # Выполнение действия через сервис
    success = (car_service.start_monitoring() if action == "start" else car_service.stop_monitoring())

    # Проверка успеха действия
    if success:
        # Определение ключей для ответов
        message_key = "/monitoring_stopped" if action == "stop" else "/monitoring_started"
        success_key = "monitoring_success_stop" if action == "stop" else "monitoring_success_start"

        logger.info(f"Successfully {action}ed monitoring for user {callback.from_user.id}")

        # Обновление сообщения и отправка ответа
        await safe_edit_message(callback, text=LEXICON_RU[message_key], reply_markup=markup_main)
        await callback.answer(LEXICON_RU[success_key])
    else:
        # Определение ключа для уже активного/неактивного состояния
        already_key = "monitoring_already_stop" if action == "stop" else "monitoring_already_start"

        logger.warning(f"Monitoring already {action}ed for user {callback.from_user.id}")
        await callback.answer(LEXICON_RU[already_key], show_alert=True)


def parse_yes_no(value: str) -> Optional[bool]:
    """
    Converts a string representation of a 'yes' or 'no' response into a boolean value.

    This function takes a string input that represents a user's response (e.g., "yes", "да", "y", etc.) and
    converts it into a boolean value. It recognizes both affirmative (yes) and negative (no) responses based
    on predefined lexicons. If the response is recognized as 'yes', it returns `True`, and if it is recognized
    as 'no', it returns `False`. If the value is unrecognized, the function will return `None`.

    Args:
        value (str): The string value representing the user's response, which is expected to be either
                     an affirmative or negative response (e.g., "yes", "no", "да", "нет", "y", "n").

    Returns:
        Optional[bool]: The boolean value corresponding to the user's response:
                         - `True` for affirmative responses
                         - `False` for negative responses
                         - `None` if the value is unrecognized

    Notes:
        The function uses predefined dictionaries `LEXICON_RU["yes"]` and `LEXICON_RU["no"]` to check for valid
        affirmative and negative responses in multiple languages and formats. If the input is not found in
        either lexicon, it returns `None`.
    """
    # Проверка на положительные ответы
    if value in LEXICON_RU["yes"]:
        return True

    # Проверка на отрицательные ответы
    elif value in LEXICON_RU["no"]:
        return False

    # Если значение не распознано
    return None