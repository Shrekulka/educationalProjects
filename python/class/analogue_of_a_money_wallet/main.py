"""Реализуйте класс Wallet, аналог денежного кошелька, содержащий информацию о валюте и остатке имеющихся средств на
счете. В данном классе должны быть реализованы:
• метод _init_, который создает атрибуты currency и balance. Значения атрибутов currency и balance поступают при вызове
  метода _init_. При этом значение атрибута currency должно быть строкой, состоящей только из трех заглавных букв. Для
  этого необходимо сделать именно в такой последовательности следующие проверки
• В случае, если передается не строка, нужно возбуждать исключение ТуреЕrror с текстом "Неверный тип валюты":
• В случае, если передается строка, длина которой не равна трем символам, нужно возбуждать исключение NameError с
  текстом "Неверная длина названия валюты"
• В случае, если строка из трех символов состоит из незаглавных букв, нужно возбуждать исключение ValueError с текстом
  "Название должно состоять только из заглавных букв"
• метод _eq_ для возможности сравнивания балансов кошельков. Операция сравнения доступна только для кошельков с
  одинаковой валютой. Если валюты различаются, необходимо возбудить исключение ValueError с текстом "Нельзя сравнить
  разные валюты". При попытке сравнить экземпляр класса Wallet с другими объектами необходимо возбудить исключение
  ТуреЕrror с текстом "Wallet не поддерживает сравнение с «объектом»";
• методы _add_ и _sub_ для возможности суммирования и вычитания кошельков. Складывать и вычитать мы можем только с
  другим экземпляром класса Wallet и только в случае, когда у них совпадает валюта (атрибуты currency). Результатом
  такого сложения должен быть новый экземпляр класса Wallet, у которого валюта совпадает с валютой операндов и значение
  баланса равно сумме/вычитанию их балансов. Если попытаются сложить с объектом не являющимся экземпляром Wallet или
  значения валют у объектов не совпадают, необходимо возбудить исключение ValueError с текстом "Данная операция запрещена"

wallet1 = Wallet ('USD', 50)
wallet2 = Wallet('UAH', 100)
wallet3 = Wallet ('UAH', 150)
wallet4 = Wallet (12, 150) # исключение ТуреЕrror( 'Неверный тип валюты")
wallet5 = Wallet('qwerty', 150) # исключение NameError ('Неверная длина названия валюты")
wallet6 = Wallet ('abc', 150) # исключение ValueError ('Название должно состоять только из заглавных букв')
print (wallet2 == wallet3) # False
print (wallet2 == 100) # TypeError ('Wallet не поддерживает сравнение с 100")
print (wallet2 == wallet1) # ValueError ('Нельзя сравнить разные валюты")
wallet7 = wallet2 + wallet3
print (wallet7.currency, wallet7.balance) #печатает 'UAH 250'
wallet2 + 45 # ValueError ("Данная операция запрещена")
"""


# Решение №1

