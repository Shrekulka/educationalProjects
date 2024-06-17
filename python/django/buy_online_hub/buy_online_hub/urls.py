"""
URL configuration for buy_online_hub project.

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
from django.urls import include, path, URLResolver

urlpatterns: list[URLResolver] = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('catalog/', include('goods.urls', namespace='catalog')),
    path('user/', include('users.urls', namespace='user')),
]

# Проверяем, находится ли проект в режиме отладки.
if settings.DEBUG:
    # Если проект находится в режиме отладки, добавляем URL-пути для отладочной панели веб-инструментов.
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

    # Затем добавляем URL-пути для медиафайлов к urlpatterns.
    # Это нужно для того, чтобы в режиме отладки Django мог обслуживать медиафайлы.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
