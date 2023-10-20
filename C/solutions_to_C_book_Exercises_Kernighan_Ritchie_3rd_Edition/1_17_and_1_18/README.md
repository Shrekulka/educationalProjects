**Exercise 1.18. Write a program that replaces consecutive spaces and tabs with a single space in each input line and 
deletes empty lines.**
**Exercise 1.17. Write a program to print all input strings containing more than 80 characters.**

**Solution:**

1. Define the 'MINIMUM_CHARACTERS' macro with a value of '80', which will be used later to determine the minimum length 
   of a line that will be displayed on the screen.
2. In the 'main()' function, declare the following variables:
    - 'character' - to store the current character.
    - 'previous_char' - to track the previous character.
    - 'i' - a counter for characters in the current line.
    - 'size' - the initial buffer size for storing a line.
    - 'current_line' - a pointer to the current line (a dynamic array).
3. Enter a 'while' loop that runs until the end of the file (EOF) is reached, reading characters from the keyboard.
4. Check if a 'q' is encountered at the beginning of a line; if so, the program exits and frees the allocated memory.
5. Check if the current line has reached the buffer size limit; if so, double the buffer size and reallocate memory.
6. When a newline character '\n' is encountered, the program checks if the line has more than 80 characters. If the 
   condition is met, the program prints the line; otherwise, it prints a message indicating that the line does not 
   contain more than 80 characters. Then, the character counter is reset for a new line.
7. Otherwise, if the current character is a space or tab and the previous character was also a space or tab, the program
   skips the character.
8. If none of the above conditions are met, the program records the current character in the current line.
9. The program saves the current character as the previous character before reading the next character.
10. After the loop is finished, the allocated memory is freed.




**Упражнение 1.18. Напишите программу, которая будет в каждой вводимой строке заменять стоящие подряд символы пробелов 
и табуляций на один пробел и удалять пустые строки.**
**Упражнение 1.17. Напишите программу печати всех вводимых строк, содержащих более 80 символов.**

**Решение:**

1. Определяем макрос 'MINIMUM_CHARACTERS' со значением '80', которое будет использоваться в дальнейшем для определения 
   минимальной длины строки, которая будет выведена на экран.
2. В функции main() объявляются следующие переменные:
    - character - для хранения текущего символа.
    - previous_char - для отслеживания предыдущего символа.
    - i - счетчик символов в текущей строке.
    - size - начальный размер буфера для хранения строки.
    - current_line - указатель на текущую строку (динамический массив).
3. Заходим в цикл while, который выполняется до достижения конца файла (EOF), считывая символы с клавиатуры.
4. Проверяем, если в начале строки встречается символ 'q', то программа завершает выполнение и освобождает выделенную 
   память.
5. Проверяем, если текущая строка достигла предела размера буфера, то увеличивает размер буфера вдвое и перераспределяет
   память.
6. При считывании символа новой строки '\n', программа проверяет, имеет ли строка более 80 символов. Если условие 
   выполняется, программа выводит строку, иначе выводит сообщение о том, что строка не содержит более 80 символов. Затем
   сбрасывает счетчик символов для новой строки.
7. В противном случае программа проверяет, не является ли текущий символ пробелом или табуляцией, и, если предыдущий 
   символ также был пробелом или табуляцией, она пропускает этот символ.
8. Если ни одно из вышеуказанных условий не выполняется, программа записывает текущий символ в текущую строку.
9. Программа сохраняет текущий символ как предыдущий перед считыванием следующего символа.
10. После завершения цикла освобождаем выделенную память.