########################################################################################################################
# Определяем класс Wallet
class Wallet:
    # Конструктор класса, принимает валюту и баланс
    def __init__(self, currency, balance):
        # Проверяем тип валюты, должен быть строкой
        if not isinstance(currency, str):
            raise TypeError("Неверный тип валют")
        # Проверяем длину названия валюты, должна быть равна 3
        if not len(currency) == 3:
            raise NameError("Неверная длина названия валюты")
        # Проверяем, что название валюты состоит только из заглавных букв
        if not all(i.isupper() for i in currency):  # или if not currency.isupper(): - проверка всей строки
            raise ValueError("Название должно состоять только из заглавных букв")
        # Инициализируем атрибуты currency и balance
        self.currency = currency
        self.balance = balance

    # Переопределение метода сравнения ==
    def __eq__(self, other):
        # Проверяем, что other также является экземпляром класса Wallet
        if not isinstance(other, Wallet):
            raise TypeError(f"Wallet не поддерживает сравнение с {type(other).__name__}")
        # Проверяем, что валюты у объектов совпадают
        if not self.currency == other.currency:
            raise ValueError("Нельзя сравнить разные валюты")
        # Сравниваем балансы объектов
        return self.balance == other.balance

    # Переопределение метода сравнения >
    def __gt__(self, other):
        # Проверяем, что other также является экземпляром класса Wallet
        if not isinstance(other, Wallet):
            raise TypeError(f"Wallet не поддерживает сравнение с {type(other).__name__}")
        # Проверяем, что валюты у объектов совпадают
        if not self.currency == other.currency:
            raise ValueError("Нельзя сравнивать разные валюты")
        # Сравниваем балансы объектов
        return self.balance > other.balance

    # Переопределение метода сложения +
    def __add__(self, other):
        # Проверяем, что other также является экземпляром класса Wallet
        if not isinstance(other, Wallet):
            raise TypeError(f"Wallet не поддерживает сложение с {type(other).__name__}")
        # Проверяем, что валюты у объектов совпадают
        if not self.currency == other.currency:
            raise ValueError("Нельзя складывать разные валюты")
        # Создаем и возвращаем новый объект Wallet с суммой балансов
        return Wallet(self.currency, self.balance + other.balance)

    # Переопределение метода вычитания -
    def __sub__(self, other):
        # Проверяем, что other также является экземпляром класса Wallet
        if not isinstance(other, Wallet):
            raise TypeError(f"Wallet не поддерживает вычитание с {type(other).__name__}")
        # Проверяем, что валюты у объектов совпадают
        if not self.currency == other.currency:
            raise ValueError("Нельзя вычитать разные валюты")
        # Проверяем, что на балансе достаточно средств для вычитания
        if self.balance < other.balance:
            print(f"Невозможно выполнить вычитание, так как недостаточно {self.currency} на балансе")
        # Создаем и возвращаем новый объект Wallet с разностью балансов
        return Wallet(self.currency, self.balance - other.balance)


# Решение №2

########################################################################################################################
# Определяем класс ImprovedWallet
class ImprovedWallet:
    # Конструктор класса, принимает валюту и баланс
    def __init__(self, currency, balance):
        # Проверяем валюту с помощью статического метода check_currency
        self.check_currency(currency)
        # Инициализируем атрибуты currency и balance
        self.currency = currency
        self.balance = balance

    # Статический метод для проверки валюты
    @staticmethod
    def check_currency(currency):
        # Проверяем тип валюты, должен быть строкой
        if not isinstance(currency, str):
            raise TypeError("Неверный тип валют")
        # Проверяем длину названия валюты, должна быть равна 3
        if not len(currency) == 3:
            raise NameError("Неверная длина названия валюты")
        # Проверяем, что название валюты состоит только из заглавных букв
        if not all(i.isupper() for i in currency):  # или if not currency.isupper(): - проверка всей строки
            raise ValueError("Название должно состоять только из заглавных букв")

    # Метод для проверки объекта other перед выполнением операций
    def check_wallet(self, other):
        # Проверяем, что other также является экземпляром класса ImprovedWallet
        if not isinstance(other, ImprovedWallet):
            raise TypeError(f"Wallet не поддерживает операцию с {type(other).__name__}")
        # Проверяем, что валюты у объектов совпадают
        if not self.currency == other.currency:
            raise ValueError("Нельзя выполнить операцию для разных валют")

    # Переопределение метода сравнения ==
    def __eq__(self, other):
        # Проверяем объект other
        self.check_wallet(other)
        # Сравниваем балансы объектов
        return self.balance == other.balance

    # Переопределение метода сравнения >
    def __gt__(self, other):
        # Проверяем объект other
        self.check_wallet(other)
        # Сравниваем балансы объектов
        return self.balance > other.balance

    # Переопределение метода сложения +
    def __add__(self, other):
        # Проверяем объект other
        self.check_wallet(other)
        # Создаем и возвращаем новый объект ImprovedWallet с суммой балансов
        return ImprovedWallet(self.currency, self.balance + other.balance)

    # Переопределение метода вычитания -
    def __sub__(self, other):
        # Проверяем объект other
        self.check_wallet(other)
        # Проверяем, что на балансе достаточно средств для вычитания
        if self.balance < other.balance:
            print(f"Невозможно выполнить вычитание, так как недостаточно {self.currency} на балансе")
        # Создаем и возвращаем новый объект ImprovedWallet с разностью балансов
        return ImprovedWallet(self.currency, self.balance - other.balance)


