# Creating and Working with a Database

## This code is designed to demonstrate the basics of working with an SQLite database in Python and includes the 
## following methods and functions:

1. main.py:
   main(): The main function that establishes a connection to the database, creates the 'users' table, generates and 
   inserts data, and performs various SQL queries.
2. utils.py:
   - fake_value(field_type): Generates values for different field types in the database.
   - generate_data_for_bd(cur, fields_and_types, num_records=10, seed=42): Generates and inserts random data into the 
     'users' table.
   - drop_table_if_exists(cur, table_name): Drops the 'users' table if it exists.
   - execute_and_log_query(cur, query): Executes an SQL query and logs the results.

## Project Structure:

   ```bash
   first_steps_with_SQLite/     # Main project folder.
   │
   ├── logger.py                # File with logger settings and functionality.
   │
   ├── main.py                  # Main application file, entry point.
   │
   ├── utils.py                 # Helper functions for the project.
   │
   ├── my_bd.db                 # Database file (SQLite).
   │
   ├── README.md                # Project description, usage instructions, and other useful information.
   │
   └── requirements.txt         # File containing project dependencies.
   
   ``` 
1. Establishes a connection to the database using a context manager with the 'my_bd.db' file (located in the same 
   directory as the executable file). If the database doesn't exist, it will be created. With this connection setup, 
   there is no need to explicitly close the connection; it will close automatically.
   ```bash
   with sq.connect("my_bd_2.db") as con:
   ```
   Alternatively (less reliable):
   Establishes a connection to the 'my_bd.db' database file (located in the same directory as the executable file). If 
   it doesn't exist, it will be created.
   ```bash
   con = sq.connect("my_bd.db")
   ```
   At the end of the code, the database is closed:
   ```bash
   con.close()
   ```
2. Uses an instance of the Cursor class to interact with the database:
   ```bash
   cur = con.cursor()
   ```
3. Creates a table 'users' if it doesn't exist (CREATE TABLE IF NOT EXISTS) with columns (user_id, name, gender, age, 
   score):
   ```bash
   cur.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                gender TEXT,
                age INTEGER NOT NULL DEFAULT 18,
                score INTEGER)""")
   ```bash 
   - user_id: an integer column, the primary key (PRIMARY KEY), and automatically incremented (AUTOINCREMENT).
   - name: a text column, cannot be empty (NOT NULL).
   - gender: a text column for gender.
   - age: an integer column for age with a default value of 18 if not specified.
   - score: an integer column for scores.
4. Drops the 'users' table if it exists:
   ```bash
   cur.execute("DROP TABLE users")
   ```
### Database Extensions:
   - .db
   - .db3
   - .sqlite
   - .sqlite3

### Data Types:
   - NULL: indicates the absence of a value.
   - INTEGER: represents an integer that can be positive or negative and may occupy 1, 2, 3, 4, 6, or 8 bytes depending 
     on its value.
   - REAL: represents a floating-point number, occupies 8 bytes in memory.
   - TEXT: a text string enclosed in single quotes, stored in the database's encoding (UTF-8, UTF-16BE, or UTF-16LE).
   - BLOB: binary data (small images).
   - 
## SELECT and INSERT Commands for Working with Database Tables

1. INSERT - adds a record to the table:
   ```bash
   INSERT INTO <table_name> (column_name1, column_name2, column_name3, ...) VALUES(<value1>, <value2>, <value3> ...)
   ```
   or if values are inserted into all fields in order (no need to specify fields):
   ```bash
   INSERT INTO <table_name> VALUES(<value1>, <value2>, <value3> ...)
   ```
   Examples:
   ```bash
   # Example of adding a record to the 'users' table with specific fields
   cur.execute("INSERT INTO users (name, gender, age, score) VALUES ('John Doe', 'Male', 30, 80)")
   
   # Example of adding a record to the 'users' table without specifying fields (in order)
   cur.execute("INSERT INTO users VALUES ('Jane Smith', 'Female', 25, 95)")
   ```
