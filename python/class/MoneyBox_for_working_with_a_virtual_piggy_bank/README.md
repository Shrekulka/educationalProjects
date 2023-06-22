Implement a MoneyBox class to work with a virtual piggy bank.
Each piggy bank has a limited capacity, which is expressed by an integer - the number of coins that can be
coins you can put into the piggy bank. The class must support information about the number of coins in the piggy bank, 
provide the ability to add more coins to the piggy bank and find out if more coins can be added to the bank without 
exceeding its capacity.

The class should look like this

```python
class MoneyBox:

    def __init__(self, capacity):
        # constructor with the argument - the capacity of the piggy bank

    def can_add(self, v):
        # True if you can add v coins, False otherwise

    def add(self, v):
        # put v coins into piggy bank
```
When a piggy bank is created, the number of coins in it is 0.

Note:
It is guaranteed that add(self, v) method will only be called if can_add(self, v) is True.




Реализуйте класс MoneyBox, для работы с виртуальной копилкой.
Каждая копилка имеет ограниченную вместимость, которая выражается целым числом – количеством монет, которые можно
положить в копилку. Класс должен поддерживать информацию о количестве монет в копилке, предоставлять возможность
добавлять монеты в копилку и узнавать, можно ли добавить в копилку ещё какое-то количество монет, не превышая ее
вместимость.

Класс должен иметь следующий вид

```python
class MoneyBox:

    def __init__(self, capacity):
        # конструктор с аргументом – вместимость копилки

    def can_add(self, v):
        # True, если можно добавить v монет, False иначе

    def add(self, v):
        # положить v монет в копилку
```
При создании копилки, число монет в ней равно 0.

Примечание:
Гарантируется, что метод add(self, v) будет вызываться только если can_add(self, v) – True.