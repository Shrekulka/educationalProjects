# backend/modules/system/backends.py
from typing import Optional

from django.contrib.auth.backends import ModelBackend, get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

# Получаем модель пользователя, которая используется в текущей конфигурации Django.
UserModel = get_user_model()

class UserModelBackend(ModelBackend):
    """
        Класс UserModelBackend расширяет стандартный ModelBackend Django для предоставления возможности аутентификации
        по username или email.

        Методы:
            authenticate(request, username=None, password=None, **kwargs) -> Optional[User]:
                Аутентифицирует пользователя по username или email и паролю.
            get_user(user_id: int) -> Optional[User]:
                Возвращает объект пользователя по его идентификатору.
    """

    def authenticate(self, request, username: str = None, password: str = None, **kwargs) -> Optional[UserModel]:
        """
            Аутентифицирует пользователя по username или email и паролю.

            Аргументы:
                request: HttpRequest объект, представляющий текущий запрос.
                username (str): Имя пользователя или email.
                password (str): Пароль пользователя.
                **kwargs: Дополнительные аргументы.

            Returns:
                Optional[User]: Объект пользователя, если аутентификация прошла успешно, иначе None.
        """
        try:
            # Ищем пользователя по username или email (независимо от регистра).
            user = UserModel.objects.get(Q(username=username) | Q(email__iexact=username))

        # Если пользователь не найден, возвращаем None.
        except UserModel.DoesNotExist:
            return None

        # Если найдено несколько пользователей, связанных с указанными username или email, берем первого найденного.
        except MultipleObjectsReturned:
            return UserModel.objects.filter(email=username).order_by('id').first()

        # Если исключения не были подняты
        else:
            # Проверяем пароль и возможность аутентификации пользователя.
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        return None

    def get_user(self, user_id: int) -> Optional[UserModel]:
        """
            Возвращает объект пользователя по его идентификатору.

            Аргументы:
                user_id (int): Идентификатор пользователя.

            Returns:
                Optional[User]: Объект пользователя, если пользователь найден и валиден, иначе None.
        """
        try:
            # Ищем пользователя по его идентификатору.
            user = UserModel.objects.get(pk=user_id)

        except UserModel.DoesNotExist:
            # Если пользователь не найден, возвращаем None.
            return None

        # Проверяем возможность аутентификации пользователя.
        return user if self.user_can_authenticate(user) else None
