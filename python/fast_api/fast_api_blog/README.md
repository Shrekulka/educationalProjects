# Exercise:
You should implement field validation and use dependency injection where eve
The Application should be connected to a MySQL DB so you should implement pydantic anc sqlalchemy schemas accordingly
You should implement the task in a MVC Design pattern. 

## Requirements:
1. Use Python and FastAPI to build the application.
2. Implement four endpoints: "signup", "login", "addPost", and "getPosts".
3. All endpoints should have appropriate input and output data using Pydantic schemas with type validation.
4. Implement authentication for the "addPost" and "getPosts" endpoints using a token obtained from the "login" endpoint.
5. If the token is not provided or invalid, the "addPost" and "getPosts" endpoints should return an appropriate error 
   response.
6. The "addPost" endpoint should save the post in memory and return the postID (can be a randomly generated string or 
   integer).
7. The "getPosts" endpoint should return all posts added by the user.
8. Implement request validation to limit the size of the payload for the "addPost" endpoint. The payload should not 
   exceed 1 MB in size, and if it does, return an appropriate error response.
9. Implement response caching for the "getPosts" endpoint, so that consecutive requests for the same user's posts return
   cached data for up to 5 minutes. Use an in-memory cache like `cachetools` for this purpose.
10. Add an additional endpoint called "deletePost" that accepts a postID and token and deletes the corresponding post 
    from memory. If the token is missing or invalid, return an appropriate error response.

## Endpoints:
1. **Signup Endpoint:**
   - Accepts email and password.
   - Returns a token (can be a randomly generated string or JWT).

2. **Login Endpoint:**
   - Accepts an email and password.
   - Returns a token (can be a randomly generated string or JWT) upon successful login.
   - Returns an appropriate error response if login fails.

3. **AddPost Endpoint:**
   - Accepts text and a token (to authenticate the request).
   - Validates the payload size and saves the post in memory, returning the postID (can be a randomly generated string or integer).
   - If the token is missing or invalid, return an appropriate error response.
   - Use dependency injection to manage token authentication.

4. **GetPosts Endpoint:**
   - Accepts a token (to authenticate the request).
   - Returns all posts added by the user.
   - If the token is missing or invalid, return an appropriate error response.
   - Use dependency injection to manage token authentication.
   - Implement response caching for consecutive requests from the same user for up to 5 minutes.

5. **DeletePost Endpoint:**
   - Accepts a postID and token (to authenticate the request).
   - Deletes the corresponding post from memory.
   - If the token is missing or invalid, return an appropriate error response.
   - Use dependency injection to manage token authentication.

## Pydantic Schemas:

Define schemas to all that is necessary.

## Instructions:
1. Use dependency injection to manage token authentication for the "addPost", "getPosts", and "deletePost" endpoints.
2. Define the necessary Pydantic schemas for input validation with appropriate type validation.
3. Implement the four endpoints with the specified functionality and authentication logic.
4. Implement request validation for the "addPost" endpoint to limit payload size.
5. Implement response caching for the "getPosts" endpoint.
6. Implement the "deletePost" endpoint to allow users to delete their posts.
7. Add documentation and comments as necessary to explain your code.

Please ensure that you utilize dependency injection to handle authentication for the "addPost" and "getPosts" endpoints,
and validate the Pydantic schemas with appropriate types. 

Feel free to add documentation and comments as necessary to explain your code. If you have any further questions or need
any additional clarifications, feel free to ask! Happy coding!


# Solution:

### This solution applies the MVC (Model-View-Controller) design pattern.
By doing so, we divided the responsibilities between models, controllers, and views, thereby improving code organization
and simplifying its further development and maintenance.

#### The project is divided into the following modules:
1. *config_data*: Contains the configuration file (config.py), where important application settings are stored, such as 
   database connection parameters, secret key, and encryption algorithm.
