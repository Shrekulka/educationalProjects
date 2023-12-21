# non_functional telegram_planfix_integration/app/services/telethon_client.py

import logging
import threading

from telethon import events, errors
from telethon.sync import TelegramClient
from telethon.tl import types

from app import db
from app.models.client import Client
from config import Config

print("telethon_client.py")


def create_telegram_client(name, channel):
    """Создание нового клиента Telegram."""
    try:
        with db.session.begin_nested():
            client = Client(name=name, channel=channel)
            db.session.add(client)
        return {'success': True, 'message': 'Client created successfully'}
    except Exception as e:
        logging.error(f"Error in create_telegram_client: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def update_telegram_client_status(session_token, enabled):
    """Обновление статуса клиента Telegram."""
    try:
        with db.session.begin_nested():
            client = Client.query.filter_by(session_token=session_token).first()
            if client:
                client.enabled = enabled
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in update_telegram_client_status: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def get_telegram_client_by_token(session_token):
    """
    Получение клиента Telegram по токену.

    :param session_token: Токен сессии клиента Telegram.
    :return: Объект клиента Telegram или None, если клиент не найден.
    """
    try:
        client = Client.query.filter_by(session_token=session_token).first()
        return client
    except Exception as e:
        # Логгирование ошибки
        logging.error(f"Error in get_telegram_client_by_token: {e}", exc_info=True)
        return None


# Функции для работы с Telegram
def start_telegram_client(session_token):
    """Запуск клиента Telegram."""
    try:
        client = TelegramClient(session_token, Config.telegram_api_id, Config.telegram_api_hash)
        client.start()

        # Настройка обработчика событий для обработки входящих сообщений
        @client.on(events.NewMessage(chats='username'))
        def handle_new_message(event):
            if isinstance(event.message, types.Message):
                logging.info(event.raw_text)  # Можем модифицировать это для сохранения сообщений в базе данных

        # Запуск клиента в отдельном потоке
        thread = threading.Thread(target=client.run_until_disconnected)
        thread.start()

        return "online"
    except Exception as e:
        logging.error(f"Ошибка при запуске клиента: {e}")
        return "offline"


def stop_telegram_client(session_token):
    """Остановка клиента Telegram."""
    try:
        client = TelegramClient(session_token, Config.telegram_api_id, Config.telegram_api_hash)

        # Проверка, что клиент был запущен
        if not client.is_connected():
            logging.warning("Попытка остановить не запущенного клиента")
            return False

        # Использование контекстного менеджера для управления соединением
        with client:
            client.disconnect()

        logging.info("Клиент успешно отключен")
        return True

    except Exception as e:
        logging.error(f"Ошибка при отключении клиента: {e}")
        return False


def send_telegram_message(session_token, receiver_username, message_text):
    """Отправка сообщения в Telegram."""
    try:
        with TelegramClient(session_token, Config.telegram_api_id, Config.telegram_api_hash) as client:
            client.send_message(receiver_username, message_text)
            logging.info("Сообщение успешно отправлено")

        return True
    except errors.FloodWaitError as e:
        logging.warning(f"Получено исключение FloodWaitError. Ожидание: {e.seconds} сек.")
        return False
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
        return False


def receive_telegram_message(session_token, limit=None):
    """Получение и обработка новых сообщений из Telegram."""
    try:
        with TelegramClient(session_token, Config.telegram_api_id, Config.telegram_api_hash) as client:
            client.start()
            # Получение всех доступных сообщений с учетом лимита
            messages = client.get_messages('me', limit=limit)

            # Обработка и возврат полученных сообщений в обратном порядке
            result_messages = []
            for message in reversed(messages):
                result_messages.append({
                    'sender': message.sender_id,
                    'message': message.text
                })
            return result_messages
    except errors.FloodWaitError as e:
        logging.warning(f"Получено исключение FloodWaitError. Ожидание: {e.seconds} сек.")
        return []
    except Exception as e:
        logging.error(f"Ошибка при получении и обработке сообщений из Telegram: {e}", exc_info=True)
        return []
