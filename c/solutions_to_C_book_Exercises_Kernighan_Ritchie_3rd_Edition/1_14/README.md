**1.14. Write a program that prints histograms of the frequency of input characters.**

**Solution:**

1. Include the `<ctype.h>` header to use the `isalpha` function, which checks if a character is alphabetic.
2. Define the constant `SIZE` as 256. This is the size of the array that will be used to count the frequency of 
   characters. In this case, we assume the use of the standard ASCII encoding, which includes 256 different characters.
3. Declare variables:
    - `currentChar` to store the currently read character.
    - `charFreq` - an array for counting the frequency of characters. Each element of the array corresponds to the ASCII
      code of a character, and we will increase the corresponding element when encountering a character.
    - `otherCharCount` to count characters that are not letters.
4. Enter a `while` loop that continues until the end of the file (EOF) is reached. Inside the loop:
    - Read a character from the input and store it in the `currentChar` variable.
    - Check if the character entered is 'q' to exit the program.
5. Check that the value of `currentChar` is in the range from 0 to `SIZE` (256). This is necessary to ensure that the 
   character is within the ASCII code range.
6. If the character is within the ASCII code range:
    - Check if the character is alphabetic using the `isalpha(currentChar)` function. If it is, increase the 
      corresponding element in the `charFreq` array for that letter.
    - Otherwise (if the character is not a letter), increase `otherCharCount` to count other characters.
7. After inputting characters, print the header "Histogram of frequency of occurrence of letters:".
8. Then, iterate through the `charFreq` array and print a histogram for each character that has been encountered at 
   least once:
    - For each character where `charFreq[i] > 0`, print the character and asterisks representing its frequency.
    - The number of asterisks printed corresponds to the frequency of the character.
9. Print the header "Frequency of other symbols:" and output the count of other characters (non-letters) that were not 
   included in the histogram.
This program analyzes input characters, counts their frequency of occurrence, builds a histogram for alphabetical 
characters, and outputs the count of other characters that are not letters.




**1.14. Напишите программу, печатающую гистограммы частот встречаемости вводимых символов.**

**Решение:**

1. <ctype.h>` для использования функции `isalpha`, которая проверяет, является ли символ буквой.
2. Определяем константу `SIZE` как 256. Это размер массива, который будет использоваться для подсчета частоты 
   встречаемости символов. В данном случае, мы предполагаем использование стандартной кодировки ASCII, которая включает 
   256 различных символов.
3. Объявляем переменные:
    - `currentChar` для хранения текущего считанного символа.
    - `charFreq` - массив для подсчета частоты встречаемости символов. Каждый элемент массива соответствует ASCII-коду 
       символа, и мы будем увеличивать соответствующий элемент при встрече символа.
    - `otherCharCount` для подсчета символов, которые не являются буквами.
4. Входим в цикл `while`, который продолжается до достижения конца файла (EOF). Внутри цикла:
    - Читаем символ из ввода и сохраняем его в переменной `currentChar`.
    - Проверяем, если введен символ 'q', то завершаем программу.
5. Проверяем, что значение `currentChar` находится в диапазоне от 0 до `SIZE` (256). Это необходимо, чтобы убедиться, 
   что символ находится в пределах ASCII-кода.
6. Если символ находится в пределах ASCII-кода:
    - Проверяем, является ли символ буквой, используя функцию `isalpha(currentChar)`. Если это так, то увеличиваем 
      соответствующий элемент массива `charFreq` для этой буквы.
    - В противном случае (если символ не является буквой), увеличиваем `otherCharCount` для подсчета других символов.
7. После завершения ввода символов, выводим заголовок "Histogram of frequency of occurrence of letters:".
8. Затем перебираем массив `charFreq` и выводим гистограмму для каждого символа, который был встречен хотя бы раз:
    - Для каждого символа, у которого `charFreq[i] > 0`, выводим символ и звездочки, представляющие его частоту.
    - Звездочки выводятся в количестве, соответствующем частоте символа.
9. Выводим заголовок "Frequency of other symbols:" и выводим количество других символов (не букв), которые не были 
   учтены в гистограмме.
Эта программа анализирует вводимые символы, подсчитывает их частоту встречаемости и строит гистограмму для буквенных 
символов, а также выводит количество других символов, которые не являются буквами.