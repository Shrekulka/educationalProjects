**Exercise 1.10. Write a program that copies input characters to the output stream, replacing tab characters with \t, 
backspace characters with \b, and each backslash with \\. This will make tab and backspace characters visible.**

**Solution:**
1. Declare a variable 'c' to read characters from the input stream.
2. Enter an infinite while loop that will run until the end of the file (EOF) is reached.
3. Inside the loop, check each read character:
    - If the character is a tab ('\t'), the program outputs a backslash ('\\') followed by 't'. This makes the tab 
      character visible as \t.
    - If the character is a backspace ('\b'), the program outputs a backslash ('\\') followed by 'b'. This makes the 
      backspace character visible as \b.
    - If the character is a backslash ('\\'), the program outputs two backslashes ('\\'). This makes the backslash 
      character visible as \\.
    - If the character is 'q', the program exits the while loop, allowing the user to terminate the program.
    - Otherwise (if the character doesn't match any of the above conditions), the program simply outputs the character 
      unchanged.
This solution makes tab and backspace characters visible when copying input characters to the output stream.





**Упражнение 1.10. Напишите программу, копирующую вводимые символы в выходной поток с заменой символа табуляции на \t, 
символа забоя на \b и каждой обратной наклонной черты на \\. Это сделает видимыми все символы табуляции и забоя.**

**Решение:**
1. Объявляем переменную 'c', которая будет использоваться для считывания символов из входного потока.
2. Входим в бесконечный цикл while, который будет выполняться до тех пор, пока не будет достигнут конец файла (EOF).
3. Внутри цикла проверяется каждый считанный символ:
   - Если символ равен табуляции ('\t'), программа выводит обратную косую черту ('\\') и символ 't'. Таким образом, 
     символ табуляции становится видимым как \t.
   - Если символ равен забою ('\b'), программа выводит обратную косую черту ('\\') и символ 'b'. Так символ забоя 
     становится видимым как \b.
   - Если символ равен обратной косой черте ('\\'), программа выводит две обратные косые черты ('\\'). Таким образом, 
     обратная косая черта становится видимой как \\.
   - Если символ равен 'q', программа выходит из цикла while, что позволяет пользователю завершить выполнение программы.
   - В противном случае (если символ не соответствует ни одному из вышеперечисленных условий), программа просто выводит 
     символ без изменений.
Это решение позволяет сделать символы табуляции, забоя и обратной косой черты более видимыми при копировании входных 
символов в выходной поток.