# integration_telegram_planfix_in_progress/config.py

# Настройки Telegram
from colorama import Fore, Style

# Ключи API для доступа к Telegram API
telegram_api_id = 'your_telegram_api_id'
telegram_api_hash = 'your_telegram_api_hash'

# Настройки Planfix
planfix_api_url = 'your_planfix_api_url'
planfix_api_key = 'your_planfix_api_key'

# Имя сессии и идентификатор интеграции с Telegram в Planfix
name_session = 'my_session'
telegram_integration_id = 'test_telegram'

# Цвета для использования в логировании
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
GREEN = Fore.GREEN
MAGENTA = Fore.MAGENTA
RESET_ALL = Style.RESET_ALL
