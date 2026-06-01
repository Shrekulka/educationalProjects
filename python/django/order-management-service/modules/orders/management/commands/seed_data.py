# order-management-service/modules/orders/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from modules.orders.models import Client, Product, Order, OrderItem


class Command(BaseCommand):
    """
    Management команда для наполнения БД тестовыми данными.

    Зачем это нужно:
    - Новый разработчик клонирует репо и за 1 команду имеет
      рабочую базу с данными для разработки
    - Можно быстро сбросить и перенаполнить базу
    - Демонстрирует знание инструментария Django

    Запуск:
        python manage.py seed_data
        docker-compose exec web python manage.py seed_data
    """

    help = 'Наповнює базу даних тестовими даними для розробки'

    def handle(self, *args, **options):
        self.stdout.write('Створення тестових даних...')

        # Клиенты
        clients_data = [
            {'name': 'ТОВ Альфа Технології', 'email': 'alpha@tech.ua', 'phone': '+380441234567'},
            {'name': 'ФОП Петренко Іван', 'email': 'petrenko@fop.ua', 'phone': '+380501234567'},
            {'name': 'ТОВ Бета Трейд', 'email': 'beta@trade.ua', 'phone': '+380671234567'},
        ]
        clients = []
        for data in clients_data:
            client, created = Client.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            clients.append(client)
            status = 'створено' if created else 'вже існує'
            self.stdout.write(f'  Клієнт "{client.name}" — {status}')

        # Товары
        products_data = [
            {'name': 'Ноутбук Dell Latitude', 'price': 45000.00, 'description': 'Бізнес ноутбук'},
            {'name': 'Миша бездротова Logitech', 'price': 1200.00, 'description': 'Офісна миша'},
            {'name': 'Клавіатура механічна', 'price': 2800.00, 'description': 'Механічна клавіатура'},
            {'name': 'Монітор 27" IPS', 'price': 18000.00, 'description': 'Офісний монітор'},
            {'name': 'Ліцензія Microsoft Office', 'price': 5500.00, 'description': 'Річна ліцензія'},
        ]
        products = []
        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            products.append(product)
            status = 'створено' if created else 'вже існує'
            self.stdout.write(f'  Товар "{product.name}" — {status}')

        # Заказы
        from django.db import transaction

        if Order.objects.exists():
            self.stdout.write('  Замовлення вже існують — пропускаємо.')
        else:
            orders_to_create = [
                {
                    'client': clients[0],
                    'items': [
                        (products[0], 2),  # 2 ноутбука
                        (products[1], 2),  # 2 мышки
                    ]
                },
                {
                    'client': clients[1],
                    'items': [
                        (products[4], 1),  # 1 лицензия Office
                    ]
                },
                {
                    'client': clients[2],
                    'items': [
                        (products[2], 5),  # 5 клавиатур
                        (products[3], 3),  # 3 монитора
                    ]
                },
            ]

            for order_data in orders_to_create:
                with transaction.atomic():
                    order = Order.objects.create(client=order_data['client'])
                    for product, quantity in order_data['items']:
                        item = OrderItem(
                            order=order,
                            product=product,
                            quantity=quantity
                        )
                        item.save(skip_recalc=True)
                    order.calculate_total()
                    self.stdout.write(
                        f'  Замовлення #{order.pk} для "{order.client.name}" '
                        f'— сума {order.total_amount} грн'
                    )

        self.stdout.write(
            self.style.SUCCESS(
                '\nГотово! Тестові дані створено успішно.'
            )
        )