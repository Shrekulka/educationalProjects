Non-Functional Telegram-Planfix Integration Example!!!

1. Структура проекта:
```bash
non_functional telegram_planfix_integration/   # Основна папка проекта.
│
│
├── app/                              # Основная папка приложения Flask.
│   ├── __init__.py                   # Файл, обозначающий эту папку как пакет Python.
│   ├── views.py                      # Файл, где находятся маршруты (роутеры) и логика обработки запросов.
│   ├── utils.py                      # Вспомогательные функции для проекта.
│   │
│   ├── services/ 
│   │   ├── telethon_client.py
│   │   └── planfix_client.py  
│   │
│   ├── models/                       # Папка, где находятся файлы для моделей данных.
│   │   ├── __init__.py               # Файл, обозначающий эту папку как пакет Python.
│   │   ├── client.py                 # Файл с моделью для клиента.
│   │   ├── session.py                # Файл с моделью для сессии.
│   │   └── message.py                # Файл с моделью для сообщения.
│
├── schemas/                          # Папка для файлов схем данных, используемых для валидации и сериализации данных.
│   ├── __init__.py                   # Файл, обозначающий эту папку как пакет Python.
│   ├── client_schema.py              # Файл с схемой для клиента.
│   ├── session_schema.py             # Файл с схемой для сессии.
│   └── session_message.py            # Файл с схемой для сообщения.
│
├── templates/                        # Папка, где можно хранить HTML-шаблоны, если они используются в приложении.
│
├── static/                           # Папка для хранения статических файлов, таких как CSS, JavaScript, изображения.
│   ├── js                            # Папка для JavaScript-файлов.
│   ├── css/                          # Папка для стилей (CSS).
│   └── img/                          # Папка для изображений.
│
├── migrations/                       # Папка для хранения миграционных скриптов базы данных.
│   ├── versions/                     # Подпапка, где хранятся версии миграций.
│   ├── alembic.ini                   # Файл конфигурации Alembic для управления миграциями.
│   ├── env.py                        # Файл настройки окружения для Alembic.
│   ├── README                        # Файл с документацией и инструкциями по миграциям.
│   └── script.py.mako                # Файл шаблона для создания новых миграций.
│
│
├── venv/          # Виртуальное окружение Python, которое рекомендуется использовать для изоляции зависимостей проекта.
│
├── .env                  # Файл с переменными окружения (например, ключами API).
│
├── config.py             # Файл с настройками для проекта.
│
├── requirements.txt      # Файл, где указаны зависимости (библиотеки и их версии) для проекта. Это может
│                         # использоваться для легкого разворачивания проекта на других системах.
│
├── app.py                # Точка входа в приложение. Файл, где находится код для создания и запуска приложения.
│
├── site.db               # Файл базы данных SQLite.
│
├── constants.py          # Файл с константами
```
2. telegram_planfix_integration/app.py
    ```bash
    from app import app
    
    if __name__ == '__main__':
        app.run(debug=True)
    ```
3. telegram_planfix_integration/config.py
    ```bash
    import os
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    
    class Config:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'site.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        telegram_api_id = os.environ.get('TELEGRAM_API_ID')
        telegram_api_hash = os.environ.get('TELEGRAM_API_HASH')
        telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        planfix_api_url = os.environ.get('PLANFIX_API_URL')
        planfix_api_key = os.environ.get('PLANFIX_API_KEY')
    ```
