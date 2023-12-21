# non_functional telegram_planfix_integration/app/views.py

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app import db
from .models.client import Client
from .models.message import Message
from .models.session import Session
from .utils import (send_telegram_message, is_valid_token, validate_channel, send_planfix_message,
                    generate_token, process_telegram_webhook, validate_message_data)
print("views.py")
print("Создание Blueprint")
# Создание Blueprint для обработки запросов, связанных с Telegram.
telegram_blueprint = Blueprint('telegram', __name__)
# Создание Blueprint для обработки запросов, связанных с получением статуса.
get_status_blueprint = Blueprint('get_status', __name__)


@telegram_blueprint.route('/create_client', methods=['POST'])
def create_client():
    try:
        # Проверяем, что содержимое запроса в формате JSON
        if request.is_json:
            # Получаем данные из запроса
            data = request.get_json()

            # Валидация запроса
            required_fields = ['name', 'channel']
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400

            channel = data.get('channel')
            if not validate_channel(channel):
                return jsonify({'error': 'Invalid channel format'}), 400

            # Генерируем токен
            token = generate_token()

            # Создаем клиента
            new_client = Client(
                name=data['name'],
                channel=channel,
                token=token  # Передаем сгенерированный токен
            )

            db.session.add(new_client)
            db.session.commit()

            # Возвращаем ответ с данными
            return jsonify({
                'message': 'Client created successfully',
                'client_id': new_client.id,
                'token': token
            }), 201
        else:
            return jsonify({'error': 'Invalid content type, JSON expected'}), 400

    except ValidationError as e:
        return jsonify({'error': str(e)}), 422
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


# Получение списка всех клиентов
@telegram_blueprint.route('/clients', methods=['GET'])
def get_client():
    clients = Client.query.all()
    clients_data = []

    for client in clients:
        clients_data.append(client.serialize)

    return jsonify(clients_data)


# Получение статуса клиента
@get_status_blueprint.route('/get_status/<int:client_id>', methods=['GET'])
def get_status(client_id):
    try:
        client = Client.query.get_or_404(client_id)
        status = client.status
        return jsonify({'status': status}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


# Обработчик HTTP-запроса на удаление клиента.
@telegram_blueprint.route('/delete_client/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"error": "Клиент не найден"}), 404

    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Клиент удален"})


@telegram_blueprint.route('/start_session/<int:client_id>', methods=['POST'])
def start_session(client_id):
    try:
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'Клиент не найден'}), 404

        # Проверяем, активна ли уже сессия
        if client.current_session and client.current_session.is_active:
            return jsonify({'error': 'Сессия уже активна'}), 400

        # Получаем имя клиента и генерируем путь для новой сессии
        session_name = f"Session_{client_id}"
        session_path = f"/sessions/{session_name}"

        # Создаем новую сессию без явного указания client_id
        new_session = Session(name=session_name, path=session_path)
        client.sessions.append(new_session)  # Добавляем сессию к клиенту
        db.session.add(new_session)
        db.session.commit()

        # Возвращаем полный объект сессии в JSON
        session_data = {
            'session_id': new_session.session_id,
            'name': new_session.name,
            'path': new_session.path,
            'client_id': client.id  # Добавляем информацию о клиенте
        }

        return jsonify({'message': 'Сессия успешно запущена', 'session': session_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Получение списка сессий для указанного клиента
@telegram_blueprint.route('/sessions/<int:client_id>', methods=['GET'])
def get_sessions(client_id):
    client = Client.query.get(client_id)

    if not client:
        return jsonify({'error': 'Client not found'})

    sessions_data = []
    for session in client.sessions:
        sessions_data.append(session.serialize)

    return jsonify(sessions_data)


@telegram_blueprint.route('/stop_session/<int:client_id>', methods=['POST'])
def stop_session(client_id):
    try:
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Проверка, есть ли активная сессия
        if not client.current_session or not client.current_session.is_active:
            return jsonify({'error': 'No active session to stop'}), 400

        # Остановка текущей сессии
        client.current_session.end_session()
        db.session.commit()

        return jsonify({'message': 'Session stopped successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Создание сообщения
@telegram_blueprint.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    # Валидация данных
    if not validate_message_data(data):
        return jsonify({'error': 'Invalid message data'}), 400

    # Извлечение данных из запроса
    client_id = data['client_id']
    text = data['text']

    # Создание нового сообщения
    message = Message(client_id=client_id, text=text)
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message created successfully', 'message_id': message.id}), 201


# Получение сообщения по ID
@telegram_blueprint.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    return jsonify(message.serialize)


# Отправка сообщения
@telegram_blueprint.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()

        # Проверка наличия обязательных параметров в запросе
        required_fields = ['token', 'chat_id', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Валидация токена и идентификатора чата (можно добавить дополнительные проверки)
        if not is_valid_token(data['token']):
            return jsonify({'error': 'Invalid token'}), 401

        if not isinstance(data['chat_id'], int) or data['chat_id'] <= 0:
            return jsonify({'error': 'Invalid chat_id'}), 400

        # Вызов синхронной функции send_telegram_message
        success = send_telegram_message(data['token'], data['chat_id'], data['message'])

        if success:
            return jsonify({'message': 'Message sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send message'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Получение сообщений от Телеграм
@telegram_blueprint.route('/receive_message', methods=['POST'])
def receive_message():
    try:
        data = request.get_json()

        if 'token' not in data or not is_valid_token(data['token']):
            return jsonify({'error': 'Invalid token'}), 401

        if 'isEcho' in data and data['isEcho']:
            return jsonify({'message': 'Ignored message (echo)'}), 200

        if 'userName' in data and data['userName'] == 'planfix_bot':
            return jsonify({'message': 'Ignored message from planfix_bot'}), 200

        # Обработка сообщения
        if 'message' in data:
            # Получаем данные из сообщения
            chat_id = data.get('chat_id', '')
            message_text = data['message']

            # Отправляем сообщение в ПланФикс
            success = send_planfix_message(data['token_planfix'], chat_id, message_text)

            if success:
                # Теперь добавим код для отправки ответа из Planfix в Telegram
                telegram_success = send_telegram_message(data['token'], data['chat_id'],
                                                         f"Planfix ответил: {message_text}")

                # Обработка вебхука от Telegram
                process_telegram_webhook(data)

                if telegram_success:
                    return jsonify({'message': 'Message sent to Planfix and Telegram successfully'}), 200
                else:
                    return jsonify({'error': 'Failed to send message to Telegram'}), 500
            else:
                return jsonify({'error': 'Failed to send message to Planfix'}), 500

        return jsonify({'message': 'Message received successfully'}), 200
    except KeyError as ke:
        return jsonify({'error': f'Missing key in data: {str(ke)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Обновление сообщения
@telegram_blueprint.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    data = request.get_json()

    # Валидация данных
    if not validate_message_data(data):
        return jsonify({'error': 'Invalid message data'}), 400

    # Обновление данных сообщения
    message.text = data['text']

    db.session.commit()

    return jsonify({'message': 'Message updated successfully'})


# Удаление сообщения
@telegram_blueprint.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'Message deleted successfully'})
