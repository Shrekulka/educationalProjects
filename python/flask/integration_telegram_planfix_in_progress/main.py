# integration_telegram_planfix_in_progress/main.py
import asyncio
import os
import secrets
import traceback
from pprint import pformat
from shlex import quote
from typing import Union, Tuple, Coroutine, Any, Dict, Optional
from urllib.parse import parse_qsl

import aiohttp
import phonenumbers
import uvicorn
from aiohttp import ClientSession
from asgiref.wsgi import WsgiToAsgi
from colorama import Fore, Style
from flask import Flask, request, jsonify, make_response, Response
from phonenumbers import NumberParseException
from telethon import events, TelegramClient, types
from telethon.tl.custom import Message

from config import planfix_api_key, planfix_api_url, telegram_api_id, telegram_api_hash, telegram_integration_id, \
    RESET_ALL, CYAN, GREEN, YELLOW, BLUE, MAGENTA, name_session
from logger import logger

# Создание объекта Flask приложения
app = Flask(__name__)

# Создание объекта ASGI-приложения (WsgiToAsgi преобразует WSGI-приложение в ASGI-приложение)
# ASGI (Asynchronous Server Gateway Interface) - это интерфейс, который позволяет асинхронно обрабатывать HTTP-запросы.
# WsgiToAsgi используется для преобразования Flask-приложения, работающего по стандарту WSGI, в ASGI-приложение.
asgi_app = WsgiToAsgi(app)

# Оптимизация сессий и путей
sessions = {}

# Глобальный словарь для резервных копий сессий
sessions_backup = {}

# Оптимизация генерации имен сессий
path_session = f'sessions/{name_session}.session'

# Блокировка для обеспечения безопасности работы с сессиями в асинхронном коде
sessions_lock = asyncio.Lock()


def get_session_path() -> str:
    """
    Function to obtain the path to the session file.

    Returns:
        str: Path to the session file.
    """
    logger.info(f"\n{CYAN}def get_session_path{RESET_ALL}\n")
    # Возвращаем путь к файлу сессии, если файл существует, иначе возвращаем имя сессии
    return path_session if os.path.isfile(path_session) else name_session


def create_or_get_telegram_client() -> Union[TelegramClient, Response]:
    """
        Function to create or retrieve a TelegramClient.

        Returns:
            Union[TelegramClient, Response]: Returns a TelegramClient object on success
                                             or a Response object in case of an error.

        Raises:
            FileNotFoundError: Raised if the session file is not found.
            Exception: Raised in case of a general error during the creation or retrieval of TelegramClient.
    """
    logger.info(f"\n{CYAN}def create_or_get_telegram_client{RESET_ALL}\n")
    try:
        # Проверка существования файла сессии
        session_path = get_session_path()
        logger.info(f"{GREEN}Session exists for {session_path}{RESET_ALL}") if os.path.exists(path_session) \
            else logger.info(f"{YELLOW}New session for {session_path}{RESET_ALL}")
        logger.info(f"{GREEN}Session created for {session_path}{RESET_ALL}")

        # Создание объекта TelegramClient с использованием данных из файла сессии
        return TelegramClient(session_path, telegram_api_id, telegram_api_hash)
    except FileNotFoundError:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Session file not found.\n{detailed_send_message_error}")

        # В случае отсутствия файла сессии, возвращаем ошибку сервера с соответствующим кодом ответа
        response = make_response(jsonify({"error": "Session file not found"}), 500)
        return response
    except Exception as error:
        detailed_send_message_error = traceback.format_exc()
        logger.error(f"Error creating or getting Telegram client: {error}\n{detailed_send_message_error}")

        # В случае общей ошибки, возвращаем ошибку сервера с соответствующим кодом ответа
        response = make_response(jsonify({"error": "Internal Server Error"}), 500)
        return response


