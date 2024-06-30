# backend/urls.py

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
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from modules.blog.feeds import LatestArticlesFeed
from modules.blog.sitemaps import StaticSitemap, ArticleSitemap

# Карты-сайта
########################################################################################################################
# Определяем словарь sitemaps, который содержит две карты-сайта для использования в Django.
# Ключ 'static' относится к карте-сайта StaticSitemap, которая содержит статичные страницы.
# Ключ 'articles' относится к карте-сайта ArticleSitemap, которая содержит страницы статей.
sitemaps = {
    'static': StaticSitemap,    # Карта-сайта для статичных страниц
    'articles': ArticleSitemap,  # Карта-сайта для статей
}
########################################################################################################################

# Определяем обработчики ошибок
########################################################################################################################
handler403 = 'modules.system.views.tr_handler403'  # Обработчик ошибки 403 (Доступ запрещен)
handler404 = 'modules.system.views.tr_handler404'  # Обработчик ошибки 404 (Страница не найдена)
handler500 = 'modules.system.views.tr_handler500'  # Обработчик ошибки 500 (Внутренняя ошибка сервера)
########################################################################################################################

# URL-маршруты
########################################################################################################################
urlpatterns = [
    # Подключаем URL-пути из приложения "django_ckeditor_5" для обработки запросов редактора CKEditor 5
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    # Подключаем URL-пути административной панели Django
    path('admin/', admin.site.urls),
    # Определяем URL-путь для sitemap.xml, который использует предопределенное представление Django для карты сайта.
    # Передаем параметр sitemaps со словарем sitemaps, определенным ранее.
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # Определяем URL-путь для ленты RSS с последними статьями. Используем представление LatestArticlesFeed,
    # которое генерирует XML для ленты RSS.
    path('feeds/latest/', LatestArticlesFeed(), name='latest_articles_feed'),
    # Добавили импорт include, для включения urls.py из приложения блог, а также указали обработку юрлов, указав
    # главную страницу
    path('', include('modules.blog.urls')),
    # Подключаем URL-пути из приложения "modules.system" для обработки запросов, связанных с системой пользователей и
    # профилями
    path('', include('modules.system.urls')),
]
########################################################################################################################

# Настройки отладки
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
