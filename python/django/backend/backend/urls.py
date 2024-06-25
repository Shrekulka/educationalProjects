"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Подключаем URL-пути из приложения "django_ckeditor_5" для обработки запросов редактора CKEditor 5
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    # Подключаем URL-пути административной панели Django
    path('admin/', admin.site.urls),
    # Добавили импорт include, для включения urls.py из приложения блог, а также указали обработку юрлов, указав
    # главную страницу
    path('', include('modules.blog.urls')),
    # Подключаем URL-пути из приложения "modules.system" для обработки запросов, связанных с системой пользователей и
    # профилями
    path('', include('modules.system.urls')),

]

########################################################################################################################
# Проверяем, находится ли проект в режиме отладки.
if settings.DEBUG:
    # Если проект находится в режиме отладки, добавляем URL-пути для отладочной панели веб-инструментов.
    # Добавляем путь для debug_toolbar в начало списка urlpatterns.
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns

    # Затем добавляем URL-пути для медиафайлов к urlpatterns.
    # Это нужно для того, чтобы в режиме отладки Django мог обслуживать медиафайлы.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

########################################################################################################################
