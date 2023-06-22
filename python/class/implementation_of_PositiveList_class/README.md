Implement a PositiveList class, inherited from the list class, to store positive integers.

Also implement new exception NonPositiveError.

In the PositiveList class, reimplement the append(self, x) method so that if you try to add a non-positive
integer, a NonPositiveError exception is thrown and the number is not added, and if you try to add a positive integer
number, the number would be added as in the standard list.

This task ensures that an integer is always passed as the x argument of the append method.

Note:
Numbers strictly greater than zero are considered positive.




Реализуйте класс PositiveList, унаследовав его от класса list, для хранения положительных целых чисел.

Также реализуйте новое исключение NonPositiveError.

В классе PositiveList переопределите метод append(self, x) таким образом, чтобы при попытке добавить неположительное
целое число бросалось исключение NonPositiveError и число не добавлялось, а при попытке добавить положительное целое
число, число добавлялось бы как в стандартный list.

В данной задаче гарантируется, что в качестве аргумента x метода append всегда будет передаваться целое число.

Примечание:
Положительными считаются числа, строго больше нуля.