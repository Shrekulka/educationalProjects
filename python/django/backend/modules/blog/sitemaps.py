# backend/modules/blog/sitemaps.py

"""
    Карта-сайта (sitemap.xml) - это файл, который содержит список всех страниц на сайте и помогает поисковым роботам
    быстрее и более эффективно индексировать сайт.
"""

import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet
from django.urls import reverse

from .models import Article


class ArticleSitemap(Sitemap):
    """
        Карта сайта для статей блога.

        Этот класс наследуется от django.contrib.sitemaps.Sitemap и предоставляет
        информацию для генерации sitemap.xml для статей блога.

        Атрибуты:
            changefreq (str): Частота изменения страниц статей.
                              Установлено на 'monthly', что означает ежемесячное обновление.
            priority (float): Приоритет страниц статей относительно других страниц сайта.
                              Установлено на 0.9, что означает высокий приоритет.
            protocol (str): Протокол, используемый для URL статей.
                            Установлено на 'https' для безопасного соединения.

        Методы:
            items(): Возвращает QuerySet всех статей для включения в sitemap.
            lastmod(obj): Возвращает дату последнего изменения для каждой статьи.
    """
    changefreq = 'monthly'  # Частота обновления страницы
    priority = 0.9  # Приоритет страницы
    protocol = 'https'  # Протокол URL

    def items(self) -> QuerySet[Article]:
        """
            Получает все статьи для включения в sitemap.

            Returns:
                QuerySet[Article]: QuerySet, содержащий все объекты модели Article.
        """
        # Возвращает QuerySet всех статей
        return Article.objects.all()

    def lastmod(self, obj: Article) -> datetime:
        """
            Определяет дату последнего изменения для каждой статьи.

            Args:
                obj (Article): Объект статьи.

            Returns:
                datetime: Дата и время последнего обновления статьи.
        """
        # Возвращает время последнего обновления статьи
        return obj.time_update


class StaticSitemap(Sitemap):
    """
        Карта сайта для статических страниц.

        Этот класс предоставляет информацию для генерации sitemap.xml
        для статических страниц сайта, таких как главная страница и страница обратной связи.

        Методы:
            items(): Возвращает список имен статических страниц для включения в sitemap.
            location(item): Генерирует URL для каждой статической страницы.
    """

    def items(self) -> list:
        """
            Определяет статические страницы для включения в sitemap.

            Returns:
                list: Список строковых имен представлений для статических страниц.
            """
        # Возвращает список имен статических страниц
        return ['feedback', 'home']

    def location(self, item: str) -> str:
        """
            Генерирует URL для каждой статической страницы.

            Args:
                item (str): Имя представления для статической страницы.

            Returns:
                str: Полный URL-путь для данной статической страницы.
        """
        # Возвращает URL-адрес для каждой статической страницы, определенный по имени
        return reverse(item)
