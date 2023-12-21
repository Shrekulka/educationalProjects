# pythonProject_1/telegram_integration_planfix.py

from typing import Optional

import aiohttp
from aiocache import SimpleMemoryCache
from telethon import TelegramClient

from config import planfix_api_url, planfix_api_key, telegram_api_id, telegram_api_hash
from flask_logging import logger

# Асинхронный кэш для хранения данных о сообщениях
messages: SimpleMemoryCache = SimpleMemoryCache()


# Асинхронная функция для отправки сообщения из Telegram в Planfix и обработки ответа
async def send_telegram_message_to_planfix(update, client_data, telegram_message_id) -> None:
    """Sends a message from Telegram to Planfix and handles the response.

    Args:
        update: Telethon update object.
        client_data: Client data.
        telegram_message_id: Telegram message ID.

    Returns:
        None
    """
    try:
        # Проверка наличия объекта update или update.message
        if update is None or update.message is None:
            logger.warning("Received None in update or update.message in send_telegram_message_to_planfix")
            return

        logger.debug(f"Full update: {update}")
        logger.debug(f"Client data: {client_data}")
        logger.debug(f"Telegram message ID: {telegram_message_id}")

        # Проверка наличия текста в сообщении
        if hasattr(update.message, 'text') and update.message.text:
            message_text = update.message.text
            logger.debug(f"Type of message_text: {type(message_text)}, Message text: {message_text}")
        else:
            logger.warning("No text attribute found in update.message")
            return

        # Отправка сообщения в Planfix и получение идентификатора сообщения
        planfix_message_id = await send_message_to_planfix(client_data, message_text)
        logger.info(f"Planfix message ID: {planfix_message_id}")

        # Сохранение соответствия идентификаторов сообщений между Telegram и Planfix
        await messages.set(planfix_message_id, {
            "telegram_message_id": telegram_message_id,
            "telegram_chat_id": update.message.chat_id
        })
        logger.info(f"Mapping saved for Planfix message ID: {planfix_message_id}")

        # Идентификатор чата в Telegram
        telegram_chat_id = update.message.chat_id
        # Вызов асинхронной функции отправки ответа из Planfix в Telegram
        await send_response_to_telegram(planfix_message_id, telegram_chat_id)
    except Exception as e:
        await handle_error(e)


# Асинхронная функция для отправки ответа из Planfix в Telegram
async def send_response_to_telegram(planfix_message_id, telegram_chat_id) -> None:
    """Sends a response from Planfix to Telegram.

    Args:
        planfix_message_id: Planfix message ID.
        telegram_chat_id: Telegram chat ID.

    Returns:
        None
    """
    try:
        # Получение текста ответа из Planfix асинхронным образом
        response_text_task = get_planfix_response(planfix_message_id)

        # Использование клиента Telegram для отправки ответа
        async with TelegramClient('session_name', telegram_api_id, telegram_api_hash) as telegram_client:
            response_text = await response_text_task

            # Отправка текста ответа в указанный чат Telegram
            await telegram_client.send_message(telegram_chat_id, response_text)
            logger.info(f"Sent response to Telegram chat {telegram_chat_id}")
    except Exception as e:
        logger.error(f"Error sending response to Telegram: {e}")
        await handle_error(e)


# Асинхронная функция для получения идентификатора сообщения в Telegram из соответствия
async def get_telegram_id_from_mapping(planfix_message_id) -> Optional[int]:
    """Gets the Telegram message ID from the mapping.

    Args:
        planfix_message_id: Planfix message ID.

    Returns:
        Optional[int]: Telegram message ID if found, otherwise None.
    """
    try:
        # Получение данных из асинхронного кеша по идентификатору сообщения в Planfix
        result = await messages.get(planfix_message_id, {})

        # Извлечение идентификатора сообщения в Telegram из полученных данных
        telegram_message_id = result.get("telegram_message_id", None)
        logger.debug(f"Telegram Message ID retrieved successfully. Planfix Message ID: {planfix_message_id}, "
                     f"Telegram Message ID: {telegram_message_id}")
        return telegram_message_id
    except Exception as e:
        logger.error(f"Error in get_telegram_id_from_mapping: {e}")
        await handle_error(e)


# Асинхронная функция для получения идентификатора чата в Telegram из соответствия
async def get_chat_id_by_message(telegram_message_id) -> Optional[int]:
    """Gets the Telegram chat ID from the mapping.

    Args:
        telegram_message_id: Telegram message ID.

    Returns:
        Optional[int]: Telegram chat ID if found, otherwise None.
    """
    try:
        # Получение данных из асинхронного кеша по идентификатору сообщения в Telegram
        result = await messages.get(telegram_message_id, {})

        # Извлечение идентификатора чата в Telegram из полученных данных
        telegram_chat_id = result.get("telegram_chat_id", None)
        logger.debug(
            f"Chat ID retrieved successfully. Telegram Message ID: {telegram_message_id}, "
            f"Telegram Chat ID: {telegram_chat_id}")
        return telegram_chat_id
    except Exception as e:
        logger.error(f"Error in get_chat_id_by_message: {e}")
        await handle_error(e)


# Асинхронная функция для отправки сообщения в Planfix
async def send_message_to_planfix(client_data, message) -> int:
    """Sends a message to Planfix.

    Args:
        client_data: Client data.
        message: Text of the message.

    Returns:
        int: Planfix message ID.
    """
    try:
        # Установка заголовков для авторизации в Planfix
        headers = {"Authorization": f"Bearer {planfix_api_key}"}

        # Подготовка данных для отправки
        data = {"client_id": client_data["client_id"], "message": message}

        # Использование aiohttp для отправки запроса POST к Planfix API
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{planfix_api_url}/messages", headers=headers, json=data) as response:
                # Проверка статуса ответа
                response.raise_for_status()
                # Получение идентификатора сообщения из ответа Planfix API
                response_json = await response.json()
                planfix_message_id = response_json["id"]
                logger.debug(f"Planfix message sent successfully. Message ID: {planfix_message_id}")
                return planfix_message_id
    except aiohttp.ClientError as e:
        logger.error(f"Error in send_message_to_planfix: {e}")
        await handle_error(e)


# Асинхронная функция для получения ответа от Planfix по идентификатору сообщения
async def get_planfix_response(message_id) -> str:
    """Gets the response from Planfix by message ID.

    Args:
        message_id: Planfix message ID.

    Returns:
        str: Text of the Planfix response.
    """
    try:
        # Установка заголовков для авторизации в Planfix
        headers = {"Authorization": f"Bearer {planfix_api_key}"}

        # Использование aiohttp для отправки запроса GET к Planfix API
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{planfix_api_url}/messages/{message_id}", headers=headers) as response:
                # Проверка статуса ответа
                response.raise_for_status()
                # Извлечение текста ответа из JSON-ответа
                response_text = (await response.json())["text"]
                logger.debug(f"Planfix response text for message ID {message_id}: {response_text}")
                return response_text
    except aiohttp.ClientError as e:
        logger.error(f"Error in get_planfix_response for message ID {message_id}: {e}")
        await handle_error(e)


# Асинхронная функция для обработки ошибки
async def handle_error(error) -> None:
    """Handles an error.

    Args:
        error: Error object.

    Returns:
        None
    """
    if error is not None:
        logger.error(f"An error occurred: {error}")
    else:
        logger.warning("Received None as an error object in handle_error")
