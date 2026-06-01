# order-management-service/modules/orders/urls.py

from django.urls import path

from . import views
from .views import APIRootView

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    # Health check
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    # Клієнти
    path('clients/', views.ClientListCreateView.as_view(), name='client-list'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),

    # Товари
    path('products/', views.ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Замовлення
    path('orders/', views.OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', views.OrderUpdateStatusView.as_view(), name='order-update-status'),
    path('order-form/', views.OrderFormView.as_view(), name='order-form'),
]
