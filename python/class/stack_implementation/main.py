"""Реализуйте структуру данных, представляющую собой расширенную структуру стек. Необходимо поддерживать добавление
элемента на вершину стека, удаление с вершины стека, и необходимо поддерживать операции сложения, вычитания, умножения
и целочисленного деления.
Операция сложения на стеке определяется следующим образом. Со стека снимается верхний элемент (top1), затем снимается
следующий верхний элемент (top2), и затем как результат операции сложения на вершину стека кладется элемент, равный
top1 + top2.
Аналогичным образом определяются операции вычитания (top1 - top2), умножения (top1 * top2) и целочисленного деления
(top1 // top2).
Реализуйте эту структуру данных как класс ExtendedStack, отнаследовав его от стандартного класса list.

Требуемая структура класса:
class ExtendedStack(list):
    def sum(self):
        # операция сложения

    def sub(self):
        # операция вычитания

    def mul(self):
        # операция умножения

    def div(self):
        # операция целочисленного деления

Примечание
Для добавления элемента на стек используется метод append, а для снятия со стека – метод pop.
Гарантируется, что операции будут совершаться только когда в стеке есть хотя бы два элемента.
"""


########################################################################################################################

class ExtendedStack(list):  # создаем класс, наследующий от встроенного класса list

    def __init__(self, items=None):  # объявляем конструктор, принимающий необязательный параметр - список items
        if items is None:  # если список не был передан, создаем пустой список
            items = []
        super().__init__(items)  # вызываем конструктор базового класса и передаем ему список items
        self.top1 = None  # инициализируем поля top1 и top2, обозначающие два последних элемента списка
        self.top2 = None

    def check(self):  # объявляем метод check, который проверяет, что в списке есть как минимум два элемента
        if len(self) >= 2:  # если в списке есть два и более элемента
            self.top1 = self.pop()  # извлекаем последний элемент и сохраняем его в поле top1
            self.top2 = self.pop()  # извлекаем предпоследний элемент и сохраняем его в поле top2
            return True  # возвращаем значение True
        else:
            return False  # иначе возвращаем значение False

    def sum(self):  # объявляем метод sum, который складывает два последних элемента списка
        if self.check():  # если в списке есть два и более элемента
            self.append(self.top1 + self.top2)  # добавляем сумму двух последних элементов в конец списка

    def sub(self):  # объявляем метод sub, который вычитает последний элемент из предпоследнего
        if self.check():  # если в списке есть два и более элемента
            self.append(self.top1 - self.top2)  # добавляем разность последних двух элементов в конец списка

    def mul(self):  # объявляем метод mul, который перемножает два последних элемента списка
        if self.check():  # если в списке есть два и более элемента
            self.append(self.top1 * self.top2)  # добавляем произведение последних двух элементов в конец списка

    def div(self):  # объявляем метод div, который делит предпоследний элемент на последний
        if self.check() and self.top2 != 0:  # если в списке есть два и более элемента и последний элемент не равен нулю
            # добавляем целочисленное частное от деления двух последних элементов в конец списка
            self.append(self.top1 // self.top2)


########################################################################################################################

# создаем объект ex_stack класса ExtendedStack, передав список элементов
ex_stack = ExtendedStack([1, 2, 3, 4, -3, 3, 5, 10])
ex_stack.div()
assert ex_stack.pop() == 2
ex_stack.sub()
assert ex_stack.pop() == 6
ex_stack.sum()
assert ex_stack.pop() == 7
ex_stack.mul()
assert ex_stack.pop() == 2
assert len(ex_stack) == 0
