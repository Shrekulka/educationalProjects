One application of multiple inheritance is to extend the functionality of a class in some predetermined way.
way. For example, if we need to log some information when accessing class methods.
Consider the Loggable class:
```python
import time

class Loggable:
    def log(self, msg):
        print(str(time.ctime()) + ": " + str(msg))
```
It has exactly one log method that allows you to print some message into the log (in this case into stdout),
Adding the current time to it.
Implement LoggableList class, inheriting it from list and Loggable classes, so that when an item
into the list using the append method, a message is sent to the log, which consists of a newly added item.

Note
Your program must not contain a Loggable class. Your program will have this class available when tested and it will
contain the log method described above.




Одно из применений множественного наследование – расширение функциональности класса каким-то заранее определенным
способом. Например, если нам понадобится логировать какую-то информацию при обращении к методам класса.
Рассмотрим класс Loggable:
```python
import time

class Loggable:
    def log(self, msg):
        print(str(time.ctime()) + ": " + str(msg))
```
У него есть ровно один метод log, который позволяет выводить в лог (в данном случае в stdout) какое-то сообщение,
добавляя при этом текущее время.
Реализуйте класс LoggableList, унаследовав его от классов list и Loggable таким образом, чтобы при добавлении элемента
в список посредством метода append в лог отправлялось сообщение, состоящее из только что добавленного элемента.

Примечание
Ваша программа не должна содержать класс Loggable. При проверке вашей программе будет доступен этот класс, и он будет
содержать метод log, описанный выше.