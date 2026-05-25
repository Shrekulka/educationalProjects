**Exercise 1.21.** Write a program `entab` that replaces strings of spaces with the minimum number of tabs and spaces 
necessary to achieve the same spacing. Use the same tab stops as `detab`. When either a tab or a single space would 
suffice to reach a tab stop, which should be given preference?

**Solution:**
1. In the `main` function, we declare variables:
    - `character`: for reading characters from input.
    - `column`: for tracking the current position in the line.
    - `space_count`: for counting consecutive spaces.
2. We start a `while` loop that will run as long as characters are read from input and we haven't reached the end of the
   file (EOF).
3. If the character at the beginning of a line is 'q', the program exits.
4. If we encounter a space:
    - Increment the `space_count` to track consecutive spaces.
    - Increment the `column` to keep track of the current position in the line.
5. If the current `column` position becomes a multiple of the tab width `TAB_WIDTH`, it means we've reached the next tab
   stop:
    - Calculate how many spaces should be output before the tab characters to align the text properly.
    - Start a `for` loop that outputs the required number of spaces and increments `column` on each iteration.
6. Reset the `space_count` as we've processed consecutive spaces.
7. If the character is not a space:
    - Output tab characters in place of accumulated spaces.
    - Reset the `space_count`.
    - Output the current character.
    - Increment `column`.
8. If we encounter a newline character ('\n'), reset `column` to 0 as we're moving to a new line.

Thus, the `entab` program replaces groups of spaces with the minimum number of tabs and spaces to maintain the text's 
formatting.




**Упражнение 1.21. Напишите программу entab, заменяющую строки из пробелов минимальным числом табуляций и пробелов таким
образом, чтобы вид напечатанного текста не изменился. Используйте те же "стопы" табуляции, что и в detab. В случае, 
когда для выхода на очередной "стоп" годится один пробел, что лучше — пробел или табуляция?**

Программа entab выполняет замену групп последовательных пробелов на минимальное количество табуляций и пробелов, чтобы 
внешний вид текста остался неизменным. Она использует те же "стопы" табуляции, что и detab, определенные константой 
TAB_WIDTH.

**Решение:**
1. В функции main, объявляем переменные:
    - character: для считывания символов из ввода.
    - column: для отслеживания текущей позиции в строке.
    - space_count: для подсчета последовательных пробелов.
2. Запускаем цикл while, который будет выполняться, пока символы считываются из ввода и не достигнут конец файла (EOF).
3. Если символ в начале строки - это 'q', программа завершает выполнение.
4. Если мы встречаем пробел:
    - Увеличиваем счетчик space_count, чтобы отслеживать последовательные пробелы.
    - Увеличиваем счетчик column, чтобы отслеживать текущую позицию в строке.
5. Если текущая позиция column становится кратной ширине табуляции TAB_WIDTH, это означает, что мы достигли следующей 
   "стопы" табуляции:
    - Мы вычисляем, сколько пробелов нужно вывести перед символами табуляции, чтобы выровнять текст.
    - Запускаем цикл for, который выводит нужное количество пробелов и увеличивает column на каждой итерации.
6. Сбрасываем счетчик space_count, так как мы уже обработали последовательные пробелы.
7. Если символ - это не пробел:
    - Выводим символы табуляции вместо накопленных пробелов.
    - Сбрасываем счетчик space_count.
    - Выводим текущий символ.
    - Увеличиваем column.
8. Если мы встречаем символ новой строки ('\n'), сбрасываем счетчик column до 0, так как мы переходим на новую строку.

Таким образом, программа entab выполняет замену групп пробелов на минимальное количество табуляций и пробелов, чтобы 
сохранить форматирование текста.