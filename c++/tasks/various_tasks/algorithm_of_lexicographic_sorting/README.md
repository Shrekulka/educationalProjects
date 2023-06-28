Нехай S = 's1s2...sa' і T = 't1t2...tb' будуть рядками довжини a і b відповідно (mi називається i-м літерою S). Ми
кажемо, що S лексикографічно менше за T, позначаючи S <lex T, якщо:
a < b і si = ti для всіх i = 1, 2, ..., a, або
Існує індекс i ≤ min {a, b}, такий, що sj = tj для всіх j = 1, 2, ..., i − 1 і si < ti.
Алгоритм лексикографічного сортування спрямований на сортування заданого набору n рядків у лексикографічному порядку
за зростанням (у разі збігів через однакові рядки, то в неспадному порядку).

Довжина кожного рядка у вхідному масиві обмежена 100 000 символами.

Кожен рядок містить лише малі латинські літери.

Сигнатура функції:

void contains(std::vector<std::string>& strings);

Напишіть рішення. Виведіть результат у консоль.

Перевірте правильність вашого алгоритму.

У коментарях поясніть час виконання і складність за простором для вашого алгоритму.

Примітка: не використовуйте функції сортування std.



Приклади тестових випадків:

Вхідні дані: ["hello", "world", "apple", "banana", "cat", "dog"]
Вихід: apple banana cat dog hello world

Вхідні дані: ["zebra", "apple", "banana", "cat", "dog"]
Вихід: apple banana cat dog zebra

Вхідні дані: ["cat", "dog", "mouse", "elephant", "tiger"]
Вихід: cat dog elephant mouse tiger

Вхідні дані: ["abcd", "abc", "abcde", "ab", "abcdef"]
Вихід: ab abc abcd abcde abcdef

Вхідні дані: []
Вихід: a aa aaa aaaa aaaaa