# /pythonProject_1/config.py

telegram_api_id = 'your_telegram_api_id'
telegram_api_hash = 'your_telegram_api_hash'
telegram_bot_token = 'your_telegram_bot_token'

planfix_api_url = 'https://api.planfix.com/xml/'
planfix_api_key = 'your_planfix_api_key'

if not telegram_api_id or not telegram_api_hash or not telegram_bot_token or not planfix_api_url or not planfix_api_key:
    print("Ошибка: Пожалуйста, укажите все необходимые переменные окружения "
          "(TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN, PLANFIX_API_URL, PLANFIX_API_KEY).")
