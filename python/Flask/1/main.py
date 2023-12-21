# pythonProject_1/main.py

import asyncio
import secrets
import uuid
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from functools import lru_cache, partial
from typing import Dict, Union, Tuple, List, Any

from flask import Flask, request, jsonify, Response
from telethon import TelegramClient, events

from config import telegram_api_id, telegram_api_hash
from flask_logging import logger
from telegram_integration_planfix import send_message_to_planfix, send_telegram_message_to_planfix

# Инициализация Flask приложения
app = Flask(__name__)

# Инициализация ThreadPoolExecutor для выполнения задач в отдельных потоках
executor = ThreadPoolExecutor()


# Декоратор lru_cache для функции get_clients, который кэширует результаты вызовов
@lru_cache(maxsize=None)  # None означает неограниченный размер кэша
def get_clients() -> Dict:
    """Get clients dictionary."""
    return {}


# Получение интернируемого объекта словаря клиентов
clients = get_clients()

# Настройка Telethon с использованием TelegramClient
client = TelegramClient('bot_session', telegram_api_id, telegram_api_hash)


# Определение перечисления (Enum) ClientStatus, представляющего статусы клиента
class ClientStatus(Enum):
    ONLINE = 'Online'
    OFFLINE = 'Offline'


# Определение перечисления (Enum) MessageType, представляющего типы сообщений
class MessageType(Enum):
    TELEGRAM = 'Telegram'
    PLANFIX = 'Planfix'


# Обработчик ошибок для исключений типа Exception
@app.errorhandler(Exception)
def handle_error(error: Exception) -> Tuple[Response, int]:
    """Handle errors.

    Args:
        error (Exception): The exception object.

    Returns:
        Tuple[Response, int]: A tuple containing a JSON response and an HTTP status code.
    """
    # Логирование ошибки
    logger.error(f"An error occurred: {error}")
    # Возврат JSON-ответа с описанием ошибки и кодом состояния 500 (Internal Server Error)
    return jsonify({'error': str(error)}), 500


# Асинхронная функция для запуска процесса polling с использованием Telethon
async def run_polling() -> None:
    """Run Telethon polling."""
    try:
        logger.info("Starting Telethon polling...")
        # Асинхронное подключение к Telegram
        await client.connect()
        # Асинхронный запуск polling до отключения
        await client.run_until_disconnected()
    except Exception as error:
        logger.error(f"Error in Telethon polling: {error}")


# Асинхронная функция для верификации ключа сессии клиента
async def verify_session_key(client_data: Dict[str, Union[str, Dict]]) -> bool:
    """Verify session key.

    Args:
        client_data (Dict[str, Union[str, Dict]]): Client data containing the session key.

    Returns:
        bool: True if the session key is valid, False otherwise.
    """
    # Получение сохраненного ключа из данных клиента
    stored_key = client_data["session_key"]
    # Извлечение текущего ключа из данных клиента
    key = client_data.get("session_key")
    # Возвращение результата сравнения ключей
    return stored_key == key


# Асинхронная функция для валидации наличия обязательных ключей в данных
async def validate_data(data: Dict[str, Union[str, Dict]], required_keys: List[str]):
    """Validate data keys.

    Args:
        data (Dict[str, Union[str, Dict]]): Data to be validated.
        required_keys (List[str]): List of required keys.

    Raises:
        ValueError: Raised if any required key is missing in the data.
    """
    # Проверка наличия всех обязательных ключей в данных
    if not all(key in data for key in required_keys):
        # В случае отсутствия ключей вызывается исключение ValueError
        raise ValueError("Missing required keys in data")


# Асинхронная функция для валидации наличия обязательных ключей в данных сообщения
async def validate_message_data(message_data: Dict[str, Union[str, Dict]], required_keys: List[str]):
    """Validate message data keys.

    Args:
        message_data (Dict[str, Union[str, Dict]]): Message data to be validated.
        required_keys (List[str]): List of required keys.

    Raises:
        ValueError: Raised if any required key is missing in the message data.
    """
    # Проверка наличия всех обязательных ключей в данных сообщения
    if not all(key in message_data for key in required_keys):
        # В случае отсутствия ключей вызывается исключение ValueError
        raise ValueError("Missing required keys in messageData")


