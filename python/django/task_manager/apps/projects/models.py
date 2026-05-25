# task_manager/apps/projects/models.py

"""
Модель Project - представляет проект с задачами.

Аргументация дизайна:
- Связь с User для обеспечения user-specific доступа
- Timestamp поля (created_at, updated_at) для аудита
- Soft delete не реализован (можно добавить флаг is_active)
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """
    Модель проекта.

    Attributes:
        user (ForeignKey): Владелец проекта (один user -> много projects)
        name (CharField): Название проекта (макс 255 символов)
        description (TextField): Описание проекта (опциональное)
        created_at (DateTimeField): Дата создания (автоматически заполняется)
        updated_at (DateTimeField): Дата последнего обновления (автоматически обновляется)
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении user удалятся все его проекты
        related_name='projects',  # Обратная связь для удобства: user.projects.all()
        verbose_name=_('User')
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Project Name'),
        help_text=_('Enter the project name')
    )

    description = models.TextField(
        blank=True,  # Опциональное поле
        null=True,
        verbose_name=_('Description'),
        help_text=_('Add project description')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,  # Устанавливается при создании объекта
        verbose_name=_('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,  # Обновляется при каждом сохранении
        verbose_name=_('Updated At')
    )

    class Meta:
        """
        Метаинформация для модели.

        Аргументация:
        - ordering = ['-created_at']: Новые проекты вверху
        - indexes: Ускорение поиска по user (очень часто используется)
        - unique_together: Имя проекта должно быть уникальным у каждого user,
          но разные users могут иметь проекты с одинаковым названием
        """
        ordering = ['-created_at']
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
        unique_together = [
            ('user', 'name'),  # Один user не может иметь два проекта с одинаковым именем
        ]

    def __str__(self) -> str:
        """Строковое представление объекта."""
        return self.name

    def get_absolute_url(self) -> str:
        """URL для просмотра проекта."""
        return reverse('project_detail', kwargs={'pk': self.pk})

    # @property
    # def task_count(self) -> int:
    #     """Количество задач в проекте."""
    #     return self.tasks.count()
    #
    # @property
    # def completed_task_count(self) -> int:
    #     """Количество выполненных задач."""
    #     return self.tasks.filter(status='completed').count()
