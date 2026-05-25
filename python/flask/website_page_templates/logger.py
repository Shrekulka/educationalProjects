# website_page_templates/logger.py

# Настройка уровня логирования и форматирование
import logging

level = logging.DEBUG
format_str = '%(asctime)s |%(lineno)04d-%(levelname)-5s| - | %(message)s |'

# Настройка логирования в файл
logging.basicConfig(filename='val.log', format=format_str, filemode='a', level=level)

# Настройка логирования в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(level)
formatter = logging.Formatter(format_str)
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# Инициализация логгера
logger: logging.Logger = logging.getLogger()
logger.info('Привет')
