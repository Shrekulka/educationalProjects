# lego_scraper/src/sync_scraper/scraper.py

import requests
from bs4 import BeautifulSoup as bs

from config.settings import config


def get_page_content(page_url: str) -> bytes:
    """
    Получает содержимое страницы по указанному URL.

    Args:
        page_url (str): URL страницы.

    Returns:
        bytes: Содержимое страницы в виде байтов.
    """
    # Установка заголовка User-Agent для имитации браузера
    headers = {"User-Agent": config.CUSTOM_USER_AGENT}

    # Отправка GET-запроса к указанному URL
    response = requests.get(page_url, headers=headers)

    # Проверка на наличие ошибок при запросе
    response.raise_for_status()

    # Возврат содержимого страницы
    return response.content


def get_soup(base_url: str, page_number: int = config.DEFAULT_PAGE) -> bs:
    """
    Получает объект BeautifulSoup для страницы по указанному URL и номеру страницы.

    Args:
        base_url (str): Базовый URL страницы.
        page_number (int): Номер страницы для получения. По умолчанию 1.

    Returns:
        bs: Объект BeautifulSoup для HTML-кода страницы.
    """
    # Формируем URL в зависимости от номера страницы
    if page_number == config.DEFAULT_PAGE:
        # Если страница по умолчанию, используем базовый URL
        html_content = get_page_content(base_url)
    else:
        # Если это не первая страница, добавляем параметры пагинации к URL
        url_with_page = f"{base_url}?page={page_number}&offset={config.DEFAULT_OFFSET}"
        html_content = get_page_content(url_with_page)

    # Создаем объект BeautifulSoup для парсинга HTML-кода страницы
    soup = bs(html_content, "lxml")

    # Возвращаем объект BeautifulSoup, готовый для дальнейшего парсинга
    return soup
