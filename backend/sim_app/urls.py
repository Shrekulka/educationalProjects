from django.urls import path

from .views import get_device_info_view, get_gwp_info_view, get_sim_info_view

# Определяем пути для API-эндпоинтов
urlpatterns = [
    # URL для получения информации об устройстве
    path('get_device_info/', get_device_info_view, name='get_device_info'),

    # URL для получения информации о GWP по ID устройства
    path('get_gwp_info/<int:device_id>/', get_gwp_info_view, name='get_gwp_info'),

    # URL для получения информации о SIM-карте по ID устройства
    path('get_sim_info/<int:device_id>/', get_sim_info_view, name='get_sim_info'),
]
