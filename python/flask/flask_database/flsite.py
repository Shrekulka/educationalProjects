# flask_database/flsite.py
# Это укажет Flask где искать статику.
import os
import sqlite3
import traceback

from flask import Flask, render_template, g

from f_data_base import FDataBase
from logger import logger

os.environ["FLASK_STATIC"] = "./static"

# Инициализация Flask-приложения
app: Flask = Flask(__name__)

# Указываем Flask использовать папку 'static' для статических файлов (CSS, изображения и т. д.).
app.static_folder = 'static'

app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


# Устанавливает соединение с BD
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


# Вспомогательная функция для создания таблиц BD
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# Соединение с BD, если оно еще не установленно
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template("index.html", menu=dbase.get_menu())


# Закрываем соединение с BD, если оно было установленно
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Запуск приложения в режиме отладки на указанном хосте и порту
if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        logger.info("Приложение прервано пользователем")
    except Exception as error:
        # Обработка неожиданных ошибок с использованием логирования
        detailed_send_message_error = traceback.format_exc()
        logger.exception(f"Неожиданная ошибка в приложении: {error}\n{detailed_send_message_error}")
