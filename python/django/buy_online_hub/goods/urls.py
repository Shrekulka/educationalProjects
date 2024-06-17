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

from goods.views import catalog, product

# Задаем имя для данного приложения, которое будет использоваться для различения его URL-адресов от URL-адресов других
# приложений.
app_name = 'goods'

# Определение маршрутов URL для представлений
urlpatterns: list[URLPattern] = [

    path('search/', catalog, name='search'),

    path('<slug:category_slug>/', catalog, name='index'),

    path('product/<int:product_id>/', product, name='product'),

    path('product/<slug:product_slug>/', product, name='product'),
]
