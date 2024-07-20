# money_convert_django/converter/forms.py

from decimal import Decimal, InvalidOperation

from django import forms


class CurrencyConverterForm(forms.Form):
    """
        Форма для конвертации валют.

        Поля:
            from_amount (CharField): Поле для ввода суммы, которую нужно конвертировать.
                - max_length (int): Максимальная длина строки (20 символов).
                - widget (TextInput): Внешний вид поля, с CSS классом 'form-control' и подсказкой 'Введите количество
                  монеток'.

            from_curr (ChoiceField): Поле для выбора исходной валюты.
                - choices (list): Список валют, задается динамически.
                - widget (Select): Внешний вид поля, с CSS классом 'form-control'.

            to_curr (ChoiceField): Поле для выбора целевой валюты.
                - choices (list): Список валют, задается динамически.
                - widget (Select): Внешний вид поля, с CSS классом 'form-control'.

        Методы:
            __init__(self, *args, **kwargs): Инициализация формы с динамическим заполнением списка валют.
                - currencies (dict): Словарь валют, передается через kwargs и используется для заполнения списка выбора
                  валют.

            clean_from_amount(self): Проверка корректности введенной суммы.
                - Возвращает (Decimal): Проверенная и преобразованная сумма.
                - Исключения:
                    - ValidationError: Если введенная сумма некорректна, отрицательная или превышает 1,000,000.

            clean(self): Дополнительная проверка полей формы.
                - Возвращает (dict): Очищенные данные формы.
                - Исключения:
                    - ValidationError: Если исходная и целевая валюты совпадают.
    """
    # Поле для ввода суммы, которую нужно конвертировать
    from_amount = forms.CharField(
        max_length=20,  # Максимальная длина строки
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите количество монеток'})
        # Внешний вид поля
    )

    # Поле для выбора исходной валюты
    from_curr = forms.ChoiceField(
        choices=[],  # Список валют будет задаваться динамически
        widget=forms.Select(attrs={'class': 'form-control'})  # Внешний вид поля
    )

    # Поле для выбора целевой валюты
    to_curr = forms.ChoiceField(
        choices=[],  # Список валют будет задаваться динамически
        widget=forms.Select(attrs={'class': 'form-control'})  # Внешний вид поля
    )

    def __init__(self, *args, **kwargs):
        """
           Инициализация формы с динамическим заполнением списка валют.

           Аргументы:
               args: Позиционные аргументы, передаваемые в базовый класс формы.
               kwargs: Именованные аргументы, включая 'currencies' для динамического заполнения списка выбора валют.
                   - currencies (dict): Словарь валют, ключи которого используются для заполнения полей from_curr и
                     to_curr.
        """
        # Извлекаем список валют из переданных аргументов
        currencies = kwargs.pop('currencies', {})

        # Вызов конструктора родительского класса
        super().__init__(*args, **kwargs)

        # Создаем список выбора валют на основе переданных данных
        currency_choices = [(currency, currency) for currency in currencies.keys()]

        # Задаем список выбора для полей from_curr и to_curr
        self.fields['from_curr'].choices = currency_choices
        self.fields['to_curr'].choices = currency_choices

    def clean_from_amount(self) -> Decimal:
        """
            Проверка корректности введенной суммы.

            Возвращает:
                Decimal: Проверенная и преобразованная сумма.

            Исключения:
                ValidationError: Если введенная сумма некорректна, отрицательная или превышает 1,000,000.
        """
        # Извлекаем введенную сумму
        amount = self.cleaned_data['from_amount']

        # Заменяем запятую на точку для корректного преобразования в Decimal
        amount = amount.replace(',', '.')

        try:
            # Преобразуем строку в Decimal
            amount = Decimal(amount)
        except InvalidOperation:
            # Если преобразование не удалось, вызываем ошибку валидации
            raise forms.ValidationError("Пожалуйста, введите корректное число.")

        # Проверка, что сумма положительная
        if amount <= 0:
            raise forms.ValidationError("Сумма должна быть положительным числом.")

        # Проверка, что сумма не превышает 1,000,000
        if amount > Decimal('1000000'):
            raise forms.ValidationError("Сумма не должна превышать 1,000,000.")

        return amount

    def clean(self) -> dict:
        """
            Дополнительная проверка полей формы.

            Возвращает:
                dict: Очищенные данные формы.

            Исключения:
                ValidationError: Если исходная и целевая валюты совпадают.
        """
        # Вызов метода clean() родительского класса для стандартной очистки данных
        cleaned_data = super().clean()

        # Извлекаем значения полей from_curr и to_curr
        from_curr = cleaned_data.get('from_curr')
        to_curr = cleaned_data.get('to_curr')

        # Проверяем, что выбраны разные валюты для конвертации
        if from_curr == to_curr:
            raise forms.ValidationError("Выберите разные валюты для конвертации.")

        return cleaned_data