# Асинхронная функция для генерации ключа сессии клиента
async def generate_client_session_key(length: int = 32) -> str:
    """Generate client session key.

    Args:
        length (int): The length of the session key.

    Returns:
        str: The generated client session key.
    """
    # Проверка, что длина ключа положительна
    if length <= 0:
        raise ValueError("Длина ключа сессии должна быть положительным целым числом.")
    # Генерация шестнадцатеричного токена указанной длины
    return secrets.token_hex(length)


# Асинхронная функция для генерации уникального идентификатора клиента
async def generate_client_id() -> str:
    """Generate client ID.

    Returns:
        str: The generated client ID.
    """
    # Генерация уникального идентификатора клиента
    return str(uuid.uuid4())


# Асинхронная функция для создания нового клиента
async def create_client() -> Dict[str, Union[str, Dict]]:
    """Create a new client.

    Returns:
        Dict[str, Union[str, Dict]]: Data of the new client.
    """
    # Генерация уникального идентификатора и ключа сессии
    client_id = await generate_client_id()
    session_key = await generate_client_session_key()
    # Возвращение данных нового клиента в виде словаря
    return {"client_id": client_id, "session_key": session_key, "telegram_to_planfix": {}}


# Асинхронная функция для получения данных клиента
async def get_client_data() -> Dict[str, Union[str, Dict]]:
    """Get client data.

    Returns:
        Dict[str, Union[str, Dict]]: Data of the client.
    """
    # Проверка, что словарь клиентов не пустой
    if not clients:
        # Генерация нового клиента и добавление его в словарь
        client_id = generate_client_id()
        clients[client_id] = await create_client()

    # Получение первого ключа словаря клиентов
    client_id = list(clients.keys())[0]
    # Получение данных клиента по ключу
    client_data = clients[client_id]

    # Проверка валидности ключа сессии
    if not await verify_session_key(client_data):
        # В случае невалидного ключа вызывается исключение ValueError
        raise ValueError("Invalid session key")

    # Возврат данных клиента в виде словаря
    return client_data


# Обработчик событий нового сообщения (исходящего и входящего)
@client.on(events.NewMessage(outgoing=True, incoming=True))
async def handle_text_message(event: events.NewMessage.Event) -> None:
    """Handle incoming and outgoing text messages.

    Arguments:
    - event (events.NewMessage.Event): The event representing a new message, either incoming or outgoing.

    Returns:
    None

    This function handles incoming and outgoing text messages, logging relevant information and processing the messages
    accordingly. It uses the Flask application context and includes debug logs for message details. The handling
    includes checking for the presence of the 'id' attribute, message text, and dispatching messages to Planfix.
    """
    # С использованием контекста приложения Flask
    with app.app_context():
        try:
            # Отладочные логи для вывода информации о сообщении и его типе
            logger.debug(f"Message: {event.message}")
            logger.debug(f"Type of message: {type(event.message)}")

            # Проверка наличия атрибута 'id' у сообщения
            if hasattr(event, 'message') and hasattr(event.message, 'id'):
                logger.debug(f"Message ID: {event.message.id}")
            else:
                logger.warning("Message or message has no 'id' attribute")

            # Проверка наличия текста в сообщении
            if event.message.text:
                message = event.message.text
                logger.debug(f"Message text: {event.message.text}")
                logger.debug(f"Type of message text: {type(event.message.text)}")

                # Получение данных клиента
                client_data = await get_client_data()
                logger.debug(f"Client data: {client_data}")

                try:
                    # Проверка наличия атрибута 'id' у сообщения
                    if hasattr(event, 'message') and hasattr(event.message, 'id'):
                        logger.debug(f"Message ID: {event.message.id}")
                    else:
                        logger.warning("Message or message has no 'id' attribute")
                except Exception as id_error:
                    logger.error(f"Error checking 'id' attribute: {id_error}")

                # Обработка входящего сообщения
                if not event.message.out:
                    logger.debug("Handling incoming message.")
                    await send_telegram_message_to_planfix(event, client_data, event.message.id)
                else:
                    logger.debug("Handling outgoing message.")
                    # Добавьте свою логику обработки исходящего сообщения здесь
            else:
                logger.warning("Message has no text")

        except Exception as error:
            # Обработка ошибок при обработке текстового сообщения
            logger.error(f"Error handling text message: {error}")


