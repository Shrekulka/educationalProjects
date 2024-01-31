# Commands for Modifying and Deleting Records in the Table.

## This Python script interacts with an SQLite database, performing the following tasks:

1. Establishes a connection to the SQLite database using a context manager. If the database does not exist, it will be 
   created.
2. Creates a 'users' table with specific fields (user_id, name, gender, age, score) if it does not already exist.
3. Checks if the 'users' table is empty and, if so, generates and inserts 10 random records into the table.
4. Executes various SQL queries to modify data in the table:
   - Resets the values in the 'score' column for all players.
   - Increases the values in the 'score' column by 100 for female players.
   - Increases the values in the 'score' column by 7 for a player named 'David Guzman'.
   - Increases the values in the 'score' column by 15 for players whose names start with the letter 'A'.
   - Deletes records from the table where user_id is equal to 2 or 5.
5. Logs the results of each SQL query and checks and displays information about the structure and content of the table.
6. Handles and logs errors, including tracking the stack for detailed error information.

In summary, this code is designed to demonstrate working with an SQLite database in Python, including creating, 
modifying data, and executing queries such as UPDATE and DELETE.

## Project Structure:
    ```bash
    commands_when_work_with_tables/  # Main project folder for working with tables.
    │
    ├── logger.py                    # File with logger settings and functionality.
    │
    ├── main.py                      # Main application file, the entry point.
    │
    ├── utils.py                     # Auxiliary functions for the project.
    │
    ├── my_bd.db                     # Database file (SQLite).
    │
    ├── README.md                    # Project description file with usage instructions.
    │
    └── requirements.txt              # File containing project dependencies.
    ```
1. UPDATE - Modifying data in records.
    ```bash
    # Update the value in the 'name_column' column in the 'name_table' table when the 'condition' is met.
    UPDATE name_table SET name_column = new_value WHERE condition
    # If you need to change values in multiple columns, use the following syntax:
    # Update values in the 'name_column1' and 'name_column2' columns in the 'name_table' table when the 'condition' is met.
    UPDATE name_table SET name_column1 = new_value1, name_column2 = new_value2 WHERE condition;
    ```
    #### Example:
    ```bash
    # Reset scores for all players
    cur.execute("UPDATE users SET score = 0")
    # Increase scores by 100 for female players
    cur.execute("UPDATE users SET score = score + 100 WHERE gender = 'Female'")
    # Increase scores by 7 for David Guzman
    cur.execute("UPDATE users SET score = score + 7 WHERE name LIKE 'David Guzman'")
    # Execute SELECT to verify that the data has been reset
    cur.execute("SELECT * FROM users")
    result = cur.fetchall()
    for row in result:
      print(row)
    ```
    #### After the LIKE operator (resource-intensive operator), we can specify both a string (field value) and a pattern.

    a) String:
        ```bash
        cur.execute("UPDATE users SET score = score + 7 WHERE name LIKE 'David Guzman'")
        ```
    b) Pattern. In the pattern, you can use the following characters:
        '%' - any continuation of the string
        '_' - any single character
        ```bash
        # Add 15 points to anyone whose name starts with the letter 'A'
        cur.execute("UPDATE users SET score = score + 15 WHERE name LIKE 'A%'")
        ```
2. DELETE - Deleting records from the table.
    ```bash
    # Delete data from the 'name_table' table based on the specified 'condition'.
    DELETE FROM name_table WHERE condition
    ```
    #### Example:
    ```bash
    # Delete records where user_id is 2 or 5
    cur.execute("DELETE FROM users WHERE user_id IN (2, 5)")
    ```



# Команды для изменения и удаления записей в таблице.

## Этот код представляет собой скрипт Python для работы с базой данных SQLite. Он выполняет следующие задачи:

1. Устанавливает связь с базой данных SQLite с использованием контекста менеджера. Если базы данных не существует, то 
   она будет создана.
2. Создает таблицу 'users' с определенными полями (user_id, name, gender, age, score), если она еще не существует.
3. Проверяет, пуста ли таблица 'users', и если да, то генерирует и вставляет 10 случайных записей в таблицу.
4. Выполняет различные SQL-запросы для изменения данных в таблице:
   - Обнуляет значения в столбце 'score' для всех игроков.
   - Увеличивает значения в столбце 'score' на 100 для игроков женского пола.
   - Увеличивает значения в столбце 'score' на 7 для игрока с именем 'David Guzman'.
   - Увеличивает значения в столбце 'score' на 15 для игроков, имена которых начинаются с буквы 'A'.
   - Удаляет записи из таблицы, у которых user_id равен 2 или 5.
5. Логгирует результаты выполнения каждого SQL-запроса, а также проверяет и выводит информацию о структуре таблицы и ее 
   содержимом.
6. Обрабатывает и логгирует ошибки, включая отслеживание стека для подробной информации об ошибках.

В целом, данный код предназначен для демонстрации работы с базой данных SQLite на языке Python, включая создание, 
изменение данных и выполнение запросов, используя такие команды как UPDATE и DELETE.

## Структура проекта:
    ```bash
    commands_when_work_with_tables/  # Основная папка проекта для работы с таблицами.
    │
    ├── logger.py                    # Файл с настройками и функциональностью логгера.
    │
    ├── main.py                      # Основной файл приложения, точка входа.
    │
    ├── utils.py                     # Вспомогательные функции для проекта.
    │
    ├── my_bd.db                     # Файл базы данных (SQLite).
    │
    ├── README.md                    # Файл с описанием проекта, инструкциями по использованию.
    │
    └──requirements.txt              # Файл, содержащий зависимости проекта.
    ```

1. UPDATE - изменение данных в записях.
    ```bash
    # Обновление значения в столбце name_column в таблице name_table при выполнении условия condition.
    UPDATE name_table SET name_column = new_value WHERE condition
    # Если необходимо изменить значения в нескольких столбцах, используем следующий синтаксис:
    # Обновление значений в столбцах name_column1 и name_column2 в таблице name_table при выполнении условия condition.
    UPDATE name_table SET name_column1 = new_value1, name_column2 = new_value2 WHERE condition;
    ```
   #### Пример:
   ```bash
   # обнулим значения для всех игроков
   cur.execute("UPDATE users SET score = 0")
   # для женского пола очки увеличим на 100
   cur.execute("UPDATE users SET score = score + 100 WHERE gender = 'Female'")
   # для David Guzman увеличим очки на 7
   cur.execute("UPDATE users SET score = score + 7 WHERE name LIKE 'David Guzman'")
   # Выполним SELECT, чтобы убедиться, что данные были обнулены
   cur.execute("SELECT * FROM users")
   result = cur.fetchall()
   for row in result:
     print(row)
   ```
   #### После оператора LIKE (ресурсоемкий оператор) можем прописывать как строку (значение поля), так и шаблон
   a) Строка:
   ```bash
   cur.execute("UPDATE users SET score = score + 7 WHERE name LIKE 'David Guzman'")
   ```
   b) Шаблон. В шаблоне можно использовать следующие символы:
   - '%' - любое продолжение строки
   - '_' - любой один символ
   ```bash
   # добавим 15 очков любому, чье имя начинается с буквы 'A'
   cur.execute("UPDATE users SET score = score + 15 WHERE name LIKE 'A%'")
   ```

2. DELETE - удаление записей из таблицы.
   ```bash
   # Удаление данных из таблицы 'name_table' по заданному условию 'condition'
   DELETE FROM name_table WHERE condition
   ```
   #### Пример:
   ```bash
   # Удалим записи у тех у кого user_id равен 2 и 5
   cur.execute("DELETE FROM users WHERE user_id IN (2, 5)")
   ```