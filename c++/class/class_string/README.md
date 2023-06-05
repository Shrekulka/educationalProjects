Программа из листинга предлагает пользователю ввести до 10 поговорок. Каждая поговорка считывается во временный
символьный массив, а затем копируется в объект String. Если пользователь вводит пустую строку, оператор break завершает
цикл ввода. После вывода введенных данных программа использует функции-члены length ( ) и operator< ( ) для нахождения
самой короткой и самой первой в алфавитном порядке строки. Программа также применяет операцию индексации ( [ ] )
для того, чтобы разместить перед каждой поговоркой ее начальный символ. Рассмотрим пример выполнения этой программы:

Hi, what's your паmе? >> Мisty Gutz
Misty Gutz, please enter up to 10 short sayings <empty line to quit>:
1: а fool and his money are soon parted
2: penny wise , pound foolish
3: the love of money is the root of much evil
4: out of siqht, out of mind
5: aЬsence makes the heart qrow fonder
6: aЬsinthe makes the hart qrow fonder

Here are your sayings :
а: а fool and his money are soon parted
р: penny wise, pound foolish
t: the love of money is the root of much evil out of sight, out of mind
о: out of siqht, out of mind
а: absence makes the heart grow fonder absinthe makes the hart grow fonder
а: aЬsinthe makes the hart qrow fonder
Shortest saying:
penny wise, pound foolish First alphabetically:
First alphabetically:
а fool and his money are soon parted
This program used 11 String objects. Вуе.