####Task:
Vasya was appointed as the head cook of the travelling group and he took a responsible approach to the preparation by 
compiling a food guide with calories per 100 grams and the protein, fat and carbohydrate content per 100 grams. He 
wasn't able to find all the information, so some cells were left blank (we can consider their value to be zero). He also
used some strange office package and separated the integer and fractional parts of the numbers with a comma. The table 
is available at the link https://stepik.org/media/attachments/lesson/245290/trekking3.xlsx

Vasya made a food layout for the whole trek (it's on the "Layout" sheet) with the number of the day, the name of the 
food and its quantity in grams. For each day, count 4 numbers: total calories and grams of protein, fat, and 
carbohydrates. Round the numbers down to whole numbers and enter them over a space. Each day should be displayed on a 
separate line.

####Solution:
The solution to this problem involves loading data from two Excel sheets using the Pandas library. Then merge the data 
by the 'Name' column, calculate the total nutrient values for each food item by weight. This is followed by aggregating 
the values by day of the week, rounding the results and adding the aggregated data back into the original table. The 
results are then displayed on the screen.





###Задача:
Васю назначили завхозом в туристической группе и он подошёл к подготовке ответственно, составив справочник продуктов с 
указанием калорийности на 100 грамм, а также содержание белков, жиров и углеводов на 100 грамм продукта. Ему не удалось 
найти всю информацию, поэтому некоторые ячейки остались незаполненными (можно считать их значение равным нулю). Также он
использовал какой-то странный офисный пакет и разделял целую и дробную часть чисел запятой. Таблица доступна по ссылке 
https://stepik.org/media/attachments/lesson/245290/trekking3.xlsx

Вася составил раскладку по продуктам на весь поход (она на листе "Раскладка") с указанием номера дня, названия продукта 
и его количества в граммах. Для каждого дня посчитайте 4 числа: суммарную калорийность и граммы белков, жиров и 
углеводов. Числа округлите до целых вниз и введите через пробел. Информация о каждом дне должна выводиться в отдельной 
строке.

###Решение:
Решение данной задачи включает в себя загрузку данных из двух листов Excel с использованием библиотеки Pandas. Затем 
происходит объединение данных по столбцу 'Name', рассчет общих значений питательных веществ для каждого продукта с 
учетом их веса. После этого производится агрегация значений по дням недели, округление результатов и добавление 
агрегированных данных обратно в исходную таблицу. Полученные результаты выводятся на экран.