**Exercise 1.8. Write a program to count spaces, tabs, and newline characters.**

1. Declare variables `c`, `count_spaces`, `count_tabulation`, and `count_new_line` to track the number of space, tab, 
   and newline characters.
2. Then, a `while` loop begins, which reads characters from the input stream (standard input) using the `getchar()` 
   function. The loop continues until the end of file (EOF) is reached.
3. Inside the loop, each character read is checked:
    - If the character is a newline character ('\n'), the `count_new_line` counter is incremented to count new lines.
    - If the character is a tab character ('\t'), the `count_tabulation` counter is incremented to count tabs.
    - If the character is a space character (' '), the `count_spaces` counter is incremented to count spaces.
    - If the character is 'q', the program exits by breaking out of the loop.
    - If the character is something else, an error message containing that character is printed.
4. After the loop finishes, the program displays the counting results, including the counts of spaces, tabs, and newlines.

The program successfully completes exercise 1.8, counting the occurrences of spaces, tabs, and newline characters in the
input data, and provides informative error messages as well as the ability to exit the program by entering 'q'.




**Упражнение 1.8. Напишите программу для подсчета пробелов, табуляций и новых строк.**

1. Объявляем переменные c, count_spaces, count_tabulation, и count_new_line для отслеживания количества символов 
   пробелов, табуляций и новых строк.
2. Затем начинается цикл while, который считывает символы из входного потока (стандартного ввода) с помощью функции 
   getchar(). Цикл продолжается до тех пор, пока не будет достигнут конец файла (EOF).
3. Внутри цикла проверяется каждый считанный символ:
   - Если символ - новая строка ('\n'), то увеличивается счетчик count_new_line для подсчета новых строк.
   - Если символ - табуляция ('\t'), то увеличивается счетчик count_tabulation для подсчета табуляций.
   - Если символ - пробел (' '), то увеличивается счетчик count_spaces для подсчета пробелов.
   - Если символ - 'q', то программа завершает выполнение, выходя из цикла.
   - Если символ - другой, выводится сообщение об ошибке, содержащее этот символ.
4. После завершения цикла, программа выводит на экран результаты подсчета, включая количество пробелов, табуляций и 
   новых строк.
Программа успешно выполняет упражнение 1.8, подсчитывая количество пробелов, табуляций и новых строк во входных данных, 
а также предоставляет информативные сообщения об ошибках и возможность завершить программу с помощью символа 'q'.