async def get_client_session(client_token: str) -> Union[aiohttp.ClientSession, Tuple[Response, int]]:
    """
        Asynchronous function to obtain a client session.

        Args:
            client_token (str): Client token.

        Returns:
            Union[aiohttp.ClientSession, Tuple[Response, int]]: Returns an aiohttp.ClientSession object on success
                                                or a tuple with a Response object and response code in case of an error.

        Raises:
            aiohttp.ClientError: Raised in case of errors during the creation or retrieval of the client session.
    """
    logger.info(f"\n{GREEN}Getting client session for token: {client_token}{RESET_ALL}")

    # Использование асинхронного контекстного менеджера для безопасного доступа к глобальной переменной sessions
    async with sessions_lock:

        # Получение данных о клиенте из глобального словаря sessions
        client_data = sessions.get(client_token)

        # Если сессия уже существует для данного токена, возвращаем её
        if client_data and 'client_session' in client_data:
            logger.info(f"{GREEN}Session retrieved for {client_token}{RESET_ALL}")
            return client_data['client_session']

        # Если сессия отсутствует, создаем новую
        else:
            logger.info(f"{YELLOW}Session already exists for {client_token}{RESET_ALL}")
            local_path_session = f"sessions/{name_session}.session"
            new_client_session = None

            try:
                # Создание новой клиентской сессии
                new_client_session = aiohttp.ClientSession()

                # Сохранение информации о новой сессии в глобальном словаре
                sessions[client_token] = {
                    'token': client_token,
                    'client_session': new_client_session,
                    'path_session': local_path_session
                }
                return new_client_session

            except aiohttp.ClientError as e:
                # Обработка ошибки при создании или получении клиентской сессии
                detailed_error = traceback.format_exc()
                logger.error(f"Error creating or getting client session: {type(e).__name__} - {e}\n{detailed_error}")

                # В случае ошибки, закрываем сессию и возвращаем ошибку сервера с соответствующим кодом ответа
                if new_client_session:
                    logger.info(f"Session closed due to an error")
                    await new_client_session.close()
                return jsonify({"error": "Client Session Error"}), 500

            finally:
                # В любом случае закрываем сессию
                if new_client_session:
                    logger.info(f"{YELLOW}Session closed successfully{RESET_ALL}")
                    await new_client_session.close()


# Использование функции для создания или получения сессии
client = create_or_get_telegram_client()


@app.route('/webhook', methods=['POST', 'GET', 'DELETE', 'PUT'])
async def process_webhook_request() -> Union[Response, Coroutine[Any, Any, Response]]:
    """
        Handling webhooks from external systems.

        Returns:
            Union[Response, Coroutine[Any, Any, Response]]: Returns a Response object in case of an error
                                                    or an asynchronous Response object in case of successful processing.
    """

    logger.info(f"\n{CYAN}process_webhook_request{RESET_ALL}\n")

    if request.method == 'POST':
        # В случае POST-запроса обрабатываем соответствующий запрос
        return await process_post_request()
    elif request.method == 'GET':
        # В случае GET-запроса обрабатываем соответствующий запрос
        return await process_get_request()
    elif request.method == 'DELETE':
        # В случае DELETE-запроса обрабатываем соответствующий запрос
        return await process_delete_request()
    elif request.method == 'PUT':
        # В случае PUT-запроса обрабатываем соответствующий запрос
        return await process_put_request()
    else:
        # В случае неизвестного HTTP-метода возвращаем ошибку с соответствующим кодом ответа
        response = make_response(jsonify({"error": "Unsupported HTTP method"}), 400)
        return response


async def process_post_request() -> Union[Response, Coroutine[Any, Any, Response]]:
    """
        Asynchronous function for handling a POST request.

        Returns:
            Union[Response, Coroutine[Any, Any, Response]]: Returns a Response object in case of an error
                                                    or an asynchronous Response object in case of successful processing.
    """

    logger.info(f"\n{CYAN}def process_post_request{RESET_ALL}\n")

    try:
        # Общая обработка запроса для извлечения данных, токена и клиентской сессии
        data_decoded, token, client_session = await process_request_common()

        # Вывод информации о полученных данных в лог
        logger.info(f"\n{MAGENTA}def process_post_request - "
                    f"data_decoded: {data_decoded}\ntoken: {token}\nclient_session: {client_session}{RESET_ALL}\n")

        # Создание данных клиента
        client_data = await create_client_data(data_decoded)

        # Создание клиентской сессии и сохранение информации о ней в глобальном словаре
        sessions[token] = await create_client_session(token, client_session, client_data)

        # Проверка, содержит ли раскодированный словарь ключ 'cmd' со значением 'newMessage'
        if data_decoded.get('cmd') == 'newMessage':
            # Обработка нового сообщения и отправка во внешнюю систему
            await send_message_from_telegram_to_planfix(token, data_decoded)

            # Возвращаем успешный ответ с соответствующими данными
            response = make_response(jsonify({"status": "OK", "token": token, "session_id": path_session}), 200)
            logger.debug(f"\n{GREEN}Response from process_post_request: {response}{RESET_ALL}\n")
            logger.debug(f"\n{GREEN}Type response from process_post_request: {type(response)}{RESET_ALL}\n")
            return response

    except aiohttp.ClientResponseError as error:
        # Обработка ошибок от клиента (внешней системы) и возвращение соответствующего ответа
        return await handle_error_response(error)

    except Exception as error:
        # Обработка общих ошибок и возвращение соответствующего ответа
        return await handle_internal_error(error)


