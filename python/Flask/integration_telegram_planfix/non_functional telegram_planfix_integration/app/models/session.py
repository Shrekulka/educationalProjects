# non_functional telegram_planfix_integration/app/models/session.py

from app import db

print("session.py")


# відстежує сесії клієнта
class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(100), nullable=False)
    # Зв'язок з Client
    client = db.relationship('Client', back_populates='sessions')

    def __init__(self, name, path, client=None, session_id=None):
        self.session_id = session_id
        self.name = name
        self.path = path
        self.client = client

    def __repr__(self):
        return f"<Session {self.session_id}>" if self.session_id else "<Session (no id)>"
