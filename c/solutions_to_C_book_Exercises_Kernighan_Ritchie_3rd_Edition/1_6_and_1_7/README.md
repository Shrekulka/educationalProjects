**Exercise 1.6. Verify that the expression getchar() != EOF yields a value of 0 or 1.**
**Exercise 1.7. Write a program that prints the value of EOF.**

1. In the while loop, use getchar() to read characters from the input stream (stdin). The loop continues executing until
   the end of file (EOF) is reached.
2. If the character read is a newline character ('\n'), the loop is terminated using break, and the program stops reading.
3. The characters read, except for newline characters ('\n'), are echoed back to the screen using putchar(c).
4. After the while loop, use (c != EOF) to output the result of the expression (getchar() != EOF), which will have a 
   value of either 0 if EOF is reached or 1 if it is not.
5. Also, output the value of EOF, which is usually -1.
The program successfully completes exercises 1.6 and 1.7 and provides clear comments to understand what is happening.




**Упражнение 1.6. Убедитесь в том, что выражение getchar() != EOF получает значение 0 или 1.**
**Упражнение 1.7. Напишите программу, печатающую значение EOF.**

1. В цикле while, используем getchar() для чтения символов из входного потока (stdin). Цикл продолжает выполнение до 
   тех пор, пока не будет достигнут конец файла (EOF).
2. Если считанный символ - символ новой строки ('\n'), то цикл прерывается с помощью break, и программа завершает чтение.
3. Считанные символы, за исключением символов новой строки ('\n'), выводятся обратно на экран с помощью putchar(c).
4. После цикла while используем (c != EOF) для вывода результата выражения (getchar() != EOF), которое будет иметь 
   значение либо 0, если достигнут конец файла, либо 1, если нет.
5. Также выводите значение EOF, которое обычно равно -1.
Программа выполняет упражнения 1.6 и 1.7 успешно и предоставляет четкие комментарии для понимания того, что происходит.