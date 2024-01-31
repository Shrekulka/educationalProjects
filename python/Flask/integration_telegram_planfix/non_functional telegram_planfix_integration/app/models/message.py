# non_functional telegram_planfix_integration/app/models/message.py

from datetime import datetime
from typing import Optional

from app import db

print("message.py")


# використовується для представлення повідомлень.
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cmd - Тип операции
    providerId - Идентификатор сторонней системы
    chat_id: Optional[str] = db.Column(db.String(255), nullable=True)
    text = db.Column(db.Text, nullable=False)
    token - Токен  клиента
    message - Содержимое  сообщения
    messageId - ID  сообщения  в  системе  Planfix



    # Уникальный идентификатор контакта
    contact_id: Optional[str] = db.Column(db.String(255), nullable=True)
    # токен авторизации клиента
    token: Optional[str] = db.Column(db.String(255), unique=True)

    # Имя контакта
    user_name: Optional[str] = db.Column(db.String(255), nullable=True)

    # Фамилия контакта
    user_last_name: Optional[str] = db.Column(db.String(255), nullable=True)

    # Фото контакта
    user_ico: Optional[str] = db.Column(db.String(255), nullable=True)

    # Email контакта
    user_email: Optional[str] = db.Column(db.String(255), nullable=True)

    # Email сотрудника-автора исходящего сообщения
    user_channel: Optional[str] = db.Column(db.String(255), nullable=True)



    # Текущая сессия клиента (отношение один к одному), каждый клиент может иметь только одну текущую сессию
    current_session = db.relationship('Session', uselist=False, backref="client")
    # Зв'язок з Client
    client = db.relationship('Client', backref='messages')

    # Зв'язок з Session
    session = db.relationship('Session', back_populates='messages')

    def __init__(self, client_id, text, timestamp=None, content=None, sender_id=None, recipient_id=None,
                 planfix_message_id=None, client=None, session=None):
        self.client_id = client_id
        self.text = text
        self.timestamp = timestamp if timestamp else datetime.utcnow()
        self.content = content
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.planfix_message_id = planfix_message_id
        self.client = client
        self.session = session

    def __repr__(self):
        return f"<Message {self.id}>"