# Обработчик маршрута /webhook с поддержкой различных HTTP-методов
@app.route('/webhook', methods=['POST', 'GET', 'DELETE', 'PUT'])
def handle_webhook() -> Tuple[Response, int]:
    """Handle webhook requests.

    Arguments:
    None

    Returns:
    Tuple[Response, int]

    This function handles HTTP requests to the '/webhook' route, supporting various HTTP methods (POST, GET, DELETE,
    PUT). It determines the appropriate asynchronous coroutine based on the request method and executes it, returning
    the result as a tuple containing a Flask Response object and an HTTP status code.
    """
    try:
        # Получение текущего цикла событий asyncio
        loop = asyncio.get_event_loop()

        # Определение асинхронной корутины в зависимости от метода HTTP-запроса
        if request.method == 'POST':
            coro = handle_post(request.json)
        elif request.method == 'GET':
            coro = handle_get()
        elif request.method == 'DELETE':
            coro = handle_delete()
        elif request.method == 'PUT':
            coro = handle_put(request.json)
        else:
            # Обработка неверного метода запроса
            response: Response = jsonify({'error': 'Invalid request method'})
            return response, 400

        # Запуск асинхронной корутины и возврат результата
        result: Any = loop.run_until_complete(loop.create_task(coro))
        return result if isinstance(result, tuple) else (result, 200)

    except Exception as error:
        # Обработка и возврат ошибки в случае исключения
        response: Response = jsonify({'error': str(error)})
        return response, 500


# Асинхронная функция для обработки входящих запросов
async def handle_request(data: Dict[str, Union[str, Dict]], send_function) -> Union[
    Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]:
    """Handle incoming requests.

    Arguments:
    - data (Dict[str, Union[str, Dict]]): The data representing the incoming request.
    - send_function: The function responsible for sending the message to Planfix.

    Returns:
    Union[Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]

    This asynchronous function handles incoming requests, validates the required data, retrieves client data, and sends
    the message to Planfix. It returns a dictionary with a successful status or an error message along with the HTTP
    status code.
    """
    try:
        # Проверка наличия обязательных ключей в данных запроса
        required_keys = ['messageData', 'telegram_message_id']
        await validate_data(data, required_keys)

        # Получение данных о сообщении из запроса
        message_data = data['messageData']
        # Проверка наличия обязательных ключей в данных сообщения
        required_message_keys = ['text', 'telegram_message_id']
        await validate_message_data(message_data, required_message_keys)

        # Получение данных клиента
        client_data, success_response, error_response = get_client_data()
        if client_data is None:
            logger.error("Client data not found")
            # Возврат словаря с ошибкой в случае отсутствия данных клиента
            return error_response

        # Получение текста сообщения
        message_text = message_data.get('text')
        logger.debug(f"Message text: {message_text}")

        # Вызов функции отправки события в Planfix и получение ID сообщения
        planfix_message_id = await send_function(message_data, client_data, message_data['telegram_message_id'])
        logger.debug(f"Planfix message ID: {planfix_message_id}")

        # Инициализация словаря, если не существует
        if 'telegram_to_planfix' not in client_data:
            client_data['telegram_to_planfix'] = {}

        # Сохранение соответствия ID сообщения в Telegram и Planfix
        client_data['telegram_to_planfix'][message_data['telegram_message_id']] = planfix_message_id
        # Обновление статуса клиента
        client_data['status'] = ClientStatus.ONLINE
        logger.info("Successfully handled request")

        # Возврат словаря с успешным ответом
        return {'status': client_data['status'], 'token': client_data['token']}
    except Exception as error:
        logger.error(f"An error occurred in handle_request: {error}")
        # Возврат словаря с ошибкой и статусом 500
        return {'error': str(error)}, 500