########################################################################################################################

wallet1 = Wallet('USD', 50)
wallet2 = Wallet('UAH', 100)
wallet3 = Wallet('UAH', 150)
# wallet4 = Wallet(12, 150)  # исключение ТуреЕггог( 'Неверный тип валюты")
# wallet5 = Wallet('qwerty', 150) # исключение NameError ('Неверная длина названия валюты")
# wallet6 = Wallet ('abc', 150) # исключение ValueError ('Название должно состоять только из заглавных букв')
print(wallet2 == wallet3)  # False
# print(wallet2 == 100)  # TypeError ('Wallet не поддерживает сравнение с 100")
# print (wallet2 == wallet1) # ValueError ('Нельзя сравнить разные валюты")
wallet7 = wallet2 + wallet3
print(wallet7.currency, wallet7.balance)  # печатает 'UAH 250'
# wallet2 + 45  # ValueError ('Данная операция запрещена")

# Создание объекта Wallet с корректными параметрами

w = Wallet("USD", 100)
assert w.currency == "USD"
assert w.balance == 100

# Создание объекта Wallet с некорректным типом валюты

try:
    w = Wallet(100, 100)
except TypeError as e:
    assert str(e) == "Неверный тип валют"

# Создание объекта Wallet с некорректной длиной названия валюты

try:
    w = Wallet("US", 100)
except NameError as e:
    assert str(e) == "Неверная длина названия валюты"

# Создание объекта Wallet с некорректным названием валюты

try:
    w = Wallet("usd", 100)
except ValueError as e:
    assert str(e) == "Название должно состоять только из заглавных букв"

# Сравнение двух объектов Wallet с разными валютами

try:
    w1 = Wallet("USD", 100)
    w2 = Wallet("EUR", 100)
    w1 == w2
except ValueError as e:
    assert str(e) == "Нельзя сравнить разные валюты"

# Сравнение двух объектов Wallet с одинаковыми валютами и одинаковым балансом

w1 = Wallet("USD", 100)
w2 = Wallet("USD", 100)
assert w1 == w2

# Сравнение двух объектов Wallet с одинаковыми валютами и разным балансом

w1 = Wallet("USD", 100)
w2 = Wallet("USD", 200)
assert w2 > w1

# Сложение двух объектов Wallet с разными валютами

try:
    w1 = Wallet("USD", 100)
    w2 = Wallet("EUR", 100)
    w1 + w2
except ValueError as e:
    assert str(e) == "Нельзя складывать разные валюты"

# Сложение двух объектов Wallet с одинаковыми валютами

w1 = Wallet("USD", 100)
w2 = Wallet("USD", 200)
w3 = w1 + w2
assert w3.currency == "USD"
assert w3.balance == 300

# Вычитание двух объектов Wallet с разными валютами

try:
    w1 = Wallet("USD", 100)
    w2 = Wallet("EUR", 100)
    w1 - w2
except ValueError as e:
    assert str(e) == "Нельзя вычитать разные валюты"

# Вычитание двух объектов Wallet с одинаковыми валютами и одинаковым балансом:

w1 = Wallet("USD", 100)
w2 = Wallet("USD", 100)
w3 = w1 - w2
assert w3.currency == "USD"
assert w3.balance == 0

# Вычитание двух объектов Wallet с одинаковыми валютами и разным балансом, где результат вычитания положительный:

w1 = Wallet("USD", 100)
w2 = Wallet("USD", 50)
w3 = w1 - w2
assert w3.currency == "USD"
assert w3.balance == 50

# Вычитание двух объектов Wallet с одинаковыми валютами и разным балансом, где результат вычитания отрицательный:

w1 = Wallet("USD", 50)
w2 = Wallet("USD", 100)
try:
    w3 = w1 - w2
except ValueError as e:
    assert str(e) == "Недостаточно средств на счете"