4. schemas/
    a) __init__.py
    b) telegram_planfix_integration/schemas/client_schema.py
    ```bash
    class SessionSchema(Schema):
        session_id = fields.Int()
        name = fields.Str()
        path = fields.Str()
    class ClientSchema(Schema):
        name = fields.Str(required=True)
        channel = fields.Str(required=True, validate=validate_channel)
        created_at = fields.DateTime()
        updated_at = fields.DateTime()
        token = fields.Str()
        user_id = fields.Int()
        name_session = fields.Str()
        path_session = fields.Str()
        chat_id = fields.Str()
        message = fields.Str()
        title = fields.Str()
        contact_id = fields.Str()
        contact_name = fields.Str()
        contact_last_name = fields.Str()
        contact_ico = fields.Str()
        contact_email = fields.Str(validate=validate_email)
        contact_data = fields.Str()
        attachments_name = fields.Str()
        attachments_url = fields.Str()
        user_email = fields.Str(validate=validate_email)
        telegram_user_name = fields.Str()
        telegram_user_id = fields.Str()
        token_planfix = fields.Str()
        url_planfix = fields.Str()
        current_session = fields.Nested(SessionSchema(), exclude=('client',))
        sessions = fields.Nested(SessionSchema(), many=True, exclude=('client',))
    
        # Валидация статуса сессии
        status = fields.Str(validate=validate.OneOf([status.value for status in SessionStatusEnum]))
    ```   
