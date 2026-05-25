# task_manager/config/urls.py

"""
Главный файл маршрутизации.

Аргументация:
- Использование include() для модульности (каждое приложение отвечает за свои URL)
- allauth URLs для аутентификации
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# URL patterns
urlpatterns = [
    # Admin панель
    path('admin/', admin.site.urls),

    # Authentication (allauth)
    path('accounts/', include('allauth.urls')),

    # Applications
    path('', include('apps.projects.urls')),
    path('tasks/', include('apps.tasks.urls')),
]