# Асинхронная функция для обработки PUT-запросов
async def handle_put(data: Dict[str, Union[str, Dict]]) -> Union[
    Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]:
    """Handle PUT requests.

    Arguments:
    - data (Dict[str, Union[str, Dict]]): The data representing the incoming PUT request.

    Returns:
    Union[Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]

    This asynchronous function handles incoming PUT requests by calling the handle_request function with the appropriate
     send function. It returns a dictionary with a successful status or an error message along with the HTTP status
     code.
     """
    # Вызов функции обработки входящего запроса с использованием функции отправки в Planfix
    return await handle_request(data, send_message_to_planfix)


# Асинхронная функция для обработки POST-запросов
async def handle_post(data: Dict[str, Union[str, Dict]]) -> Union[
    Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]:
    """Handle POST requests.

    Arguments:
    - data (Dict[str, Union[str, Dict]]): The data representing the incoming POST request.

    Returns:
    Union[Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]

    This asynchronous function handles incoming POST requests by running the handle_request function in a separate
    thread. It returns a dictionary with a successful status or an error message along with the HTTP status code.
    """
    # Получение текущего цикла событий
    loop = asyncio.get_event_loop()
    # Вызов функции обработки входящего запроса в отдельном потоке
    return await loop.run_in_executor(executor, partial(handle_request, data, send_telegram_message_to_planfix))


# Асинхронная функция для обработки GET-запросов
async def handle_get() -> Union[Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]:
    """Handle GET requests.

    Arguments:
    None

    Returns:
    Union[Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]

    This asynchronous function handles incoming GET requests, retrieves client data, and returns a dictionary with a
    successful status or an error message along with the HTTP status code.
    """
    try:
        # Получение данных клиента и ответов на успех и ошибку
        client_data, success_response, error_response = get_client_data()
        if client_data is None:
            # Возврат словаря с ошибкой в случае отсутствия данных клиента
            return error_response

        # Возврат словаря с успешным ответом, содержащим статус клиента
        return success_response({'status': client_data['status']})
    except Exception as error:
        # Возврат словаря с ошибкой и статусом 500 в случае исключения
        return {'error': str(error)}, 500


# Асинхронная функция для обработки DELETE-запросов
async def handle_delete() -> Union[Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]:
    """Handle DELETE requests.

    Arguments:
    None

    Returns:
    Union[Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]

    This asynchronous function handles incoming DELETE requests, sets the client status to OFFLINE, and returns a
    dictionary with a successful status or an error message along with the HTTP status code.
    """
    try:
        # Получение данных клиента и ответов на успех и ошибку
        client_data, success_response, error_response = get_client_data()
        if client_data is None:
            # Возврат словаря с ошибкой в случае отсутствия данных клиента
            return error_response

        # Установка статуса клиента в OFFLINE
        client_data['status'] = ClientStatus.OFFLINE

        # Возврат словаря с успешным ответом, содержащим статус клиента
        return success_response({'status': client_data['status']})
    except Exception as error:
        # Возврат словаря с ошибкой и статусом 500 в случае исключения
        return {'error': str(error)}, 500


# Блок выполнения кода при запуске программы
if __name__ == '__main__':
    try:
        # Запуск обработчика входящих сообщений от бота Telegram
        asyncio.get_event_loop().run_until_complete(run_polling())
        # Запуск веб-приложения Flask на порту 5000
        app.run(port=5000)
    except KeyboardInterrupt:
        # Обработка прерывания по Ctrl+C
        logger.info("Program interrupted by user")
    except Exception as e:
        # Обработка неожиданной ошибки
        logger.error(f"An unexpected error occurred: {e}")
