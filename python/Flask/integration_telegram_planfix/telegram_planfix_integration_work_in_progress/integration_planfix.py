import xml.etree.ElementTree as ET

import aiohttp
from flask import request

from config import planfix_api_key, planfix_api_url
from flask_logging import logger
from integration_telegram import send_message_to_planfix, handle_error
from main import app


async def process_new_message_command(params):
    try:
        # Извлекаем параметры из запроса
        chat_id = params.get('chatId')
        planfix_token = params.get('planfix_token')
        message = params.get('message')
        contact_id = params.get('contactId')
        contact_name = params.get('contactName')
        contact_last_name = params.get('contactLastName')
        contact_ico = params.get('contactIco')
        contact_email = params.get('contactEmail')
        contact_phone = params.get('contactPhone')
        contact_data = params.get('contactData')
        attachments = params.get('attachments', [])

        # Отправляем сообщение в Планфикс
        action_id = await send_message_to_planfix(chat_id, planfix_token, message, contact_id, contact_name,
                                                  contact_last_name, contact_ico, contact_email, contact_phone,
                                                  contact_data, attachments)

        # Возвращаем успешный ответ
        return {"chatId": chat_id, "actionId": action_id}
    except Exception as e:
        logger.error(f"Error processing newMessage command: {e}")
        return {"error": "Internal server error"}


# Добавим обработчик команды в функцию обработки вебхука
async def handle_planfix_notification(xml_data):
    try:
        root = ET.fromstring(xml_data)
        command = root.find(".//cmd").text
        params = {elem.tag: elem.text for elem in root.iter() if elem.tag not in ['request', 'cmd']}

        if command == 'newMessage':
            result = await process_new_message_command(params)
            logger.info(f"Processed newMessage command. Result: {result}")
        else:
            logger.warning(f"Unsupported command: {command}")
    except Exception as e:
        logger.error(f"Error in handle_planfix_notification: {e}")


# Обновим вебхук для новой команды
@app.route('/webhook', methods=['POST'])
def planfix_webhook():
    try:
        xml_data = request.data.decode('utf-8')
        handle_planfix_notification(xml_data)
        return 'OK', 200
    except Exception as e:
        logger.error(f"Error in planfix_webhook: {e}")
        return 'Error', 500


def get_planfix_contact_number(contact_id, planfix_token):
    pass


async def process_get_contact_command(params):
    try:
        # Извлекаем параметры из запроса
        contact_id = params.get('contactId')
        planfix_token = params.get('planfix_token')

        # Получаем номер контакта в Планфиксе
        number = await get_planfix_contact_number(contact_id, planfix_token)

        # Возвращаем успешный ответ
        return {"number": number}
    except Exception as e:
        logger.error(f"Error processing getContact command: {e}")
        return {"error": "Internal server error"}


# Обновим обработчик команд в функции handle_planfix_notification
async def handle_planfix_notification(xml_data):
    try:
        root = ET.fromstring(xml_data)
        command = root.find(".//cmd").text
        params = {elem.tag: elem.text for elem in root.iter() if elem.tag not in ['request', 'cmd']}

        if command == 'newMessage':
            result = await process_new_message_command(params)
            logger.info(f"Processed newMessage command. Result: {result}")
        elif command == 'getContact':
            result = await process_get_contact_command(params)
            logger.info(f"Processed getContact command. Result: {result}")
        else:
            logger.warning(f"Unsupported command: {command}")
    except Exception as e:
        logger.error(f"Error in handle_planfix_notification: {e}")

# Асинхронная функция для получения ответа от Planfix по идентификатору сообщения
async def get_planfix_response(message_id) -> str:
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