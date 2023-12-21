# non_functional telegram_planfix_integration/app/utils.py

import re
import secrets
import time
import uuid
from email.utils import parseaddr
from functools import wraps

from flask import abort
from flask import request
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from wtforms.validators import ValidationError

from app import db
from app.models.client import Client
from app.models.message import Message
from app.services.planfix_client import send_planfix_message, get_planfix_message
from app.services.telethon_client import receive_telegram_message, send_telegram_message
from config import logger

print("utils.py")


# Автентифікація
def check_auth(f):
    """Декоратор для перевірки наявності токена автентифікації."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Auth-Token')
        if not token:
            logger.warning('Token is missing')
            abort(401, 'Token is missing')

        client = Client.query.filter_by(token=token).first()
        if not client:
            logger.warning('Invalid token')
            abort(401, 'Invalid token')

        return f(*args, **kwargs)

    return decorated


def save_message(client_id, text):
    """Збереження повідомлення в базі даних."""
    message = Message(client_id=client_id, text=text)
    db.session.add(message)
    db.session.commit()


def get_user_message(client_id):
    """Отримання повідомлень користувача з бази даних."""
    messages = Message.query.filter_by(client_id=client_id).all()
    return messages


# Бизнес-логика
def process_new_message(user_id, text):
    """Обробка нового повідомлення."""

    try:
        # Сохраняем сообщение в базе данных
        save_message(user_id, text)

        # Получаем информацию о клиенте по user_id
        client = Client.query.get(user_id)

        if client:
            # Проверяем, есть ли у клиента токен Planfix
            if client.token_planfix:
                # Отправляем сообщение в Planfix
                success = send_planfix_message(client.token_planfix, client.user_id, text)
                if success:
                    logger.info("Сообщение успешно отправлено в Planfix")
                else:
                    logger.warning("Не удалось отправить сообщение в Planfix")
            else:
                logger.warning("Клиент не имеет токен Planfix. Сообщение не отправлено.")
        else:
            logger.warning(f"Клиент с user_id={user_id} не найден. Сообщение не отправлено.")

    except IntegrityError as e:
        # Обработка ошибок IntegrityError
        logger.error(f"Ошибка IntegrityError при сохранении сообщения в базе данных: {e}")

    except SQLAlchemyError as e:
        # Обработка других ошибок SQLAlchemy
        logger.error(f"Ошибка SQLAlchemy при сохранении сообщения: {e}")

    except Exception as e:
        # Обработка других неожиданных ошибок
        logger.error(f"Необработанная ошибка: {e}")


def forward_message(source_user, dest_user, text):
    """Пересылка сообщения."""
    try:
        # Сохранение пересланного сообщения в базе данных
        save_message(dest_user, f"Forwarded from {source_user}: {text}")

        # Получение информации о клиентах отправителя и получателя
        source_client = Client.query.get(source_user)
        dest_client = Client.query.get(dest_user)

        if source_client and dest_client:
            # Проверка наличия токенов Planfix у отправителя и получателя
            if source_client.token_planfix and dest_client.token_planfix:
                # Отправка сообщения в Planfix с указанием отправителя и текста сообщения
                success = send_planfix_message(dest_client.token_planfix, dest_client.user_id,
                                               f"Forwarded from {source_user}: {text}")
                if success:
                    logger.info(f"Сообщение успешно переслано в Planfix от {source_user} к {dest_user}")
                else:
                    logger.warning(f"Не удалось переслать сообщение в Planfix от {source_user} к {dest_user}")
            else:
                logger.warning(f"Отправитель или получатель не имеют токен Planfix. Сообщение не переслано.")
        else:
            logger.warning(f"Отправитель или получатель не найдены. Сообщение не переслано.")

    except Exception as e:
        logger.error(f"Ошибка при пересылке сообщения: {e}")


def synchronize_messages_bidirectional():
    """Синхронизация новых сообщений между Telegram и Planfix в обе стороны."""
    while True:
        try:
            logger.info("Начало итерации синхронизации")
            print("Начало итерации синхронизации")

            # Получаем все новые сообщения из Telegram
            session_token = get_session_token()
            telegram_messages = receive_telegram_message(session_token)  # используйте синхронную версию
            logger.debug(f"Получено {len(telegram_messages)} новых сообщений из Telegram")
            print(f"Получено {len(telegram_messages)} новых сообщений из Telegram")

            # Перебираем полученные сообщения из Telegram
            for message in telegram_messages:
                # Получаем информацию о пользователе, отправившем сообщение
                source_user = message.get("sender")
                text = message.get("message")

                # Сохраняем полученное сообщение в базе данных
                save_message(source_user, text)
                logger.debug(f"Сообщение от пользователя {source_user} сохранено в базе данных")
                print(f"Сообщение от пользователя {source_user} сохранено в базе данных")

                # Добавляем логику синхронизации сообщения в Planfix
                client = Client.query.get(source_user)

                if client:
                    # Проверяем, есть ли у пользователя токен Planfix
                    if client.token_planfix:
                        # Отправляем сообщение в Planfix с указанием отправителя и текста сообщения
                        success = send_planfix_message(client.token_planfix, client.user_id,
                                                       f"Received from Telegram: {text}")
                        if success:
                            logger.info(f"Сообщение успешно синхронизировано в Planfix от пользователя {source_user}")
                            print(f"Сообщение успешно синхронизировано в Planfix от пользователя {source_user}")
                        else:
                            logger.warning(
                                f"Не удалось синхронизировать сообщение в Planfix от пользователя {source_user}")
                            print(f"Не удалось синхронизировать сообщение в Planfix от пользователя {source_user}")
                    else:
                        logger.warning(
                            f"Пользователь {source_user} не имеет токена Planfix. Сообщение не синхронизировано.")
                        print(f"Пользователь {source_user} не имеет токена Planfix. Сообщение не синхронизировано.")
                else:
                    logger.warning(f"Пользователь {source_user} не найден. Сообщение не синхронизировано.")
                    print(f"Пользователь {source_user} не найден. Сообщение не синхронизировано.")

            # Получаем все новые сообщения из Planfix
            planfix_messages = get_planfix_message('token_planfix')
            logger.debug(f"Получено {len(planfix_messages)} новых сообщений из Planfix")
            print(f"Получено {len(planfix_messages)} новых сообщений из Planfix")

            # Перебираем полученные сообщения из Planfix
            for planfix_message in planfix_messages:
                # Получаем информацию о пользователе и текст сообщения из Planfix
                planfix_user_id = planfix_message.get("user_id")
                planfix_text = planfix_message.get("text")

                # Сохраняем полученное сообщение в базе данных
                save_message(planfix_user_id, planfix_text)
                logger.debug(f"Сообщение от пользователя {planfix_user_id} сохранено в базе данных")
                print(f"Сообщение от пользователя {planfix_user_id} сохранено в базе данных")

                # Добавляем логику синхронизации сообщения в Telegram
                planfix_client = Client.query.filter_by(user_id=planfix_user_id).first()

                if planfix_client:
                    # Проверяем, есть ли у пользователя токен Telegram
                    if planfix_client.session_token:
                        # Отправляем сообщение в Telegram с указанием отправителя и текста сообщения
                        success = send_telegram_message(planfix_client.session_token, 'username',
                                                        f"Received from Planfix: {planfix_text}")
                        if success:
                            logger.info(
                                f"Сообщение успешно синхронизировано в Telegram от пользователя {planfix_user_id}")
                            print(f"Сообщение успешно синхронизировано в Telegram от пользователя {planfix_user_id}")
                        else:
                            logger.warning(
                                f"Не удалось синхронизировать сообщение в Telegram от пользователя {planfix_user_id}")
                            print(f"Не удалось синхронизировать сообщение в Telegram от пользователя {planfix_user_id}")
                    else:
                        logger.warning(
                            f"Пользователь {planfix_user_id} не имеет токена Telegram. Сообщение не синхронизировано.")
                        print(
                            f"Пользователь {planfix_user_id} не имеет токена Telegram. Сообщение не синхронизировано.")
                else:
                    logger.warning(f"Пользователь {planfix_user_id} не найден. Сообщение не синхронизировано.")
                    print(f"Пользователь {planfix_user_id} не найден. Сообщение не синхронизировано.")

            # Пауза между итерациями (например, каждую секунду)
            time.sleep(1)

            logger.info("Завершение итерации синхронизации")
            print("Завершение итерации синхронизации")

        except Exception as e:
            logger.error(f"Ошибка в фоновой задаче синхронизации: {e}", exc_info=True)
            print(f"Ошибка в фоновой задаче синхронизации: {e}")
            time.sleep(1)


# Вебхуки
def get_session_token():
    """Получение токена сессии из объекта запроса Flask."""
    return request.headers.get('X-Session-Token')


def process_telegram_webhook(data):
    """Обробка вебхука від Telegram."""
    try:
        # Проверяем наличие ключей в словаре data
        user_id = data.get("user_id")
        message_text = data.get("message_text")

        if user_id is not None and message_text is not None:
            # Пример: сохраняем полученное сообщение в базе данных
            save_message(user_id, message_text)

            # Добавьте здесь логику для дальнейшей обработки входящего вебхука от Telegram

            logger.info(f"Получен вебхук от Telegram. Пользователь {user_id} отправил сообщение: {message_text}")
        else:
            logger.warning("Получен неполный вебхук от Telegram. Отсутствуют ключи 'user_id' или 'message_text'.")
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука от Telegram: {e}")


def process_planfix_webhook(data):
    """Обробка вебхука від Planfix."""
    try:
        # Проверяем наличие ключей в словаре data
        user_id = data.get("user_id")
        message_text = data.get("message_text")

        if user_id is not None and message_text is not None:
            # Пример: сохраняем полученное сообщение в базе данных
            save_message(user_id, message_text)

            # Добавьте здесь логику для дальнейшей обработки входящего вебхука от Planfix

            logger.info(f"Получен вебхук от Planfix. Пользователь {user_id} отправил сообщение: {message_text}")
        else:
            logger.warning("Получен неполный вебхук от Planfix. Отсутствуют ключи 'user_id' или 'message_text'.")
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука от Planfix: {e}")


def validate_message_data(data):
    """Валідація даних для відправки повідомлення."""
    if data.get("session_token") is not None and data.get("receiver_username") is not None and data.get(
            "message_text") is not None:
        return True
    else:
        logger.warning("Неполные данные для відправки повідомлення: %s", data)
        return False


def validate_notifications_data(data):
    """Валідація даних для отримання повідомлень."""
    if data.get("session_token") is not None:
        return True
    else:
        logger.warning("Неполные дані для отримання повідомлень: %s", data)
        return False


def generate_token(length=32):
    """
    Генерирует криптографически безопасный случайный токен.

    Parameters:
    - length (int): Длина токена. По умолчанию 32.

    Returns:
    - str: Сгенерированный токен.
    """
    try:
        if not isinstance(length, int) or length <= 0:
            raise ValueError("Длина токена должна быть положительным целым числом.")

        return secrets.token_hex(length)
    except Exception as e:
        logger.error(f"Ошибка при генерации токена: {e}")
        raise


def is_valid_token(field):
    """Валидация токена.

    Parameters:
    - field: Токен для валидации.

    Raises:
    - ValidationError: Если токен имеет неверный формат.
    """
    if not re.fullmatch(r"^[a-fA-F0-9]{32}$", field):
        logger.warning(f"Неверный формат токена: {field}")
        raise ValidationError("Токен должен состоять из 32 шестнадцатеричных символов.")


def validate_client_data(data):
    """Валідація даних для створення клієнта."""
    try:
        if "name" in data and "number" in data:
            return True, generate_token()
        else:
            return False, None
    except Exception as e:
        logger.error(f"Помилка при валідації даних клієнта: {e}")
        return False, None


def validate_channel(channel):
    """
    Проверяет, что номер телефона состоит из 10 цифр.

    Parameters:
    - channel (str or None): Номер телефона для валидации.

    Returns:
    - bool: True, если номер телефона валиден, иначе False.
    """
    if channel is not None and re.match(r'^\d{10}$', str(channel)) is not None:
        return True
    else:
        logger.warning("Невалидний номер телефону: %s", channel)
        return False


def validate_email(email):
    """
    Валидация электронной почты.
    """
    if not email:
        raise ValueError("Email address is required")

    # Используем функцию parseaddr для анализа электронного адреса
    _, addr = parseaddr(email)

    # Проверяем, что адрес электронной почты не пустой и соответствует шаблону
    if not re.match(r"[^@]+@[^@]+\.[^@]+", addr):
        raise ValueError("Invalid email address")

    return email


def generate_session_id():
    """Генерація ідентифікатора сесії."""
    try:
        return str(uuid.uuid4())
    except Exception as e:
        logger.error(f"Помилка при генерації ідентифікатора сесії: {e}")
        raise


def format_datetime_iso(dt):
    """Форматування дати у форматі ISO."""
    try:
        return dt.isoformat() if dt else None
    except Exception as e:
        logger.warning(f"Помилка при форматуванні дати: {e}")
        return None