5. app/
    a) __init__.py
    ```bash
    # non_functional telegram_planfix_integration/app/__init__.py
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db) 
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    from app.views import telegram_blueprint
    app.register_blueprint(telegram_blueprint, url_prefix='/telegram')
    app.register_blueprint(get_status_blueprint, url_prefix='/get_status')
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Client': Client, 'Message': Message, 'Session': Session}
    ```
    b) utils.py
    ```bash
    # non_functional telegram_planfix_integration/app/utils.py - реализован следующий фунционал
    # Декоратор для проверки наличия токена аутентификации.
    def check_auth(f):
    # Сохранение сообщения в базе данных.
    def save_message(client_id, text):
    # Получение пользовательских сообщений из базы данных.
    def get_user_message(client_id):
    # Обработка нового сообщения.
    def process_new_message(user_id, text):
    # Пересылка сообщения.
    def forward_message(source_user, dest_user, text):
    # Синхронизация новых сообщений между Telegram и Planfix в обеих сторонах.
    def synchronize_messages_bidirectional():
    # Получение токена сессии из объекта запроса Flask.
    def get_session_token():  
    # Обработка вебхука от Telegram.
    def process_telegram_webhook(data):
    # Обработка вебхука от Planfix.
    def process_planfix_webhook(data):
    # Валидация данных для отправки сообщения.
    def validate_message_data(data):
    # Валидация данных для получения сообщений.
    def validate_notifications_data(data):
    #  Генерирует криптографически безопасный случайный токен.
    def generate_token(length=32):
    # Валидация токена.
    def is_valid_token(field):
    # Валидация данных для создания клиента.
    def validate_client_data(data):
    # Проверяет, что номер телефона состоит из 10 цифр.
    def validate_channel(channel):
    # Валидация электронной почты.
    def validate_email(email):
    # Генерация идентификатора сессии
    def generate_session_id():
    # Форматирование даты в формате ISO.
    def format_datetime_iso(dt):
    ```
    c) views.py
    ```bash
    # non_functional telegram_planfix_integration/app/views.py - реализован следующий фунционал
    # Создание Blueprint для обработки запросов, связанных с Telegram.
    telegram_blueprint = Blueprint('telegram', __name__)
    # Создание Blueprint для обработки запросов, связанных с получением статуса.
    get_status_blueprint = Blueprint('get_status', __name__)
    # Обработчик запроса на создание нового клиента.
    @telegram_blueprint.route('/create_client', methods=['POST'])
    def create_client():
    # Получение списка всех клиентов
    @telegram_blueprint.route('/clients', methods=['GET'])
    def get_client():
   # Получение статуса клиента
    @get_status_blueprint.route('/get_status/<int:client_id>', methods=['GET'])
    def get_status(client_id):
    # Обработчик HTTP-запроса на удаление клиента.
    @telegram_blueprint.route('/delete_client/<int:client_id>', methods=['DELETE'])
    def delete_client(client_id):
    # Обработчик запроса на начало новой сессии для клиента.
    @telegram_blueprint.route('/start_session/<int:client_id>', methods=['POST'])
    def start_session(client_id):
    # Получение списка сессий для указанного клиента
    @telegram_blueprint.route('/sessions/<int:client_id>', methods=['GET'])
    def get_sessions(client_id):
    # Обработчик запроса на завершение текущей сессии для клиента.
    @telegram_blueprint.route('/stop_session/<int:client_id>', methods=['POST'])
    def stop_session(client_id):
    # Создание сообщения
    @telegram_blueprint.route('/messages', methods=['POST'])
    def create_message():
   # Получение сообщения по ID
    @telegram_blueprint.route('/messages/<int:message_id>', methods=['GET'])
    def get_message(message_id):
    # Отправка сообщения
    @telegram_blueprint.route('/send_message', methods=['POST'])
    def send_message():
    # Получение сообщений от Телеграм
    @telegram_blueprint.route('/receive_message', methods=['POST'])
    def receive_message():
    # Обновление сообщения
    @telegram_blueprint.route('/messages/<int:message_id>', methods=['PUT'])
    def update_message(message_id):
    # Удаление сообщения
    @telegram_blueprint.route('/messages/<int:message_id>', methods=['DELETE'])
    def delete_message(message_id):
    ```
    d) services/
    * planfix_client.py
    ```bash
    # Отримання користувача з Planfix за токеном.
    def get_planfix_user(token):
    # Відправлення повідомлення в Planfix."
    def send_planfix_message(token_planfix, user_id, text):
    # Отримання всіх нових повідомлень з Planfix.
    def get_planfix_message(token_planfix, limit=10):
    ```
    * telethon_client.py
    ```bash
    # Создание нового клиента Telegram.
    def create_telegram_client(name, channel):
    # Обновление статуса клиента Telegram.
    def update_telegram_client_status(session_token, enabled):
    # Получение клиента Telegram по токену.
    def get_telegram_client_by_token(session_token):
    # Запуск клієнта Telegram.
    def start_telegram_client(session_token):
    # Остановка клиента Telegram.
    def stop_telegram_client(session_token):
    # Отправка сообщения в Telegram.
    def send_telegram_message(session_token, receiver_username, message_text):
    # Получение и обработка новых сообщений из Telegram.
    def receive_telegram_message(session_token, limit=None):
    ```
    e) models/
    * __init__.py
    * client.py
    ```bash
    # non_functional telegram_planfix_integration/app/models/client.py - реализован следующий фунционал
    class SessionStatusEnum(Enum):
        """Enum для статусов сессии."""
        ONLINE = "online"
        OFFLINE = "offline"
    class Client(db.Model):
    # 1) Основные поля для таблицы Client
    id: int = db.Column(db.Integer, primary_key=True) # Уникальный идентификатор записи
    name: str = db.Column(db.String(255)) # Название клиента
    channel: str = db.Column(db.String(255), nullable=False, unique=True) # Номер телефона
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow) # Время создания записи
    updated_at: Optional[datetime] = db.Column(db.DateTime, onupdate=datetime.utcnow) # Время последнего обновления записи
    token: Optional[str] = db.Column(db.String(255), unique=True) # Токен клиента
    user_id: Optional[int] = db.Column(db.Integer, db.ForeignKey('user.id')) # Идентификатор пользователя (внешний ключ)
    user = relationship('User') # Позволяет установить отношение с моделью User и создать обратную ссылку, чтобы можно было легко получать клиентов,
    # связанных с конкретным пользователем.
    name_session: Optional[str] = db.Column(db.String(255), nullable=True) # Имя сессии
    path_session: Optional[str] = db.Column(db.String(255), nullable=True) # Путь к сессии (локальное сховище)
    chat_id: Optional[str] = db.Column(db.String(255), nullable=True)  # Уникальный id чата
    message: Optional[str] = db.Column(db.String, nullable=True) # Содержимое сообщения
    title: Optional[str] = db.Column(db.String(255), nullable=True) # Заголовок сообщения
    contact_id: Optional[str] = db.Column(db.String(255), nullable=True) # Уникальный идентификатор контакта
    contact_name: Optional[str] = db.Column(db.String(255), nullable=True) # Имя контакта
    contact_last_name: Optional[str] = db.Column(db.String(255), nullable=True) # Фамилия контакта
    contact_ico: Optional[str] = db.Column(db.String(255), nullable=True) # Фото контакта
    contact_email: Optional[str] = db.Column(db.String(255), nullable=True) # Email контакта
    contact_data: Optional[str] = db.Column(db.String(255), nullable=True) # Дополнительные данные контакта
    attachments_name: Optional[str] = db.Column(db.String(255), nullable=True) # Имя файла вложения
    attachments_url: Optional[str] = db.Column(db.String(255), nullable=True) # Ссылка на вложение
    user_email: Optional[str] = db.Column(db.String(255), nullable=True) # Email сотрудника-автора исходящего сообщения
    telegram_user_name: Optional[str] = db.Column(db.String(255), nullable=True) # Псевдоним телеграм
    telegram_user_id: Optional[str] = db.Column(db.String(255), nullable=True) # ID юзера телеграм
    current_session = db.relationship('Session', uselist=False, backref="client") # Текущая сессия клиента (отношение один к одному), каждый клиент может иметь только одну текущую сессию
    token_planfix: Optional[str] = db.Column(db.String(255), nullable=True) # Токен ПланФикса
    url_planfix: Optional[str] = db.Column(db.String(255), nullable=True) # URL ПланФикса
    sessions = db.relationship('Session', back_populates='client') # Связь с сессиями клиента (отношение один ко многим), у клиента может быть несколько сессий
    # Конструктор класса
    def __init__(self, name, channel, created_at=None, updated_at=None, token=None, user_id=None, name_session=None, path_session=None, chat_id=None, message=None, title=None,
                 contact_id=None, contact_name=None, contact_last_name=None, contact_ico=None, contact_email=None, contact_data=None, attachments_name=None, attachments_url=None,
                 user_email=None, telegram_user_name=None, telegram_user_id=None, token_planfix=None, url_planfix=None, user=None, current_session=None, sessions=None):
    # Метод для сериализации объекта в формат JSON.
    @property
    def serialize(self):
    # Метод для получения текущего статуса клиента (онлайн/офлайн).
    @property
    def status(self): 
    ```
    * message.py
    ```bash
    # non_functional telegram_planfix_integration/app/models/message.py - реализован следующий фунционал
    # Используется для представления сообщений.
    class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # нежеуказанные поля пока не используем
    content = db.Column(db.String(255), nullable=True)
    sender_id = db.Column(db.Integer, nullable=True)
    recipient_id = db.Column(db.Integer, nullable=False)
    planfix_message_id = db.Column(db.String(50), nullable=True) 
    client = db.relationship('Client', backref='messages') # Связь с Client
    session = db.relationship('Session', back_populates='messages') # Связь с Session
    # Конструктор класса
    def __init__(self, client_id, text, timestamp=None, content=None, sender_id=None, recipient_id=None,
                 planfix_message_id=None, client=None, session=None):
    # Метод для представления объекта Message при его отображении в виде строки.
    def __repr__(self):
    ```
    * session.py
    ```bash
    # non_functional telegram_planfix_integration/app/models/session.py - реализован следующий фунционал
    # Отслеживает сессии клиента
    class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(100), nullable=False)
    client = db.relationship('Client', back_populates='sessions') # Связь с Client
    # Конструктор класса
    def __init__(self, name, path, client=None, session_id=None):
    # Метод для представления объекта Session при его отображении в виде строки.
    def __repr__(self):
    ```
    
    # Чтобы узнать используемые версии библиотек в вашем проекте, вы можете воспользоваться командой pip freeze. 
    Она покажет список всех установленных пакетов и их версии.
    Откройте командную строку или терминал в директории вашего проекта.
    Введите следующую команду:
        ```bash
        # pip freeze > requirements.txt
        ```
    #Эта команда сохранит текущие версии всех установленных библиотек в файл requirements.txt.
    
    # Для установки всех зависимостей, указанных в файле requirements.txt, вы можете использовать следующую команду в 
      вашем терминале или командной строке:
        ```bash
        pip install -r requirements.txt
    ```