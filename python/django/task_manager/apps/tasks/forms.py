# task_manager/apps/tasks/forms.py

"""
Forms для задач.

Аргументация:
- Отдельные формы для разных действий (создание vs обновление)
- HTMX атрибуты для интерактивности
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.tasks.models import Task


class TaskForm(forms.ModelForm):
    """Базовая форма для создания/обновления задачи."""

    class Meta:
        model = Task
        fields = ['name', 'description', 'priority', 'deadline', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Task name'),
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Task description (optional)'),
                'rows': 3,
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')

        if deadline and deadline < timezone.now() and not self.instance.pk:  # ← проверка только для новых
            raise ValidationError(_('Deadline cannot be in the past'))

        return deadline


class TaskQuickAddForm(forms.ModelForm):
    """
    Форма для быстрого добавления задачи (только имя).

    Используется для добавления задач без всех полей.
    """

    class Meta:
        model = Task
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Start typing here to create a task...'),
                'required': True,
            }),
        }