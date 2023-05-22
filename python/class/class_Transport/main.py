"""В этой задаче у нас будет один родительский класс Transport и три дочерних класса (Car, Boat, Plane).

В классе Transport должны быть реализованы:
•	метод _init_, который создает атрибуты brand, max_speed и kind. Значения атрибутов brand, max_speed, kind
    поступают при вызове метода _init 	При этом значение kind не является обязательным и по умолчанию имеет
значение None;
•	метод _str_ который будет возвращать строку формата: "Тип транспорта <kind> марки <brand> может развить
    скорость <максимальная скорость> км/ч".

В классе Саг должны быть реализованы:
•	метод _init_, создающий у экземпляра атрибуты brand, max_speed, mileage и приватный атрибут gasoline_residue.
    Все значения этих атрибутов передаются при вызове класса Саr. Внутри инициализации делегируйте создание
    атрибутов brand, max_speed, kind родительскому классу Transport, при этом атрибуту kind передайте значение "Саг";
•	свойство-геттер gasoline, который будет возвращать строку: "Осталось бензина на <gasoline_residue> км";
•	свойство-сеттер gasoline, которое должно принимать ТОЛЬКО целое число value, увеличивает уровень топлива
    gasoline_residue на переданное значение и затем вывести фразу 'Объем топлива увеличен на <value> л и составляет
    <gasoline_residue> л'. Если в значение value подается не целое число, вывести 'Ошибка заправки автомобиля'.

В классе Boat должны быть реализованы:
•	метод _init_ создающий у экземпляра атрибуты brand, max_speed, kind, owners_name. Все значения этих атрибутов
    передаются при вызове класса Boat. Внутри инициализации делегируйте создание атрибутов brand, max_speed, kind
    родительскому классу Transport, при этом атрибуту kind передайте значение "Boat";
•	метод _str_ который будет возвращать строку: 'Этой лодкой марки <brand> владеет <owners_name>'.

В классе Plane должны быть реализованы:
•	метод _init_ создающий у экземпляра атрибуты brand, max_speed, capacity. Внутри инициализации делегируйте
    создание атрибутов brand, max_speed, kind родительскому классу Transport, при этом атрибуту kind передайте
    значение "Plane";
•	метод _str_ который будет возвращать строку: 'Самолет марки <brand> вмещает в себя <capacity> людей'.

transport = Transport('Telega', 10)
print(transport) # Тип транспорта None марки Telega может развить скорость 10 км/ч
bike = Transport('Shkolnik', 20, 'bike')
print(bike) # Тип транспорта bike марки Shkolnik может развить скорость 28 км/ч
first_plane = Plane ('Virgin Atlantic', 700, 450)
print(first_plane) # Самолет марки Virgin Atlantic вмещает в себя 450 людей
first_car = Car('BMW', 230, 75000, 300)
print(first_car) # Тип транспорта Car марки BMW может развить скорость 230 км/ч
print(first_car.gasoline) # сталось бензина на 300 км
first_car.gasoline = 20 # Печатает 'Объем топлива увеличен на 20 л и составляет 320 л'
print(first_car.gasoline) # Осталось бензина на 320 км
second_car = Car('Audi', 230, 70000, 130)
second_car.gasoline - [None] # Печатает 'Ошибка заправки автомобиля'
first_boat = Boat('Yamaha', 40, 'Petr')
print(first_boat) # Этой лодкой марки Yamaha владеет Petr
"""


########################################################################################################################
# Объявление класса Transport.
class Transport:
    # Инициализация объекта класса Transport с атрибутами brand, max_speed и необязательным атрибутом kind.
    def __init__(self, brand, max_speed, kind=None):
        self.brand = brand
        self.max_speed = max_speed
        self.kind = kind

    # Метод __str__, который возвращает строковое представление объекта класса Transport.
    def __str__(self):
        return f"Тип транспорта {self.kind} марки {self.brand} может развить скорость {self.max_speed} км/ч"


# Объявление класса Car, который наследуется от класса Transport.
class Car(Transport):
    # Инициализация объекта класса Car с атрибутами brand, max_speed, mileage и __gasoline_residue.
    def __init__(self, brand, max_speed, mileage, __gasoline_residue):
        # Вызов конструктора родительского класса Transport с помощью метода super().
        super().__init__(brand, max_speed, kind="Car")  # Инициализация атрибута kind класса Car значением "Car".
        self.mileage = mileage
        self.__gasoline_residue = __gasoline_residue

    @property
    # Объявление свойства gasoline, которое возвращает строку с информацией об остатке бензина.
    def gasoline(self):
        return f"Осталось бензина на {self.__gasoline_residue} км"

    @gasoline.setter
    # Объявление сеттера gasoline, который позволяет установить значение остатка бензина.
    def gasoline(self, value):
        # Проверка типа и значения входного аргумента value с помощью условия и возбуждение исключения ValueError в
        # случае ошибки.
        if not isinstance(value, int) or value < 0:
            raise ValueError("Ошибка заправки автомобиля")
        # Увеличение значения приватного атрибута __gasoline_residue на значение value.
        self.__gasoline_residue += value
        # Вывод информации о новом объеме топлива.
        print(f"Объем топлива увеличен на {value} л и состовляет {self.__gasoline_residue} л")


# Объявление класса Boat, который наследуется от класса Transport.
class Boat(Transport):
    # Инициализация объекта класса Boat с атрибутами brand, max_speed и owners_name.
    def __init__(self, brand, max_speed, owners_name):
        # Вызов конструктора родительского класса Transport с помощью метода super().
        super().__init__(brand, max_speed, kind="Boat")  # Инициализация атрибута kind класса Boat значением "Boat".
        self.owners_name = owners_name

    # Переопределение метода __str__, который возвращает строку с информацией о владельце лодки.
    def __str__(self):
        return f"Этой лодкой марки {self.brand} владеее {self.owners_name}"


# Объявление класса Plane, который наследуется от класса Transport.
class Plane(Transport):
    # Инициализация объекта класса Plane с атрибутами brand, max_speed и capacity.
    def __init__(self, brand, max_speed, capacity):
        # Вызов конструктора родительского класса Transport с помощью метода super().
        super().__init__(brand, max_speed, kind="Plane")  # Инициализация атрибута kind класса Plane значением "Plane".
        self.capacity = capacity

    # Переопределение метода __str__, который возвращает строку с информацией о вместимости самолета.
    def __str__(self):
        return f"Самолет марки {self.brand} вмещает в себя {self.capacity} людей"


########################################################################################################################

transport = Transport("Telega", 10)
print(transport)  # Тип транспорта None марки Telega может развить скорость 10 км/ч

bike = Transport("shkolnik", 20, "bike")
print(bike)  # Тип транспорта bike марки shkolnik может развить скорость 20 км/ч

first_plane = Plane("Virgin Atlantic", 700, 450)
print(first_plane)  # Самолет марки Virgin Atlantic вмещает в себя 450 людей

first_car = Car("BMW", 230, 75000, 300)
print(first_car)  # Тип транспорта Car марки BMW может развить скорость 230 км/ч

print(first_car.gasoline)  # Осталось бензина на 300 км
first_car.gasoline = 20  # Объем топлива увеличен на 20 л и составляет 320 л
print(first_car.gasoline)  # Осталось бензина на 320 км

second_car = Car("Audi", 230, 70000, 130)
# second_car.gasoline = [None] # ValueError: Ошибка заправки автомобиля

first_boat = Boat("Yamaha", 40, "Peter")
print(first_boat)  # Этой лодкой марки Yamaha владеее Peter
