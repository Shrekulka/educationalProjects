**Exercise 1.13: Write a program to print the histograms of the lengths of input words. Drawing a horizontal histogram
is easy, but drawing a vertical one is a bit more challenging.**

**Solution:**

1. `const int SIZE = 21;` - Here, we declare a constant SIZE representing the maximum word length to be analyzed. We 
   chose 21 as the maximum value, but you can change it as needed.
2. `int currentChar = 0;` - We declare the variable currentChar to store the current character from the input.
3. `int currentLength = 0;` - This variable will be used to track the current word's length.
4. `int wordLengths[SIZE] = { 0 };` - The array 'wordLengths' represents counters for word lengths. Initially, all its 
   elements are set to 0.
5. `while ((currentChar = getchar()) != EOF)` - We start an infinite loop that will read characters from the input until
   the end of the file (EOF) is reached.
6. `if (currentChar == 'q') break;` - If the character 'q' is entered, the program exits and breaks out of the loop.
7. `if (currentChar == ' ' || currentChar == '\n' || currentChar == '\t')` - Here, we check whether the current character
   is a word separator. This includes spaces, newline characters, and tabs.
8. `if (currentLength >= 0 && currentLength < SIZE)` - We check if the current word's length is within valid bounds 
   (from 0 to SIZE-1).
9. `++wordLengths[currentLength];` - If the word length is within valid bounds, we increment the corresponding element 
   in the 'wordLengths' array for that length.
10. `else if (currentLength >= SIZE)` - If the word length exceeds the maximum value 'SIZE', we increment the counter for 
   the maximum word length (the last element of the array).
11. `currentLength = 0;` - We reset the current word's length counter because the word has ended.
12. `++currentLength;` - If the current character is not a word separator, we increment the current word's length counter.
13. After finishing the loop, we move on to outputting the histogram.
14. We print the histogram by iterating through all possible word lengths (from 1 to SIZE-1). For each word length, we 
   print the number of words of that length as asterisks.

In the end, the program builds a histogram of the lengths of words entered by the user, where each row represents a word
length, and the number of asterisks on that row shows how many words of that length were entered.




**Упражнение 1.13. Напишите программу, печатающую гистограммы длин вводимых слов. Гистограмму легко рисовать 
горизонтальными полосами. Рисование вертикальными полосами — более трудная задача.**

**Решение:**

1. 'const int SIZE = 21;' - Здесь объявляется константа SIZE, которая представляет максимальную длину слова для анализа. 
   Мы выбрали 21 как максимальное значение, но вы можете изменить его по своему усмотрению.
2. 'int currentChar = 0;' - Объявляется переменная currentChar, которая будет использоваться для хранения текущего 
   символа из ввода.
3. 'int currentLength = 0;' - Эта переменная будет использоваться для отслеживания текущей длины слова.
4. 'int wordLengths[SIZE] = { 0 };' - Массив 'wordLengths' представляет собой счетчики для длин слов. Изначально все его
   элементы устанавливаются в 0.
5. 'while ((currentChar = getchar()) != EOF)' - Мы начинаем бесконечный цикл, который будет читать символы из ввода до 
   достижения конца файла (EOF).
6. 'if (currentChar == 'q') break;' - Если вводится символ 'q', программа завершает выполнение и выходит из цикла.
7. 'if (currentChar == ' ' || currentChar == '\n' || currentChar == '\t')' - Здесь мы проверяем, является ли текущий 
   символ разделителем слов. Это включает пробелы, символы новой строки и табуляции.
8. 'if (currentLength >= 0 && currentLength < SIZE)' - Мы проверяем, находится ли текущая длина слова в допустимых 
   пределах (от 0 до SIZE-1).
9. '++wordLengths[currentLength];' - Если длина слова находится в допустимых пределах, мы увеличиваем соответствующий 
   элемент массива 'wordLengths' для этой длины.
10. 'else if (currentLength >= SIZE)' - Если длина слова превышает максимальное значение 'SIZE', мы увеличиваем счетчик 
    для максимальной длины слова (последний элемент массива).
11. 'currentLength = 0;' - Мы сбрасываем счетчик текущей длины слова, так как слово завершилось.
12. '++currentLength;' - Если текущий символ не является разделителем, мы увеличиваем счетчик текущей длины слова.
13. После завершения цикла мы переходим к выводу гистограммы.
14. Мы выводим гистограмму, пройдясь по всем возможным длинам слов (от 1 до SIZE-1). Для каждой длины слова мы выводим 
    количество слов данной длины в виде звездочек.

В итоге программа строит гистограмму длин слов, введенных пользователем, где каждая строка представляет собой длину 
слова, а количество звездочек на этой строке показывает, сколько слов такой длины было введено.