2. *controllers*: Contains the logic of controllers, which handle requests processing and interact with data models.
3. *database*: Contains modules for working with the database, including SQLAlchemy initialization and session retrieval.
4. *models*: Contains SQLAlchemy data model definitions, which map to tables in the database.
5. *schemas*: Defines Pydantic schemas for input data validation and object serialization/deserialization.
6. *utils*: Contains auxiliary modules, such as a cache module (cache.py), an authentication module (auth.py), and a 
   logging module (logger_config.py).
7. *views*: Contains FastAPI routers that define endpoints for handling HTTP requests.

##### Configuration
The *config_data* module defines a *Settings* class, which inherits from *pydantic.BaseSettings*. This class contains 
fields for storing important application settings such as database connection parameters, secret key, and encryption 
algorithm. The values of these settings are loaded from the .env file using Pydantic functionality.

##### Database and Data Models
The *database* module initializes SQLAlchemy and creates tables in the database. Data models are defined in the *models*
module using SQLAlchemy's declarative style.

###### Main Models:
- *User*: Represents the users table with fields for email, password, and hashed password.
- *Post*: Represents the posts table with fields for text, title, content, status, and a relationship with the User 
  model (foreign key).
- *TokenTable*: Represents the tokens table with fields for access token, refresh token, status, and a relationship with
  the User model (foreign key).

##### Pydantic Schemas
The *schemas* module defines Pydantic schemas for input data validation and object serialization/deserialization.
###### Main Schemas:
- *UserCreate*: Schema for creating a new user with *email* and *password* fields.
- *LoginRequest*: Schema for logging in with *email* and *password* fields.
- *PostCreate*: Schema for creating a new post with *text* and *status* fields.
- *Post*: Schema for representing a post with *id*, *text*, *status*, *created_date*, and *updated_date* fields.
Schemas use Pydantic validators to check the correctness of data, such as password length and email format.

##### Controllers
###### The *controllers* module defines handler functions for core application operations:
- *auth_controller.py*: Contains functions for registration, logging in, and token refreshing.
- *post_controller.py*: Contains functions for creating, retrieving, and deleting posts.
These functions interact with SQLAlchemy data models, perform necessary business logic, and return corresponding HTTP 
responses.

##### Views
The *views* module defines FastAPI routers that bind URL paths to corresponding handler functions from controllers.
###### Main Routers:
- *auth_views.py*: Defines endpoints for registration, logging in, and token refreshing.
- *post_views.py*: Defines endpoints for creating, retrieving, and deleting posts.
Routers use dependency injection to pass necessary objects, such as database session instances and current user objects,
to handler functions.

##### Authentication and Authorization
The *utils/auth.py* module contains functions for working with access and refresh tokens, as well as for extracting the 
current user from the access token.
Authentication and authorization are implemented using JSON Web Tokens (JWT). Upon registration and logging in, access 
and refresh tokens are generated and returned to the client.
For protected endpoints (creating, retrieving, and deleting posts), the *get_current_user* dependency from *auth.py* 
module is used. This dependency extracts the current user from the access token passed in the Authorization header. If 
the access token is missing or invalid, the dependency generates an appropriate HTTP error.

##### Caching
The *utils/cache.py* module contains functions for caching a user's post list. Caching is implemented using a simple 
Python dictionary, where the key is the user's email and the value is a tuple containing the list of posts and the cache
expiration time.
When retrieving posts (*get_posts_handler*), it first checks if there are cached data for the current user. If cached 
data exists and has not expired (cache lifetime - 5 minutes), it is returned. Otherwise, posts are fetched from the 
database and saved in the cache.
When creating or deleting a post, the cache for the current user is cleared.

##### Logging
The *utils/logger_config.py* module configures a logger to track errors and important events in the application. The 
logger uses Python's built-in logging module and writes messages to the console.

##### Migrations
To manage database migrations, Alembic is used. Migrations allow safely applying changes to the database schema and 
updating existing databases.
In the *migrations* directory, you can find migration scripts generated by Alembic. The main migration script 
*4ff27af43811_initial_migration.py* creates indexes for the *posts* table.
To run migrations, Alembic commands are used, such as *alembic upgrade head*.

