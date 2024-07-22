# scraper_spider/books/books/spiders/books_crawl.py

from urllib.parse import urljoin

import scrapy


# Определяем класс паука, наследуясь от scrapy.Spider
class BooksCrawlSpider(scrapy.Spider):
    # Задаем имя паука, которое будет использоваться при запуске
    name = "books_crawl"

    # Указываем домены, с которых разрешено собирать данные
    allowed_domains = ["books.toscrape.com"]

    # Определяем начальные URL, с которых паук начнет работу
    start_urls = ["https://books.toscrape.com"]

    # Метод parse вызывается для каждого ответа, полученного с start_urls
    def parse(self, response):
        # Находим все элементы книг на странице с помощью XPath
        books = response.xpath("//ol[@class='row']/li")

        # Перебираем каждую найденную книгу
        for book in books:
            # Извлекаем относительный URL изображения книги
            image_relative_url = book.xpath(".//div[@class='image_container']/a/img/@src").get()

            # Преобразуем относительный URL в абсолютный
            image_absolute_url = urljoin(response.url, image_relative_url)

            # Создаем словарь с данными о книге и передаем его далее
            yield {
                "image": image_absolute_url,  # Абсолютный URL изображения
                "title": book.xpath(".//h3/a/@title").get(),  # Название книги
                "price": book.xpath(".//p[@class='price_color']/text()").get(),  # Цена книги
            }
