Let's imagine that in 2020, a survey was conducted in Dnipro to find out which class people identify themselves with. 
According to the results of the survey divided all the people into sweet eaters, vegetarians and meat eaters.

Let's write a programme to help us summarise the results of the survey. In order to create the programme, the following 
are needed:

1.	Create a parent class Initialization, which consists of:
- an initialization method that receives the following arguments: capacity - an integer, food - a list of string names of
  food. If capacity is not an integer, print "Number of people must be an integer" and do not create attributes capacity
  and food for these instances.

2.	Create a child class Vegetarian from Initialization class, which consists of:
- Initialization method that accepts the arguments capacity, food. We need to create attributes with the same name by 
  calling parent method _init
- method _str_, which returns string with format "<capacity> people prefer not to eat meat! They prefer <food>."

3.	Create a child class MeatEater from the Initialization class, which consists of:
- Initialization method accepting arguments capacity, food. We need to create attributes of the same name by calling
  parent method _init_.
- method _str_, which returns the string format "<capacity> meat-eaters in Dnepr! In addition to meat they also eat <food>".
4.	Create a child class SweetTooth from Initialization class, which consists of:
- Initialization method, accepting arguments capacity, food. We need to create attributes with the same name by calling
  the _init_ parent method.
- The magic _str_ method, which returns a string with the format "SweetTooth in Dnieper <capacity>. Their most favourite
  food: <food>"
- magic method _eq_, which will allow us to compare instances of the SweetTooth class with numbers and our other classes.
  If the comparison is to an integer and the attribute capacity matches it, you must return True, otherwise it returns 
  False. If we do the comparison with our other class (Vegetarian or MeatEater) and the of the capacity attributes are 
  equal, we return True, otherwise - False. And if it's compared to another data type data type, return "Can't compare 
  sweetener quantity to <value>".
- of the magic _lt_ method. If the comparison is to an integer and the number of sweetbreads (attribute capacity) is 
  less than, return True, otherwise return False. If the comparison is made with an instance of one of our classes
  Vegetarian or MeatEater and the sweetener is less, return True, otherwise return False. In case of the comparison goes
  with the rest of the data types, return "Can't compare the number of sweeteners to "value"".
- magic _gt_ method. If the comparison is with an integer and the number of sweetbreads is higher, return True, 
  otherwise False. If the comparison takes place with our other class Vegetarian or MeatEater and the number of sweet 
  eaters is greater, then return True, otherwise - False. In case the comparison is with other data types, return "Can't
  compare number of sweetbreads to 'value'".
```python
v_first = Vegetarian(10000, ['Nuts', 'vegetables', 'fruit'])

print(v_first) # 10000 people prefer not to eat meat! They prefer ['Nuts', 'Vegetables', 'Fruits']

v_second - Vegetarian([23], ['nothing']) # The number of people should be an integer
                              
m_first - MeatEater(15900, ['chips', 'fish'])
                              
print(m_first) # 15000 meat-eaters in Dnipro! Besides meat they eat ['fried potatoes', 'fish'] as well.
                              
s_first = SweetTooth(30000, ['Ice Cream,' 'Chips,' 'CHOCOLAD'])
                             
print(s_first) # SweetTooth in Dnieper is 30000. Their favourite food is ['Ice-cream', 'Chips', 'CHOCOLAD'].
                             
print(s_first > v_first) # True
                             
print(30000 == s_first) # True
                             
print(s_first == 25000) # False
                             
print(100000 < s_first) # False
                             
print(100 < s_first) # True
```



Давайте представим, что в 2020 году в Днепре проводили опрос и выявили, к какому классу люди себя относят. По
результатам опроса все люди разделились на сладкоежек, вегетарианцев и любителей мяса.

Давайте напишем программу, которая поможет нам подвести итоги опроса. Для создания программы нужно:

1.	Создать родительский класс Initialization, который состоит из:
•	метода инициализации, в который поступают аргументы: capacity - целое число, food - список из строковых названий
    еды. Если в значение capacity передаётся не целое число, вывести надпись "Количество людей должно быть целым числом"
    и не создавать для таких экземпляров атрибуты capacity и food.

2.	Создать дочерний класс Vegetarian от класса Initialization, который состоит из:
•	метода инициализации, принимающего аргументы capacity, food. Нужно создать одноименные атрибуты через вызов
    родительского метода _init
•	метода _str_, который возвращает строку формата "<capacity> людей предпочитают не есть мясо! Они предпочитают <food>"

3.	Создать дочерний класс MeatEater от класса Initialization, который состоит из:
•	метода инициализации, принимающего аргументы capacity, food. Нужно создать одноименные атрибуты через вызов
    родительского метода _init_.
•	метода _str_, который возвращает строку формата "<capacity> мясоедов в Днепре! Помимо мяса они едят еще и <food>"
4.	Создать дочерний класс SweetTooth от класса Initialization, который состоит из:
•	метода инициализации, принимающего аргументы capacity, food. Нужно создать одноименные атрибуты через вызов
    родительского метода _init_.
•	магического метода _str_, который возвращает строку формата "Сладкоежек в Днепре <capacity>. Их самая любимая еда:
    <food>"
•	магического метода _eq_, который будет позволять сравнивать экземпляры класса SweetTooth с числами и другими нашими
    классами. Если сравнение происходит с целым числом и атрибут capacity с ним совпадает, то необходимо вернуть True,
    в противном случае - False. Если же сравнение идёт с другим нашим классом (Vegetarian или MeatEater) и значения
    атрибутов capacity равны, то возвращается True, в противном случае - False. А если же сравнивается с другим типом
    данных, верните "Невозможно сравнить количество сладкоежек с <значение>"
•	магического метода _lt_. Если сравнение происходит с целым числом и количество сладкоежек (атрибут capacity) меньше,
    необходимо вернуть True, в противном случае - False. Если сравнение происходит с экземпляром одного из наших классов
    Vegetarian или MeatEater и сладкоежек меньше, то верните True, в противном случае верните False. В случае если
    сравнение идет с остальными типами данных, верните "Невозможно сравнить количество сладкоежек с «значение»"
•	магического метода _gt_. Если сравнение происходит с целым числом и количество сладкоежек больше, необходимо вернуть
    значение True, в противном же случае - False. Если сравнение происходит с другим нашим классом Vegetarian или
    MeatEater и сладкоежек больше, то верните True, в противном случае - False. В случае если сравнение идет с
    остальными типами данных, верните "Невозможно сравнить количество сладкоежек с «значение»"

```python
v_first = Vegetarian(10000, ['Орехи', 'овощи', 'фрукты'])

print(v_first) # 10000 людей предпочитают не есть мясо! Они предпочитают ['Орехи', 'овощи', 'фрукты']

v_second - Vegetarian([23], [ nothing']) # Количество людей должно быть целым числом
                              
m_first - MeatEater(15900, ['Жареную картошку', 'рыба'])
                              
print(m_first) # 15000 мясоедов в Днепре! Помимо мяса они едят ещё и ['Жареную картошку', 'рыба']
                              
s_first = SweetTooth(30000, ['Мороженое , 'Чипсы', 'ШОКОЛАД'])
                             
print(s_first) # Сладкоежек в Днепре 30000. Их самая любимая еда: ['Мороженое', 'Чипсы', 'ШОКОЛАД']
                             
print(s_first > v_first) # True
                             
print(30000 == s_first) # True
                             
print(s_first == 25000) # False
                             
print(100000 < s_first) # False
                             
print(100 < s_first) # True
```