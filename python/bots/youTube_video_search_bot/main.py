"""Бот для поиска видео на YouTube.

Этот бот позволяет пользователям искать видео на YouTube на основе указанных критериев,
таких как запрос поиска, категория, регион и дата публикации. Затем результаты поиска
периодически отправляются в указанный чат в Telegram в виде ссылок на видео.

Необходимые библиотеки Python: asyncio, aiohttp, aiogram, dateutil, google-api-python-client, python-dotenv.

Использование:
1. Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные окружения:
    - API_KEY: Ваш ключ от YouTube Data API v3.
    - TELEGRAM_BOT_TOKEN: Токен вашего Telegram бота.
    - TELEGRAM_CHAT_ID: Идентификатор чата, куда бот будет отправлять ссылки на видео.

2. Запустите скрипт `main.py`, чтобы запустить бота.

Автор: [Роман Штефанеса]
"""

import asyncio
import logging
import os
from dotenv import load_dotenv
from modules.menu import Menu

# Установите соответствующий уровень журналирования
logging.basicConfig(level=logging.INFO)


async def main():
    """Основная функция для запуска бота поиска видео на YouTube."""
    # Загрузка переменных среды из файла .env
    load_dotenv()

    # Получение ключа API, токена Telegram бота и идентификатора чата из переменных окружения
    api_key = os.getenv('API_KEY')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # Проверка наличия всех необходимых переменных окружения
    if not api_key or not bot_token or not chat_id:
        print("Ошибка: Пожалуйста, укажите все необходимые переменные окружения "
              "(API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID).")
        return

    # Инициализация экземпляра Menu с предоставленным ключом API, токеном бота и идентификатором чата
    menu = Menu(api_key, bot_token, int(chat_id))

    try:
        # Показать меню, чтобы пользователь мог указать критерии поиска
        await menu.show_menu()
    except KeyboardInterrupt:
        # Обработка прерывания по сигналу SIGINT (например, Ctrl+C)
        print()
        logger = logging.getLogger(__name__)
        logger.info("\nThe bot was stopped by the user.")
        loop = asyncio.get_event_loop()
        loop.stop()


if __name__ == "__main__":
    # Создание цикла событий и запуск основной корутины
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
