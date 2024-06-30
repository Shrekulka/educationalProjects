# backend/modules/system/middleware.py

from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpRequest
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class ActiveUserMiddleware(MiddlewareMixin):
    """
        Middleware для отслеживания активности пользователей.

        При каждом запросе проверяет, аутентифицирован ли пользователь и имеет ли текущая сессия ключ.
        Если условия выполнены, обновляет время последнего входа пользователя в базе данных и устанавливает или
        обновляет запись в кэше о последнем входе.

        Attributes:
            request: Объект запроса, содержащий информацию о текущем HTTP-запросе.

        Methods:
            process_request(self, request: HttpRequest) -> None:
                Обрабатывает каждый входящий запрос.
                Если пользователь аутентифицирован и сессия имеет ключ, обновляет последний вход пользователя и
                устанавливает запись в кэше с временем последнего входа.
    """

    def process_request(self, request: HttpRequest) -> None:
        """
            Обрабатывает каждый входящий запрос.

            Args:
                request: Объект запроса, содержащий информацию о текущем HTTP-запросе.
        """
        # Проверяем, аутентифицирован ли пользователь и имеет ли текущая сессия ключ.
        # Это условие гарантирует, что пользователь аутентифицирован и его сессия активна.
        if request.user.is_authenticated and request.session.session_key:

            # Создаем ключ кэша в формате 'last-seen-id-пользователя'
            cache_key: str = f'last-seen-{request.user.id}'

            # Получаем последнее время входа из кэша по ключу
            last_login = cache.get(cache_key)

            # Если в кэше нет записи, обновляем время последнего входа пользователя в базе данных
            if not last_login:
                User.objects.filter(id=request.user.id).update(last_login=timezone.now())
                # Устанавливаем кэширование на 300 секунд с текущей датой по ключу 'last-seen-id-пользователя'
                cache.set(cache_key, timezone.now(), 300)
