# /telegram_planfix_integration_work_in_progress/config.py

import os

from dotenv import load_dotenv

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
