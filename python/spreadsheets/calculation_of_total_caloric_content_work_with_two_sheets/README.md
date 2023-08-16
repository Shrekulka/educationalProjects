###Task:
Vasya has been appointed as a quartermaster for a tourist group, and he took his responsibilities seriously by creating 
a reference guide for food items, including the caloric content per 100 grams as well as the content of proteins, fats
and carbohydrates per 100 grams of each product. However, he couldn't find all the information, so some cells remained 
empty (you can consider their value as zero). He also used some strange office software that used a comma to separate 
the integer and decimal parts of numbers. The table is available at the 
link: https://stepik.org/media/attachments/lesson/245290/trekking2.xlsx.

Vasya prepared a daily food plan (it's on the "Раскладка" sheet) with the names of the food items and their quantities 
in grams. Calculate four numbers: the total caloric content, and the grams of proteins, fats, and carbohydrates. Round 
the numbers down to the nearest integer and enter them separated by a space.

###Solution:
This code processes data from two sheets of an Excel file, performing a merge operation based on a common 'Name' column.
First, display options are set for more convenient output. Then, data is loaded from the first and second sheets, with 
column renaming in both cases.

Subsequently, a merge operation is performed on the `table_first` and `table_second` tables based on the 'Name' column, 
retaining only rows where the 'Name' column values match in both tables. Next, the total values of calories, proteins, 
fats and carbohydrates are calculated by multiplying the values from the corresponding columns by the weight of each 
product in each row. The results are then displayed.

As a result, the code provides the cumulative information about calories, proteins, fats, and carbohydrates contained in
the combined data from the two Excel file sheets.




###Задача:
Васю назначили завхозом в туристической группе и он подошёл к подготовке ответственно, составив справочник продуктов с 
указанием калорийности на 100 грамм, а также содержание белков, жиров и углеводов на 100 грамм продукта. Ему не удалось
найти всю информацию, поэтому некоторые ячейки остались незаполненными (можно считать их значение равным нулю). Также он
использовал какой-то странный офисный пакет и разделял целую и дробную часть чисел запятой. Таблица доступна по ссылке 
https://stepik.org/media/attachments/lesson/245290/trekking2.xlsx 

Вася составил раскладку по продуктам на один день (она на листе "Раскладка") с указанием названия продукта и его 
количества в граммах. Посчитайте 4 числа: суммарную калорийность и граммы белков, жиров и углеводов. Числа округлите до 
целых вниз и введите через пробел.

###Решение:
Данный код выполняет обработку данных из двух листов Excel-файла, проводя объединение (слияние) информации из этих 
листов на основе общего столбца 'Name'. Вначале устанавливаются параметры отображения для более удобного вывода. Затем 
происходит загрузка данных из первого и второго листов, с переименованием столбцов в обоих случаях.

После этого выполняется операция объединения (слияния) таблиц table_first и table_second на основе столбца 'Name', 
сохраняя только те строки, где значение столбца 'Name' совпадает в обоих таблицах. Затем вычисляются суммарные значения 
калорий, белков, жиров и углеводов, умножая значения из соответствующих столбцов на вес продукта в каждой строке, и 
производится вывод результатов.

В результате получается суммарная информация о калориях, белках, жирах и углеводах, которые содержатся в объединенных 
данных из двух листов Excel-файла.