2. SELECT - retrieves data from the table (including creating a pivot selection from multiple tables):
   ```bash
   # Selecting specific columns from the table
   cur.execute("SELECT col1, col2, col3, ... FROM <table_name>")
   
   # Selecting all columns from the table
   cur.execute("SELECT * FROM <table_name>")
   
   # Selecting specific columns with a condition
   cur.execute("SELECT col1, col2, col3, ... FROM <table_name> WHERE <condition>")
   ```
   #### Query Examples:
   ```bash
   # Selecting specific columns from the 'users' table
   cur.execute("SELECT name, gender, age FROM users")  
   # Selecting all columns from the 'users' table
   cur.execute("SELECT * FROM users")  
   # Selecting records from 'users' with a condition score < 50
   cur.execute("SELECT * FROM users WHERE score < 50")  
   # Selecting records from 'users' with a condition score between 50 and 80
   cur.execute("SELECT * FROM users WHERE score BETWEEN 50 and 80")  
   # Selecting records from 'users' with a condition score equal to 60
   cur.execute("SELECT * FROM users WHERE score == 60")  
   # Selecting records from 'users' with a condition score equal to 60 and ordering by the age column in ascending order
   cur.execute("SELECT * FROM users WHERE score == 60 ORDER BY age")  
   # Selecting records from 'users' with a condition score equal to 60 and ordering by the age column, explicitly 
   # specifying ascending order
   cur.execute("SELECT * FROM users WHERE score == 60 ORDER BY age ASC")  
   # Selecting records from 'users' with a condition score equal to 60 and ordering by the name column in descending order
   cur.execute("SELECT * FROM users WHERE score == 60 ORDER BY name DESC")  
   # Selecting records from 'users' with a condition score equal to 60 and limiting the number of rows to 2
   cur.execute("SELECT * FROM users WHERE score == 60 LIMIT 2")  
   # Selecting records from 'users' with a condition score equal to 60 and limiting the number of rows to 2, skipping 
   # the first row
   cur.execute("SELECT * FROM users WHERE score == 60 LIMIT 2 OFFSET 1")  
   # Alternatively, we can write it like this
   cur.execute("SELECT * FROM users WHERE score == 60 LIMIT 1, 2") 
   ``` 
   ### Comparison Operators:
      = : Equal to <result_equal = cur.execute("SELECT * FROM users WHERE score = 60")>
      == : Equal to <result_equal = cur.execute("SELECT * FROM users WHERE score = 60")>
      : Greater than <result_greater_than = cur.execute("SELECT * FROM users WHERE score > 60")>
      < : Less than <result_less_than = cur.execute("SELECT * FROM users WHERE score < 60")>
      = : Greater than or equal to <result_greater_than_or_equal = cur.execute("SELECT * FROM users WHERE score >= 60")>
      <= : Less than or equal to <result_less_than_or_equal = cur.execute("SELECT * FROM users WHERE score <= 60")>
      != : Not equal to <result_not_equal = cur.execute("SELECT * FROM users WHERE score != 60")>
      BETWEEN : In range <result_between = cur.execute("SELECT * FROM users WHERE score BETWEEN 50 AND 80")>

   ### Additional Keywords:

   #### In SELECT, ORDER BY can be specified at the end:
   ORDER BY column_name1: sort by the specified column in ascending order
   ORDER BY column_name1 ASC: sort by the specified column, explicitly specifying ascending order
   ORDER BY column_name1 DESC: sort by the specified column in descending order
   In SELECT, LIMIT can be specified at the end:
   LIMIT <max>[OFFSET offset]: the number of rows to display or the first number of records to skip (offset) and then select the next number (max)
   LIMIT <offset, max> or write it like this (simple notation): offset (offset), number of records (max)

   #### After selection, call one of the following methods:
   a) fetchall to retrieve all results of SQL queries - result = cur.fetchall()
   ```bash
   cur.execute("SELECT * FROM users")
   result = cur.fetchall()
   print(result)  # gets a list of tuples
   ```
   or for large volumes to save memory:
   ```bash
   cur.execute("SELECT * FROM users")
   for result in cur:
   print(result)  # gets tuples
   ```
   b) fetchmany(size) - returns the specified number of records - result = cur.fetchmany(2)
   ```bash
   cur.execute("SELECT * FROM users")
   result = cur.fetchmany(2)
   print(result)  # gets a list of two tuples
   ```
   c) fetchone() - returns the first record
   ```bash
   cur.execute("SELECT * FROM users")
   result = cur.fetchone()
   print(result)  # gets the first record
   ```



# Создание и работа с BD

## Этот код создан для демонстрации основ работы с базой данных SQLite на языке Python и включает в себя следующие 
## методы и функции:
1. main.py:
   - main(): Основная функция, устанавливающая связь с базой данных, создающая таблицу 'users', генерирующая и 
     вставляющая 
  данные, а также выполняющая различные SQL-запросы.
2. utils.py:
   - fake_value(field_type): Генерация значений для различных типов полей в таблице.
   - generate_data_for_bd(cur, fields_and_types, num_records=10, seed=42): Генерация и вставка случайных данных в 
     таблицу 'users'.
   - drop_table_if_exists(cur, table_name): Удаление таблицы 'users', если она существует.
   - execute_and_log_query(cur, query): Выполнение SQL-запроса и логирование результатов.
   
