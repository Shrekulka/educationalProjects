# task_manager/apps/projects/views.py

"""
Class-Based Views для проектов.

Аргументация использования CBV:
- Встроенная защита от CSRF (POST методы)
- Наследование (DRY принцип)
- Встроенная пагинация, фильтрация, поиск
- Меньше кода, чем функциональные views
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from apps.projects.forms import ProjectForm
from apps.projects.models import Project
from apps.tasks.forms import TaskQuickAddForm
from apps.tasks.models import Task


class ProjectListView(LoginRequiredMixin, ListView):
    """
    Вывод списка проектов текущего пользователя.

    Особенности:
    - LoginRequiredMixin: доступ только авторизованным пользователям
    - get_queryset(): фильтрует проекты текущего user
    - Автоматически передает контекст 'object_list' и 'page_obj' в шаблон
    """

    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10  # 10 проектов на странице

    def get_queryset(self):
        return (
            Project.objects
            .filter(user=self.request.user)
            .annotate(
                task_count=Count('tasks'),  # ← добавляем подсчёт
                completed_task_count=Count('tasks', filter=Q(tasks__status='completed'))  # ← для completed
            )
            .prefetch_related('tasks')
            .order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = TaskQuickAddForm()
        context['total_projects'] = self.object_list.count()
        context['total_tasks'] = Task.objects.filter(user=self.request.user).count()
        context['statuses'] = Task.STATUS_CHOICES
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """
    Детальный просмотр одного проекта с его задачами.

    Особенности:
    - Получение проекта по ID
    - Вывод всех задач в проекте
    - HTMX интеграция для динамического обновления задач
    """

    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        """Получить только проекты текущего пользователя."""
        return Project.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Добавить задачи в контекст."""
        context = super().get_context_data(**kwargs)
        project = self.object

        # Фильтрация задач по статусу (из GET параметра)
        status_filter = self.request.GET.get('status')
        tasks = project.tasks.all()

        if status_filter:
            tasks = tasks.filter(status=status_filter)

        context['tasks'] = tasks.order_by('priority', 'order')
        context['task_form'] = TaskQuickAddForm()
        context['statuses'] = Task.STATUS_CHOICES
        context['selected_status'] = status_filter

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    Создание нового проекта.

    Особенности:
    - form_valid(): автоматически устанавливает текущего user
    - success_url: редирект на список проектов
    """

    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        """
        Обработка валидной формы.

        Устанавливаем текущего пользователя как владельца проекта.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    Обновление существующего проекта.

    Аргументация:
    - Только владелец проекта может его редактировать
    """

    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def get_queryset(self):
        """Только проекты текущего user."""
        return Project.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Редирект на обновленный проект."""
        return self.object.get_absolute_url()


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление проекта.

    Осторожно: также удалит все связанные задачи (CASCADE delete).
    """

    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def get_queryset(self):
        """Только проекты текущего user."""
        return Project.objects.filter(user=self.request.user)


class ProjectSearchView(LoginRequiredMixin, ListView):
    """
    Поиск проектов по названию (для HTMX).

    Аргументация:
    - GET параметр 'q' для поиска
    - Возвращает только HTML фрагмент (partial) для HTMX замены
    """

    model = Project
    template_name = 'projects/project_list_partial.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        """Поиск по названию проекта."""
        queryset = Project.objects.filter(user=self.request.user)
        query = self.request.GET.get('q', '').strip()

        if query:
            # icontains для case-insensitive поиска
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

        return queryset.order_by('-created_at')
