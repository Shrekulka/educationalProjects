# non_functional telegram_planfix_integration/config.py

import logging
import os

from dotenv import load_dotenv

print("создание абсолютных путей к файлам и директориям внутри проекта.")
basedir = os.path.abspath(os.path.dirname(__file__))

# Загрузка переменных среды из файла .env
load_dotenv()

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


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    telegram_api_id = os.getenv('TELEGRAM_API_ID')
    telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    planfix_api_url = os.getenv('PLANFIX_API_URL')
    planfix_api_key = os.getenv('PLANFIX_API_KEY')

    if not telegram_api_id or not telegram_api_hash or not telegram_bot_token or not planfix_api_url or not planfix_api_key:
        print("Ошибка: Пожалуйста, укажите все необходимые переменные окружения "
              "(TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN, PLANFIX_API_URL, PLANFIX_API_KEY).")
