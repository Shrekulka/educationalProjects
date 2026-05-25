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

    telegram_api_id = '22870332'
    telegram_api_hash = 'fafcdb82d4f83d15be0fbd6457f6cd8e'
    planfix_api_url = 'https://api.planfix.com/xml/'
    planfix_api_key = '0c8271c614a138a01b31c9309208a732'

    if not telegram_api_id or not telegram_api_hash  or not planfix_api_url or not planfix_api_key:
        print("Ошибка: Пожалуйста, укажите все необходимые переменные окружения "
              "(TELEGRAM_API_ID, TELEGRAM_API_HASH, PLANFIX_API_URL, PLANFIX_API_KEY).")




