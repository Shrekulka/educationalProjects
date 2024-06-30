# backend/modules/blog/templatetags/blog_tags.py

from datetime import datetime, date, time, timedelta
from typing import List, Dict

from django import template
from django.db.models import Count, Q, QuerySet
from django.utils import timezone
from taggit.models import Tag

from modules.blog.models import Comment, Article

# Используется для регистрации пользовательских тегов и фильтров в Django. Это общий шаблонный регистратор, который
# позволяет добавлять новые теги и фильтры для использования в шаблонах Django.
register = template.Library()


########################################################################################################################
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


########################################################################################################################

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


########################################################################################################################
@register.simple_tag
def popular_articles() -> 'QuerySet[Article]':
    """
    Возвращает список популярных статей за последние 7 дней, отсортированных по числу просмотров.

    Использует аннотации QuerySet для подсчета общего числа просмотров статей и числа просмотров за текущий день.
    Просмотры за последние 7 дней считаются с использованием фильтрации по датам.

    Returns:
        QuerySet[Article]: Queryset популярных статей, отсортированных по числу просмотров.
    """
    # Получаем текущую дату и время в формате datetime
    now = timezone.now()
    # Вычисляем дату начала дня (00:00) 7 дней назад
    start_date = now - timedelta(days=7)
    # Вычисляем дату начала текущего дня (00:00)
    today_start = timezone.make_aware(datetime.combine(date.today(), time.min))

    # Получаем queryset всех статей с аннотациями числа просмотров за последние 7 дней и за сегодня.
    # Отбираются первые 10 статей.
    articles = Article.objects.annotate(
        total_view_count=Count('views', filter=Q(views__viewed_on__gte=start_date)),
        today_view_count=Count('views', filter=Q(views__viewed_on__gte=today_start))
    ).prefetch_related('views')

    # Сортируем статьи по числу просмотров, сначала по просмотрам за сегодня, затем за все время
    popular_articles = articles.order_by('-total_view_count', '-today_view_count')[:10]

    # Возвращаем список 10 самых популярных статей за последние 7 дней, отсортированных по количеству просмотров за
    # сегодняшний день и за все время.
    return popular_articles
########################################################################################################################
