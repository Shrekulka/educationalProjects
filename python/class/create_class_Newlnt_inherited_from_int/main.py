"""Создайте класс Newlnt, который унаследован от целого типа int, то есть мы будем унаследовать поведение целых чисел и
значит экземплярам нашего класса будут поддерживать те же операции, что и целые числа.

Дополнительно в классе Newint нужно создать:
• метод repeat, который принимает одно целое положительное число n (по умолчанию равное 2), обозначающее сколько раз
  нужно продублировать данное число. Метод гере должен возвращать новое число, продублированное n раз (см пример ниже);
• метод to_bin, который возвращает двоичное представление числа в виде числа (может пригодиться функция bin)

# Кстати, как вы думаете, что вернет данный вызов NewInt() ?
"""


########################################################################################################################
# Объявление класса NewInt, который наследуется от встроенного класса int
class NewInt(int):
    # Метод repeat, возвращающий новое число, полученное путем повторения текущего числа
    # k раз (по умолчанию 2 раза)
    def repeat(self, k=2):
        return int(str(self) * k)

    # Метод to_bin, возвращающий целое число, представленное в двоичной системе счисления
    def to_bin(self):
        return int(bin(self)[2:])


########################################################################################################################

a = NewInt(9)
print(a.repeat())  # печатает число 99

d = NewInt(a + 5)
print(d.repeat(3))  # печатает число 141414

b = NewInt(NewInt(7) * NewInt(5))
print(b.to_bin())  # печатает 100011 - двоичное представление числа 35

print(NewInt())  # 0
