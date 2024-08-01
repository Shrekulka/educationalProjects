# lego_scraper/src/thread_scraper/processors.py

from typing import List, Dict, Optional

from config.settings import config
from src.thread_scraper.extractors import extract_toy_count_and_pages, extract_toys_from_page
from src.thread_scraper.scraper import get_soup
from utils.logger_config import logger


def process_theme(theme: Dict[str, str]) -> List[Dict[str, Optional[str]]]:
    """
    Обрабатывает данные о игрушках для заданной темы, извлекая информацию о всех игрушках с нескольких страниц.

    Функция выполняет следующие шаги:
    1. Загружает HTML-код страницы темы и извлекает количество игрушек и страниц.
    2. Логирует информацию о найденных игрушках и страницах.
    3. Проходит по каждой странице с игрушками, извлекает данные и добавляет их в общий список.

    Args:
        theme (Dict[str, str]): Словарь, содержащий данные о теме, включая 'title' и 'url'.

    Returns:
        List[Dict[str, Optional[str]]]: Список словарей, каждый из которых содержит информацию об игрушке.
    """
    # Получаем HTML-код страницы темы и создаем объект BeautifulSoup
    theme_page_soup = get_soup(theme['url'])

    # Извлекаем количество игрушек и количество страниц с игрушками для текущей темы
    number_of_toys, number_of_pages = extract_toy_count_and_pages(theme_page_soup)
    logger.info(f"\nНайдено {number_of_toys} игрушек на {number_of_pages} страницах")

    # Инициализация списка для хранения данных обо всех игрушках
    all_toy_data = []

    # Проходим по каждой странице с игрушками
    for page_number in range(config.DEFAULT_PAGE, number_of_pages + 1):
        # Логируем текущую страницу и тему
        logger.info(f"\nОбработка №{page_number} страницы из {number_of_pages} для темы {theme['title']}\n")

        # Получаем HTML-код текущей страницы с игрушками и создаем объект BeautifulSoup
        toy_page_soup = get_soup(theme['url'], page_number)

        # Извлекаем данные об игрушках с текущей страницы
        toys_data_on_page = extract_toys_from_page(toy_page_soup, theme['title'])

        # Добавляем данные с текущей страницы к общему списку
        all_toy_data.extend(toys_data_on_page)

    # Возвращаем собранные данные обо всех игрушках
    return all_toy_data
