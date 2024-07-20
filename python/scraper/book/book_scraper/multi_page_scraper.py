# book_scraper/multi_page_scraper.py

import traceback
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup as bs

from logger_config import logger

# Определение констант
BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = f"{BASE_URL}page-1.html"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


def get_page_content(url: str) -> str:
    """
    Получает HTML-контент страницы по указанному URL.

    Args:
        url (str): URL страницы для скрапинга.

    Returns:
        str: HTML-контент страницы.

    Raises:
        requests.RequestException: Если возникла ошибка при запросе страницы.
    """
    # Установка заголовка User-Agent для имитации браузера
    headers = {"User-Agent": USER_AGENT}

    # Отправка GET-запроса к указанному URL
    response = requests.get(url, headers=headers)

    # Проверка на наличие ошибок при запросе
    response.raise_for_status()

    # Возврат содержимого страницы
    return response.content


def parse_books(content: str) -> List[Dict[str, str]]:
    """
    Извлекает данные о книгах из HTML-контента страницы.

    Args:
        content (str): HTML-контент страницы.

    Returns:
        List[Dict[str, str]]: Список словарей с данными о книгах.
    """
    # Создание объекта BeautifulSoup для парсинга HTML
    soup = bs(content, "html.parser")

    # Поиск всех элементов книг на странице
    # Используем метод select() для поиска элементов по CSS-селектору
    # "ol.row li" означает:
    #   - ищем элемент <ol> с классом "row"
    #   - внутри него ищем все элементы <li>
    # Каждый <li> представляет отдельную книгу на странице
    book_items = soup.select("ol.row li")

    # Список книг
    book_data_list = []

    # Обработка каждой книги
    for book_item in book_items:
        # Извлечение URL изображения книги
        image_url = BASE_URL + book_item.select_one('div.image_container img')['src']
        # Извлечение заголовка книги
        title = book_item.select_one('h3 a')['title']
        # Извлечение цены книги
        price = book_item.select_one('p.price_color').text

        # Добавление данных о книге в список
        book_data_list.append({
            'image_url': image_url,
            'title': title,
            'price': price,
        })

    return book_data_list


def get_next_page_url(content: str) -> Optional[str]:
    """
    Находит URL следующей страницы в HTML-контенте текущей страницы.

    Args:
        content (str): HTML-контент текущей страницы.

    Returns:
        Optional[str]: URL следующей страницы или None, если следующей страницы нет.
    """
    # Создание объекта BeautifulSoup для парсинга HTML
    soup = bs(content, "html.parser")

    # Поиск элемента, содержащего ссылку на следующую страницу
    # Используем метод select_one() для поиска первого элемента, соответствующего CSS-селектору
    # "li.next a" означает:
    #   - ищем элемент <li> с классом "next"
    #   - внутри него ищем элемент <a> (ссылку)
    # Этот селектор предполагает, что на странице есть элемент списка с классом "next",
    # содержащий ссылку на следующую страницу
    # Если такой элемент найден, next_page_element будет содержать этот элемент
    # Если не найден, next_page_element будет None
    next_page_element = soup.select_one("li.next a")

    if next_page_element:
        # Если элемент найден, возвращаем полный URL следующей страницы
        return BASE_URL + next_page_element['href']
        # Если элемент не найден, возвращаем None
    return None


def main() -> None:
    """
    Основная функция для выполнения многостраничного веб-скрапинга книжного магазина.
    """
    try:
        logger.info("Начало процесса многостраничного веб-скрапинга")

        # Инициализация списка для хранения данных всех книг
        all_books_data: List[Dict[str, str]] = []
        # Установка начального URL
        current_url = START_URL
        # Счетчик страниц
        page_number = 1

        # Цикл обработки страниц
        while current_url:
            logger.info(f"Обработка страницы {page_number}: {current_url}")

            # Получение HTML-контента текущей страницы
            page_content = get_page_content(current_url)

            # Извлечение данных о книгах с текущей страницы
            books_on_page = parse_books(page_content)
            # Добавление данных о книгах в общий список
            all_books_data.extend(books_on_page)

            logger.info(f"Получено {len(books_on_page)} книг с страницы {page_number}")

            # Получение URL следующей страницы
            current_url = get_next_page_url(page_content)
            # Увеличение счетчика страниц
            page_number += 1

        logger.info(f"Всего собрано данных о {len(all_books_data)} книгах с {page_number - 1} страниц")

    except requests.RequestException as e:
        # Обработка ошибок, связанных с запросами к серверу
        logger.error(f"Ошибка при запросе страницы: {str(e)}")
    except Exception as e:
        # Обработка непредвиденных ошибок
        detailed_error = traceback.format_exc()
        logger.error(f"Неожиданная ошибка: {str(e)}\n{detailed_error}")
    finally:
        # Завершающее сообщение, которое выполнится в любом случае
        logger.info("Процесс многостраничного веб-скрапинга завершен")


if __name__ == "__main__":
    try:
        # Запуск основной функции
        main()
    except KeyboardInterrupt:
        # Обработка прерывания пользователем (Ctrl+C)
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        # Обработка непредвиденных ошибок при запуске приложения
        detailed_error = traceback.format_exc()
        logger.error(f"Неожиданная ошибка приложения: {error}\n{detailed_error}")
