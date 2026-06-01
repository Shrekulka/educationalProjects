# order-management-service/modules/orders/admin.py

from django.contrib import admin
from .models import Client, Product, Order, OrderItem


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Колонки в списку клієнтів
    list_display = ['id', 'name', 'email', 'phone', 'created_at']
    # Поле пошуку
    search_fields = ['name', 'email']
    # Фільтр по даті
    list_filter = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


class OrderItemInline(admin.TabularInline):
    """
    Inline — дозволяє редагувати позиції замовлення
    прямо всередині форми замовлення.
    Це класичний ERP-підхід: замовлення + його позиції на одному екрані.
    """
    model = OrderItem
    extra = 1  # одне порожнє поле для нової позиції
    # price і amount — readonly, вони заповнюються автоматично
    readonly_fields = ['price', 'amount']
    fields = ['product', 'quantity', 'price', 'amount']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['client__name']  # пошук по імені клієнта через JOIN
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]  # підключаємо позиції до форми замовлення

    # Групуємо поля у форм-сети для зручності
    fieldsets = [
        ('Основна інформація', {
            'fields': ['client', 'status']
        }),
        ('Фінанси', {
            'fields': ['total_amount']
        }),
        ('Дати', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']  # згорнута секція
        }),
    ]