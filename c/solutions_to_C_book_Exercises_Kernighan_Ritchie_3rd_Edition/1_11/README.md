**Exercise 1.11. How to Test the Word Count Program? What Input Is Likely to Detect Errors if Any Were Made?**

**Solution:**

The program counts lines, words, and characters in the input data. Here's a brief description of the solution:

1. We use the header files `<stdio.h>` and `<ctype.h>`, which provide functionality for input-output and working with 
   characters, respectively.
2. We define two macros, `INSIDE_WORD` and `OUTSIDE_WORD`, to represent the states "inside a word" and "outside a word."
3. We initialize variables `currentChar`, `numberOfLines`, `numberOfWords`, `numberOfCharacters`, and `state`. 
   `currentChar` is used to store the current character, while `numberOfLines`, `numberOfWords`, and `numberOfCharacters`
   are used to count lines, words, and characters, respectively. `state` represents the current state, either inside a 
   word or outside a word, and it starts with the "outside word" state.
4. In a `while` loop, we read characters from the input until we encounter the 'q' character, which exits the program.
5. Inside the loop, we have several conditions:

   - We increment `numberOfCharacters` to count the total number of characters.

   - If the character is a newline `'\n'`, we increment the `numberOfLines` counter.

   - We use the `isalnum(currentChar) && !isdigit(currentChar)` function to check if the current character is a letter 
     (not a digit). If it is and the previous state was "outside word," we increment `numberOfWords`, and `state` is set
     to `INSIDE_WORD`. Otherwise, `state` is set to `OUTSIDE_WORD`.
6. After exiting the loop, we print the results of the count, including the number of lines, words, and characters.

You have conducted testing of the program by providing several input examples and obtaining the expected results, which 
is good. The input examples include various scenarios, such as lines with punctuation characters, empty lines, lines 
with multiple spaces and tabs. Such testing helps ensure the correctness of the program and identify potential errors.

**Note:** The 'q' character is used to exit the program and is not counted in the program's word count.

Example:
```
Hello World! This is a test.
q
Number of Lines: 1
Number of Words: 6
Number of Characters: 29
```

Example:
```
This text

has
multiple

lines.
q
Number of Lines: 6
Number of Words: 5
Number of Characters: 32
```

Example:
```
Input: Hello, World! 1234 @#$%
q
Number of Lines: 1
Number of Words: 3
Number of Characters: 31
```





**Упражнение 1.11. Как протестировать программу подсчета слов? Какой ввод вероятнее всего обнаружит ошибки, если они были 
допущены?**

**Решение:**

Программа выполняет подсчет строк, слов и символов во входных данных. Вот краткое описание решения:

1. Используем заголовочные файлы `<stdio.h>` и `<ctype.h>`, которые предоставляют функциональность для ввода-вывода и 
   работы с символами, соответственно.

2. Определили два макроса `INSIDE_WORD` и `OUTSIDE_WORD` для представления состояний "внутри слова" и "вне слова".

3. Инициализировали переменные `currentChar`, `numberOfLines`, `numberOfWords`, `numberOfCharacters` и `state`. 
   `currentChar` используется для хранения текущего символа, а `numberOfLines`, `numberOfWords` и `numberOfCharacters` 
   используются для подсчета строк, слов и символов соответственно. `state` представляет текущее состояние - внутри 
   слова или вне слова, и начинается с состояния "вне слова".

4. В цикле `while` считываем символы из ввода до тех пор, пока не встретится символ 'q', что приводит к выходу из 
   программы.

5. Внутри цикла есть несколько условий:

    - Инкрементируем `numberOfCharacters` для подсчета общего количества символов.

    - Если символ новой строки `'\n'`, то увеличивается счетчик строк `numberOfLines`.

    - Используем функцию `isalnum(currentChar) && !isdigit(currentChar)`, чтобы проверить, является ли текущий символ 
      буквой (не цифрой). Если это так и предыдущее состояние было "вне слова", то инкрементируется `numberOfWords`, и 
      `state` устанавливается в INSIDE_WORD. В противном случае `state` устанавливается в OUTSIDE_WORD.

6. После выхода из цикла выводим результаты подсчета, включая количество строк, слов и символов.

Провел тестирование программы, предоставив несколько примеров ввода и получив ожидаемые результаты, что хорошо. 
Примеры ввода включают в себя различные сценарии, такие как строки с символами пунктуации, пустые строки, строки с 
множеством пробелов и табуляций. Такое тестирование помогает убедиться в корректности работы программы и обнаружить 
возможные ошибки.


**`q` - это выход из программы и он не считается при подсчете в программе.**

Пример:
```
Hello World! This is a test.
q
Number of Lines: 1
Number of Words: 6
Number of Characters: 29
```
Пример:
```
This text

has
multiple

lines.
q
Number of Lines: 6
Number of Words: 5
Number of Characters: 32
```

Пример:
```
Input: Hello, World! 1234 @#$%
q
Number of Lines: 1
Number of Words: 3
Number of Characters: 31
```