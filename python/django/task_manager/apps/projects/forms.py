# task_manager/apps/projects/forms.py

"""
Forms для проектов.

Аргументация:
- ModelForm наследует валидацию из модели
- Custom clean() методы для cross-field валидации
- exclude для исключения полей из формы (user устанавливается в view)
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.projects.models import Project


class ProjectForm(forms.ModelForm):
    """
    Форма для создания/обновления проекта.

    Особенности:
    - Автоматическое добавление Bootstrap классов для стилизации
    - Валидация имени (не пустое, не слишком длинное)
    """

    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter project name'),
                'required': True,
                'maxlength': 255,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Enter project description (optional)'),
                'rows': 4,
            }),
        }
        labels = {
            'name': _('Project Name'),
            'description': _('Description'),
        }

    def clean_name(self) -> str:
        """Валидация имени проекта."""
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise ValidationError(_('Project name cannot be empty'))

        if len(name) < 3:
            raise ValidationError(_('Project name must be at least 3 characters long'))

        return name

    def clean(self) -> dict:
        """Общая валидация формы."""
        cleaned_data = super().clean()

        # Проверка что описание не слишком длинное
        description = cleaned_data.get('description', '')
        if len(description) > 2000:
            self.add_error('description', _('Description is too long (max 2000 characters)'))

        return cleaned_data