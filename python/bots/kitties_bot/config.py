# kitties_bot/config.py

# URL для обращения к Telegram Bot API
API_URL = 'https://api.telegram.org/bot'

# Токен нашего бота
BOT_TOKEN = 'your_telegram_bot_token'

# URL для получения случайного изображения с котом
CATS_API_URL = 'https://api.thecatapi.com/v1/images/search'

# URL для получения случайного изображения с собакой
DOGS_API_URL = 'https://random.dog/woof.json'

# URL для получения случайного изображения с лисой
FOXES_API_URL = 'https://randomfox.ca/floof/'

# Список API для получения изображений разных животных
ANIMALS = [CATS_API_URL, DOGS_API_URL, FOXES_API_URL]

# Текст ошибки, который отправится пользователю в случае неудачи при получении изображения
ERROR_TEXT = f'There should have been a picture of an {ANIMALS} here :('

# Максимальное количество попыток выполнения запросов
MAX_ATTEMPTS = 10

# Задержка между запросами в секундах
DELAY_BETWEEN_REQUESTS = 1
