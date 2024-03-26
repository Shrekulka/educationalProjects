# Task:

#### Your task is to extend the existing FastAPI application by adding the following:
1. Define a Pydantic model named "User" in the models.py file with the following fields:
   - `name` (str)
   - `id` (int)
2. Import the models.py module into the main application file and create an instance of the User class with the 
   corresponding fields of the User model:
   - `name`: "John Doe"
   - `id`: 1
3. Implement a function that, upon receiving a GET request to the additional route /users, returns JSON data about the 
   user.

# Solution:

1. In the file src/models.py, a Pydantic model User is defined with the following fields:
   - name (str)
   - id (int)
2. In the src/main.py file, the models.py module is imported and an instance of the User class is created with the 
   corresponding fields:
   - name: "John Doe"
   - id: 1
A function get_user() is implemented, which upon receiving a GET request to the /users route returns JSON with data 
about the user (an instance of the User class).
The uvicorn library is used to run the application.
When running the application with the command uvicorn src.main:create_app --host 127.0.0.1 --port 5080, it will be 
available at http://127.0.0.1:5080/users/, and sending a GET request to this URL will return JSON with user data in the 
following format:
```bash
{"name":"John Doe","id":1}
```

## Project Structure:
```bash
📁 fastapi_project_skeleton/   # Root directory of the entire project
│
│
├── 📁 src/                    # Main directory with the source code of the application
│   │
│   ├── logger_config.py       # Logger configuration.
│   │ 
│   ├── main.py                # Main script to run the application.
│   │ 
│   └── models.py              # File with global models
│
├── README.md                  # Project description file.
│
└── requirements.txt           # Project dependencies file.   
```
Educational material on Stepik - https://stepik.org/course/179694/syllabus





# Задание:

#### Ваша задача состоит в том, чтобы расширить существующее приложение FastAPI, добавив в него следующее:
1. Определите в файле models.py Pydantic модель с именем "Пользователь" ("User") со следующими полями:
   - `name` (str)
   - `id` (int)

2. Импортируете модуль models.py в основной файл приложения и создайте в нем экземпляр класса User, с соответствующими 
   полями модели `User`:
   - `name`: "John Doe"
   - `id`: 1

3. Реализуйте функцию, которая при получении GET-запроса по дополнительному маршруту `/users` возвращала бы JSON с 
   данными о пользователе (юзере).

# Решение:
1. В файле src/models.py определена Pydantic модель User со следующими полями:
   - name (str)
   - id (int)
2. В файле src/main.py импортирован модуль models.py и создан экземпляр класса User с соответствующими полями:
   - name: "John Doe"
   - id: 1
Реализована функция get_user(), которая при получении GET-запроса по маршруту /users возвращает JSON с данными о 
пользователе (экземпляр класса User).
Для запуска приложения используется библиотека uvicorn.
При запуске приложения командой uvicorn src.main:create_app --host 127.0.0.1 --port 5080 оно будет доступно по адресу
http://127.0.0.1:5080/users/, и при отправке GET-запроса на этот URL будет возвращен JSON с данными о пользователе в
следующем формате:
```bash
{"name":"John Doe","id":1}
```

## Структура проекта:
```bash
📁 fastapi_project_skeleton/   # Корневая директория всего проекта
│
│
├── 📁 src/                    # Основная директория с исходным кодом приложения
│   │
│   ├── logger_config.py       # Конфигурация логгера.
│   │ 
│   ├── main.py                # Основной скрипт для запуска приложения.
│   │ 
│   └── models.py              # Файл с глобальными моделями
│
├── README.md                  # Файл с описанием проекта.
│
└── requirements.txt           # Файл с зависимостями проекта.   
```
Учебный материал на Stepik - https://stepik.org/course/179694/syllabus