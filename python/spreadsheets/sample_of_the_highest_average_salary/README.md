#### Task:
Vasya is planning a career and a move. To do this, he made a table in which for each region he wrote down the salaries 
for different professions he is interested in professions of interest to him. The table is available at 
https://stepik.org/media/attachments/lesson/245267/salaries.xlsx. 
Print the name of the region with the highest median salary (the median is the element standing in the middle of the 
array after its ordering) and output the name of the region with the highest median salary after its ordering) and, 
after a space, the name of the profession with the highest median salary in all regions. 

####Solutions:

####First solution 
Uses the pandas library to work with data from an Excel file. Here we use the method pd.read_excel() to read data from 
the file and create a DataFrame (table). Then we use the median() and mean() methods to calculate the median and mean 
respectively. Then, using the idxmax() method, we find the names of the region and the occupation with the highest 
median salary and the highest mean salary, respectively. Display the results on the screen.

####The second solution 
Uses the openpyxl library to work with data from an Excel file. Here we load the data into the Workbook and then go 
through each row in the table (rows 2-9) and calculate the median salary for each region. Then we find the region with 
the highest median wage. Next, we go through each occupation, calculate the median wage for each occupation and find the
occupation with the highest median wage occupation and find the occupation with the maximum median salary. We display 
the results on the screen.

Both solutions allow you to find the name of the region with the highest median salary and the name of the profession 
with the highest average salary based on the data from the average salary based on data from the file 'salaries.xlsx'.





###Задача:
Вася планирует карьеру и переезд. Для это составил таблицу, в которой для каждого региона записал зарплаты для разных 
интересные ему профессий. Таблица доступна по ссылке https://stepik.org/media/attachments/lesson/245267/salaries.xlsx. 
Выведите название региона с самой высокой медианной зарплатой (медианой называется элемент, стоящий в середине массива 
после его упорядочивания) и, через пробел, название профессии с самой высокой средней зарплатой по всем регионам. 

###Решения:

####Первое решение 
Использует библиотеку pandas для работы с данными из Excel-файла. Здесь мы используем метод 
pd.read_excel() для чтения данных из файла и создания DataFrame (таблицы). Затем мы используем методы median() и mean() 
для вычисления медианы и среднего значения соответственно. Затем, с помощью метода idxmax() находим названия региона и 
профессии с самой высокой медианной зарплатой и самой высокой средней зарплатой, соответственно. Выводим результаты на 
экран.

####Второе решение 
Использует библиотеку openpyxl для работы с данными из Excel-файла. Здесь мы загружаем данные в Workbook,а затем 
проходим по каждой строке в таблице (строки 2-9) и вычисляем медианную зарплату для каждого региона. Затем находим 
регион с максимальной медианной зарплатой. Далее, проходим по каждой профессии, вычисляем среднюю зарплату для каждой 
профессии и находим профессию с максимальной средней зарплатой. Выводим результаты на экран.

Оба решения позволяют найти название региона с самой высокой медианной зарплатой и название профессии с самой высокой 
средней зарплатой на основе данных из файла 'salaries.xlsx'.