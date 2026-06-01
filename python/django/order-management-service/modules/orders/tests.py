# order-management-service/modules/orders/tests.py

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient

from modules.orders.models import Client, Product, Order, OrderItem


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client_obj(db):
    return Client.objects.create(
        name='ТОВ Тест',
        email='test@test.com'
    )


@pytest.fixture
def product_obj(db):
    return Product.objects.create(
        name='Товар 1',
        price=100.00
    )


@pytest.fixture
def product_obj2(db):
    return Product.objects.create(
        name='Товар 2',
        price=250.00
    )


# ─── Клієнти ─────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestClientAPI:
    def test_create_client(self, api_client):
        url = reverse('client-list')
        data = {'name': 'ТОВ Ромашка', 'email': 'romashka@test.com'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'ТОВ Ромашка'

    def test_list_clients(self, api_client, client_obj):
        url = reverse('client-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['count'] >= 1

    def test_duplicate_email_fails(self, api_client, client_obj):
        """Два клієнти не можуть мати однаковий email."""
        url = reverse('client-list')
        data = {'name': 'Інший клієнт', 'email': client_obj.email}
        response = api_client.post(url, data, format='json')
        assert response.status_code == 400


# ─── Товари ──────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestProductAPI:
    def test_create_product(self, api_client):
        url = reverse('product-list')
        data = {'name': 'Ноутбук', 'price': '25000.00'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201

    def test_negative_price_fails(self, api_client):
        """Бізнес-правило: ціна не може бути від'ємною."""
        url = reverse('product-list')
        data = {'name': 'Товар', 'price': '-100'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == 400

    def test_zero_price_fails(self, api_client):
        """Бізнес-правило: ціна не може бути нульовою."""
        url = reverse('product-list')
        data = {'name': 'Товар', 'price': '0'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == 400


# ─── Замовлення ───────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestOrderAPI:

    def test_create_order(self, api_client, client_obj, product_obj):
        """Основний сценарій: створити замовлення з одним товаром."""
        url = reverse('order-list')
        data = {
            'client_id': client_obj.id,
            'items': [{'product_id': product_obj.id, 'quantity': 2}]
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201
        assert float(response.data['total_amount']) == 200.0

    def test_order_with_multiple_items(
            self, api_client, client_obj, product_obj, product_obj2
    ):
        """
        Замовлення з кількома позиціями.
        Товар 1: 100 × 2 = 200
        Товар 2: 250 × 3 = 750
        Разом:             950
        """
        url = reverse('order-list')
        data = {
            'client_id': client_obj.id,
            'items': [
                {'product_id': product_obj.id, 'quantity': 2},
                {'product_id': product_obj2.id, 'quantity': 3},
            ]
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201
        assert float(response.data['total_amount']) == 950.0
        assert len(response.data['items']) == 2

    def test_order_without_client_fails(self, api_client):
        """Бізнес-правило: не можна створити замовлення без клієнта."""
        url = reverse('order-list')
        data = {'client_id': 9999, 'items': []}
        response = api_client.post(url, data, format='json')
        assert response.status_code == 400

    def test_order_without_items_fails(self, api_client, client_obj):
        """Бізнес-правило: у замовленні має бути хоча б один товар."""
        url = reverse('order-list')
        data = {'client_id': client_obj.id, 'items': []}
        response = api_client.post(url, data, format='json')
        assert response.status_code == 400

    def test_order_with_nonexistent_product_fails(
            self, api_client, client_obj
    ):
        """Неіснуючий товар у замовленні."""
        url = reverse('order-list')
        data = {
            'client_id': client_obj.id,
            'items': [{'product_id': 9999, 'quantity': 1}]
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == 400

    def test_order_with_zero_quantity_fails_via_api(
            self, api_client, client_obj, product_obj
    ):
        """
        API відхиляє quantity=0 на рівні серіалізатора (min_value=1).

        Це перший рубіж захисту — дані не доходять до моделі взагалі.
        Другий рубіж — OrderItem.clean() — покритий окремо в
        TestOrderItemModel.test_zero_quantity_raises_validation_error.

        Принцип "defense in depth": кожен шар незалежно
        гарантує коректність, а не покладається на попередній.
        """
        url = reverse('order-list')
        data = {
            'client_id': client_obj.id,
            'items': [{'product_id': product_obj.id, 'quantity': 0}]
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == 400

    def test_filter_orders_by_client(
            self, api_client, client_obj, product_obj
    ):
        """Фільтрація замовлень по клієнту."""
        order = Order.objects.create(client=client_obj)
        item = OrderItem(
            order=order,
            product=product_obj,
            quantity=1
        )
        item.save(skip_recalc=True)
        order.calculate_total()

        url = reverse('order-list')
        response = api_client.get(url, {'client_id': client_obj.id})
        assert response.status_code == 200
        for order_data in response.data['results']:
            assert order_data['client'] == client_obj.id

    def test_protect_prevents_product_deletion(
            self, api_client, client_obj, product_obj
    ):
        """
        Бізнес-правило: не можна видалити товар, якщо він є в замовленнях.
        API має повернути 409 Conflict.
        """
        order = Order.objects.create(client=client_obj)
        item = OrderItem(
            order=order,
            product=product_obj,
            quantity=1
        )
        item.save(skip_recalc=True)
        order.calculate_total()

        url = reverse('product-detail', kwargs={'pk': product_obj.id})
        response = api_client.delete(url)

        assert response.status_code == 409
        assert 'Неможливо видалити товар' in response.data['detail']
        # Товар залишився в базі
        assert Product.objects.filter(id=product_obj.id).exists()

    def test_total_auto_calculation(
            self, api_client, client_obj, product_obj
    ):
        """Сума розраховується автоматично."""
        url = reverse('order-list')
        data = {
            'client_id': client_obj.id,
            'items': [{'product_id': product_obj.id, 'quantity': 5}]
        }
        response = api_client.post(url, data, format='json')
        assert float(response.data['total_amount']) == 500.0


# ─── Зміна статусу замовлення (PATCH /api/orders/{id}/status/) ─────────────────────

@pytest.mark.django_db
class TestOrderStatusUpdate:

    def test_update_status_to_processing(self, api_client, client_obj, product_obj):
        """Створити замовлення та змінити статус на 'processing'."""
        order = Order.objects.create(client=client_obj)
        item = OrderItem(order=order, product=product_obj, quantity=1)
        item.save(skip_recalc=True)
        order.calculate_total()

        url = reverse('order-update-status', kwargs={'pk': order.pk})
        response = api_client.patch(url, {'status': 'processing'}, format='json')

        assert response.status_code == 200
        assert response.data['status'] == 'processing'

    def test_update_status_to_completed(self, api_client, client_obj, product_obj):
        """Змінити статус на 'completed'."""
        order = Order.objects.create(client=client_obj)
        item = OrderItem(order=order, product=product_obj, quantity=1)
        item.save(skip_recalc=True)
        order.calculate_total()
        order.status = 'processing'
        order.save()

        url = reverse('order-update-status', kwargs={'pk': order.pk})
        response = api_client.patch(url, {'status': 'completed'}, format='json')

        assert response.status_code == 200
        assert response.data['status'] == 'completed'

    def test_cannot_change_completed_order(self, api_client, client_obj, product_obj):
        """
        Бізнес-правило: завершене замовлення не можна змінювати.
        """
        order = Order.objects.create(client=client_obj, status='completed')
        item = OrderItem(order=order, product=product_obj, quantity=1)
        item.save(skip_recalc=True)
        order.calculate_total()

        url = reverse('order-update-status', kwargs={'pk': order.pk})
        response = api_client.patch(url, {'status': 'processing'}, format='json')

        assert response.status_code == 400
        assert 'Неможливо змінити статус завершеного замовлення' in str(response.data)

    def test_cannot_change_cancelled_order(self, api_client, client_obj, product_obj):
        """
        Бізнес-правило: скасоване замовлення не можна змінювати.
        """
        order = Order.objects.create(client=client_obj, status='cancelled')
        item = OrderItem(order=order, product=product_obj, quantity=1)
        item.save(skip_recalc=True)
        order.calculate_total()

        url = reverse('order-update-status', kwargs={'pk': order.pk})
        response = api_client.patch(url, {'status': 'processing'}, format='json')

        assert response.status_code == 400
        assert 'Скасоване замовлення не можна змінювати' in str(response.data)

    def test_cannot_revert_from_processing_to_new(self, api_client, client_obj, product_obj):
        """
        Бізнес-правило: не можна повернути з 'processing' до 'new'.
        """
        order = Order.objects.create(client=client_obj, status='processing')
        item = OrderItem(order=order, product=product_obj, quantity=1)
        item.save(skip_recalc=True)
        order.calculate_total()

        url = reverse('order-update-status', kwargs={'pk': order.pk})
        response = api_client.patch(url, {'status': 'new'}, format='json')

        assert response.status_code == 400
        assert 'Неможливо повернути замовлення зі статусу' in str(response.data)

    def test_invalid_status_value(self, api_client, client_obj, product_obj):
        """
        Перевірка, що недопустиме значення статусу відхиляється.
        """
        order = Order.objects.create(client=client_obj)
        item = OrderItem(order=order, product=product_obj, quantity=1)
        item.save(skip_recalc=True)
        order.calculate_total()

        url = reverse('order-update-status', kwargs={'pk': order.pk})
        response = api_client.patch(url, {'status': 'invalid_status'}, format='json')

        assert response.status_code == 400


# ─── Тести рівня моделі ───────────────────────────────────────────────────────

@pytest.mark.django_db
class TestOrderItemModel:
    """
    Тести що перевіряють OrderItem.clean() безпосередньо,
    в обхід серіалізатора та API.

    Навіщо потрібен окремий рівень:
    - Серіалізатор захищає тільки HTTP-вхід
    - clean() захищає від некоректних даних з будь-якого джерела:
      Django Admin, management команди, прямі виклики в тестах,
      майбутні інтеграції (імпорт з Excel, синхронізація тощо)
    - Без цього тесту можна видалити рядок у clean() і жоден
      з API-тестів не впаде — помилка залишиться непоміченою
    """

    def test_zero_quantity_raises_validation_error(
            self, client_obj, product_obj
    ):
        """
        full_clean() → clean() відхиляє quantity=0.

        Ключовий нюанс Django 5:
        PositiveIntegerField додає MinValueValidator(0), тобто нуль
        вважається допустимим на рівні поля і проходить clean_fields().
        Наш clean() — єдиний захист від quantity=0 на рівні моделі.

        Саме тому цей тест важливий: він покриває сценарій, який
        серіалізатор (min_value=1) блокує, а Django сам по собі — ні.
        """
        order = Order.objects.create(client=client_obj)
        item = OrderItem(
            order=order,
            product=product_obj,
            quantity=0,
            price=product_obj.price,  # фіксуємо ціну вручну (як при save())
            amount=0,                  # 0 * price
        )
        with pytest.raises(ValidationError) as exc_info:
            item.full_clean()

        # Перевіряємо що помилка прив'язана саме до поля quantity,
        # а не є загальною помилкою моделі
        assert 'quantity' in exc_info.value.message_dict

    def test_negative_quantity_raises_validation_error(
            self, client_obj, product_obj
    ):
        """
        full_clean() відхиляє від'ємну кількість.

        На відміну від quantity=0, від'ємне значення може бути
        перехоплено ще на рівні clean_fields() самим PositiveIntegerField.
        В обох випадках ValidationError гарантований — тест перевіряє
        загальну гарантію "будь-яке не-позитивне значення заборонено".
        """
        order = Order.objects.create(client=client_obj)
        item = OrderItem(
            order=order,
            product=product_obj,
            quantity=-5,
            price=product_obj.price,
            amount=0,
        )
        with pytest.raises(ValidationError):
            item.full_clean()


# ─── Health Check ─────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestHealthCheck:
    def test_health_endpoint(self, api_client):
        url = reverse('health-check')
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['status'] == 'ok'
        assert response.data['database'] == 'ok'