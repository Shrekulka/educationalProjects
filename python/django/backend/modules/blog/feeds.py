# backend/modules/blog/feeds.py

"""
    Будет представлять RSS ленту на сайте.
"""

from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.urls import reverse

from modules.blog.models import Article


class LatestArticlesFeed(Feed):
    """
        Фид последних статей

        Определяет, какие данные будут включены в фид последних статей.

        Атрибуты класса:
        - title: Заголовок фида ("Ваш сайт - последние статьи")
        - link: Ссылка на фид ("/feeds/")
        - description: Описание фида ("Новые статьи на моем сайте.")

        Методы:
        - items(): Возвращает последние 5 статей, отсортированные по времени обновления.
        - item_title(item): Возвращает заголовок каждой статьи для фида.
        - item_description(item): Возвращает краткое описание каждой статьи для фида.
        - item_link(item): Возвращает URL-адрес каждой статьи для фида, используя функцию reverse.
    """
    # Заголовок фида
    title = "Ваш сайт - последние статьи"

    # Ссылка на фид
    link = "/feeds/"

    # Описание фида
    description = "Новые статьи на моем сайте."

    def items(self) -> QuerySet[Article]:
        """
            Возвращает последние 5 статей, отсортированные по времени обновления.

            Returns:
                QuerySet[Article]: QuerySet, содержащий последние 5 статей.
        """
        # Возвращает последние 5 статей, отсортированные по времени обновления
        return Article.objects.order_by('-time_update')[:5]

    def item_title(self, item: Article) -> str:
        """
            Возвращает заголовок каждой статьи для фида.

            Args:
                item (Article): Объект статьи.

            Returns:
                str: Заголовок статьи.
        """
        # Возвращает заголовок каждой статьи для фида
        return item.title

    def item_description(self, item: Article) -> str:
        """
            Возвращает краткое описание каждой статьи для фида.

            Args:
                item (Article): Объект статьи.

            Returns:
                str: Краткое описание статьи.
        """
        # Возвращает краткое описание каждой статьи для фида
        return item.short_description

    def item_link(self, item: Article) -> str:
        """
            Возвращает URL-адрес каждой статьи для фида, используя функцию reverse.

            Args:
                item (Article): Объект статьи.

            Returns:
                str: URL-адрес статьи.
        """
        # Возвращает URL-адрес каждой статьи для фида
        return reverse('articles_detail', args=[item.slug])


