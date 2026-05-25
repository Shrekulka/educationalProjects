# task_manager/apps/projects/urls.py

"""
URL routes для приложения projects.

Аргументация именования:
- Использование name для обратных ссылок ({% url 'name' %} в шаблонах)
- Следование Django конвенции: list, detail, create, update, delete
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('search/', views.ProjectSearchView.as_view(), name='project_search'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]