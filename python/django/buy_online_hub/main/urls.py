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
from django.urls import path, URLPattern

from main.views import index, about, delivery_and_payment, contacts

# Задаем имя для данного приложения, которое будет использоваться для различения его URL-адресов от URL-адресов других
# приложений.
app_name = 'main'

# Определение маршрутов URL для представлений
urlpatterns: list[URLPattern] = [
    # Главная страница, вызывает функцию index из файла views.py
    path('', index, name='index'),

    # Страница "О нас", вызывает функцию about из файла views.py
    path('about/', about, name='about'),

    # Страница "Доставка и оплата", вызывает функцию delivery_and_payment из файла views.py
    path('delivery_and_payment/', delivery_and_payment, name='delivery_and_payment'),

    # Страница "Контакты", вызывает функцию contacts из файла views.py
    path('contacts/', contacts, name='contacts'),
]
