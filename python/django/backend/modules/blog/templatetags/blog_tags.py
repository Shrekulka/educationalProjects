# backend/modules/blog/templatetags/blog_tags.py

from typing import List, Dict

from django import template
from django.db.models import Count
from taggit.models import Tag

from modules.blog.models import Comment

# Используется для регистрации пользовательских тегов и фильтров в Django. Это общий шаблонный регистратор, который
# позволяет добавлять новые теги и фильтры для использования в шаблонах Django.
register = template.Library()


@register.simple_tag
def popular_tags() -> List[Dict[str, str]]:
    """
        Возвращает список популярных тегов, отсортированных по количеству статей,
        содержащих эти теги, в виде списка словарей.

        Returns:
            List[Dict[str, str]]: Список словарей с ключами 'name', 'num_times' и 'slug',
                                  где 'name' - имя тега, 'num_times' - количество статей с тегом,
                                  'slug' - уникальный идентификатор тега.
    """
    # Получаем список тегов, сгруппированных по количеству статей
    tags = Tag.objects.annotate(num_times=Count('article')).order_by('-num_times')

    # Преобразуем QuerySet в список словарей с нужными полями
    tag_list = list(tags.values('name', 'num_times', 'slug'))

    # Возвращаем список популярных тегов
    return tag_list


@register.inclusion_tag('includes/latest_comments.html')
def show_latest_comments(count=5) -> dict:
    """
        Создает inclusion tag для вывода последних опубликованных комментариев.

        Args:
            count (int, optional): Количество комментариев для отображения. По умолчанию 5.

        Returns:
            dict: Словарь с последними комментариями, доступный в шаблоне 'latest_comments.html'.
    """
    # Выбираем последние опубликованные комментарии, включая информацию об авторах
    comments = Comment.objects.select_related('author').filter(status='published').order_by('-time_create')[:count]
    # Возвращаем словарь с комментариями для использования в шаблоне 'latest_comments.html'
    return {'comments': comments}
