**Exercise 1.15:** Rewrite the temperature conversion program, separating the conversion itself into a separate function.

**Solution:**

1. Define macros to control the table parameters:
    - `FAHRENHEIT_TO_CELSIUS(f)` - a macro for converting Fahrenheit degrees `f` to Celsius degrees.
    - `LOWER_LIMIT` - the lower temperature limit in Fahrenheit (0).
    - `UPPER_LIMIT` - the upper temperature limit in Fahrenheit (300).
    - `STEP_SIZE` - the temperature change step in Fahrenheit (20).
2. Next, there is a prototype of the `printTemperatureTable()` function, which will be used to print the table.
3. In the `main()` function, the program calls `printTemperatureTable()` and returns 0, ending its execution.
4. The `printTemperatureTable()` function performs the following steps:
    - Outputs the table header with formatted column headings for "Fahrenheit" and "Celsius".
    - Starts a loop to iterate through temperatures in Fahrenheit within the specified range.
    - Inside the loop:
        - Calculates the temperature in Celsius degrees using the `FAHRENHEIT_TO_CELSIUS()` macro.
        - Outputs the temperature in Fahrenheit and Celsius with improved formatting. The output is left-aligned with a
          fixed number of digits after the decimal point (1 decimal place).

Thus, the program creates a readable table that contains temperature conversions from Fahrenheit to Celsius and displays
it on the screen.




**Упражнение 1.15. Перепишите программу преобразования температур, выделив само преобразование в отдельную функцию.**

**Решение:**

1. Опеределяем макросы для управления параметрами таблицы:
    - FAHRENHEIT_TO_CELSIUS(f) - макрос для преобразования градусов Фаренгейта f в градусы Цельсия.
    - LOWER_LIMIT - нижний предел температуры в Фаренгейтах (0).
    - UPPER_LIMIT - верхний предел температуры в Фаренгейтах (300).
    - STEP_SIZE - шаг изменения температуры в Фаренгейтах (20).
2. Далее идет прототип функции printTemperatureTable(), которая будет использоваться для вывода таблицы.
3. В функции main(), программа вызывает printTemperatureTable() и возвращает 0, завершая выполнение.
4. Функция printTemperatureTable() выполняет следующие шаги:
    - Выводит заголовок таблицы с форматированными заголовками для столбцов "Fahrenheit" и "Celsius".
    - Запускает цикл для перебора температур в Фаренгейтах в заданном диапазоне.
    - Внутри цикла:
      - Вычисляет температуру в градусах Цельсия, используя макрос FAHRENHEIT_TO_CELSIUS().
      - Выводит температуру в градусах Фаренгейта и Цельсия с улучшенным форматированием. Вывод производится с 
        выравниванием слева и с фиксированным числом знаков после запятой (1 знак после десятичной точки).
Таким образом, программа создает читаемую таблицу, которая содержит преобразования температур из градусов Фаренгейта в 
градусы Цельсия и выводит ее на экран. 