async def process_get_request() -> Union[Response, Coroutine[Any, Any, Response]]:
    """
        Asynchronous function for handling a GET request.

        Returns:
            Union[Response, Coroutine[Any, Any, Response]]: Returns a Response object in case of an error
                                                    or an asynchronous Response object in case of successful processing.
    """
    logger.info(f"\n{CYAN}def process_get_request{RESET_ALL}\n")

    try:
        # Извлечение токена из заголовка запроса
        token = request.headers.get("Token")
        logger.debug(f"{BLUE}GET request from {request.remote_addr}, token: {token}{RESET_ALL}")

        # В случае отсутствия токена, возвращаем ошибку с соответствующим кодом ответа
        if not token:
            response = make_response(jsonify({"error": "Token is missing"}), 401)
            return response

        # В случае невалидного токена, возвращаем ошибку с соответствующим кодом ответа
        if token not in sessions:
            response = make_response(jsonify({"error": "Invalid token"}), 404)
            return response

        # Извлечение данных запроса в формате JSON
        request_data = request.get_json()

        # Проверка наличия данных запроса и наличия ключа 'number' в этих данных
        if request_data and 'number' in request_data:
            # Проверка и обработка данных запроса, связанных с номером
            await validate_and_check_number(token, request_data['number'], request_data.get('name', ''))

            # Возвращаем успешный ответ с соответствующими данными
            response = make_response(jsonify({"status": "online"}), 200)
            return response

        # В случае некорректных или отсутствующих данных в запросе, возвращаем ошибку с соответствующим кодом ответа
        response = make_response(jsonify({"error": "Invalid or missing number in request data"}), 400)
        return response

    except Exception as error:
        # Обработка общих ошибок и возвращение соответствующего ответа
        return await handle_internal_error(error)


async def process_delete_request() -> Union[Response, Coroutine[Any, Any, Response]]:
    """
        Asynchronous function for handling a DELETE request.

        Returns:
            Union[Response, Coroutine[Any, Any, Response]]: Returns a Response object in case of an error
                                                    or an asynchronous Response object in case of successful processing.
    """
    logger.info(f"\n{CYAN}def process_delete_request{RESET_ALL}\n")

    try:
        # Валидация токена в заголовках запроса
        token = await validate_token_in_headers()
        logger.debug(f"{BLUE}DELETE request from {request.remote_addr}, token: {token}{RESET_ALL}")

        # Извлечение данных запроса в формате JSON
        data = request.get_json()

        # В случае отсутствия данных или отсутствия ключа 'number' в данных, возвращаем ошибку с кодом ответа
        if not data or 'number' not in data:
            response = make_response(jsonify({"error": "Invalid or missing data in the request"}), 400)
            return response

        # Остановка клиента и возвращение соответствующего ответа
        await stop_client_and_return_response(token, data['number'])
        response = make_response(jsonify({"status": "Client stopped successfully"}), 200)
        return response

    except Exception as error:
        # Обработка общих ошибок и возвращение соответствующего ответа
        return await handle_internal_error(error)


async def process_put_request() -> Union[Response, Coroutine[Any, Any, Response]]:
    """
        Asynchronous function for handling a PUT request.

        Returns:
            Union[Response, Coroutine[Any, Any, Response]]: Returns a Response object in case of an error
                                                    or an asynchronous Response object in case of successful processing.
    """
    logger.info(f"\n{CYAN}def process_put_request{RESET_ALL}\n")

    try:
        # Извлечение данных запроса в формате JSON
        data_decoded = request.get_json()

        # В случае отсутствия данных или отсутствия ключа 'number' в данных, возвращаем ошибку с кодом ответа
        if not data_decoded or not data_decoded.get('number'):
            logger.warning(f"\n{MAGENTA}Invalid request data (process_put_request){RESET_ALL}\n")
            response = make_response(jsonify({"error": "Invalid request data"}), 400)
            return response

        # В случае невалидного телефонного номера, возвращаем ошибку с соответствующим кодом ответа
        if not is_valid_phone_number(data_decoded['number']):
            logger.warning(f"\n{MAGENTA}Didn't valid_phone_number (process_put_request){RESET_ALL}\n")
            response = make_response(jsonify({"error": "Invalid phone number"}), 400)
            return response

        # Обновление данных клиента и запуск интеграции
        await update_client_data_and_start_integration(data_decoded)

        # Возвращаем успешный ответ с соответствующим сообщением
        response = make_response(jsonify({"status": "Client data successfully updated"}), 200)
        return response

    except Exception as error:
        # Обработка общих ошибок и возвращение соответствующего ответа
        return await handle_internal_error(error)