## Структура проекта:
   ```bash
   first_steps_with_SQLite/     # Основна папка проекту.
   │
   ├── logger.py                # Файл с настройками и функциональностью логгера.
   │
   ├── main.py                  # Основной файл приложения, точка входа.
   │
   ├── utils.py                 # Вспомогательные функции для проекта.
   │
   ├── my_bd.db                 # Файл базы данных (SQLite).
   │
   ├── README.md                # Файл с описанием проекта, инструкциями по использованию и другой полезной информацией.
   │
   └── requirements.txt         # Файл, содержащий зависимости проекта.
   
   ```bash

1. Устанавливает связь, с помощью контекста менеджера, с BD - my_bd.db (находится в каталоге, где и исполняемый файл), 
   если ее нет, то создастся. При такой установке связи не нужно закрывать соединение, оно закроется автоматически
   ```bash
   with sq.connect("my_bd_2.db") as con:
   ```
   или второй вариант (менее надежный):
   Устанавливаем связь с BD (находится в каталоге, где и исполняемый файл), если ее нет, то создастся
   ```bash
   con = sq.connect("my_bd.db")
   ```
   В конце кода - закрываем BD
   ```bash
   con.close()
   ```
2. Для взаимодействия с BD используем экземпляр класса Cursor
   ```bash
   cur = con.cursor()
   ```
3. Cоздаем таблицу, если ее нет (CREATE TABLE IF NOT EXISTS), с таким именем - users и колонками (name,gender,age,score)
   ```bash
   cur.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                gender TEXT,
                age INTEGER NOT NULL DEFAULT 18,
                score INTEGER)""")
   ```
   - user_id - целочисленная колонка, являющаяся первичным ключом (PRIMARY KEY), и автоматически увеличиваемой 
     (AUTOINCREMENT)
   - name - текстовая колонка, не может быть пустой (NOT NULL)
   - gender - текстовая колонка для пола
   - age - целочисленная колонка для возраста, значение по умолчанию 18, если не указано
   - score - целочисленная колонка для баллов
   
4. Удаляем таблицу 'users', если она существует
   ```bash
   cur.execute("DROP TABLE users")
   ```

## Расширения BD:
   - .db
   - .db3
   - .sqlite
   - .sqlite3

## Типы данных:
   - NULL: указывает фактически на отсутствие значения
   - INTEGER: представляет целое число, которое может быть положительным и отрицательным и в зависимости от своего 
   значения может занимать 1, 2, 3, 4, 6 или 8 байт
   - REAL: представляет число с плавающей точкой, занимает 8 байт в памяти=
   - TEXT: строка текста в одинарных кавычках, которая сохраняется в кодировке базы данных (UTF-8, UTF-16BE или UTF-16LE)
   - BLOB: бинарные данные (небольшие изображения)

## Команды SELECT и INSERT при работе с таблицами БД
1. INSERT - добавление записи в таблицу
   ```bash
   INSERT INTO <table_name> (column_name1, column_name2, column_name3, ...) VALUES(<value1>, <value2>, <value3> ...)
   ```
   или если значения будем записывать во все поля по порядку (не указываем поля)
   ```bash
   INSERT INTO <table_name> VALUES(<value1>, <value2>, <value3> ...)
   ```
   ### Примеры:
   ```bash
   # Пример добавления записи в таблицу 'users' с указанием конкретных полей
   cur.execute("INSERT INTO users (name, gender, age, score) VALUES ('John Doe', 'Male', 30, 80)")
   
   # Пример добавления записи в таблицу 'users' без указания полей (по порядку)
   cur.execute("INSERT INTO users VALUES ('Jane Smith', 'Female', 25, 95)")
   ```
