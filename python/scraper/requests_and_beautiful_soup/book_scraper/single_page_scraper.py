# book_scraper/single_page_scraper.py

import traceback

import requests
from bs4 import BeautifulSoup as bs

from logger_config import logger

# Константа для URL страницы
BOOKS_URL = "https://books.toscrape.com/"


def main() -> None:
    try:
        logger.info("Начало процесса веб-скрапинга")

        # 1) Получаем HTML-код страницы
        response = requests.get(BOOKS_URL)

        # 2) Получаем статус-код ответа от сервера и логируем его
        status_code = response.status_code
        logger.info(f"Status code of {BOOKS_URL} is {status_code}")

        # 3) Получаем HTML-контент страницы и логируем его
        page_html = response.content
        logger.info(f"HTML page content of {BOOKS_URL} is:\n{page_html}")

        # 4) Создаем суп, чтобы BeautifulSoup мог работать с HTML-страницей
        soup = bs(page_html, "html.parser")
        logger.info(f"Parsed HTML soup is:\n{soup}")

        # 5) Ищем всю информацию, которая находится в теге <section> - получаем список
        section_tags = soup.select('section')
        logger.info(f"Found sections are:\n{section_tags}")

        # 6) Получаем количество найденных секций и логируем его
        number_of_sections = len(section_tags)
        logger.info(f"Number of sections found: {number_of_sections}")

        # 7) Получаем первый <section> элемент из списка секций и логируем его содержимое
        first_section_tag = section_tags[0]
        logger.info(f"First section is:\n{first_section_tag}")

        # 8) Ищем элемент <ol> с классом 'row' внутри первого <section> и логируем его содержимое
        book_list_tag = first_section_tag.select_one('ol[class=row]')
        logger.info(f"Books list block is:\n{book_list_tag}")

        # 9) Ищем все элементы <li> внутри <ol> блока с книгами
        book_items = book_list_tag.select('li')
        logger.info(f"Found books are:\n{book_items}")

        # 10) Логируем количество найденных книг
        number_of_books = len(book_items)
        logger.info(f"Number of books found: {number_of_books}")

        # 11) Список для хранения данных о книгах
        book_data_list = []
        book_count = 0

        # Обрабатываем каждую книгу в списке
        for book_item in book_items:
            book_count += 1

            # Получаем URL изображения книги
            image_url = BOOKS_URL + book_item.find('div', attrs={'class': 'image_container'}).find('img')['src']

            # Получаем заголовок книги
            title = book_item.find('h3').find('a')['title']

            # Получаем цену книги
            price = book_item.find('div', attrs={'class': 'product_price'}).find('p',
                                                                                 attrs={'class': 'price_color'}).text

            # Логируем детали книги
            logger.info(f"Book {book_count} details:\nImage: {image_url}\nTitle: '{title}'\nPrice: {price}")

            # 12) Создаем словарь с данными о книге и добавляем его в список
            book_dict = {
                'image_url': image_url,
                'title': title,
                'price': price,
            }
            book_data_list.append(book_dict)

        # Логируем общее количество собранных книг
        logger.info(f"Total books collected: {len(book_data_list)}")

        # Логируем данные о собранных книгах
        logger.info(f"Collected books data:\n{book_data_list}")

    except Exception as e:
        detailed_error = traceback.format_exc()
        logger.error(f"Error occurred: {str(e)}\n{detailed_error}")
    finally:
        logger.info("Процесс веб-скрапинга завершен")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем")
    except Exception as error:
        detailed_error = traceback.format_exc()
        logger.error(f"Unexpected application error: {error}\n{detailed_error}")
