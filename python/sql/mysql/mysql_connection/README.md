This code is an example of a simple MySQL database program using the `pymysql` module.

The functions defined in the code perform the following tasks:

1. `create_table(connection)`: Creates a table named "users" if it does not exist. The table has four columns:
    "id" (auto-increment), "name", "password" and "email". The function executes a query to create a table and outputs
    successful creation message.

2. `insert_data(connection)`: Prompts the user for data (name, password, email) and inserts it into table "users". The 
    function executes a request to insert data and displays a message that the insert was successful.

3. `update_data(connection)`: Prompts the user for a user ID and a new password, then updates the password of the user
    with the specified id in the "users" table. The function executes a request to update the data and displays a 
    message that the update was successful.

4. `delete_data(connection)`: Prompts the user for a user ID and deletes the user with the specified ID from the "users"
    table. The function executes a request to delete data and displays a success message removal.

5. `drop_table(connection)`: Asks the user for confirmation to drop the "users" table. If the user agrees, the function 
    executes the request to delete the table and displays a message that the delete was successful. Otherwise in this 
    case, the function displays a message about canceling the deletion.

6. `select_all_data(connection)`: Retrieves all data from the "users" table and displays it. The function executes a 
    request for fetching the data and outputting each line of data to the console.

The `main()` function connects to the database using the specified parameters (host, user, password, database name) and
then brings up a menu for the user to select the action they want to perform (create table, add data, update data, 
delete data, delete table, retrieve all data, or program exit).

The entire program focuses on simple MySQL database operations and demonstrates the use of the `pymysql` module to
executing queries and interacting with the database.




Данный код представляет собой пример простой программы для работы с базой данных MySQL с использованием модуля `pymysql`.

Функции, определенные в коде, выполняют следующие задачи:

1. `create_table(connection)`: Создает таблицу с именем "users", если она не существует. Таблица имеет четыре столбца: 
    "id" (автоинкрементный), "name", "password" и "email". Функция выполняет запрос на создание таблицы и выводит 
    сообщение об успешном создании.

2. `insert_data(connection)`: Запрашивает у пользователя данные (имя, пароль, адрес электронной почты) и вставляет их в 
    таблицу "users". Функция выполняет запрос на вставку данных и выводит сообщение об успешном добавлении.

3. `update_data(connection)`: Запрашивает у пользователя идентификатор пользователя и новый пароль, а затем обновляет 
    пароль пользователя с указанным идентификатором в таблице "users". Функция выполняет запрос на обновление данных и 
    выводит сообщение об успешном обновлении.

4. `delete_data(connection)`: Запрашивает у пользователя идентификатор пользователя и удаляет пользователя с указанным 
    идентификатором из таблицы "users". Функция выполняет запрос на удаление данных и выводит сообщение об успешном 
    удалении.

5. `drop_table(connection)`: Запрашивает подтверждение пользователя для удаления таблицы "users". Если пользователь 
    соглашается, функция выполняет запрос на удаление таблицы и выводит сообщение об успешном удалении. В противном 
    случае функция выводит сообщение об отмене удаления.

6. `select_all_data(connection)`: Извлекает все данные из таблицы "users" и выводит их. Функция выполняет запрос на 
    извлечение данных и выводит каждую строку данных в консоли.

Функция `main()` осуществляет подключение к базе данных с использованием указанных параметров (хост, пользователь, 
пароль, имя базы данных), а затем выводит меню для пользователя, где он может выбрать действие, которое хочет выполнить 
(создание таблицы, добавление данных, обновление данных, удаление данных, удаление таблицы, извлечение всех данных или 
выход из программы).

Вся программа нацелена на простые операции с базой данных MySQL и демонстрирует использование модуля `pymysql` для 
выполнения запросов и взаимодействия с базой данных.