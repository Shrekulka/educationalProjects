# Task:
We have a file with a large set of integers (the file can be downloaded from the link: link).

## Task - find the following four/six values:
1. Maximum number in the file;
2. Minimum number in the file;
3. Median (https://goo.gl/hiCwVw);
4. Mean (average) value (https://goo.gl/XJeAjZ);
5*. The longest sequence of numbers (that go one after the other) which increases (optional);
6*. The longest sequence of numbers (that go one after the other) which decreases (optional).

The proposed solution method should find all four/six values from the file in no more than 90 seconds. This condition is
optional, but it will be a significant advantage if your solution meets it.

## Additional Information:

- Median: If the set of numbers has an even number of elements, then to determine the median, the sum of two adjacent 
  values should be used. For example, in the set {1, 8, 14, 19}, the median will be 11 (because 0.5*(8+14)=11).
- Sequence of numbers: This refers to the order of numbers in the file that go one after the other. Even randomly 
  generated datasets may have quite long sequences. For example, an increasing sequence may look like this: -4390, -503,
  3, 16, 5032.

You are practically unrestricted in the choice of method and approach to solving the problem. You can use any means, 
methods, approaches (except for the two restrictions listed below) to solve the task. You can write a program in any 
programming language you know, or you can use existing programs/utilities. Of course, you can use ready-made sets of 
statistical classes/functions/libraries, but this is not the best option.

## There are only two limitations to consider when choosing a solution method:

### Limitation #1:
Any person should be able to use your method. This means, for example, if you used your own program to solve the task, 
any other person should be able to compile/run it, etc.; if you used third-party programs/utilities, then any person 
should be able to install and use them; also, any person may take a completely different file with a different set of 
integers and find all four specified values.

### Limitation #2:
When solving the task, you cannot use illegal software (proprietary software that has been cracked, pirated copies of 
software, etc.). Also, if you borrowed the idea of the solution, software, or source code (or any part of it) from 
another person/colleague/the internet/anywhere else, please mention the source.

# The proposed solution is a program for analyzing numeric data from a file. It includes a set of functions that perform 
# various tasks related to number analysis:

1. Getting numeric data from a file:
   The get_numbers_from_file() function is responsible for loading the file from the specified source and extracting 
   numbers from it for further analysis.
2. Finding the maximum and minimum numbers:
   The find_max_number() and find_min_number() functions determine the largest and smallest numbers in the list, 
   respectively.
3. Calculating the median and mean (average) value:
   The find_median() and find_average() functions perform calculations for the median (the central value of an ordered 
   list of numbers) and the mean (the sum of all numbers divided by their count), respectively.
4. Determining the longest sequences of increasing and decreasing numbers:
   The find_longest_sequence() function identifies sequences of numbers that go one after the other and finds the 
   longest sequences that increase and decrease.
5. Additionally, the program includes error handling and outputs detailed logs containing information about the 
   execution time of each operation.

The result of this program is a comprehensive and accurate analysis of numeric data from the file, as well as clear and 
informative reporting for the user.

## Project Structure:
```bash
📁 numeric_data_file_analyzer               # Root directory of the project
 │
 ├── main.py                                # Main module of the program
 │
 ├── requirements.txt                       # File containing project dependencies
 │
 ├── logger_config.py                       # Logger configuration
 │
 ├── README.md                              # Project description file
 │
 ├── 📁 config_data/                        # Directory containing configuration module
 │   ├── __init__.py                        # Initialization file for the package
 │   └── config_data.py                     # Module for configuration
 │
 └── 📁 services/                           # Directory containing services
     ├── __init__.py                        # Initialization file for the directory
     └── number_analyzer.py                 # Module for number analysis
```




# Завдання:
У нас є файл, з  великим набором цілих чисел (файл можна скачати за посиланням: 
https://drive.google.com/file/d/1LxSB6UEAVK0NLgU0ah5y0CBbD0gL_oO9/ ).

## Завдання - знайти наступні чотири/шість значень:
    1. максимальне число в файлі;
    2. мінімальне число в файлі;
    3. медіану ( https://goo.gl/hiCwVw );
    4. середнє арифметичне значення ( https://goo.gl/XJeAjZ );
    5*. найбільшу послідовність чисел (які ідуть один за одним), яка збільшується (опціонально)
    6*. найбільшу послідовність чисел (які ідуть один за одним), яка зменьшується (опціонально)

Запропонований метод рішення повинен знаходити всі чотири/шість величин з файлу не більше ніж за 90 секунд. Ця умова
є необов'язковою, однак буде істотним плюсом, якщо ваше рішення буде її задовольняти.

## Додаткова інформація:
- Медіана: Якщо в наборі чисел парна кількість елементів, то для визначення медіани повинна використовуватися 
  півсума двох сусідніх значень. Тобто наприклад, у наборі {1, 8, 14, 19} медіаною буде 11 (бо 0.5*(8+14)=11).

- Послідовність чисел - це порядок чисел у файлі, що йдуть один за одним. Навіть випадкові генеровані набори даних 
  можуть мати досить довгі послідовності. Наприклад, зростаюча послідовність може виглядати так: -4390, -503, 3, 16,
  5032

Ви практично не обмежені у виборі методу та способу вирішення задачі. Ви можете використовувати будь-які засоби, 
методи, підходи (крім двох обмежень, що наведені нижче). Ви можете написати програму будь-якою відомою вам мовою 
програмування, або можете використовувати наявні програми/утиліти. Звісно, ви можете використовувати готові набори 
статистичних класів/функцій/бібліотек, але це не найкращий варіант.

## Існують лише такі обмеження, які слід враховувати при виборі способу вирішення задачі:

### Обмеження #1:
Будь-яка людина повинна мати можливість скористатися вашим методом. Це означає, наприклад, якщо для вирішення 
завдання Ви використовували свою власну програму, то будь-яка інша людина повинна мати можливість її скомпілювати/
запустити і т.д.; якщо Ви використовували сторонні програми/утиліти, то будь-яка людина повинна мати можливість їх 
також встановити та користуватися; також будь-яка людина може взяти зовсім інший файл з іншим набором цілих чисел і
знайти всі чотири вказані величини);
    
### Обмеження #2:
при вирішенні задачі не можна використовувати нелегальне програмне забезпечення (пропрієтарне ПЗ, яке зазнало злому,
піратські копії ПЗ, тощо). Також якщо ви запозичили ідею рішення, ПЗ або вихідні джерела (або якусь їх частину) у 
друга/колеги/в інтернеті/де-завгодно, то згадайте джерело.

# Запропоноване рішення представляє собою програму для аналізу числових даних з файлу. Вона включає в себе низку 
# функцій, які виконують різні завдання з аналізу чисел:

  1. Отримання числових даних з файлу:
     Функція get_numbers_from_file() відповідає за завантаження файлу з вказаного джерела та витягування чисел з цього 
     файлу для подальшого аналізу.
  2. Знаходження максимального та мінімального чисел:
     Функції find_max_number() та find_min_number() визначають найбільше та найменше число в списку відповідно.
  3. Обчислення медіани та середнього арифметичного значення:
     Функції find_median() та find_average() виконують обчислення медіани (центрального значення впорядкованого списку 
     чисел) та середнього арифметичного (сума всіх чисел, поділена на їх кількість) відповідно.
  4. Визначення найдовших послідовностей зростаючих та спадаючих чисел:
     Функція find_longest_sequence() визначає послідовності чисел, що йдуть одне за одним, та знаходить найдовші 
     послідовності, які зростають і спадають.
  5. Крім того, програма включає обробку можливих помилок та виведення детальних журналів, які містять інформацію про
     час виконання кожної операції.
    
    Результатом роботи цієї програми є повний та коректний аналіз числових даних з файлу, а також зрозуміла та 
    інформативна звітність для користувача.



## Структура проекту:
```bash
📁 numeric_data_file_analyzer               # Коренева тека всього проекту
 │
 ├── main.py                                # Основний модуль програми
 │
 ├── requirements.txt                       # Файл залежностей проекту.
 │
 ├── logger_config.py                       # Конфігурація логгера.
 │
 ├── README.md                              # Файл з описом проекту.
 │
 ├── 📁 config_data/                        # Тека з модулем конфігурації 
 │   ├── __init__.py                        # Файл-ініціалізатор пакету. 
 │   └── config_data.py                     # Модуль для конфігурації 
 │
 └── 📁 services/                           # Тека з сервісами
     ├── __init__.py                        # Файл-ініціалізатор теки. 
     └── number_analyzer.py                 # Модуль для аналізу чисел
```