async def process_request_common() -> Tuple[Union[Dict[str, Any], Response], Optional[str], Optional[ClientSession]]:
    """
        Asynchronous function for handling common actions during request processing.

        Returns:
            Tuple[Dict[str, Any], Optional[str], Optional[ClientSession]]:
                Returns a tuple of decoded request data, client token, and client session (optional).
    """
    logger.info(f"\n{CYAN}def process_request_common{RESET_ALL}\n")

    # Получение данных запроса в текстовом формате
    data = request.get_data(as_text=True)
    logger.debug(f"{MAGENTA}Processing request from {request.remote_addr}: {data}{RESET_ALL}")

    # Получение раскодированных данных из формы запроса
    data_decoded = request.form
    logger.debug(f"{MAGENTA}'process_request_common'\n{pformat(data_decoded, width=40)}{RESET_ALL}")

    # Извлечение номера клиента из данных запроса
    client_number = data_decoded.get("number")
    logger.debug(f"{MAGENTA}client_number: {client_number}{RESET_ALL}")

    # Проверка, что номер клиента не является None
    if client_number is not None:
        # Преобразование номера в строковый формат и проверка его валидности
        client_number = str(client_number)
        logger.debug(f"{MAGENTA}Client_number: {client_number}{RESET_ALL}")

        # В случае невалидного номера, возвращаем ошибку с соответствующим кодом ответа
        if not is_valid_phone_number(client_number):
            response = make_response(jsonify({"error": "Invalid phone number"}), 400)
            logger.debug(f"{MAGENTA}Response: {response}{RESET_ALL}")
            return response, None, None

    # Извлечение токена клиента из данных запроса
    client_token = data_decoded.get('client_token')
    # Получение клиентской сессии
    client_session = await get_client_session(client_token)
    logger.debug(f"{MAGENTA}Client_token: {client_token}\nclient_session: {client_session}\n"
                 f"data_decoded: {data_decoded}{RESET_ALL}")
    # Возврат кортежа из раскодированных данных запроса, токена клиента и клиентской сессии
    return data_decoded, client_token, client_session


async def validate_and_check_number(client_token: str, client_number: str, client_name: str) -> Union[Response, None]:
    """
        Asynchronous function for validating and checking the client number.

        Args:
            client_token (str): Client token.
            client_number (str): Client number.
            client_name (str): Client name.

        Returns:
          Union[Response, None]: Returns a Response object in case of an error or None in case of successful validation.
    """
    logger.info(f"\n{CYAN}def validate_and_check_number{RESET_ALL}\n")

    # Проверка наличия данных о клиенте и номера в сессии
    if 'client_data' in sessions[client_token] and 'number' in sessions[client_token]['client_data']:
        saved_client_number = sessions[client_token]['client_data']['number']
        saved_client_name = sessions[client_token]['client_data'].get('name', '')

        # Проверка валидности номера телефона
        if not is_valid_phone_number(client_number):
            logger.error(f"Invalid phone number: {client_number}")
            response = make_response(jsonify({"error": "Invalid phone number"}), 400)
            return response

        # Проверка совпадения запрошенного номера с сохраненным
        if saved_client_number != client_number:
            logger.error(f"Number mismatch: requested {client_number}, saved {saved_client_number}")
            response = make_response(jsonify({"error": "Number mismatch"}), 400)
            return response

        # Проверка совпадения запрошенного имени с сохраненным (если сохранено имя)
        if saved_client_name and client_name and saved_client_name != client_name:
            logger.error(f"Name mismatch: requested {client_name}, saved {saved_client_name}")
            response = make_response(jsonify({"error": "Name mismatch"}), 400)
            return response

        # В случае успешной проверки возвращаем успешный ответ
        logger.info(f"validate_and_check_number request from {request.remote_addr}, token: {client_token}")
        response = make_response(jsonify({"status": "online"}), 200)
        return response


async def validate_token_in_headers() -> Union[str, Response]:
    """
        Asynchronous function for validating the token in the request headers.

        Returns:
            Union[str, Response]: Returns the token on successful validation or a Response object in case of an error.
    """
    logger.info(f"\n{CYAN}def validate_token_in_headers{RESET_ALL}\n")

    # Извлечение токена из заголовков запроса
    token = request.headers.get("Token")
    logger.debug(f"{BLUE}'validate_token_in_headers' request from {request.remote_addr}, token: {token}{RESET_ALL}")

    # Проверка наличия токена
    if not token:
        response = make_response(jsonify({"error": "Token is missing"}), 401)
        return response

    # Проверка валидности токена
    if token not in sessions:
        response = make_response(jsonify({"error": "Invalid token"}), 404)
        return response

    # В случае успешной валидации возвращаем токен
    return token


