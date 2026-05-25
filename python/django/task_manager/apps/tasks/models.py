# task_manager/apps/tasks/models.py

"""
Модель Task - представляет отдельную задачу в проекте.

Аргументация дизайна:
- Status choices для ограничения возможных значений
- Priority levels (1-3) вместо текстовых значений для сортировки
- Deadline может быть None (опциональная дата)
- completed_at фиксирует время завершения (для аналитики)
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.projects.models import Project


class Task(models.Model):
    """
    Модель задачи.

    Статусы:
        - pending: Ожидает выполнения
        - in_progress: В процессе выполнения
        - completed: Завершена
        - on_hold: На паузе
    """

    # Выбор для статуса задачи
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('on_hold', _('On Hold')),
    ]

    # Приоритеты (1 - самый низкий, 3 - самый высокий)
    PRIORITY_CHOICES = [
        (1, _('Low')),
        (2, _('Medium')),
        (3, _('High')),
    ]

    # Основные поля
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,  # При удалении проекта удалятся все задачи
        related_name='tasks',
        verbose_name=_('Project')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('User')
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Task Name')
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description')
    )

    # Статус задачи
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )

    # Приоритет (1-3)
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2,  # По умолчанию средний приоритет
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name=_('Priority')
    )

    # Сроки
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Deadline')
    )

    # Временные метки
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Completed At'),
        help_text=_('Automatically set when task is marked as completed')
    )

    # Порядок при отображении (для приоритизации)
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('Lower values appear first (used for sorting within priority)')
    )

    class Meta:
        """Метаинформация для модели."""
        ordering = ['priority', 'order', '-created_at']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self) -> str:
        """Строковое представление объекта."""
        return self.name

    def mark_completed(self) -> None:
        """Отметить задачу как завершенную."""
        if self.status != 'completed':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()

    def mark_pending(self) -> None:
        """Отметить задачу как ожидающую."""
        if self.status != 'pending':
            self.status = 'pending'
            self.completed_at = None
            self.save()

    @property
    def is_overdue(self) -> bool:
        """Проверить, просрочена ли задача."""
        if not self.deadline or self.status == 'completed':
            return False
        return self.deadline <= timezone.now()

    @property
    def days_until_deadline(self) -> int | None:
        """Количество дней до сроку."""
        if not self.deadline:
            return None
        delta = self.deadline.date() - timezone.now().date()
        return delta.days
