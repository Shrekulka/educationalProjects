1. Схема проекта 
```bash
/telegram_planfix_integration_work_in_progress/main.py/   # Основная папка проекта.
│
├── main.py                                     # Основная папка приложения Flask.
│
├── telegram_integration_planfix.py             # Модуль для интеграции Telegram с Planfix и Planfix с Telegram.
│
├── config.py                                   # Файл с настройками для проекта.
│
├── flask_logging.py                            # Модуль для обработки логирования в приложении Flask.
│
├── .env                                        # Файл конфигурации для переменных окружения.
│
├── README.md                                   # Документация проекта.
│
└── venv/          # Виртуальное окружение Python, которое рекомендуется использовать для изоляции зависимостей проекта.
```
2. /telegram_planfix_integration_work_in_progress/main.py
    ```bash
    # Инициализация Flask приложения
    app = Flask(__name__)
    
    # Инициализация ThreadPoolExecutor для выполнения задач в отдельных потоках
    executor = ThreadPoolExecutor()
    
    # Декоратор lru_cache для функции get_clients, который кэширует результаты вызовов
    @lru_cache(maxsize=None)  # None означает неограниченный размер кэша
    def get_clients() -> Dict:
    
    # Получение интернируемого объекта словаря клиентов
    clients = get_clients()
    
    # Настройка Telethon с использованием TelegramClient
    client = TelegramClient('bot_session', telegram_api_id, telegram_api_hash)
    
    # Определение перечисления (Enum) ClientStatus, представляющего статусы клиента
    class ClientStatus(Enum):
        ONLINE = 'Online'
        OFFLINE = 'Offline'
    
    # Определение перечисления (Enum) MessageType, представляющего типы сообщений
    class MessageType(Enum):
        TELEGRAM = 'Telegram'
        PLANFIX = 'Planfix'
    
    # Обработчик ошибок для исключений типа Exception
    @app.errorhandler(Exception)
    def handle_error(error: Exception) -> Tuple[Response, int]:
       
    # Асинхронная функция для запуска процесса polling с использованием Telethon
    async def run_polling() -> None:
    
    # Асинхронная функция для верификации ключа сессии клиента
    async def verify_session_key(client_data: Dict[str, Union[str, Dict]]) -> bool:
    
    # Асинхронная функция для валидации наличия обязательных ключей в данных
    async def validate_data(data: Dict[str, Union[str, Dict]], required_keys: List[str]):
      
    # Асинхронная функция для валидации наличия обязательных ключей в данных сообщения
    async def validate_message_data(message_data: Dict[str, Union[str, Dict]], required_keys: List[str]):
       
    # Асинхронная функция для генерации ключа сессии клиента
    async def generate_client_session_key(length: int = 32) -> str:
     
    # Асинхронная функция для генерации уникального идентификатора клиента
    async def generate_client_id() -> str:
       
    # Асинхронная функция для создания нового клиента
    async def create_client() -> Dict[str, Union[str, Dict]]:
       
    # Асинхронная функция для получения данных клиента
    async def get_client_data() -> Dict[str, Union[str, Dict]]:
       
    # Обработчик событий нового сообщения (исходящего и входящего)
    @client.on(events.NewMessage(outgoing=True, incoming=True))
    async def handle_text_message(event: events.NewMessage.Event) -> None:
      
    # Обработчик маршрута /webhook с поддержкой различных HTTP-методов
    @app.route('/webhook', methods=['POST', 'GET', 'DELETE', 'PUT'])
    def handle_webhook() -> Tuple[Response, int]:
       
    # Асинхронная функция для обработки входящих запросов
    async def handle_request(data: Dict[str, Union[str, Dict]], send_function) -> Union[
      
    # Асинхронная функция для обработки PUT-запросов
    async def handle_put(data: Dict[str, Union[str, Dict]]) -> Union[
       
    # Асинхронная функция для обработки POST-запросов
    async def handle_post(data: Dict[str, Union[str, Dict]]) -> Union[
      
    # Асинхронная функция для обработки GET-запросов
    async def handle_get() -> Union[Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]:
       
    # Асинхронная функция для обработки DELETE-запросов
    async def handle_delete() -> Union[Dict[str, Union[str, Dict]], Tuple[Dict[str, str], int]]:
      
    # Блок выполнения кода при запуске программы
    if __name__ == '__main__':
        try:
            asyncio.get_event_loop().run_until_complete(run_polling())
            app.run(port=5000)
        except KeyboardInterrupt:
            logger.info("Program interrupted by user")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
    ```
3. /telegram_planfix_integration_work_in_progress/telegram_integration_planfix.py
    ```bash
    # Асинхронный кэш для хранения данных о сообщениях
    messages: SimpleMemoryCache = SimpleMemoryCache()
    
    # Асинхронная функция для отправки сообщения из Telegram в Planfix и обработки ответа
    async def send_telegram_message_to_planfix(update, client_data, telegram_message_id) -> None:
    
    # Асинхронная функция для отправки ответа из Planfix в Telegram
    async def send_response_to_telegram(planfix_message_id, telegram_chat_id) -> None:
    
    # Асинхронная функция для получения идентификатора сообщения в Telegram из соответствия
    async def get_telegram_id_from_mapping(planfix_message_id) -> Optional[int]:
    
    # Асинхронная функция для получения идентификатора чата в Telegram из соответствия
    async def get_chat_id_by_message(telegram_message_id) -> Optional[int]:
    
    # Асинхронная функция для отправки сообщения в Planfix
    async def send_message_to_planfix(client_data, message) -> int:
      
    # Асинхронная функция для получения ответа от Planfix по идентификатору сообщения
    async def get_planfix_response(message_id) -> str:
    
    # Асинхронная функция для обработки ошибки
    async def handle_error(error) -> None:
    ```
4. /telegram_planfix_integration_work_in_progress/flask_logging.py
    ```bash
    leve1 = logging.DEBUG
    format1 = '%(asctime)s |%(filename)s |%(lineno)04d-%(levelname)-5s| - | %(message)s |'
    logging.basicConfig(filename='val.log', format=format1, filemode='a', level=leve1)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(leve1)
    formatter = logging.Formatter(format1)
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)
    logger = logging.getLogger()
    logger.info('hello')
    ```
5. /telegram_planfix_integration_work_in_progress/config.py
    ```bash
    # Загрузка переменных среды из файла .env
    load_dotenv()
    
    telegram_api_id = os.getenv('TELEGRAM_API_ID')
    telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    planfix_api_url = os.getenv('PLANFIX_API_URL')
    planfix_api_key = os.getenv('PLANFIX_API_KEY')
    
    if not telegram_api_id or not telegram_api_hash or not telegram_bot_token or not planfix_api_url or not planfix_api_key:
        print("Ошибка: Пожалуйста, укажите все необходимые переменные окружения "
              "(TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN, PLANFIX_API_URL, PLANFIX_API_KEY).")
    ```	  
6. /telegram_planfix_integration_work_in_progress/.env
    ```bash
    TELEGRAM_API_ID=your_TELEGRAM_API_ID
    TELEGRAM_API_HASH=your_TELEGRAM_API_HASH
    TELEGRAM_BOT_TOKEN=your_TELEGRAM_BOT_TOKEN
    PLANFIX_API_URL=https://api.planfix.com/xml/
    PLANFIX_API_KEY=your_PLANFIX_API_KEY
    ```