##### Running the Application
The entry point to the application is located in the *main.py* file. In this file, an instance of FastAPI is created, 
routers for endpoints are connected, and the FastAPI server is started.
To run the application, execute the command *uvicorn main:app --reload* in the terminal. This command will start the 
FastAPI server in development mode with automatic reloading when the code changes.
After the server is started, you can test the application's endpoints by sending HTTP requests using API testing tools 
like Postman or curl.

## Project Structure:
```bash
📁 fast_api_blog/           # Main project directory.
│
├── 📁 config_data/         # Package for configuration data.
│   ├── __init__.py         # Marks the directory as a Python package.
│   └── config.py           # Module containing configuration data.
│
├── 📁 controllers/         # Directory for application controllers.
│   ├── __init__.py         # Initialization of the controllers module.
│   ├── auth_controller.py  # Controller for user authentication.
│   └── post_controller.py  # Controller for handling posts.
│
├── 📁 database/            # Package for modules related to database operations.
│   ├── __init__.py         # Initialization of the database package.
│   ├── database.py         # Module for establishing database connection.
│   └── session.py          # Module for working with database sessions.
│
├── 📁 migrations/          # Directory for database migrations.
│   ├── 📁versions/         # Directory containing migration versions.
│   ├── env.py              # Script for handling migrations.
│   ├── README              # File describing migrations.
│   └── script.py.mako      # Template for creating migration scripts.
│
├── 📁 models/              # Package for data models.
│   ├── __init__.py         # Initialization of the models package.
│   └── models.py           # Module with data model definitions.
│
├── 📁 schemas/             # Package for data schemas.
│   ├── __init__.py         # Initialization of the schemas package.
│   ├── auth.py             # Module with authentication data schemas.
│   └── posts.py            # Module with post data schemas.
│
├── 📁 utils/               # Package for utility functions.
│   ├── __init__.py         # Initialization of the utils package.
│   ├── auth.py             # Module with authentication utilities.
│   ├── cache.py            # Module for caching functionality.
│   └── logger_config.py    # Module for logging configuration.
│
├── 📁 views/               # Package for views.
│   ├── __init__.py         # Initialization of the views package.
│   ├── auth_views.py       # Module with views for authentication.
│   └── post_views.py       # Module with views for handling posts.
│
├── .env                    # Configuration and secrets file.
│ 
├── .gitignore              # File specifying intentionally untracked files to ignore.
│ 
├── alembic.ini             # Alembic configuration file for managing migrations.
│
├── main.py                 # Main application module.
│
├── requirements.txt        # File containing project dependencies.
│
└──  README.md              # Project information.
```





# Задание:
Необходимо реализовать валидацию полей и использовать внедрение зависимостей там, где это возможно.
Приложение должно быть подключено к базе данных MySQL, поэтому вам нужно реализовать схемы pydantic и sqlalchemy 
соответственно.
Вы должны реализовать задачу в шаблоне проектирования MVC.

## Требования:
1. Используйте Python и FastAPI для создания приложения.
2. Реализуйте четыре конечные точки: "signup", "login", "addPost" и "getPosts".
3. Все конечные точки должны иметь соответствующие входные и выходные данные с использованием схем Pydantic с валидацией
   типов.
4. Реализуйте аутентификацию для конечных точек "addPost" и "getPosts" с использованием токена, полученного из конечной
   точки "login".
5. Если токен не предоставлен или недействителен, конечные точки "addPost" и "getPosts" должны вернуть соответствующий 
   ответ об ошибке.
6. Конечная точка "addPost" должна сохранять сообщение в памяти и возвращать postID (может быть случайно сгенерированной
   строкой или целым числом).
7. Конечная точка "getPosts" должна возвращать все сообщения, добавленные пользователем.
8. Реализуйте валидацию запроса для ограничения размера полезной нагрузки для конечной точки "addPost". Размер полезной
   нагрузки не должен превышать 1 МБ, и если это происходит, верните соответствующий ответ об ошибке.
9. Реализуйте кэширование ответа для конечной точки "getPosts", чтобы последующие запросы на сообщения того же 
   пользователя возвращали кэшированные данные до 5 минут. Для этой цели используйте кэш в памяти, такой как cachetools.
