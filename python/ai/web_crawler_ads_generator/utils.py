# web_crawler_ads_generator/utils.py

import argparse
from urllib.parse import urlparse

from config import DEFAULT_MAX_PAGES, DEFAULT_DEPTH, DEFAULT_AD_LENGTH


def validate_url(url: str) -> bool:
    """
        Проверяет, является ли переданный URL допустимым.

        Args:
            url (str): URL для проверки.

        Returns:
            bool: True, если URL допустим, иначе False.
    """
    try:
        # Пытаемся разобрать URL с помощью функции urlparse
        result = urlparse(url)
        # Проверяем, что в результате есть схема и сетевое местоположение
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def parse_arguments() -> argparse.Namespace:
    """
        Разбирает аргументы командной строки для веб-краулера и генератора объявлений.

        Returns:
            argparse.Namespace: Объект с атрибутами, соответствующими разобранным аргументам.
                                 Содержит атрибуты: url, max_pages, depth, ad_length, keywords.
    """
    # Создаем парсер аргументов командной строки с описанием
    parser = argparse.ArgumentParser(description="Web crawler and ad generator")

    # Добавляем обязательный аргумент для URL сайта
    parser.add_argument("url", type=str, help="URL of the website to crawl")

    # Опция для задания максимального количества страниц для краулинга
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES, help="Maximum number of pages to crawl")

    # Опция для задания максимальной глубины краулинга
    parser.add_argument("--depth", type=int, default=DEFAULT_DEPTH, help="Maximum depth for crawling")

    # Опция для задания максимальной длины генерируемых объявлений
    parser.add_argument("--ad-length", type=int, default=DEFAULT_AD_LENGTH, help="Maximum length of generated ads")

    # Опция для задания ключевых слов для генерации объявлений
    parser.add_argument("--keywords", type=str, nargs='+', help="Keywords for ad generation")

    # Парсим аргументы командной строки
    args = parser.parse_args()

    # Проверяем валидность переданного URL с помощью функции validate_url
    if not validate_url(args.url):
        raise ValueError("Invalid URL provided")

    # Возвращаем объект с аргументами командной строки
    return args
