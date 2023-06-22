In this task we will have one parent class Transport and three child classes (Car, Boat, Plane).

The Transport class should implement:
- The _init_ method, which creates the attributes brand, max_speed and kind. The values of attributes brand, max_speed,
  kind attributes are called using the _init_ method; in this case, the value of the kind is optional and defaults to
  value is None;
- method _str_ which will return a format string: "Type of transport <kind> brand <brand> can reach
  speed <max speed> km/h".

The Sag class must implement:
- _init_ method, which creates the attributes brand, max_speed, mileage and the private attribute gasoline_residue from 
  the instance. All values of these attributes are passed when the Sag class is called. Within the initialization, 
  delegate the creation of attributes brand, max_speed, kind to the parent Transport class, and pass the value "Sag" to 
  the kind attribute;
- getter property gasoline which will return the string: "Gasoline remaining for <gasoline_residue> km";
- the getter property gasoline, which shall take ONLY an integer value, increases the
  gasoline_residue by passed value and then output phrase 'Fuel volume increased by <value> l and is <gasoline_residue> 
  l'. If the value of value is not an integer, print 'Vehicle refueling error'.

The following must be implemented in the Boat class:
- _init_ method which creates the attributes brand, max_speed, kind, owners_name from the instance. All values of these 
  attributes
  are passed on when the Boat class is called. Inside the initialization delegate the creation of the attributes brand,
  max_speed, kind to the parent Transport class, and pass the value "Boat" to the kind attribute;
- the _str_ method which will return a string: 'This boat brand <brand> is owned by <owners_name>'.

The Plane class must implement:
- _init_ method that creates brand, max_speed, capacity attributes from the instance. Inside of the initialization 
  delegate creation of the brand, max_speed and kind attributes to the Transport parent class with the attribute with 
  the value "Plane";
- the _str_ method which will return a string: 'Plane brand <brand> holds <capacity> people'.

```python

transport = Transport('Telega', 10)

print(transport) # Transport type None of the Telega brand can reach speeds of 10km/h



bike = Transport('Shkolnik', 20, 'bike')

print(bike) # The bike of the Shkolnik brand can reach 28 km/h



first_plane = Plane ('Virgin Atlantic', 700, 450)

print(first_plane) # Virgin Atlantic plane can hold 450 people



first_car = Car('BMW', 230, 75000, 300)

print(first_car) # BMW Car can do 230

print(first_car.gasoline) # We have enough gasoline for 300km



first_car.gasoline = 20 # print(first_car.gasoline) "Fuel volume increased by 20l, it is 320l

print(first_car.gasoline) # 320 km of petrol left



second_car = Car('Audi', 230, 70000, 130)

second_car.gasoline - [None] # Prints 'Car filling error'.

first_boat = Boat('Yamaha', 40, 'Petr')

print(first_boat) # This Yamaha boat is owned by Petr
```





В этой задаче у нас будет один родительский класс Transport и три дочерних класса (Car, Boat, Plane).

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

```python
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
```