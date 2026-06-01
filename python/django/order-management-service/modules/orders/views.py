# order-management-service/modules/orders/views.py

from django.db import connection
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client, Product, Order
from .serializers import (
    ClientSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderCreateSerializer, OrderUpdateStatusSerializer,
)


class APIRootView(APIView):
    """
    GET /api/ – корінь API, повертає посилання на основні розділи.
    """

    def get(self, request):
        return Response({
            "clients": request.build_absolute_uri(reverse('client-list')),
            "products": request.build_absolute_uri(reverse('product-list')),
            "orders": request.build_absolute_uri(reverse('order-list')),
            "order_form": request.build_absolute_uri(reverse('order-form')),
            "swagger": request.build_absolute_uri(reverse('swagger-ui')),
            "redoc": request.build_absolute_uri(reverse('redoc')),
            "health": request.build_absolute_uri(reverse('health-check')),
        })


class HealthCheckView(APIView):
    """
    GET /api/health/

    Проверяет что сервис работает и БД доступна.

    Почему это важно:
    - Load balancer может проверять /health/ перед отправкой трафика
    - Мониторинг (Prometheus, Grafana) использует этот endpoint
    - При деплое можно убедиться что новая версия поднялась корректно
    - Docker healthcheck может использовать этот endpoint

    Возвращает 200 если всё ок, 500 если БД недоступна.
    """

    def get(self, request):
        try:
            # Простой запрос к БД — проверяем что соединение живое
            connection.ensure_connection()
            return Response({
                'status': 'ok',
                'database': 'ok',
                'service': 'K2 ERP Orders API',
            })
        except Exception as e:
            return Response(
                {'status': 'error', 'database': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClientListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/clients/  — список клієнтів
    POST /api/clients/  — створити клієнта

    generics.ListCreateAPIView — вбудований DRF view,
    який автоматично реалізує обидві дії.
    Нам залишається тільки вказати queryset і serializer.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/clients/{id}/  — отримати клієнта
    PUT    /api/clients/{id}/  — оновити клієнта
    DELETE /api/clients/{id}/  — видалити клієнта
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/products/  — список товарів
    POST /api/products/  — створити товар
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/products/{id}/
    PUT    /api/products/{id}/
    DELETE /api/products/{id}/
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            # Товар используется в заказах — удаление запрещено бизнес-правилом
            return Response(
                {
                    'detail': (
                        'Неможливо видалити товар, оскільки він '
                        'використовується в одному або кількох замовленнях.'
                    ),
                    'protected_objects': str(e),
                },
                status=status.HTTP_409_CONFLICT,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/orders/           — список замовлень
    GET  /api/orders/?client_id=1  — замовлення конкретного клієнта
    POST /api/orders/           — створити замовлення
    """

    def get_queryset(self):
        """
        Перевизначаємо get_queryset для фільтрації по клієнту.
        select_related('client') — один SQL запит замість N+1.
        prefetch_related('items__product') — ефективна вибірка позицій.
        """
        queryset = Order.objects.select_related('client').prefetch_related(
            'items__product'
        )
        # Якщо передано client_id — фільтруємо
        client_id = self.request.query_params.get('client_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset

    def get_serializer_class(self):
        """
        Різні серіалізатори для читання і запису.
        GET → OrderSerializer (повна інформація)
        POST → OrderCreateSerializer (тільки потрібні поля)
        """
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Перевизначаємо create щоб повернути повну інформацію
        про замовлення після створення (через OrderSerializer),
        а не через OrderCreateSerializer.
        """
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        # Повертаємо повну інформацію про замовлення
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    """
    GET /api/orders/{id}/  — деталі замовлення
    """
    queryset = Order.objects.select_related('client').prefetch_related(
        'items__product'
    )
    serializer_class = OrderSerializer


class OrderUpdateStatusView(APIView):
    """PATCH /api/orders/{id}/status/ – зміна статусу замовлення"""
    queryset = Order.objects.all()
    serializer_class = OrderUpdateStatusSerializer

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderUpdateStatusSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order.status = serializer.validated_data['status']
        order.save(update_fields=['status'])
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class OrderFormView(TemplateView):
    """
    Простейшая HTML-форма для создания заказа.
    """
    template_name = 'orders/order_form.html'
