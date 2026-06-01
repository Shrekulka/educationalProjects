# order-management-service/modules/orders/serializers.py

from rest_framework import serializers
from .models import Client, Product, Order, OrderItem
from django.db import transaction


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_price(self, value):
        """
        Валідація на рівні серіалізатора.
        validate_<field_name> — конвенція DRF для валідації окремого поля.
        """
        if value <= 0:
            raise serializers.ValidationError('Ціна має бути більше нуля.')
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    # Показуємо назву товару в читабельному форматі
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'amount']
        read_only_fields = ['id', 'price', 'amount']  # рахуються автоматично


class OrderItemCreateSerializer(serializers.Serializer):
    """
    Окремий серіалізатор для створення позицій.
    Чому окремий? Бо при створенні нам потрібен тільки
    product_id і quantity — решта рахується автоматично.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(f'Товар з id={value} не існує.')
        return value


class OrderSerializer(serializers.ModelSerializer):
    """
    Серіалізатор замовлення для читання.
    Показує повну інформацію включно з позиціями і клієнтом.
    """
    # Вкладені серіалізатори для повного відображення
    items = OrderItemSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'client', 'client_name', 'status', 'status_display',
            'total_amount', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    """
    Серіалізатор для СТВОРЕННЯ замовлення.

    Чому не ModelSerializer?
    Тому що логіка створення складна:
    - треба перевірити клієнта
    - треба перевірити що є хоча б один товар
    - треба створити Order і OrderItem в одній транзакції

    Явний Serializer дає більше контролю.
    """
    client_id = serializers.IntegerField()
    items = OrderItemCreateSerializer(many=True)

    def validate_client_id(self, value):
        """Бізнес-правило: не можна створити замовлення без клієнта"""
        if not Client.objects.filter(id=value).exists():
            raise serializers.ValidationError(f'Клієнт з id={value} не існує.')
        return value

    def validate_items(self, value):
        """Бізнес-правило: у замовленні має бути хоча б один товар"""
        if not value:
            raise serializers.ValidationError(
                'Замовлення має містити хоча б один товар.'
            )
        return value

    def create(self, validated_data):
        with transaction.atomic():
            client = Client.objects.get(id=validated_data['client_id'])
            order = Order.objects.create(client=client)

            # об’єднуємо дублікати товарів =
            items_dict = {}
            for item_data in validated_data['items']:
                product_id = item_data['product_id']
                quantity = item_data['quantity']
                items_dict[product_id] = items_dict.get(product_id, 0) + quantity
            for product_id, total_quantity in items_dict.items():
                product = Product.objects.get(id=product_id)
                item = OrderItem(
                    order=order,
                    product=product,
                    quantity=total_quantity
                )
                item.save(skip_recalc=True)

            order.calculate_total()
            order.refresh_from_db()
            return order

class OrderUpdateStatusSerializer(serializers.Serializer):
    """Серіалізатор для часткового оновлення статусу замовлення (PATCH)."""
    status = serializers.ChoiceField(choices=Order.Status)

    def validate(self, attrs):
        """
        Перевіряє бізнес-правила зміни статусу.
        """
        # Отримуємо поточний екземпляр замовлення
        instance = getattr(self, 'instance', None)
        if instance is None:
            raise serializers.ValidationError(
                "Серіалізатор використовується без прив'язки до об'єкта замовлення. Очікується оновлення."
            )

        new_status = attrs.get('status')
        old_status = instance.status

        # Правило 1: Завершене замовлення не можна змінювати
        if old_status == Order.Status.COMPLETED and new_status != Order.Status.COMPLETED:
            raise serializers.ValidationError(
                {"status": "Неможливо змінити статус завершеного замовлення."}
            )

        # Правило 2: Скасоване замовлення не можна змінювати
        if old_status == Order.Status.CANCELLED:
            raise serializers.ValidationError(
                {"status": "Скасоване замовлення не можна змінювати."}
            )

        # Правило 3: Не можна повернути зі статусу "В обробці" до "Нове"
        if old_status == Order.Status.PROCESSING and new_status == Order.Status.NEW:
            raise serializers.ValidationError(
                {"status": "Неможливо повернути замовлення зі статусу 'В обробці' до 'Нове'."}
            )

        return attrs