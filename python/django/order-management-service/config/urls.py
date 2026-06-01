# order-management-service/config/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API модуля замовлень
    path('api/', include('modules.orders.urls')),

    # OpenAPI схема (JSON) — машиночитаемый формат
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI — красивый интерфейс для тестирования API прямо в браузере
    # Почему это важно: любой разработчик/интегратор сразу видит все endpoints,
    # параметры, форматы запросов и ответов без чтения кода
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),

    # ReDoc — альтернативный UI, более удобен для чтения документации
    path('api/schema/redoc/', SpectacularRedocView.as_view(
        url_name='schema'), name='redoc'),
]