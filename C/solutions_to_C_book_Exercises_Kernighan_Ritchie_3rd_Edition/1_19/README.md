**Exercise 1.19:** Write a function `reverse(s)` that reverses the characters in a string `s`. Apply this function to a 
program that reverses each input line.

**Solution:**

1. Read input lines from the user and store them in reverse order.
2. Terminate the program upon detecting a 'q' character at the beginning of a line.

The program uses a dynamic array (buffer) that automatically expands as needed to accommodate strings of varying lengths.
Here's a more detailed description of the steps:

1. Variable initialization:
    - `character`: holds the current read character.
    - `i`: character counter in the current line.
    - `size`: initial buffer size for storing the line (1024 characters).
    - `current_line`: pointer to the current line (dynamic array).
2. Enter a `while` loop that runs until the end of the file (EOF) is reached, reading characters from the keyboard.
3. If a 'q' character is detected at the beginning of a line and `i` is 0, the program frees memory and exits.
4. If the current line has reached the buffer size limit (`i == size - 1`), double the buffer size, and reallocate memory
   to ensure enough space.
5. Upon encountering a newline character '\n', the program terminates the current line, calls the `reverse` function to 
   reverse the line, and then prints the result to the screen. After this, the character counter `i` is reset to process
   the next line.
6. Otherwise, the character is added to the current line, and the character counter `i` is incremented.
7. The `reverse` function reverses the characters in a string by iterating through half of the string and swapping 
   characters from the beginning and end of the string.
8. After the loop finishes, the allocated memory is freed.
This allows the program to read input lines from the user, reverse them, and display the result on the screen. When a 'q'
character is entered at the beginning of a line, the program exits.




**Упражнение 1.19. Напишите функцию reverse(s), размещающую символы в строке s в обратном порядке. Примените ее при 
написании программы, которая каждую вводимую строку располагает в обратном порядке.**

**Решение:**

1. Считывает строки с ввода пользователя и сохраняет их в обратном порядке.
2. При обнаружении символа 'q' в начале строки завершает программу.

Программа использует динамический массив (буфер), который автоматически расширяется по мере необходимости, чтобы 
обеспечить хранение строк переменной длины. Вот более подробное описание шагов:

1. Инициализация переменных:
    - `character`: хранит текущий считанный символ.
    - `i`: счетчик символов в текущей строке.
    - `size`: начальный размер буфера для хранения строки (1024 символа).
    - `current_line`: указатель на текущую строку (динамический массив).
2. Вход в цикл `while`, который выполняется до достижения конца файла (EOF), считывая символы с клавиатуры.
3. Если в начале строки обнаружен символ 'q' и `i` равно 0, программа освобождает память и завершает выполнение.
4. Если текущая строка достигла предела размера буфера (`i == size - 1`), размер буфера удваивается, и память для буфера
   перераспределяется, чтобы обеспечить достаточно места.
5. При считывании символа новой строки '\n', программа завершает текущую строку, вызывает функцию `reverse` для разворота
   строки в обратном порядке, а затем выводит результат на экран. После этого счетчик символов `i` сбрасывается для 
   обработки следующей строки.
6. В противном случае символ добавляется в текущую строку, и счетчик символов `i` увеличивается.
7. Функция `reverse` выполняет разворот строки в обратном порядке, пробегая половину строки и обменивая символы с начала
   и конца строки.
8. После завершения цикла освобождается выделенная память.
Это позволяет программе считывать строки с ввода пользователя, разворачивать их в обратном порядке и выводить результат 
на экран. Когда символ 'q' вводится в начале строки, программа завершает выполнение.