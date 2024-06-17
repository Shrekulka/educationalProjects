from django import template
from django.db.models.manager import BaseManager
from django.utils.http import urlencode

from goods.models import Categories

# Регистрируем наш тег в системе шаблонов Django
register = template.Library()


# Определение простого тега tag_categories
@register.simple_tag()
def tag_categories() -> BaseManager[Categories]:
    """
        Retrieve all categories.

        Returns:
            BaseManager[Categories]: Queryset of all categories.
    """
    # Возвращаем все категории из базы данных
    return Categories.objects.all()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs) -> str:
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
