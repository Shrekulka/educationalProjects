# zodiac_portal/horoscope/urls.py

from django.urls import path

from horoscope import views

urlpatterns = [
    # Маршрут для главной страницы (index view).
    path('', views.index),

    # Маршрут для получения типов знаков зодиака (get_zodiac_types view).
    path('type', views.get_zodiac_types, name='zodiac-types'),

    # Маршрут для получения знаков зодиака по элементу (get_signs_by_element view).
    path('type/<str:element>', views.get_signs_by_element, name='horoscope-element'),

    # Маршрут для получения информации о знаке зодиака по дате (get_info_by_date view).
    path('<int:month>/<int:day>', views.get_info_by_date),

    # Маршрут для получения информации о знаке зодиака по номеру (get_info_about_sign_zodiac_by_number view).
    path('<int:sign_zodiac>', views.get_info_about_sign_zodiac_by_number),

    # Маршрут для получения информации о знаке зодиака по имени (get_info_about_sign_zodiac view).
    path('<str:sign_zodiac>', views.get_info_about_sign_zodiac, name='horoscope-name'),
]