2. SELECT - выборка данных из таблицы(в том числе при создании сводной выборки из нескольких таблиц)
   
    ```bash
   # Выбор определенных столбцов из таблицы
   cur.execute("SELECT col1, col2, col3, ... FROM <table_name>")
   
   # Выбор всех столбцов из таблицы
   cur.execute("SELECT * FROM <table_name>")
   
   # Выбор определенных столбцов с условием
   cur.execute("SELECT col1, col2, col3, ... FROM <table_name> WHERE <условие>")
     ```
   #### Примеры запросов:
   ```bash
   # Выбор определенных столбцов из таблицы 'users'
   cur.execute("SELECT name, gender, age FROM users")  
   # Выбор всех столбцов из таблицы 'users'
   cur.execute("SELECT * FROM users")  
   # Выбор записей из 'users' с условием score < 50
   cur.execute("SELECT * FROM users WHERE score < 50")  
   # Выбор записей из 'users' с условием score между 50 и 80
   cur.execute("SELECT * FROM users WHERE score BETWEEN 50 and 80")  
   # Выбор записей из 'users' с условием score равным 60
   cur.execute("SELECT * FROM users WHERE score == 60")  
   # Выбор записей из 'users' с условием score равным 60 и сортировкой по столбцу age, по возрастанию
   cur.execute("SELECT * FROM users WHERE score == 60 ORDER BY age")  
   # Выбор записей из 'users' с условием score равным 60 и сортировкой по столбцу age, явно указываем по возрастанию
   cur.execute("SELECT * FROM users WHERE score == 60 ORDER BY age ASC")  
   # Выбор записей из 'users' с условием score равным 60 и сортировкой по столбцу name, по убыванию
   cur.execute("SELECT * FROM users WHERE score == 60 ORDER BY name DESC")  
   # Выбор записей из 'users' с условием score равным 60 и количеством строк, которое хотим выбрать = 2
   cur.execute("SELECT * FROM users WHERE score == 60 LIMIT 2")  
   # Выбор записей из 'users' с условием score равным 60 и количеством строк, которое хотим выбрать = 2, при этом - 
   # первая строка будет пропущена
   cur.execute("SELECT * FROM users WHERE score == 60 LIMIT 2 OFFSET 1")  
   # или можем это прописать так
   cur.execute("SELECT * FROM users WHERE score == 60 LIMIT 1, 2")  
   ```
   ### Операторы сравнения:
   - = : Равно <result_equal = cur.execute("SELECT * FROM users WHERE score = 60")>
   - == : Равно <result_equal = cur.execute("SELECT * FROM users WHERE score = 60")>
   - > : Больше <result_greater_than = cur.execute("SELECT * FROM users WHERE score > 60")>
   - < : Меньше <result_less_than = cur.execute("SELECT * FROM users WHERE score < 60")>
   - >= : Больше или равно <result_greater_than_or_equal = cur.execute("SELECT * FROM users WHERE score >= 60")>
   - <= : Меньше или равно <result_less_than_or_equal = cur.execute("SELECT * FROM users WHERE score <= 60")>
   - != : Не равно <result_not_equal = cur.execute("SELECT * FROM users WHERE score != 60")>
   - BETWEEN : В диапазоне <result_between = cur.execute("SELECT * FROM users WHERE score BETWEEN 50 AND 80")>
   
   ### Можно использовать следующее ключевые слова (расставлены по приоритету с самого высокого):
   - NOT : НЕ <result_not = cur.execute("SELECT * FROM users WHERE NOT score = 60")>
   - AND : И <result_and = cur.execute("SELECT * FROM users WHERE score > 50 AND age < 30")>
   - OR : ИЛИ <result_or = cur.execute("SELECT * FROM users WHERE score > 50 OR age < 30")>
   - IN : Входит в множество <result_in = cur.execute("SELECT * FROM users WHERE age IN (25, 30, 35)")>
   - NOT IN : Не входит в множество <result_not_in = cur.execute("SELECT * FROM users WHERE age NOT IN (25, 30, 35)")>

   ### Дополнительно:

   ### В SELECT в конце можно указать ORDER BY:
   - ORDER BY column_name1: сортировка по указанному столбцу, по возрастанию 
   - ORDER BY column_name1 ASC : сортировка по указанному столбцу, явно указываем по возрастанию 
   - ORDER BY column_name1 DESC: сортировка по указанному столбцу, по убыванию 

   ### В SELECT в конце можно указать LIMIT:
   - LIMIT <max>[OFFSET offset] - количество выводимых строк или первое количество записей (offset) хотим пропустить и 
     выбираем следующее количество (max)
     LIMIT <offset, max> или записать вот так (простая запись) - смещение (offset), количество записей (max)

3. После выборки, вызываем метод один из следующих методов:
   a) fetchall для получения всех результатов отбора sql запросов - result = cur.fetchall()
   ```bash
   cur.executer("SELECT * FROM users")
   result = cur.fetchall()
   print(result) # получаем список из кортежей
   ```
   или при больших объемах для экономии памяти 
   ```bash
   cur.executer("SELECT * FROM users")
   for result in cur
      print(result) # получаем кортежи 
   ```
   
   b) fetchmany(size) - возвращает число записей - size
   ```bash
   cur.executer("SELECT * FROM users")
   result = cur.fetchmany(2)
   print(result) # получаем список из двух кортежей
   ```
   
   с) fetchone() - возвращает первую запись
   ```bash
   cur.executer("SELECT * FROM users")
   result = cur.fetchone()
   print(result) # получаем первую запись
   ```