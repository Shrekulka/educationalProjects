# Task:

Your task is to create a FastAPI application that implements cookie-based authentication.
## Complete the following steps:
1. Create a simple login route at "/login" that accepts a username and password as form data. If the credentials are 
   valid, set a secure HTTP cookie with the name "session_token" and a unique value.
2. Implement a protected route at "/user" that requires authentication using the "session_token" cookie. If the cookie 
   is valid and contains correct authentication data, return a JSON response with user profile information.
3. If the "session_token" cookie is missing or invalid, the "/user" route should return an error response with a status
   code of 401 (Unauthorized) or a message {"message": "Unauthorized"}.

#### Example:
POST request to /login with form data:
```bash
{
  "username": "user123",
  "password": "password123"
} 
```
The response should contain a "session_token" cookie.

GET request to /user with a "session_token" cookie:
```bash
session_token: "abc123xyz456"
```
The response should return user profile information.

GET request to /user without a "session_token" cookie or with an invalid cookie, for example:
```bash
session_token: "invalid_token_value"
```
The response should return an error message with a status code of 401 or a message {"message": "Unauthorized"}.

Please test your implementation using tools such as "curl", Postman, or any other API client to verify the cookie-based 
authentication functionality.

# Solution:

This FastAPI application implements cookie-based authentication.
It consists of two main routes:

1. POST /login: This route is for user login. It accepts a username and password as form data. If the credentials are 
   valid, a secure cookie named "session_token" with a unique session token value is set.
2. GET /user: This protected route requires authentication using the "session_token" cookie. If the cookie is valid and 
   contains correct authentication data, a JSON response with user profile information is returned. Otherwise, an error
   response with a status code of 401 (Unauthorized) is returned.

# Testing:

1. POST http://127.0.0.1:5080/login
    Request body (raw JSON):
    ```bash
    {
      "username": "user123",
      "password": "password123"
    } 
    ```
    Response body (Pretty JSON):
    ```bash
    {
        "session_token": "b9a734a77e66472a74318da10d3285087cf34d61c4ba1ee0cf9c31b516bc4317"
    }
    ```
2. GET http://127.0.0.1:5080/login
    Request header:
    ```bash
    {
        "session_token": "b9a734a77e66472a74318da10d3285087cf34d61c4ba1ee0cf9c31b516bc4317"
    }
    ```
    Response body (Pretty JSON):
    ```bash
    {
        "user": {
            "username": "user123",
            "password": "password123",
            "session_token": "b9a734a77e66472a74318da10d3285087cf34d61c4ba1ee0cf9c31b516bc4317"
        }
    }
    ```
## Project Structure:
```bash
📁 feedback_service/              # Root directory of the project
│
├── README.md                     # File containing project description
│
├── requirements.txt              # File listing project dependencies
│
└── 📁 src/                       # Main directory containing source code of the application
    │
    ├── database.py               # List of dictionaries containing product data
    │
    ├── logger_config.py          # Module for configuring logging
    │
    ├── main.py                   # Main module containing FastAPI application code
    │
    ├── utils.py                  # File containing helper functions
    │
    └── models.py                 # Module containing Pydantic model for feedback
```




# Задача:
Ваша задача - создать приложение FastAPI, которое реализует аутентификацию на основе файлов cookie. 
## Выполните следующие действия:
1. Создайте простой маршрут входа в систему по адресу "/login", который принимает имя пользователя и пароль в качестве 
   данных формы. Если учетные данные действительны, установите безопасный файл cookie только для HTTP с именем 
   "session_token" с уникальным значением.
2. Реализуйте защищенный маршрут в "/user", который требует аутентификации с использованием файла cookie "session_token".
   Если файл cookie действителен и содержит правильные данные аутентификации, верните ответ в формате JSON с информацией
   профиля пользователя.
3. Если файл cookie "session_token" отсутствует или недействителен, маршрут "/user" должен возвращать ответ об ошибке с 
   кодом состояния 401 (неавторизован) или сообщение {"message": "Unauthorized"}.

#### Пример:
POST-запрос в `/login` с данными формы:
```bash
{
  "username": "user123"
  "password": "password123"
} 
```
Ответ должен содержать файл cookie "session_token".

GET-запрос к `/user` с помощью файла cookie "session_token":
```bash
session_token: "abc123xyz456"
```
Ответ должен возвращать информацию профиля пользователя.

GET-запрос к `/user` без файла cookie "session_token" или с недопустимым файлом cookie, например:
```bash
session_token: "invalid_token_value"
```
Ответ должен возвращать сообщение об ошибке с кодом состояния 401 или сообщение {"message": "Unauthorized"}.

Пожалуйста, протестируйте свою реализацию с помощью таких инструментов, как "curl", Postman или любой другой клиент API,
чтобы проверить функциональность аутентификации на основе файлов cookie.

# Решение:
Данное приложение FastAPI реализует аутентификацию на основе файлов cookie. 
Оно состоит из двух основных маршрутов:
1. POST /login: Этот маршрут предназначен для входа пользователя в систему. Он принимает имя пользователя и пароль в 
   качестве данных формы. Если учетные данные действительны, устанавливается безопасный файл cookie с именем 
   "session_token", содержащий уникальное значение сессионного токена.
2. GET /user: Этот защищенный маршрут требует аутентификации с использованием файла cookie "session_token". Если файл 
   cookie действителен и содержит правильные данные аутентификации, возвращается ответ в формате JSON с информацией 
   профиля пользователя. В противном случае возвращается ответ об ошибке с кодом состояния 401 (неавторизован).

# Тестирование:
1. POST http://127.0.0.1:5080/login
   Тело запроса (raw JSON):
   ```bash
   {
     "username": "user123",
     "password": "password123"
   } 
   ```
   Тело ответа (Pretty JSON):
   ```bash
   {
       "session_token": "b9a734a77e66472a74318da10d3285087cf34d61c4ba1ee0cf9c31b516bc4317"
   }
   ```

2. GET http://127.0.0.1:5080/login
   Заголовок запроса:
   ```bash
   {
       "session_token": "b9a734a77e66472a74318da10d3285087cf34d61c4ba1ee0cf9c31b516bc4317"
   }
   ```
   Тело ответа (Pretty JSON):
   ```bash
   {
       "user": {
           "username": "user123",
           "password": "password123",
           "session_token": "b9a734a77e66472a74318da10d3285087cf34d61c4ba1ee0cf9c31b516bc4317"
       }
   }
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
    ├── database.py               # Список словарей, которые содержат данные о продуктах
    │
    ├── logger_config.py          # Модуль для настройки логирования
    │
    ├── main.py                   # Основной модуль, содержащий код FastAPI приложения
    │
    ├── utils.py                  # Файл с вспомогательными функциями
    │
    └── models.py                 # Модуль, содержащий Pydantic модель для отзыва
```