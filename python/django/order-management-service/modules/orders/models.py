# order-management-service/modules/orders/models.py

from django.db import models
from django.core.exceptions import ValidationError


class Client(models.Model):
    """
    Клієнт — юридична або фізична особа яка робить замовлення.
    В реальному ERP тут буде ще ЄДРПОУ, адреса, контакти тощо.
    Для тестового завдання — мінімально необхідний набір.
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Назва клієнта',
        help_text='Повна назва компанії або ПІБ'
    )
    email = models.EmailField(
        unique=True,  # два клієнти не можуть мати однаковий email
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,  # необов'язкове поле
        verbose_name='Телефон'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # встановлюється автоматично при створенні
        verbose_name='Дата створення'
    )

    class Meta:
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'
        ordering = ['-created_at']  # нові клієнти першими

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Товар або послуга.
    В реальному ERP тут буде артикул, одиниця виміру,
    категорія, залишки на складі тощо.
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Назва товару'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,  # ціна з копійками: 999.99
        verbose_name='Ціна'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Опис'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.price} грн)"

    def clean(self):
        """
        Валидация на уровне модели.
        Вызывается через full_clean() — из Django Admin автоматически,
        из DRF — вручную в сериализаторе.
        Держим здесь бизнес-правило чтобы оно работало
        независимо от того откуда создаётся объект.
        """
        if self.price is not None and self.price <= 0:
            raise ValidationError({'price': 'Ціна товару має бути більше нуля.'})


class Order(models.Model):
    """
    Замовлення — головна сутність модуля.

    Важливе архітектурне рішення: зв'язок з товарами йде через
    проміжну модель OrderItem (а не через ManyToManyField напряму).
    Чому? Тому що нам треба зберігати кількість і ціну на момент
    замовлення (ціна товару може змінитися, але в замовленні
    вона має залишитися зафіксованою).
    """

    class Status(models.TextChoices):
        """
        TextChoices — зручний спосіб задати enum для поля.
        Перший параметр — значення в БД, другий — відображення.
        """
        NEW = 'new', 'Нове'
        PROCESSING = 'processing', 'В обробці'
        COMPLETED = 'completed', 'Виконано'
        CANCELLED = 'cancelled', 'Скасовано'

    # ForeignKey — замовлення належить одному клієнту
    # on_delete=PROTECT — не дозволить видалити клієнта якщо є замовлення
    # Це важливе бізнес-правило для ERP: не можна випадково
    # видалити клієнта і втратити історію замовлень
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='orders',  # client.orders.all() — зручний доступ
        verbose_name='Клієнт'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='Статус'
    )
    # total_amount — зберігаємо в БД (денормалізація)
    # Чому не рахуємо щоразу? В ERP таблиці замовлень можуть
    # містити мільйони записів. Рахувати суму через JOIN кожен
    # раз при виборці — дорого. Зберігаємо і оновлюємо при змінах.
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Сума замовлення'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # оновлюється автоматично при кожному save()
        verbose_name='Дата оновлення'
    )

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f"Замовлення #{self.pk} — {self.client.name}"

    def calculate_total(self):
        """
        Рахує загальну суму замовлення на основі OrderItem.
        Викликається після будь-яких змін у позиціях.
        """
        from django.db.models import Sum
        result = self.items.aggregate(total=Sum('amount'))
        self.total_amount = result['total'] or 0
        self.save(update_fields=['total_amount'])


class OrderItem(models.Model):
    """
    Позиція замовлення — проміжна модель між Order і Product.

    Зберігає:
    - яке замовлення
    - який товар
    - кількість
    - ціну на момент замовлення (важливо!)
    - суму по позиції
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,  # видалення замовлення = видалення всіх позицій
        related_name='items',
        verbose_name='Замовлення'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,  # не можна видалити товар якщо він є в замовленнях
        related_name='order_items',
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Кількість'
    )
    # Фіксуємо ціну на момент замовлення
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Ціна на момент замовлення'
    )
    # Сума по позиції = quantity * price
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Сума по позиції'
    )

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        """
        Перевизначаємо save() щоб автоматично:
        1. Зафіксувати ціну товару на момент створення позиції
        2. Порахувати суму по позиції
        3. Перерахувати загальну суму замовлення
        """
        # Извлекаем наш кастомный параметр до вызова super()
        # (super().save() не знает про skip_recalc и выбросит ошибку)
        skip_recalc = kwargs.pop('skip_recalc', False)

        # Фиксируем цену товара если не задана явно
        if self.price is None:
            self.price = self.product.price

        # Считаем сумму по позиции
        self.amount = self.quantity * self.price

        super().save(*args, **kwargs)

        # Пересчитываем общую сумму заказа если не попросили пропустить
        if not skip_recalc:
            self.order.calculate_total()

    def clean(self):
        if self.quantity is not None and self.quantity <= 0:
            raise ValidationError({'quantity': 'Кількість має бути більше нуля.'})