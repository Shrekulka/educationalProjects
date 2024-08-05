# find_all_links_on_web_pages/solution_using_functions.py

from typing import Tuple
from urllib.parse import urlparse, urljoin, unquote

import requests
from bs4 import BeautifulSoup

url = 'https://ru.wikipedia.org/wiki/Python'


def get_html_content(url: str) -> bytes:
    """
    Получает содержимое веб-страницы по указанному URL.

    Аргументы:
    url (str): URL веб-страницы.

    Возвращает:
    bytes: Содержимое HTML-кода страницы в виде байтов.

    Исключения:
    Exception: Если возникла ошибка при получении веб-страницы, выбрасывается исключение с сообщением об ошибке.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception("Ошибка при получении веб-страницы. Код статуса:", response.status_code)


def extract_links(soup: BeautifulSoup) -> Tuple[set, set]:
    """
    Извлекает внутренние и внешние ссылки со страницы.

    Аргументы:
    soup (BeautifulSoup): Объект BeautifulSoup, содержащий HTML-код страницы.

    Возвращает:
    Tuple[set, set]: Кортеж с двумя множествами - внутренних и внешних ссылок.
    """
    internal_links = set()
    external_links = set()

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            if href.startswith('#'):
                continue

            parsed_url = urlparse(href)
            if parsed_url.netloc:
                external_links.add(href)
            else:
                internal_links.add(urljoin(url, href))

    return internal_links, external_links


def print_links(links: set, link_type: str) -> None:
    """
    Выводит список ссылок в читаемом формате.

    Аргументы:
    links (set): Множество ссылок.
    link_type (str): Тип ссылок, например, "Внутренние" или "Внешние".
    """
    print(f"{link_type} ссылки:")
    for idx, link in enumerate(links, start=1):
        print(f"{idx}. {unquote(link)}")


def main() -> None:
    """
    Основная функция для выполнения анализа веб-страницы и вывода ссылок.
    """
    url = 'https://ru.wikipedia.org/wiki/Python'
    html_content = get_html_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')

    internal_links, external_links = extract_links(soup)

    print_links(internal_links, "Внутренние")
    print("\n")
    print_links(external_links, "Внешние")


if __name__ == "__main__":
    main()