async def stop_client_and_return_response(client_token: str, client_number: str) -> Response:
    """
        Asynchronous function for stopping the client and returning a successful response.

        Args:
            client_token (str): Client token.
            client_number (str): Client number.

        Returns:
            Response: Returns a Response object with a message about the successful client stop.
    """

    logger.info(f"\n{CYAN}def stop_client_and_return_response{RESET_ALL}\n")

    # Остановка клиента
    await stop_client(client_token, client_number)

    # Создание объекта Response с сообщением об успешной остановке
    response = make_response(jsonify({"status": "Client stopped successfully"}), 200)
    return response


async def create_client_session(token: str, client_session: ClientSession, client_data: dict) -> dict:
    """
        Asynchronous function for creating a client session object.

        Args:
            token (str): Client token.
            client_session (ClientSession): Client session object.
            client_data (dict): Client data.

        Returns:
            dict: Returns a dictionary with client session data.
    """

    logger.info(f"\n{CYAN}def create_client_session{RESET_ALL}\n")

    # Создание словаря с данными о сессии клиента
    return {
        'token': token,
        'client_session': client_session,
        'path_session': path_session,
        'client_data': client_data,
        'receiver': {
            "id": client_data.get('telegramUserId'),
            "username": client_data.get('telegramUserName')
        }
    }


async def create_client_data(data_decoded: dict) -> dict:
    """
        Asynchronous function for creating a client data object.

        Args:
            data_decoded (dict): Decoded data from the request.

        Returns:
            dict: Returns a dictionary with client data.
    """

    # Вывод информационного сообщения в лог о вызове функции
    logger.info(f"\n{CYAN}def create_client_data{RESET_ALL}\n")

    # Создание словаря с данными о клиенте
    return {
        "number": data_decoded.get("number"),
        "name": data_decoded.get("name"),
        "token": data_decoded.get("token"),
        "url_planfix": data_decoded.get("url_planfix"),
        "token_planfix": data_decoded.get("token_planfix")
    }


async def update_client_data_and_start_integration(data_decoded: dict) -> Response:
    """
        Asynchronous function for updating client data and starting integration.

        Args:
            data_decoded (dict): Decoded data from the request.

        Returns:
            Response: Returns a Response object with a message about the successful update of client data.
    """
    logger.info(f"\n{CYAN}def update_client_data_and_start_integration{RESET_ALL}\n")

    # Извлечение необходимых данных из раскодированных данных запроса
    token = data_decoded.get('token')
    client_name = data_decoded.get('name')
    client_number = data_decoded.get('number')
    url_planfix = data_decoded.get('url_planfix')
    token_planfix = data_decoded.get('token_planfix')
    name_session_param = data_decoded.get('name_session')
    path_session_param = data_decoded.get('path_session')

    # Проверка существования токена в сессиях
    if token not in sessions:
        response = make_response(jsonify({"error": "Invalid client token"}), 404)
        return response

    # Сохранение текущих данных о клиенте перед обновлением
    if token in sessions:
        session_data = sessions[token]
        sessions_backup[token] = {
            "client_session": session_data["client_session"],
            "client_data": session_data["client_data"]
        }

        logger.debug(f"Saved client data: {sessions_backup[token]}")

    # Остановка текущего клиента
    await stop_client(token, client_number)

    # Обновление данных о клиенте
    sessions[token]['client_data']['name'] = client_name
    sessions[token]['client_data']['number'] = client_number
    sessions[token]['client_data']['url_planfix'] = url_planfix
    sessions[token]['client_data']['token_planfix'] = token_planfix
    sessions[token]['name_session'] = name_session_param
    sessions[token]['path_session'] = path_session_param

    # Запуск интеграции для обновленного клиента
    logger.debug(f"{BLUE}Starting update for client {token}{{RESET_ALL}}")
    await start_integration_for_client(token)

    # Создание объекта Response с сообщением об успешном обновлении данных
    response = make_response(jsonify({"status": "Client data successfully updated"}), 200)
    return response


async def handle_error_response(error: aiohttp.ClientResponseError) -> Response:
    """
        Asynchronous function for handling client response errors.

        Args:
            error (aiohttp.ClientResponseError): Client response error.

        Returns:
            Response: Returns a Response object with information about the client response error.
    """
    logger.info(f"\n{CYAN}def handle_error_response{RESET_ALL}\n")

    # Получение детальной информации об ошибке из трассировки стека
    detailed_error = traceback.format_exc()

    # Логирование ошибки клиентского ответа
    logger.error(f"ClientResponseError: {error.status}: {error.message}\n{detailed_error}")

    # Обработка специфического случая ошибки с кодом 400
    if error.status == 400:
        response_text = error.message
        logger.error(f"Response text: {response_text}\n{detailed_error}")

    # Создание объекта Response с информацией об ошибке клиентского ответа
    response = make_response(jsonify({"error": "Client Response Error"}), 500)
    return response


