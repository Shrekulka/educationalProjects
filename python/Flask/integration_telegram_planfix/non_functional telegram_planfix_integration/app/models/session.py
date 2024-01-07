# non_functional telegram_planfix_integration/app/models/session.py
from typing import Optional

from app import db

print("session.py")


# відстежує сесії клієнта
class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    # Имя сессии
    session_name: Optional[str] = db.Column(db.String(50), nullable=False)
    # Путь к сессии (локальное сховище)
    session_path: Optional[str] = db.Column(db.String(100), nullable=False)
    # Зв'язок з Client
    client = db.relationship('Client', back_populates='sessions')
    messages = db.relationship('Message', back_populates='session')

    def __init__(self, name, path, client=None, session_id=None):
        self.session_id = session_id
        self.name = name
        self.path = path
        self.client = client

    def __repr__(self):
        return f"<Session {self.session_id}>" if self.session_id else "<Session (no id)>"
