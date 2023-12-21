# non_functional telegram_planfix_integration/app/models/message.py

from datetime import datetime

from app import db

print("message.py")


# використовується для представлення повідомлень.
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # нежеуказанные поля пока не используем
    content = db.Column(db.String(255), nullable=True)
    sender_id = db.Column(db.Integer, nullable=True)
    recipient_id = db.Column(db.Integer, nullable=False)
    planfix_message_id = db.Column(db.String(50), nullable=True)  # Додайте колонку для ID повідомлення в Планф

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
