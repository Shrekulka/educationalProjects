from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')

    class Meta:
        # Настройки метаданных модели
        db_table: str = 'user'  # Имя таблицы в базе данных
        verbose_name: str = 'пользователя'  # Отображаемое название модели в единственном числе
        verbose_name_plural: str = 'пользователи'  # Отображаемое название модели во множественном числе

        # Метод для представления объекта в виде строки

    def __str__(self) -> str:
        return self.username
