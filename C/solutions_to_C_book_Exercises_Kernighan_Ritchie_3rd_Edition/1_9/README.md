**Exercise 1.9. Write a program that copies input characters to the output stream and replaces consecutive spaces with a single space.**

**Solution:**
1. Declare variables `c` and `last_char_was_space`. Variable `c` is used to store the current character, and 
   `last_char_was_space` is used to track whether the previous character was a space.
2. In a `while` loop, read characters from the input stream (stdin) using `getchar()`. The loop continues until the end 
   of the file (EOF) is reached.
3. Inside the loop, each character read is checked:
    - If the character is a space, the program checks whether the previous character was also a space 
    (`!last_char_was_space`). If the previous character was not a space, the current character is output using 
    `putchar(c)`, and the `last_char_was_space` flag is set to `true`.
    - If the character is not a space, it is also output using `putchar(c)`, and the `last_char_was_space` flag is reset
    to `false`.
4. If the character 'q' is detected, the program exits by breaking out of the loop.
5. As a result, characters are copied to the output stream, and consecutive spaces are replaced with a single space.




**Упражнение 1.9. Напишите программу, копирующую символы ввода в выходной поток и заменяющую стоящие подряд пробелы на
один пробел.**

**Решение:**
1. Объявляем переменные 'c' и 'last_char_was_space'. Переменная c используется для хранения текущего символа, а 
   'last_char_was_space' - для отслеживания, был ли предыдущий символ пробелом.
2. В цикле while, считываем символы из входного потока (stdin) с помощью 'getchar()'. Цикл продолжается до тех пор, пока 
   не будет достигнут конец файла (EOF).
3. Внутри цикла проверяется каждый считанный символ:
   - Если символ - пробел, то программа проверяет, был ли предыдущий символ тоже пробелом (!last_char_was_space). Если 
   предыдущий символ не был пробелом, то текущий символ выводится с помощью 'putchar(c)', и флаг 'last_char_was_space' 
   устанавливается в 'true'.
   - Если символ не является пробелом, он также выводится с помощью 'putchar(c)', и флаг 'last_char_was_space' 
   сбрасывается в 'false'.
4. Если символ 'q' обнаружен, программа завершает выполнение, выходя из цикла.
5. Как результат, символы копируются в выходной поток, и стоящие подряд пробелы заменяются на один пробел.
