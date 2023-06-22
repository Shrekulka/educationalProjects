You are given a sequence of integers, and you have to process it and display the sum of the first five numbers in that 
sequence, then the sum of the second five, etc. of this sequence, then the sum of the second five, and so on.
But the sequence is not given to you in its entirety at once. Over time its successive parts come to you.
For example, first the first three elements, then the next six, then the next two, etc.
Implement a Buffer class that will accumulate the elements of the sequence and print the sum of fives of consecutive 
elements as they accumulate.
One of the requirements for the class is that it must not hold more elements than it really needs i.e., it must not 
store elements that are already part of the five for which the sum has been printed.

The class should have the following form
```python
class Buffer:
    def __init__(self):
        # constructor without arguments

    def add(self, *a):
        # add the next part of the sequence

    def get_current_part(self):
        # return the currently saved sequence elements in the order in which they were
        # added
```

An example of working with a class
```python
buf = Buffer()
buf.add(1, 2, 3)
buf.get_current_part() # return [1, 2, 3]
buf.add(4, 5, 6) # print(15) - print sum of first five elements
buf.get_current_part() # return [6]
buf.add(7, 8, 9, 10) # print(40) - output sum of the second five elements
buf.get_current_part() # return []
buf.add(1, 1, 1, 1, 1, 1, 1, 1, 1, 1) # print(5), print(5) - print the sum of the third and fourth five
buf.get_current_part() # return [1]
```
Note that it may be necessary to output the sum of fives several times during the add method, until there are fewer than
five elements left in the buffer.




Вам дается последовательность целых чисел и вам нужно ее обработать и вывести на экран сумму первой пятерки чисел из
этой последовательности, затем сумму второй пятерки, и т. д.
Но последовательность не дается вам сразу целиком. С течением времени к вам поступают её последовательные части.
Например, сначала первые три элемента, потом следующие шесть, потом следующие два и т. д.
Реализуйте класс Buffer, который будет накапливать в себе элементы последовательности и выводить сумму пятерок
последовательных элементов по мере их накопления.
Одним из требований к классу является то, что он не должен хранить в себе больше элементов, чем ему действительно
необходимо, т. е. он не должен хранить элементы, которые уже вошли в пятерку, для которой была выведена сумма.

Класс должен иметь следующий вид
```python
class Buffer:
    def __init__(self):
        # конструктор без аргументов

    def add(self, *a):
        # добавить следующую часть последовательности

    def get_current_part(self):
        # вернуть сохраненные в текущий момент элементы последовательности в порядке, в котором они были
        # добавлены
```

Пример работы с классом
```python
buf = Buffer()
buf.add(1, 2, 3)
buf.get_current_part() # вернуть [1, 2, 3]
buf.add(4, 5, 6) # print(15) – вывод суммы первой пятерки элементов
buf.get_current_part() # вернуть [6]
buf.add(7, 8, 9, 10) # print(40) – вывод суммы второй пятерки элементов
buf.get_current_part() # вернуть []
buf.add(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) # print(5), print(5) – вывод сумм третьей и четвертой пятерки
buf.get_current_part() # вернуть [1]
```python
Обратите внимание, что во время выполнения метода add выводить сумму пятерок может потребоваться несколько раз до тех
пор, пока в буфере не останется менее пяти элементов.