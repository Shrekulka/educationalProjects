Implement a data structure that is an extended stack structure. It needs to support adding
element to a stack vertex, removal from a stack vertex, and must support addition, subtraction, multiplication
and integer division operations.
An addition operation on the stack is defined as follows. The top element (top1) is removed from the stack, then the
element (top2) is removed from the stack, and then the result of the addition operation is an element equal to
top1 + top2.
Similarly, operations of subtraction (top1 - top2), multiplication (top1 * top2) and integer division are defined
(top1 // top2).
Implement this data structure as an ExtendedStack class by inheriting it from the standard list class.

The required class structure is:

```python
class ExtendedStack(list):
    def sum(self):
        # addition operation

    def sub(self):
        # sub operation

    def mul(self):
        # operation of multiplication

    def div(self):
        # integer division operation
```
Note
The append method is used to add an element to the stack, and the pop method is used to remove an element from the stack.
It is guaranteed that operations will only be performed when there are at least two elements on the stack.




Реализуйте структуру данных, представляющую собой расширенную структуру стек. Необходимо поддерживать добавление
элемента на вершину стека, удаление с вершины стека, и необходимо поддерживать операции сложения, вычитания, умножения
и целочисленного деления.
Операция сложения на стеке определяется следующим образом. Со стека снимается верхний элемент (top1), затем снимается
следующий верхний элемент (top2), и затем как результат операции сложения на вершину стека кладется элемент, равный
top1 + top2.
Аналогичным образом определяются операции вычитания (top1 - top2), умножения (top1 * top2) и целочисленного деления
(top1 // top2).
Реализуйте эту структуру данных как класс ExtendedStack, унаследовав его от стандартного класса list.

Требуемая структура класса:

```python
class ExtendedStack(list):
    def sum(self):
        # операция сложения

    def sub(self):
        # операция вычитания

    def mul(self):
        # операция умножения

    def div(self):
        # операция целочисленного деления
```
Примечание
Для добавления элемента на стек используется метод append, а для снятия со стека – метод pop.
Гарантируется, что операции будут совершаться только когда в стеке есть хотя бы два элемента.