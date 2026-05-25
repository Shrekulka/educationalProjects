**Exercise 1.20. Write a program `detab` that replaces tab characters in the input text with the appropriate number of 
spaces (up to the next "tab stop"). It is assumed that tab stops are placed at a fixed distance from each other, say, 
every n positions. Is it better to define n as a variable or as a named constant?**

**Solution:**

1. Define a named constant `TAB_WIDTH` with a value of 4. This constant will be used to determine the width of tab stops.
   This means that each tab stop is placed every 4 positions.
2. In the `main` function, declare variables:
    - `character`: Used for reading characters from input.
    - `column`: Used to track the current position in the line.
3. Enter a `while` loop that will execute until characters are read from the input and the end of file (EOF) is not 
   reached.
4. Inside the loop, check if the character at the beginning of the line is equal to 'q'. If so, exit the program by 
   breaking out of the loop.
5. If the read character is a tab character ('\t'), calculate how many spaces need to be inserted before the next tab 
   stop. This is done by using the remainder of the division of `column` by `TAB_WIDTH`. For example, if the current 
   position `column` is 5, and the tab width `TAB_WIDTH` is 4, we need to insert one space to align the text to the next
   tab stop.
6. Next, start a `for` loop that inserts the required number of spaces before the tab character, as calculated earlier. 
   Each space is added using `putchar(' ')`, and the `column` counter is updated to keep track of the current position.
7. If the read character is a newline character ('\n'), output it to the screen and reset the `column` counter to 0, as 
   a new line is starting.
8. Otherwise, if the read character is neither a tab nor a newline character, simply output it to the screen and 
   increment the `column` counter.
9. Upon exiting the loop, the program terminates.

This solution replaces tab characters in the text with the appropriate number of spaces to align the text to tab stops, 
as defined by the `TAB_WIDTH` constant.




**Упражнение 1.20. Напишите программу detab, заменяющую символы табуляции во вводимом тексте нужным числом пробелов (до 
следующего "стопа" табуляции). Предполагается, что "стопы" табуляции расставлены на фиксированном расстоянии друг от 
друга, скажем, через n позиций. Как лучше задавать n — в виде значения переменной или в виде именованной константы?**

**Решение:**

1. Определяем именованную константу `TAB_WIDTH` равную 4. Эта константа будет использоваться для определения ширины 
   табуляции. Это означает, что каждая "стопа" табуляции будет расставлена через 4 позиции.
2. В функции `main` объявляем переменные:
    - `character`: используется для считывания символов из ввода.
    - `column`: используется для отслеживания текущей позиции в строке.
3. Заходим в цикл `while`, который будет выполняться до тех пор, пока символы считываются из ввода и не достигнут конец 
   файла (EOF).
4. Внутри цикла проверяем, если символ в начале строки равен 'q', то завершаем выполнение программы, выходя из цикла.
5. Если считанный символ - это символ табуляции (`'\t'`), то мы вычисляем, сколько пробелов нужно вставить перед этой 
   "стопой" табуляции. Мы используем остаток от деления `column` на `TAB_WIDTH` для этого расчета. Например, если текущая
   позиция `column` равна 5, и ширина табуляции `TAB_WIDTH` равна 4, то нам нужно вставить один пробел, чтобы выровнять 
   текст по следующей "стопе" табуляции.
6. Затем запускаем цикл `for`, который выполняет вставку нужного количества пробелов перед табуляцией, как было 
   рассчитано ранее. Каждый пробел добавляется с помощью `putchar(' ')`, и счетчик `column` обновляется для отслеживания
   текущей позиции.
7. Если считанный символ - это символ новой строки (`'\n'`), то мы выводим его на экран и сбрасываем счетчик `column` до
   0, так как мы начинаем новую строку.
8. В противном случае, если считанный символ не является ни табуляцией, ни символом новой строки, мы просто выводим его 
   на экран и увеличиваем счетчик `column`.
9. По завершении цикла, программа завершает выполнение.

Это решение выполняет замену символов табуляции в тексте на нужное количество пробелов, чтобы выровнять текст по "стопам"
табуляции, как определено константой `TAB_WIDTH`.