async def handle_internal_error(error: Exception) -> Response:
    """
        Asynchronous function for handling internal server errors.

        Args:
            error (Exception): Internal server error.

        Returns:
            Response: Returns a Response object with information about the internal server error.
    """
    logger.info(f"\n{CYAN}def handle_internal_error{RESET_ALL}\n")

    # Получение детальной информации об ошибке из трассировки стека
    detailed_error = traceback.format_exc()

    # Логирование внутренней ошибки сервера
    logger.error(f"Error handling request: {error}\n{detailed_error}")

    # Создание объекта Response с информацией о внутренней ошибке сервера
    response = make_response(jsonify({"error": "Internal Server Error"}), 500)
    return response


def is_valid_phone_number(phone_number: str) -> bool:
    """
        Function for validating the phone number.

        Args:
            phone_number (str): Phone number to validate.

        Returns:
            bool: Returns True if the number is valid, otherwise False.
    """
    logger.info(f"\n{CYAN}def is_valid_phone_number{RESET_ALL}\n")

    try:
        # Логирование входящего телефонного номера для отладки
        logger.debug(f"\n{MAGENTA}is_valid_phone_number - phone_number: {phone_number}{RESET_ALL}\n")

        # Парсинг телефонного номера с использованием библиотеки phonenumbers
        parsed_number = phonenumbers.parse(phone_number, None)

        # Логирование распарсенного номера для отладки
        logger.debug(f"\n{MAGENTA}parsed_number: {parsed_number}{RESET_ALL}\n")

        # Проверка валидности номера и его принадлежности к какому-либо региону
        is_valid_and_region = (
                phonenumbers.is_valid_number(parsed_number) and
                phonenumbers.region_code_for_number(parsed_number) is not None)

        # Логирование результата проверки для отладки
        logger.debug(f"\n{MAGENTA}is_valid_and_region: {is_valid_and_region}{RESET_ALL}\n")

        return is_valid_and_region
    except NumberParseException:
        # Логирование исключения NumberParseException и возврат False в случае ошибки
        detailed_error = traceback.format_exc()
        logger.error(f"Except NumberParseException: {detailed_error}")
        return False


async def send_message_from_planfix_to_telegram(data_decoded: dict, token: str) -> Response:
    """
        Asynchronous function for sending a message from Planfix to Telegram.

        Args:
            data_decoded (dict): Decoded data from the request.
            token (str): Token of the current client.

        Returns:
            Response: Response object for the HTTP request.
    """
    logger.info(f'\n{Fore.CYAN}def send_message_from_planfix_to_telegram{Style.RESET_ALL}\n')

    try:
        # Извлечение асинхронной сессии текущего клиента из словаря
        client_session = sessions[token]['client_session']

        # Логирование информации о полученных данных
        logger.info(f"'Post'\n{pformat(data_decoded, width=40)}")

        # Асинхронное управление клиентом Telegram
        async with client_session:
            try:
                # Получение информации о себе (боте) с использованием метода get_me()
                me = await client.get_me()

                # Вывод всей информации о пользователе в лог
                logger.debug("User info: %s", me.stringify())

                # Извлечение нужных параметров из информации о пользователе
                pretty_data = pformat(data_decoded, width=40)
                logger.debug(f"Sending a message in def send_message_from_planfix_to_telegram(...): {pretty_data}")

                # Отправка сообщения в Telegram с использованием метода send_message()
                await client.send_message(me.id, str(pretty_data))
                response = make_response(jsonify({"status": "Message sent successfully"}), 200)
                return response

            except Exception as send_message_error:
                detailed_send_message_error = traceback.format_exc()
                logger.error(
                    f"Error when calling client.send_message(): {send_message_error}\n{detailed_send_message_error}")

        logger.info("Message successfully sent to Telegram.")

    except Exception as error:
        # Используйте traceback.format_exc() для получения детальной трассировки стека
        detailed_error = traceback.format_exc()
        logger.error(f"Error sending message to Telegram: {error}\n{detailed_error}")

        # Возвращение асинхронного ответа в случае ошибки
        response = make_response(jsonify({"error": "Failed to send message to Telegram"}), 500)
        return response