10. Добавьте дополнительную конечную точку с именем "deletePost", которая принимает postID и токен, а затем удаляет 
    соответствующее сообщение из памяти. Если токен отсутствует или недействителен, верните соответствующий ответ об 
    ошибке.

## Конечные точки:
1. Конечная точка регистрации (Signup Endpoint):
    - Принимает электронную почту и пароль.
    - Возвращает токен (может быть случайно сгенерированной строкой или JWT).
2. Конечная точка входа (Login Endpoint):
    - Принимает электронную почту и пароль.
    - При успешном входе в систему возвращает токен (может быть случайно сгенерированной строкой или JWT).
    - При неудачной попытке входа в систему возвращает соответствующий ответ об ошибке.
3. Конечная точка добавления сообщения (AddPost Endpoint):
    - Принимает текст и токен (для аутентификации запроса).
    - Проверяет размер полезной нагрузки и сохраняет сообщение в памяти, возвращая postID (может быть случайно 
      сгенерированной строкой или целым числом).
    - Если токен отсутствует или недействителен, возвращает соответствующий ответ об ошибке.
    - Используйте внедрение зависимостей для управления аутентификацией токена.
4. Конечная точка получения сообщений (GetPosts Endpoint):
    - Принимает токен (для аутентификации запроса).
    - Возвращает все сообщения, добавленные пользователем.
    - Если токен отсутствует или недействителен, возвращает соответствующий ответ об ошибке.
    - Используйте внедрение зависимостей для управления аутентификацией токена.
    - Реализуйте кэширование ответа для последующих запросов от одного и того же пользователя до 5 минут.
5. Конечная точка удаления сообщения (DeletePost Endpoint):
    - Принимает postID и токен (для аутентификации запроса).
    - Удаляет соответствующее сообщение из памяти.
    - Если токен отсутствует или недействителен, возвращает соответствующий ответ об ошибке.
    - Используйте внедрение зависимостей для управления аутентификацией токена.
   
## Схемы Pydantic:
Определите схемы для всего необходимого.

## Инструкции:
1. Используйте внедрение зависимостей для управления аутентификацией токена для конечных точек "addPost", "getPosts" и 
   "deletePost".
2. Определите необходимые схемы Pydantic для валидации входных данных с соответствующей валидацией типов.
3. Реализуйте четыре конечные точки с указанной функциональностью и логикой аутентификации.
4. Реализуйте валидацию запроса для конечной точки "addPost" для ограничения размера полезной нагрузки.
5. Реализуйте кэширование ответа для конечной точки "getPosts".
6. Реализуйте конечную точку "deletePost", чтобы пользователи могли удалять свои сообщения.
7. Добавьте документацию и комментарии по необходимости, чтобы объяснить свой код.

Пожалуйста, убедитесь, что вы используете внедрение зависимостей для обработки аутентификации для конечных точек 
"addPost" и "getPosts", и проверяете схемы Pydantic с соответствующими типами.

Не стесняйтесь добавлять документацию и комментарии по необходимости, чтобы объяснить свой код. Если у вас есть 
дополнительные вопросы или нужны дополнительные пояснения, не стесняйтесь спрашивать! Удачи в кодинге!

# Решение:

### В данном решении применен шаблон проектирования MVC (Model-View-Controller).
Таким образом, мы разделили ответственность между моделями, контроллерами и представлениями, тем самым улучшили 
организацию кода и упростили его дальнейшее развитие и сопровождение.

#### Проект разделен на следующие модули:
1. *config_data*: Содержит файл конфигурации (config.py), где хранятся важные настройки приложения, такие как параметры 
   подключения к базе данных, секретный ключ и алгоритм шифрования.
2. *controllers*: Содержит логику контроллеров, которые отвечают за обработку запросов и взаимодействие с моделями данных.
3. *database*: Содержит модули для работы с базой данных, включая инициализацию SQLAlchemy и получение сессий.
4. *models*: Содержит определения моделей данных SQLAlchemy, которые отображаются на таблицы в базе данных.
5. *schemas*: Определяет схемы Pydantic для валидации входных данных и сериализации/десериализации объектов.
6. *utils*: Содержит вспомогательные модули, такие как модуль для работы с кэшем (cache.py), модуль для аутентификации 
   (auth.py) и модуль для логгирования (logger_config.py).
