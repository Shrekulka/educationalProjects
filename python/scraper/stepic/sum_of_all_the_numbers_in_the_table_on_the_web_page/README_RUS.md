###Задача:
В файле https://stepik.org/media/attachments/lesson/209723/3.html находится одна таблица. Просуммируйте все числа в ней 
и введите в качестве ответа одно число - эту сумму. Для доступа к ячейкам используйте возможности BeautifulSoup.

Когда код запущен, он отправляет запрос на веб-страницу, представленную URL-адресом 
"https://stepik.org/media/attachments/lesson/209723/3.html".
Если запрос успешен и страница доступна (статус код равен 200), то код начинает анализировать содержимое HTML-страницы.
Он ищет все ячейки (<td>) в таблице и извлекает числа из каждой ячейки.
Числа добавляются в список numbers_in_table.
После того, как все числа извлечены, программа вычисляет их сумму с помощью функции sum() и сохраняет результат в 
переменную total_sum.
Наконец, программа выводит на экран полученную сумму.

Если на странице содержится только одна таблица с числами, то результатом работы программы будет одно число - сумма всех
чисел в этой таблице. Если на странице присутствуют другие элементы, не являющиеся таблицами или числами, они будут 
проигнорированы, и программа вычислит сумму только чисел из таблицы.