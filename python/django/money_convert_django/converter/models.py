# money_convert_django/converter/models.py

import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class ConversionHistory(models.Model):
    """
        Модель для хранения истории конверсий валют.

        Поля:
            from_currency (str): Код валюты, из которой производится конвертация (максимальная длина - 3 символа).
            to_currency (str): Код валюты, в которую производится конвертация (максимальная длина - 3 символа).
            amount (Decimal): Сумма, которая конвертируется. Должна быть положительным числом с максимумом 10 знаков,
                              из которых 2 знака после запятой.
            converted_amount (Decimal): Результат конвертации. Максимум 10 знаков, из которых 2 знака после запятой.
            conversion_date (datetime): Дата и время выполнения конвертации. Устанавливается автоматически при создании
                                        записи.

        Методы:
            __str__(): Возвращает строковое представление объекта конверсии, показывающее сумму и валюты.
    """

    # Код валюты, из которой производится конвертация (например, 'USD')
    from_currency: str = models.CharField(max_length=3)

    # Код валюты, в которую производится конвертация (например, 'EUR')
    to_currency: str = models.CharField(max_length=3)

    # Сумма для конвертации, максимум 10 знаков с 2 знаками после запятой, значение должно быть не менее 0.01
    amount: Decimal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    # Результат конвертации, максимум 10 знаков с 2 знаками после запятой
    converted_amount: Decimal = models.DecimalField(max_digits=10, decimal_places=2)

    # Дата и время выполнения конвертации, автоматически устанавливается при создании записи
    conversion_date: datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
            Возвращает строковое представление объекта конверсии.

            Returns:
                str: Строковое представление объекта в формате "{amount} {from_currency} to {converted_amount}
                {to_currency}".
        """
        # Форматируем строку, показывающую сумму и валюты
        return f"{self.amount} {self.from_currency} to {self.converted_amount} {self.to_currency}"

    class Meta:
        """
            Метаданные для модели ConversionHistory.

            Атрибуты:
                indexes (List[models.Index]): Список индексов для ускорения поиска по полям 'from_currency',
                'to_currency' и 'conversion_date'.
        """
        # Список индексов для ускорения поиска по полям 'from_currency', 'to_currency' и 'conversion_date'
        indexes = [
            models.Index(fields=['from_currency', 'to_currency', 'conversion_date']),
        ]
