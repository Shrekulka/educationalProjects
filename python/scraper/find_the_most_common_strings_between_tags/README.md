#Task: Finding frequently occurring lines of code on a web page

The file https://stepik.org/media/attachments/lesson/209719/2.html contains a Wikipedia article about the Python 
language. In this article uses code tags to distinguish constructs in the Python language. You need to find all the 
lines contained between the <code> and </code> tags, determine those lines that occur most often and output them to 
alphabetically, separated by spaces.

Input example:

```
Copy code
<code>a</code>
<a>bracadabr</a>
<code>c</code>
<code>b</code>
<code>b</code>
<code>c</code>
```
Sample output:

```
b c
```
Two approaches can be used to solve the problem:

1. Web scraping using the requests library and regular expressions.
2. Web scraping using the requests library and a structured approach.





#Задача: Поиск часто встречающихся строк кода на веб-странице

Файл https://stepik.org/media/attachments/lesson/209719/2.html содержит статью с Википедии про язык Python. В этой 
статье используются теги code, которыми выделяются конструкции на языке Python. Вам необходимо найти все строки, 
содержащиеся между тегами <code> и </code>, определить те строки, которые встречаются чаще всего, и вывести их в 
алфавитном порядке, разделяя пробелами.

Пример входных данных:

```
Copy code
<code>a</code>
<a>bracadabr</a>
<code>c</code>
<code>b</code>
<code>b</code>
<code>c</code>
```
Пример вывода:

```
b c
```
Для решения задачи можно использовать два подхода:

1. Веб-скрейпинг с использованием библиотеки requests и регулярных выражений.
2. Веб-скрейпинг с использованием библиотеки requests и структурированного подхода.