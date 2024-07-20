from django.urls import path

from converter.views import money_convert

urlpatterns = [
    path('', money_convert),  # URL-путь без дополнительного пути, направляющий на представление money_convert
]