async def send_message_from_telegram_to_planfix(token: str, planfix_data: dict) -> str:
    """
        Asynchronous function for sending a message from Telegram to Planfix.

        Args:
            token (str): Token of the current client.
            planfix_data (dict): Data to be sent to Planfix.

        Returns:
            str: Response text from Planfix.
    """

    logger.info(f'\n{Fore.CYAN}def send_message_from_telegram_to_planfix{Style.RESET_ALL}\n')

    try:
        # Преобразование словаря в формат x-www-form-urlencoded
        planfix_data_str = "&".join(f"{quote(key)}={quote(value)}" for key, value in planfix_data.items())
        logger.debug(f"\n{Fore.YELLOW}Planfix_data_str:\n{planfix_data_str}{Style.RESET_ALL}")
        logger.debug(f"{Fore.YELLOW}Hex string: {planfix_data_str.encode('utf-8').hex()}{Style.RESET_ALL}")
        decoded_data = dict(parse_qsl(planfix_data_str))
        logger.debug(f"{Fore.YELLOW}Decoded data: {decoded_data}{Style.RESET_ALL}")

        # Вывод информации из planfix_data в консоль для отладки
        logger.info(f"\n{GREEN}Data in planfix_data:{RESET_ALL}\n")
        for key, value in planfix_data.items():
            logger.debug(f"{MAGENTA}{key}: {value}{RESET_ALL}")

        # Асинхронное управление клиентом aiohttp. Создается новая сессия для каждого запроса,
        # и контекстный менеджер 'async with' гарантирует корректное открытие и закрытие сессии.
        async with aiohttp.ClientSession() as session:

            # Заголовки для запроса
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded ',
                "Authorization": f"Bearer {planfix_api_key}"
            }

            # Проверка, что хотя бы одно поле содержит данные
            if any(value for value in planfix_data.values()):
                # Отправка POST-запроса с использованием библиотеки aiohttp
                async with session.post(planfix_api_url, headers=headers, data=planfix_data_str) as response:
                    # Получение тела ответа
                    response_text = await response.text()
                    logger.debug(f"{MAGENTA}Response from Planfix: {response_text}{RESET_ALL}")
                    return response_text
            # Если все поля в данных для Planfix пусты, выводим предупреждение в лог и возвращаем ошибку с кодом 400.
            else:
                logger.warning("All fields in planfix_data are empty. Skipping the request.")
                return ""
    except aiohttp.client_exceptions.ClientResponseError as error:
        # Обработка ошибок, связанных с ответами от сервера Planfix
        detailed_error = traceback.format_exc()
        logger.error(
            f"Error sending message to Planfix: {error.status}, message='{error.message}', "
            f"url={error.request_info.url}\n{detailed_error}")

        # Обработка дополнительных случаев ошибок Bad Request (400)
        if error.status == 400:
            response_text = error.message
            logger.error(f"Response text from Planfix: {response_text}")
        # Перевыбрасывание текущего исключения. Используется для повторного возбуждения
        # исключения после его обработки в блоке except, чтобы сохранить стек трассировки.
        raise
    except Exception as error:
        # Используйте traceback.format_exc() для получения детальной трассировки стека
        detailed_error = traceback.format_exc()
        logger.error(f"Error sending message to Planfix: {error}\n{detailed_error}")


@client.on(events.NewMessage())
async def handle_incoming_message(event: events.NewMessage.Event) -> None:
    """
        Asynchronous function handler for a new message from Telegram.

        Args:
            event (events.NewMessage.Event): New message event.

        Returns:
            None
    """
    logger.info(f'\n{Fore.CYAN}def handle_incoming_message{Style.RESET_ALL}\n')
    try:
        # Получение информации об отправителе сообщения
        sender = await event.get_sender()
        logger.info(f"Received message from sender type: {type(sender)}")

        # Добавьте проверку для приватных сообщений
        if not event.message.is_private or isinstance(event.message, types.MessageService) or event.message.out:
            return

        # Проверка, что сообщение не от бота 'planfix_bot'
        is_planfix_bot = event.message.from_id == 'planfix_bot'

        # Игнорирование сообщений от 'planfix_bot'
        if is_planfix_bot:
            return

        # Извлечение данных из сообщения и отправка их в Planfix
        planfix_data = await extract_telegram_data(event)
        # Ожидание отправки сообщения из Telegram в Planfix с использованием указанного API-URL и данных из Telegram.
        await send_message_from_telegram_to_planfix(planfix_api_url, planfix_data)

    except Exception as error:
        # Используйте traceback.format_exc() для получения детальной трассировки стека
        detailed_error = traceback.format_exc()
        logger.error(f"Error processing incoming message: {error}\n{detailed_error}")


