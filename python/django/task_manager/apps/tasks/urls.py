# task_manager/apps/tasks/urls.py

"""URL routes для приложения tasks."""

from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    # POST создание задачи (быстрое)
    path('create/<int:project_id>/', views.TaskCreateView.as_view(), name='task_create'),

    # POST создание задачи (полная форма)
    path('create-full/<int:project_id>/', views.TaskFullCreateView.as_view(), name='task_create_full'),

    # POST обновление задачи
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),

    # POST удаление задачи
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    # AJAX переключение статуса
    path('<int:task_id>/toggle-status/', views.TaskToggleStatusView.as_view(), name='task_toggle_status'),

    # AJAX обновление порядка
    path('bulk-update-order/', views.TaskBulkUpdateOrderView.as_view(), name='task_bulk_update_order'),

    # AJAX список задач (контейнер)
    path('list/<int:project_id>/', views.TaskListContainerView.as_view(), name='task_list_container'),
]
