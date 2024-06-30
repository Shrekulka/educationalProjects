# backend/modules/services/mixins.py

from datetime import timedelta
from typing import Any, Union

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Model
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone

from .utils import get_client_ip
from ..blog.models import ViewCount


class AuthorRequiredMixin(AccessMixin):
    """
        Миксин для контроля доступа к объектам на основе авторства.

        Этот миксин проверяет, является ли текущий аутентифицированный пользователь автором объекта.
        Если пользователь не является автором и не является сотрудником (staff), выводится сообщение
        и происходит перенаправление на домашнюю страницу.

        Методы:
            dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
                Переопределяет метод dispatch базового класса.
    """

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
            Обработка запроса и контроль доступа.

            Переопределяет метод dispatch базового класса.
            Проверяет, является ли текущий аутентифицированный пользователь автором объекта.
            Если пользователь не является автором и не является сотрудником (staff),
            выводится сообщение и происходит перенаправление на домашнюю страницу.

            Аргументы:
                request (HttpRequest): Объект HTTP-запроса.
                *args (Any): Позиционные аргументы.
                **kwargs (Any): Именованные аргументы.

            Возвращает:
                HttpResponse: Объект HTTP-ответа.
        """
        # Проверяем, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Проверяем, что пользователь является автором объекта или сотрудником
        if request.user.is_authenticated:
            obj = self.get_object()
            if request.user != obj.author and not request.user.is_staff:
                # Выводим сообщение и перенаправляем на домашнюю страницу
                messages.info(request, 'Изменение и удаление статьи доступно только автору')
                return redirect('home')

        # Если все проверки пройдены, вызываем метод dispatch базового класса
        return super().dispatch(request, *args, **kwargs)


########################################################################################################################

class UserIsNotAuthenticated(UserPassesTestMixin):
    """
    Миксин для запрета доступа к странице для аутентифицированных пользователей.

    Этот миксин проверяет, не является ли текущий пользователь аутентифицированным.
    Если пользователь аутентифицирован, выводится сообщение и вызывается исключение PermissionDenied.

    Методы:
        test_func(self) -> bool:
            Проверяет, не является ли текущий пользователь аутентифицированным.
        handle_no_permission(self) -> HttpResponse:
            Обрабатывает случай, когда доступ запрещен.
    """

    def test_func(self) -> bool:
        """
            Проверяет, не является ли текущий пользователь аутентифицированным.

            Если пользователь аутентифицирован, выводится сообщение и вызывается исключение PermissionDenied.

            Возвращает:
                bool: True, если пользователь не аутентифицирован.
        """
        # Проверяем, аутентифицирован ли пользователь
        if self.request.user.is_authenticated:
            # Выводим сообщение и вызываем исключение PermissionDenied
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
        # Если пользователь не аутентифицирован, возвращаем True
        return True

    def handle_no_permission(self) -> HttpResponse:
        """
            Обрабатывает случай, когда доступ запрещен.

            Перенаправляет пользователя на домашнюю страницу.

            Возвращает:
                HttpResponse: Объект HTTP-ответа с перенаправлением.
        """
        # Перенаправляем пользователя на домашнюю страницу
        return redirect('home')


########################################################################################################################
class ViewCountMixin:
    """
        Миксин для увеличения счетчика просмотров статьи.

        Этот миксин добавляет функциональность для отслеживания просмотров статьи,
        увеличивая счетчик просмотров каждый раз, когда статья запрашивается.

        Методы:
            get_object() -> Union[Model, Any]: Возвращает объект статьи и увеличивает счетчик просмотров.
    """

    def get_object(self) -> Union[Model, Any]:
        """
            Получает объект статьи и увеличивает счетчик просмотров.

            Метод переопределяет стандартный get_object, добавляя функционал
            для учета просмотров статьи. Просмотр засчитывается, если с данного
            IP-адреса не было просмотров этой статьи за последние 7 дней.

            Returns:
                Union[Model, Any]: Объект статьи.

            Note:
                Метод создает новую запись в модели ViewCount, если
                для данного IP и статьи не было просмотров за последнюю неделю.
        """
        # Получаем статью по заданному slug
        obj = super().get_object()

        # Получаем IP-адрес пользователя
        ip_address = get_client_ip(self.request)

        # Получаем текущую дату и время
        now = timezone.now()

        # Вычисляем дату неделю назад
        week_ago = now - timedelta(days=7)

        # Создаем новую запись просмотра, если не было просмотров за последнюю неделю
        ViewCount.objects.get_or_create(
            article=obj,
            ip_address=ip_address,
            viewed_on__gte=week_ago
        )

        # Возвращаем объект статьи
        return obj
########################################################################################################################