async def extract_telegram_data(event: Message) -> dict:
    """
        Asynchronous function for extracting data from a Telegram event.

        Args:
            event (Message): Telegram event.

        Returns:
            dict: Returns a dictionary with extracted data.
    """
    logger.info(f'\n{Fore.CYAN}def extract_telegram_data{Style.RESET_ALL}\n')

    # Извлечение и преобразование данных из события
    chat_id = str(event.chat_id)
    message_text = event.text

    # Извлечение отправителя сообщения из события Telegram
    sender = await event.get_sender()

    # Проверка типа отправителя

    # Если отправитель - пользователь, используем его имя (если доступно)
    if isinstance(sender, types.User):
        contact_name = sender.first_name if sender.first_name else ""
    # Если отправитель - канал, используем его название (если доступно)
    elif isinstance(sender, types.Channel):
        contact_name = sender.title if sender.title else ""
    # В случае неизвестного типа отправителя
    else:
        # Логирование других случаев для отладки
        logger.debug(f"Received message from unknown sender type: {type(sender)}")
        contact_name = ""

    # Формирование словаря с извлеченными данными
    return {
        'cmd': 'newMessage',
        'providerId': telegram_integration_id,
        'chatId': chat_id,
        'planfix_token': planfix_api_key,
        'message': message_text,
        'contactId': await generate_contact_id(),
        'contactName': contact_name,
    }


async def generate_contact_id(length: int = 32) -> str:
    """
        Asynchronous function for generating a contact identifier.

        Args:
            length (int): Length of the generated token (default is 32).

        Returns:
            str: Returns the generated token.
    """
    logger.info(f'\n{Fore.CYAN}def generate_contact_id{Style.RESET_ALL}\n')

    try:
        # Проверка корректности входного параметра
        if not isinstance(length, int) or length <= 0:
            logger.error("Token length should be a positive integer.")
            raise ValueError("Token length should be a positive integer.")

        # Генерация токена
        logger.info("Token generated successfully.")
        return secrets.token_urlsafe(length)
    except Exception as error:
        # Обработка ошибок и логирование
        detailed_error = traceback.format_exc()
        logger.error(f"Error generating token: {error}\n{detailed_error}")
        raise


async def stop_client(client_token: str, client_number: str):
    """
        Asynchronous function for stopping the client.

        Args:
            client_token (str): Client token.
            client_number (str): Client number.

        Returns:
            None
    """

    # Вывод информационного сообщения в лог о вызове функции
    logger.info(f"\n{CYAN}def stop_client{RESET_ALL}\n")

    # Получение данных клиента
    client_data = sessions.get(client_token, {}).get('client_data', {})
    client_numbers = client_data.get('numbers', [])

    # Проверка на последний номер
    if len(client_numbers) == 1 and client_number in client_numbers:
        sessions[client_token]['status'] = 'offline'
        logger.info(f"Client {client_token} fully stopped")

    # Удаление номера клиента из списка
    if client_number in client_numbers:
        client_numbers.remove(client_number)
        sessions[client_token]['client_data']['numbers'] = client_numbers
        logger.info(f"Client {client_number} stopped successfully")

    # В случае, если клиент с указанным номером не найден для данного токена, логируем ошибку
    else:
        logger.error(f"Client {client_number} not found for token {client_token}")


async def start_integration_for_client(token: str):
    """
        Asynchronous function for starting integration for a client.

        Args:
            token (str): Client token.

        Returns:
            None
    """
    logger.info(f"\n{CYAN}def start_integration_for_client{RESET_ALL}\n")

    # Проверка наличия токена в резервных копиях сессий
    if token in sessions_backup:
        # Восстановление данных сессии из резервных копий
        session_data = sessions_backup[token]

        # Восстановление сохраненной сессии
        sessions[token]["client_session"] = session_data["client_session"]

        # Запуск интеграции
        await start()


async def start():
    """
        Asynchronous function for initializing and starting the Telegram client and uvicorn server.

        Returns:
            None
    """
    logger.debug(f'\n{Fore.CYAN}def start(){Style.RESET_ALL}\n')

    try:
        # Запуск клиента Telegram только если он еще не запущен
        if not client.is_connected():
            await client.start()

        # Конфигурация сервера uvicorn
        config = uvicorn.Config("__main__:asgi_app", port=5000, log_level="info")
        server = uvicorn.Server(config)

        # Запуск сервера uvicorn
        await server.serve()

    finally:
        # Отключение клиента Telegram
        await client.disconnect()

        # Очистка сессий при отключении клиента Telegram
        for token, session_data in sessions.items():
            await session_data['client_session'].close()
            logger.info(f"Session closed for token: {token}")

        # Ожидание отключения клиента Telegram
        await client.run_until_disconnected()


# Проверка, что код выполняется как отдельный скрипт
if __name__ == '__main__':
    client.loop.run_until_complete(start())
