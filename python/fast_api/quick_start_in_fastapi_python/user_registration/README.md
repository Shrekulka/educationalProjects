# Task:
Your task is to create a FastAPI endpoint that accepts a POST request with user data in the request body.
##### User data should include the following fields:
- `name` (str): User's name (required).
- `email` (str): User's email address (required and must have a valid email format).
- `age` (int): User's age (optional but must be a positive integer if provided).
- `is_subscribed` (bool): Flag indicating whether the user is subscribed to a newsletter (optional).

1. Define a Pydantic model named `UserCreate` to represent user data. Apply appropriate validation rules to ensure data 
   correctness.
2. Create a POST route `/create_user` that accepts JSON data according to the `UserCreate` model.
3. Implement a function to handle incoming user data and return a response with the received user information.
    ##### Example:
    JSON Request:
    ```bash
    {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "is_subscribed": true
    }
    ```
    JSON Response:
    ```bash
    {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "is_subscribed": true
    }
    ```
Please test your implementation using tools such as "curl", Postman, or any other API client to submit user data and 
verify the response.

## Solution Description:

In the `models.py` file, a Pydantic model named `UserCreate` was defined to describe the data structure for storing user
information.
The model contains attributes `name`, `email`, `age`, and `is_subscribed`, corresponding to user data fields, with 
appropriate validation rules applied.
In the `main.py` file, a function `create_app()` was created, which creates a FastAPI instance and sets up routes to 
handle requests. This function includes routes to get a list of created users and add a new user based on the provided 
data. User data is stored in a list to track all created users.

### Steps to Test Your Application Using Postman:

#### POST Verification Algorithm:
1. Start your FastAPI application.
2. Open Postman and create a new request.
3. Set the request type to POST.
4. Enter the URL of your route `/create_user`, for example:
    ```bash
    http://127.0.0.1:5080/create_user.
    ```
5. Select the Body tab, then select raw, and ensure that JSON format is selected.
6. In the request body, enter JSON data representing the user, for example:
    ```bash
    {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "is_subscribed": true
    }
    ```
7. Click the "Send" button.
8. You should receive a JSON response from your application confirming successful user creation, for example:
    ```bash
    {
        "message": "Thank you, Alice!"
    }
    ```
    Thus, data about the new user has been successfully added to the database.

#### GET Verification Algorithm:
1. Set the request type to GET.
2. Enter the URL of your route `/create_user`, for example:
    ```bash
    http://127.0.0.1:5080/create_user
    ```
3. Click the "Send" button.
4. You should receive a JSON response from your application containing a list of all created users, stored in the
   database.
   Example response:
   ```bash
       [
           {
               "name": "Bro",
               "email": "bro@example.com",
               "age": 18,
               "is_subscribed": false
           },
           {
               "name": "Alice",
               "email": "alice@example.com",
               "age": 30,
               "is_subscribed": true
           }
       ...
       ]
   ```
## Project Structure:
```bash
📁 feedback_service/              # Root directory of the entire project
│
├── README.md                     # Project description file
│
├── requirements.txt              # File listing project dependencies
│
└── 📁 src/                       # Main directory containing the application source code
    │
    ├── logger_config.py          # Module for configuring logging
    │
    ├── main.py                   # Main module containing the FastAPI application code
    │
    └── models.py                 # Module containing the Pydantic model for feedback
```





# Задание:
Ваша задача - создать конечную точку FastAPI, которая принимает POST-запрос с данными о пользователе/юзере в теле 
запроса. 
##### Пользовательские данные должны включать следующие поля:
- `name` (str): Имя пользователя (обязательно).
- `email` (str): адрес электронной почты пользователя (обязателен и должен иметь допустимый формат электронной почты).
- `age` (int): возраст пользователя (необязательно, но должно быть положительным целым числом, если указано).
- `is_subscribed` (bool): Флажок, указывающий, подписан ли пользователь на новостную рассылку (необязательно).

1. Определите Pydantic модель с именем `UserCreate` для представления данных о пользователе. Применяйте соответствующие 
   правила проверки, чтобы обеспечить правильность данных.
2. Создайте маршрут POST `/create_user`, который принимает данные JSON в соответствии с моделью `UserCreate`.
3. Реализуйте функцию для обработки входящих пользовательских данных и возврата ответа с полученной пользовательской 
   информацией.
    ##### Пример:
    Запрос JSON:
    ```bash
    {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "is_subscribed": true
    }
    ```
    Ответ JSON:
    ```bash
    {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "is_subscribed": true
    }
    ```
Пожалуйста, протестируйте свою реализацию, используя такие инструменты, как "curl", Postman или любой другой клиент API,
чтобы отправить пользовательские данные и проверить ответ.

## Описание решения:

В файле models.py была определена Pydantic модель UserCreate, которая описывает структуру данных для хранения информации
о пользователе. Модель содержит атрибуты name, email, age и is_subscribed, соответствующие полям данных о пользователе, 
с применением соответствующих правил проверки.

В файле main.py была создана функция create_app(), которая создает экземпляр FastAPI и настраивает маршруты для 
обработки запросов. Эта функция включает маршруты для получения списка созданных пользователей и добавления нового 
пользователя на основе переданных данных. Данные пользователей сохраняются в списке для отслеживания всех созданных 
пользователей.

### Шаги для тестирования нашего приложения через Postman:

#### Алгоритм проверки "POST":
1. Запустите ваше приложение FastAPI.
2. Откройте Postman и создайте новый запрос.
3. Укажите тип запроса как POST.
4. Введите URL вашего маршрута /create_user, например:
    ```bash
    http://127.0.0.1:5080/create_user.
    ```
5. Выберите вкладку Body, затем выберите raw, и убедитесь, что выбран формат JSON.
6. В теле запроса введите JSON-данные, представляющие пользователя, например:
    ```bash
    {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "is_subscribed": true
    }
    ```
7. Нажмите кнопку "Send" (Отправить).
8. Вы должны получить ответ от вашего приложения в формате JSON, подтверждающий успешное создание пользователя, например:
    ```bash
    {
        "message": "Thank you, Alice!"
    }
    ```
    Таким образом, данные о новом пользователе были успешно добавлены в базу данных.

#### Алгоритм проверки "GET":
1. Укажите тип запроса как GET.
2. Введите URL вашего маршрута /create_user, например:
    ```bash
    http://127.0.0.1:5080/create_user
    ```
3. Нажмите кнопку "Send" (Отправить).
4. Вы должны получить ответ от вашего приложения в формате JSON, содержащий список всех созданных пользователей, 
   сохраненных в базе данных.
   Пример ответа:
   ```bash
       [
           {
               "name": "Bro",
               "email": "bro@example.com",
               "age": 18,
               "is_subscribed": false
           },
           {
               "name": "Alice",
               "email": "alice@example.com",
               "age": 30,
               "is_subscribed": true
           }
       ...
       ]
   ```
## Структура проекта:
```bash
📁 feedback_service/              # Корневая директория всего проекта
│
├── README.md                     # Файл с описанием проекта
│
├── requirements.txt              # Файл с перечнем зависимостей проекта
│
└── 📁 src/                       # Основная директория с исходным кодом приложения
    │
    ├── logger_config.py          # Модуль для настройки логирования
    │
    ├── main.py                   # Основной модуль, содержащий код FastAPI приложения
    │
    └── models.py                 # Модуль, содержащий Pydantic модель для отзыва
```