7. *views*: Содержит маршрутизаторы FastAPI, которые определяют конечные точки (endpoints) для обработки HTTP-запросов.

##### Конфигурация
В модуле *config_data* определен класс *Settings*, который наследуется от *pydantic.BaseSettings*. Этот класс содержит 
поля для хранения важных настроек приложения, таких как параметры подключения к базе данных, секретный ключ и алгоритм 
шифрования. Значения этих настроек загружаются из файла .env с помощью функциональности Pydantic.

##### База данных и модели данных
В модуле *database* происходит инициализация SQLAlchemy и создание таблиц в базе данных. Модели данных определены в 
модуле *models* с использованием декларативного стиля SQLAlchemy.

###### Основные модели:
- *User*: Представляет таблицу пользователей с полями для email, пароля и хешированного пароля.
- *Post*: Представляет таблицу постов с полями для текста, заголовка, содержания, статуса и связью с моделью User 
  (внешний ключ).
- *TokenTable*: Представляет таблицу токенов с полями для токена доступа, токена обновления, статуса и связью с моделью 
  User (внешний ключ).

##### Схемы Pydantic
В модуле *schemas* определены схемы Pydantic для валидации входных данных и сериализации/десериализации объектов. 
###### Основные схемы:
- *UserCreate*: Схема для создания нового пользователя с полями *email* и *password*.
- *LoginRequest*: Схема для запроса входа в систему с полями *email* и *password*.
- *PostCreate*: Схема для создания нового поста с полями *text* и *status*.
- *Post*: Схема для представления поста с полями *id*, *text*, *status*, *created_date* и *updated_date*.
Схемы используют валидаторы Pydantic для проверки корректности данных, таких как длина пароля и формат электронной почты.

##### Контроллеры
###### В модуле *controllers* определены функции-обработчики для основных операций приложения:
- *auth_controller.py*: Содержит функции для регистрации, входа в систему и обновления токенов.
- *post_controller.py*: Содержит функции для создания, получения и удаления постов.
Эти функции взаимодействуют с моделями данных *SQLAlchemy*, выполняют необходимую бизнес-логику и возвращают 
соответствующие HTTP-ответы.

##### Представления (Views)
В модуле *views* определены маршрутизаторы FastAPI, которые связывают URL-пути с соответствующими функциями-обработчиками
из контроллеров.
###### Основные маршрутизаторы:
- *auth_views.py*: Определяет конечные точки для регистрации, входа в систему и обновления токенов.
- *post_views.py*: Определяет конечные точки для создания, получения и удаления постов.
Маршрутизаторы используют dependency injection для передачи необходимых объектов, таких как экземпляры сессии базы 
данных и объекты текущего пользователя, в функции-обработчики.

##### Аутентификация и авторизация
Модуль *utils/auth.py* содержит функции для работы с токенами доступа и обновления, а также для извлечения текущего 
пользователя из токена доступа.
Аутентификация и авторизация реализованы с использованием JSON Web Tokens (JWT). При регистрации и входе в систему 
генерируются токены доступа и обновления, которые возвращаются клиенту.
Для защищенных конечных точек (создание, получение и удаление постов) используется зависимость *get_current_user* из 
модуля *auth.py*. Эта зависимость извлекает текущего пользователя из токена доступа, переданного в заголовке 
Authorization. Если токен доступа отсутствует или недействителен, зависимость генерирует соответствующую HTTP-ошибку.

##### Кэширование
Модуль *utils/cache.py* содержит функции для кэширования списка постов пользователя. Кэширование реализовано с 
использованием простого словаря Python, где ключом является email пользователя, а значением - кортеж, содержащий список
постов и время кэширования.
При получении постов (*get_posts_handler*) сначала проверяется, есть ли кэшированные данные для текущего пользователя. 
Если кэшированные данные существуют и не истекли (время жизни кэша - 5 минут), они возвращаются. В противном случае 
посты извлекаются из базы данных и сохраняются в кэше.
При создании или удалении поста кэш для текущего пользователя очищается.

