# task_manager/apps/tasks/views.py
"""
Class-Based Views для задач.
"""

import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render  # Убедитесь, что этот импорт есть
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView, DeleteView, View, ListView

from apps.projects.models import Project
from apps.tasks.forms import TaskForm, TaskQuickAddForm
from apps.tasks.models import Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskQuickAddForm
    template_name = 'tasks/task_form_quick.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(
            Project,
            pk=kwargs.get('project_id'),
            user=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Принудительно сохраняем задачу с нужными полями
        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.user = self.request.user
        self.object.save()

        # Если это HTMX-запрос — возвращаем HTML только что созданной задачи
        if self.request.headers.get('HX-Request'):
            return render(self.request, 'tasks/task_item.html', {'task': self.object})

        # Для обычных запросов — редирект на страницу проекта
        return super().form_valid(form)

    def get_success_url(self):
        return self.project.get_absolute_url()


class TaskFullCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm  # ← полная форма
    template_name = 'tasks/task_form.html'  # ← полный шаблон

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(
            Project,
            pk=kwargs.get('project_id'),
            user=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.project.get_absolute_url()


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        return self.object.project.get_absolute_url()

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['tasks/task_item.html']
        return super().get_template_names()


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        return self.object.project.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        """
        Обработка DELETE-запроса (HTMX) и POST-запроса (обычный).
        """
        self.object = self.get_object()
        self.object.delete()

        # Если это HTMX-запрос, возвращаем пустой ответ,
        # чтобы HTMX удалил элемент из DOM (hx-swap="outerHTML")
        if request.headers.get('HX-Request'):
            return HttpResponse('')

        # Для обычных POST-запросов — редирект
        return HttpResponseRedirect(self.get_success_url())


class TaskToggleStatusView(LoginRequiredMixin, View):
    """
    Переключение статуса задачи (AJAX).
    Логика: completed → pending, иначе → completed.
    Возвращает HTML элемента задачи (task_item.html) для hx-swap="outerHTML".
    """

    @method_decorator(require_http_methods(["POST"]))
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        if task.status == 'completed':
            task.status = 'pending'
            task.completed_at = None
        else:
            task.status = 'completed'
            task.completed_at = timezone.now()
        task.save()
        return render(request, 'tasks/task_item.html', {'task': task})


class TaskBulkUpdateOrderView(LoginRequiredMixin, View):
    @method_decorator(require_http_methods(["POST"]))
    def post(self, request):
        data = json.loads(request.body)
        task_ids = data.get('task_ids', [])

        tasks_by_id = {t.id: t for t in Task.objects.filter(id__in=task_ids, user=request.user)}
        ordered_tasks = []
        for index, task_id in enumerate(task_ids):
            task = tasks_by_id.get(int(task_id))
            if task:
                task.order = index
                ordered_tasks.append(task)

        with transaction.atomic():
            Task.objects.bulk_update(ordered_tasks, ['order'])

        return JsonResponse({'success': True})


class TaskListContainerView(LoginRequiredMixin, ListView):
    """
    Возвращает блок с фильтром статусов и списком задач для конкретного проекта.
    Используется в project_list.html для каждого проекта.
    """
    model = Task
    template_name = 'tasks/task_list_container.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        project = get_object_or_404(
            Project,
            id=self.kwargs['project_id'],
            user=self.request.user
        )
        queryset = Task.objects.filter(project=project)
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('priority', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(
            Project,
            id=self.kwargs['project_id'],
            user=self.request.user
        )
        context['statuses'] = Task.STATUS_CHOICES
        context['selected_status'] = self.request.GET.get('status', '')
        return context
