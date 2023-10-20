**Exercise 1.12.** Write a program that prints the contents of its input, placing one word per line.

**Solution:**
1. Define two macros, `INSIDE_WORD` and `OUTSIDE_WORD`, to represent the states "inside a word" and "outside a word."
2. Initialize the variable `currentChar` to store the current character and `state` to represent the current state 
   (starting with "outside a word").
3. Start an infinite `while` loop that will read characters from the input until the end of the file (EOF) is reached.
4. If the character 'q' is entered, the program terminates and exits the loop.
5. If the current character is a space, newline, or tab, we check the current state. If the previous state was "inside 
   a word," it means we have completed a word, so we add a newline character, and the state transitions to "outside a 
   word."
6. If the current character is not a separator and the previous state was "outside a word," it means we are starting a 
   new word. We transition the state to "inside a word" and print the current character.
7. If the current character is not a separator and the previous state was "inside a word," it means we are still inside 
   a word, so we simply print the current character.
8. After completing the loop, we print the counting results, including the number of lines, words, and characters.

This program breaks down the input into words, separating them with space, newline, or tab characters, and prints each 
word on a separate line.




**Упражнение 1.12. Напишите программу, которая печатает содержимое своего ввода, помещая по одному слову на каждой 
строке.**

**Решение:**
1. Определяем два макроса INSIDE_WORD и OUTSIDE_WORD, чтобы представлять состояния "внутри слова" и "вне слова".
2. Инициализируем переменную 'currentChar' для хранения текущего символа, 'state' для представления текущего состояния 
   (начинаем с "вне слова").
3. Запускаем бесконечный цикл while, который будет читать символы из ввода до достижения конца файла (EOF).
4. Если вводится символ 'q', программа завершает выполнение и выходит из цикла.
5. Если текущий символ - пробел, новая строка или табуляция, мы проверяем текущее состояние. Если предыдущее состояние 
   было "внутри слова", это означает, что мы завершили слово и добавляем символ новой строки, а состояние переходит в 
   "вне слова".
6. Если текущий символ не является разделителем и предыдущее состояние было "вне слова", это означает, что мы начали 
   новое слово. Мы переводим состояние в "внутри слова" и выводим текущий символ.
7. Если текущий символ не является разделителем и предыдущее состояние было "внутри слова", это означает, что мы все еще
   внутри слова, и мы просто выводим текущий символ.
8. После завершения цикла выводим результаты подсчета, включая количество строк, слов и символов.

Эта программа разбивает ввод на слова, разделяя их символами пробела, новой строки или табуляции, и выводит каждое слово
на отдельной строке.