##### Логгирование
В модуле *utils/logger_config.py* настроен логгер для отслеживания ошибок и важных событий в приложении. Логгер 
использует встроенный модуль logging Python и записывает сообщения в консоль.

##### Миграции
Для управления миграциями базы данных используется Alembic. Миграции позволяют безопасно применять изменения схемы базы
данных и обновлять существующие базы данных.
В директории *migrations* находятся скрипты миграций, сгенерированные Alembic. Основной скрипт миграции 
*4ff27af43811_initial_migration.py* создает индексы для таблицы *posts*.
Для запуска миграций используются команды Alembic, такие как alembic upgrade head.

##### Запуск приложения
Точка входа в приложение находится в файле *main.py*. В этом файле создается экземпляр FastAPI, подключаются 
маршрутизаторы для конечных точек и запускается сервер FastAPI.
Для запуска приложения необходимо выполнить команду *uvicorn main:app --reload* в терминале. Эта команда запустит сервер
FastAPI в режиме разработки с автоматической перезагрузкой при изменении кода.
После запуска сервера можно тестировать конечные точки приложения, отправляя HTTP-запросы с помощью инструментов для 
тестирования API, таких как Postman или curl.

## Структура проекта:
```bash
📁 fast_api_blog/           # Основной каталог проекта.
│
├── 📁 config_data/         # Пакет с конфигурационными данными.
│   ├── __init__.py         # Файл, обозначающий, что директория является пакетом Python.
│   └── config.py           # Модуль с конфигурационными данными.
│
├── 📁 controllers/         # Каталог с контроллерами приложения.
│   ├── __init__.py         # Инициализация модуля контроллеров.
│   ├── auth_controller.py  # Контроллер для аутентификации пользователей.
│   └── post_controller.py  # Контроллер для работы с постами.
│
├── 📁 database/            # Пакет с модулями для работы с базой данных.
│   ├── __init__.py         # Инициализация пакета для работы с базой данных.
│   ├── database.py         # Модуль для установления соединения с базой данных.
│   └── session.py          # Модуль для работы с сессиями базы данных.
│
├── 📁 migrations/          # Директория для миграций базы данных.
│   ├── 📁versions/         # Директория с версиями миграций.
│   ├── env.py              # Скрипт для работы с миграциями.
│   ├── README              # Файл с описанием миграций.
│   └── script.py.mako      # Шаблон для создания миграционных скриптов.
│
├── 📁 models/              # Пакет с моделями данных.
│   ├── __init__.py         # Инициализация пакета с моделями данных.
│   └── models.py           # Модуль с определением моделей данных.
│
├── 📁 schemas/             # Пакет с схемами данных.
│   ├── __init__.py         # Инициализация пакета с схемами данных.
│   ├── auth.py             # Модуль с схемами данных для аутентификации.
│   └── posts.py            # Модуль с схемами данных для постов.
│
├── 📁 utils/               # Пакет с вспомогательными утилитами.
│   ├── __init__.py         # Инициализация пакета с утилитами.
│   ├── auth.py             # Модуль с утилитами для аутентификации.
│   ├── cache.py            # Модуль для работы с кэшем.
│   └── logger_config.py    # Модуль для логирования.        
│
├── 📁 views/               # Пакет с представлениями (view).
│   ├── __init__.py         # Инициализация пакета с представлениями.
│   ├── auth_views.py       # Модуль с представлениями для аутентификации.
│   └── post_views.py       # Модуль с представлениями для работы с постами.
│
├── .env                    # Файл с конфигурацией и секретами.
│ 
├── .gitignore              # Файл для игнорирования файлов системой контроля версий.
│ 
├── alembic.ini             # Файл конфигурации Alembic для работы с миграциями.
│
├── main.py                 # Основной модуль приложения.
│
├── requirements.txt        # Файл с зависимостями проекта.
│
└──  README.md              # Информация о проекте.
```