# backend/modules/services/utils.py

from typing import Optional
from uuid import uuid4

from django.db.models import Model
from django.http import HttpRequest
from pytils.translit import slugify


########################################################################################################################
def unique_slugify(instance: Model, slug: str) -> str:
    """
    Функция для генерации уникальных SLUG для объектов модели.

    Args:
        instance (Model): Экземпляр модели, для которой генерируется SLUG.
        slug (str): Исходный SLUG.

    Returns:
        str: Уникальный SLUG.
    """
    model = instance.__class__  # Получаем класс модели из экземпляра
    unique_slug = slugify(slug)  # Преобразуем исходный SLUG в URL-подобный формат

    # Проверяем, существует ли объект с таким SLUG в базе данных
    while model.objects.filter(slug=unique_slug).exists():
        # Если SLUG уже занят, генерируем новый с использованием уникального идентификатора
        unique_slug = f"{unique_slug}-{uuid4().hex[:8]}"

    return unique_slug  # Возвращаем уникальный SLUG


########################################################################################################################
def get_client_ip(request: HttpRequest) -> Optional[str]:
    """
        Получает IP-адрес клиента из заголовков HTTP-запроса.

        Если запрос был проксирован, функция пытается получить оригинальный IP-адрес клиента из заголовка
        'HTTP_X_FORWARDED_FOR'. В противном случае, она возвращает IP-адрес из заголовка 'REMOTE_ADDR'.

        Аргументы:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            Optional[str]: IP-адрес клиента в виде строки, или None, если IP-адрес не был найден.
    """
    # Получаем IP-адрес из заголовка 'HTTP_X_FORWARDED_FOR', если запрос был проксирован
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    # Если заголовок 'HTTP_X_FORWARDED_FOR' присутствует, берем первый IP-адрес из списка
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        # Иначе, берем IP-адрес из заголовка 'REMOTE_ADDR'
        ip = request.META.get('REMOTE_ADDR')

    return ip
