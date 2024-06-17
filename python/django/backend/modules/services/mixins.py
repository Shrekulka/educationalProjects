# backend/modules/services/mixins.py

from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


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