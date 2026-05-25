# non_functional telegram_planfix_integration/app/__init__.py

import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from config import Config  # Импорт конфига

print("__init__.py")
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Инициализация Flask-Migrate

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.DEBUG)
print("Настройка логирования")
from app.views import telegram_blueprint, get_status_blueprint

# Регистрация Blueprint'ов
print("Регистрация Blueprint'ов")
app.register_blueprint(telegram_blueprint, url_prefix='/telegram')
app.register_blueprint(get_status_blueprint, url_prefix='/get_status')


@app.shell_context_processor
def make_shell_context():
    from app.models.client import Client
    from app.models.message import Message
    from app.models.session import Session
    print("def make_shell_context()")
    return {'db': db, 'Client': Client, 'Message': Message, 'Session': Session}

# from app.utils import synchronize_messages_bidirectional
# # Запуск синхронізації повідомлень після ініціалізації додатку
# synchronize_messages_bidirectional()
