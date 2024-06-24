# web_crawler_ads_generator/main.py

import asyncio
import os
import traceback

from dotenv import load_dotenv
from openai import AsyncOpenAI

from ad_generator import generate_ads
from config import DEFAULT_MAX_PAGES, DEFAULT_DEPTH, DEFAULT_AD_LENGTH
from crawler import crawl_site_async
from csv_writer import write_csv
from logger_config import logger
from summary_generator import generate_summary
from utils import parse_arguments


async def main() -> None:
    """
        Основная функция для запуска приложения веб-краулера и генератора рекламных объявлений.

        Загружает переменные среды из файла .env, парсит аргументы командной строки,
        выполняет краулинг сайта, генерирует объявления и краткие сводки, записывает объявления в CSV файл.

        Raises:
            ValueError: Если возникает проблема с валидацией URL.
            Exception: Для неожиданных ошибок во время выполнения.

        Returns:
            None
    """
    try:
        logger.debug("########## main function works! ##########")
        # Вызываем функцию load_dotenv(), чтобы загрузить переменные окружения из файла .env
        load_dotenv()

        # Парсинг аргументов командной строки с помощью функции parse_arguments()
        args = parse_arguments()

        # Извлечение URL сайта из аргументов командной строки
        site_url = args.url

        # Извлечение ключевых слов из аргументов командной строки (если они заданы)
        keywords = args.keywords

        # Логирование извлеченных значений аргументов командной строки и значений по умолчанию
        logger.debug(f"URL сайта: {site_url}")
        logger.debug(f"Максимальное количество страниц: {DEFAULT_MAX_PAGES}")
        logger.debug(f"Максимальная глубина краулинга: {DEFAULT_DEPTH}")
        logger.debug(f"Максимальная длина объявления: {DEFAULT_AD_LENGTH}")
        logger.debug(f"Ключевые слова: {keywords}")

        # Асинхронный краулинг сайта с использованием заданных параметров
        pages = await crawl_site_async(site_url, max_pages=DEFAULT_MAX_PAGES, depth=DEFAULT_DEPTH)
        logger.debug(f"Количество собранных страниц: {len(pages)}")

        # Преобразование генератора страниц в список
        pages = list(pages)

        # Генерация краткой сводки на основе собранных страниц
        summary = await generate_summary(pages)
        logger.debug(f"Сгенерированная краткая сводка: {summary}")

        # Инициализация клиента OpenAI для генерации объявлений
        client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        # Генерация объявлений на основе собранных страниц и ключевых слов
        ads = await generate_ads(pages, client, ad_length=DEFAULT_AD_LENGTH, keywords=keywords)
        logger.debug(f"Количество сгенерированных объявлений: {len(ads)}")

        # Запись сгенерированных объявлений в файл CSV
        write_csv(ads, 'ads.csv')
        logger.debug("Запись в файл 'ads.csv' выполнена успешно")

        logger.debug("########## Завершение работы функции main ##########")

    except ValueError as e:
        logger.error(f"Ошибка валидации URL: {e}")
    except Exception as error:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Произошла неожиданная ошибка в приложении: {error}\n{detailed_error_message}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Приложение завершено пользователем")
    except Exception as error:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Неожиданная ошибка в приложении: {error}\n{detailed_error_message}")
