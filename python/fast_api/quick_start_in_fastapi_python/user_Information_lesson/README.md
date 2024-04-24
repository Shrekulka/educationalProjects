# FastAPI is built on top of Starlette and Pydantic, which provide it with speed and ease of use.

## Key Features of FastAPI:
1. *Asynchronous Support*: FastAPI fully supports asynchronous programming, allowing you to write asynchronous route
   handlers and leverage the async/await syntax in Python for non-blocking I/O operations.
2. *Automatic Documentation*: FastAPI automatically generates interactive and user-friendly API documentation. It uses
   OpenAPI and JSON Schema standards to provide comprehensive documentation for your API, including input data
   validation, expected responses, and more.
3. *Type Hints and Data Validation*: Thanks to its integration with Pydantic, FastAPI allows you to define data models
   using Python type hints, ensuring automatic data validation and serialization. This feature helps catch errors
   early in the development process and enhances code readability.
4. *Dependency Injection*: FastAPI supports dependency injection, allowing you to efficiently manage dependencies and
   organize them. This feature is especially useful when working with database connections, authentication, and other
   shared resources.
5. *Simple and Intuitive Syntax*: FastAPI's syntax is clear, easy to read, and closely resembles standard Python
   function definitions, making it accessible to both beginners and experienced developers.

## Installing FastAPI:
1. To start using FastAPI, you'll need to install it via pip. Open your terminal or command prompt and enter the
   following command:
   ```bash
   pip install fastapi
   ```
2. To run FastAPI, you need a server, so you also need to install "uvicorn" (a lightning-fast ASGI server for 
   efficiently running your FastAPI applications), or more specifically, to verify that everything is installed 
   correctly:
   ```bash
   pip install uvicorn
   ```

## The call to the application will be like this:
```bash
uvicorn main:app --reload
```
*uvicorn* is a Python library used to run an ASGI server and handle requests to applications created with web frameworks
like FastAPI or Starlette.

*main:app* indicates where the instance of the FastAPI application to run is located.

*main* is the filename containing the code initializing the FastAPI application. Typically, this file is named main.py.

*app* is the name of the variable assigned to the FastAPI application instance. For example, in the main.py file, there 
might be a line app = FastAPI(), where an instance of FastAPI is created and assigned to the variable app.

So, *main:app* points to the app in the main.py file.

*--reload* is an additional parameter telling uvicorn to reload the server when the source code changes. This is very 
convenient during development, as you don't need to manually restart the server.
In summary, the command uvicorn main:app --reload runs the server serving the FastAPI application defined in the app 
variable of the main.py file, and the server will automatically reload when changes are made to the source code.

## If the main.py file is located in another directory, for example src, then instead of main:app, you need to use 
## src.main:app.
```bash
uvicorn src.main:app --reload
```

## FastAPI has had (and still has) alternatives:
1. *Flask* - a lightweight and widely used web framework in the Python ecosystem. It's easy to use and get started with,
   but lacks built-in support for asynchronous and type hint-based automatic validation.
2. *Django* - a full-featured web framework that follows the "batteries included" philosophy. It provides a plethora of
   out-of-the-box functionalities including ORM, admin interface, and more, but for small and simple APIs, it might be 
   overkill. Additionally, Django is criticized for being tightly coupled to the MVC (model-view-controller) pattern and
   being a monolithic modular, less flexible compared to FastAPI.
3. *Tornado* - an asynchronous web framework capable of handling a large number of simultaneous connections. It's often
   used in scenarios requiring high levels of parallelism, but may have a steeper learning curve compared to FastAPI 
   (heavier, less intuitive, not very convenient).
4. *Bottle* - a minimalist web framework designed for small-scale applications. It's lightweight and easy to use, but 
   lacks the speed, scalability, and performance optimizations present in FastAPI.

We can view the documentation at the following links: http://127.0.0.1:8000/docs and http://127.0.0.1:8000/redoc 
(alternative).

## Project Structure:
```bash
📁 fastapi_project_skeleton/   # Root directory of the entire project
│
├── 📁 alembic/                # Directory for database migrations using Alembic
│
├── 📁 src/                    # Main directory containing the source code of the application
│   │
│   ├── 📁 auth/               # Module for authentication and authorization functions
│   │   │ 
│   │   ├── router.py          # File defining endpoints for the auth module
│   │   │ 
│   │   ├── schemas.py         # File defining Pydantic schemas for data validation in the auth module
│   │   │ 
│   │   ├── models.py          # File defining database models for the auth module
│   │   │ 
│   │   ├── dependencies.py    # File defining dependencies for auth module routes
│   │   │ 
│   │   ├── config.py          # File containing configuration for the auth module
│   │   │ 
│   │   ├── constants.py       # File containing constants and error codes for the auth module
│   │   │ 
│   │   ├── exceptions.py      # File defining exceptions for the auth module
│   │   │ 
│   │   ├── service.py         # File containing business logic for the auth module
│   │   │ 
│   │   └── utils.py           # File containing utility functions for the auth module
│   │   
│   │   
│   ├── 📁 aws/                # Module for interacting with AWS
│   │   │ 
│   │   ├── client.py          # File defining client for interacting with AWS
│   │   │ 
│   │   ├── schemas.py         # File defining Pydantic schemas for the aws module
│   │   │ 
│   │   ├── config.py          # File containing configuration for the aws module
│   │   │ 
│   │   ├── constants.py       # File containing constants for the aws module
│   │   │ 
│   │   ├── exceptions.py      # File defining exceptions for the aws module
│   │   │ 
│   │   └── utils.py           # File containing utility functions for the aws module
│   │   
│   │   
│   ├── 📁 posts/              # Module for working with posts
│   │   │ 
│   │   ├── router.py          # File defining routes for the posts module
│   │   │ 
│   │   ├── schemas.py         # File defining Pydantic schemas for the posts module
│   │   │
│   │   ├── models.py          # File defining database models for the posts module
│   │   │
│   │   ├── dependencies.py    # File defining dependencies for posts module routes
│   │   │
│   │   ├── constants.py       # File containing constants and error codes for the posts module
│   │   │
│   │   ├── exceptions.py      # File defining exceptions for the posts module
│   │   │
│   │   ├── service.py         # File containing business logic for the posts module
│   │   │
│   │   └── utils.py           # File containing utility functions for the posts module
│   │   
│   │   
│   ├── config.py              # File containing global configuration for the application
│   │   
│   ├── models.py              # File containing global database models
│   │   
│   ├── exceptions.py          # File containing global exceptions
│   │   
│   ├── pagination.py          # File containing module for pagination
│   │   
│   ├── database.py            # File for connecting to the database
│   │   
│   └── main.py                # Main application file initializing FastAPI
│   
│   
├── 📁 tests/                  # Directory for tests
│   │  
│   ├── 📁 auth/               # Directory for tests of the auth module
│   │   
│   ├── 📁 aws/                # Directory for tests of the aws module
│   │   
│   └── 📁 posts/              # Directory for tests of the posts module
│   
│   
├── 📁 templates/              # Directory for HTML templates
│   │   
│   └── index.html             # File with HTML template
│   
│   
├── 📁 requirements/           # Directory for dependency files
│   │  
│   ├── base.txt               # File with base dependencies
│   │   
│   ├── dev.txt                # File with dependencies for development
│   │   
│   └── prod.txt               # File with dependencies for production
│   
│   
├── .env                       # File with environment variables
│
├── .gitignore                 # File with Git ignore rules
│
├── logging.ini                # File with logging configuration
│
├── requirements.txt           # File listing project dependencies
│
└── alembic.ini                # File with Alembic configuration 
```
Educational material on Stepik - https://stepik.org/course/179694/syllabus






# FastAPI построен на базе Starlette и Pydantic, которые обеспечивают его скорость и простоту использования.

## Ключевые особенности FastAPI:
1. *Поддержка асинхронности*: FastAPI полностью поддерживает асинхронное программирование, позволяя вам писать 
   асинхронные обработчики маршрутов и использовать преимущества синтаксиса async /await в Python для неблокирующих 
   операций ввода-вывода.
2. *Автоматическое документирование*: FastAPI автоматически генерирует интерактивную и удобную для пользователя 
   документацию по API. Он использует стандарты OpenAPI и JSON Schema для предоставления исчерпывающей документации для 
   вашего API, включая проверку входных данных, ожидаемые ответы и многое другое.
3. *Подсказки типов и проверка данных*: Благодаря интеграции FastAPI с Pydantic вы можете определять модели данных с 
   помощью подсказок типов (type hints) Python, обеспечивая автоматическую проверку данных и сериализацию. Эта функция 
   помогает выявлять ошибки на ранних стадиях процесса разработки и повышает читаемость кода.
4. *Внедрение зависимостей*: FastAPI поддерживает внедрение зависимостей, позволяя вам эффективно управлять зависимостями
   и организовывать их. Эта функция особенно полезна при работе с подключениями к базе данных, аутентификацией и другими
   общими ресурсами.
5. *Простой и интуитивно понятный синтаксис*: синтаксис FastAPI понятен, легок для чтения и очень похож на стандартное 
   определение функций Python, что делает его доступным как для начинающих, так и для опытных разработчиков.

## Установка FastAPI:
1. Чтобы начать работу с FastAPI, вам нужно будет установить его с помощью pip. Откройте свой терминал или командную 
   строку и введите следующую команду:
   ```bash
   pip install fastapi
   ```
2. Для запуска FastAPI нужен сервер, поэтому вам также нужно установить "uvicorn" (это молниеносный сервер ASGI, для 
   эффективного запуска ваших приложений FastAPI), точнее проверить, что все установилось корректно:
   ```bash
   pip install uvicorn
   ```
## Вызов приложения будет таким:
   ```bash
   uvicorn main:app --reload
   ```
*uvicorn* - это библиотека для Python, которая используется для запуска ASGI-сервера и обслуживания запросов к 
приложениям, созданным с помощью веб-фреймворков, таких как FastAPI или Starlette.

*main:app* - это способ указать, где находится экземпляр приложения FastAPI, который нужно запустить.

*main* - это имя файла, в котором находится код, инициализирующий приложение FastAPI. Обычно этот файл называется 
main.py.

*app* - это имя переменной, которой присвоен экземпляр приложения FastAPI. Например, в файле main.py может быть строка 
app = FastAPI(), где создается экземпляр FastAPI и присваивается переменной app.

Таким образом, *main:app* указывает на app из файла main.py.

*--reload* - это дополнительный параметр, который говорит uvicorn перезагружать сервер при изменении исходного кода. Это 
очень удобно в процессе разработки, так как вам не нужно постоянно перезапускать сервер вручную.
В целом, команда uvicorn main:app --reload запускает сервер, обслуживающий приложение FastAPI, определенное в переменной
app файла main.py, и при этом сервер будет автоматически перезагружаться при внесении изменений в исходный код.

## Если файл main.py находится d другой директории, например src, то вместо main:app нужно использовать src.main:app.
```bash
uvicorn src.main:app --reload
```

## Альтернативы были (и есть) у FastAPI:
1. *Flask* - это легкий и широко используемый веб-фреймворк в экосистеме Python. Он прост в использовании и с ним легко 
   начать работу, но ему не хватает встроенной поддержки асинхронности и автоматической проверки на основе подсказок 
   типов.
2. *Django* - это полнофункциональный веб-фреймворк, который следует философии "батарейки включены" (швейцарский нож - 
   все в комплекте). Он предоставляет множество готовых функциональных возможностей, включая ORM, интерфейс 
   администратора и многое другое, но для небольших и простых API это может оказаться излишним. В дополнение можно 
   поругать джангу, тем что в нем зашит паттерн MVC (model-view-controller, или model-view-template по-джанговски), а 
   также это по сути модульный монолит и он не такой гибкий, как FastAPI.
3. *Tornado* - это асинхронный веб-фреймворк, который может обрабатывать большое количество одновременных подключений. 
   Он часто используется в сценариях, требующих высокого уровня параллелизма, но может иметь более крутую кривую 
   обучения по сравнению с FastAPI (тяжёл, местами не очевиден, не очень удобен).
4. *Bottle* - это минималистичный веб-фреймворк, разработанный для маломасштабных приложений. Он легкий и простой в 
   использовании, но ему не хватает скорости, масштабируемости и оптимизации производительности, присутствующих в 
   FastAPI.


Документацию можем посмотреть по ссылкам http://127.0.0.1:8000/docs и http://127.0.0.1:8000/redoc (альтернативная).

## Структура проекта:
```bash
📁 fastapi_project_skeleton/   # Корневая директория всего проекта
│
├── 📁 alembic/                # Директория для миграций базы данных с помощью Alembic
│
├── 📁 src/                    # Основная директория с исходным кодом приложения
│   │
│   ├── 📁 auth/               # Модуль для функций аутентификации и авторизации
│   │   │ 
│   │   ├── router.py          # Файл с определением маршрутов (endpoints) для модуля auth
│   │   │ 
│   │   ├── schemas.py         # Файл с определением схем Pydantic для валидации данных в модуле auth
│   │   │ 
│   │   ├── models.py          # Файл с определением моделей базы данных для модуля auth
│   │   │ 
│   │   ├── dependencies.py    # Файл с определением зависимостей для маршрутов модуля auth
│   │   │ 
│   │   ├── config.py          # Файл с конфигурацией для модуля auth
│   │   │ 
│   │   ├── constants.py       # Файл с константами и кодами ошибок для модуля auth
│   │   │ 
│   │   ├── exceptions.py      # Файл с определением исключений для модуля auth
│   │   │ 
│   │   ├── service.py         # Файл с бизнес-логикой для модуля auth
│   │   │ 
│   │   └── utils.py           # Файл с вспомогательными функциями для модуля auth
│   │   
│   │   
│   ├── 📁 aws/                # Модуль для взаимодействия с AWS
│   │   │ 
│   │   ├── client.py          # Файл с определением клиента для взаимодействия с AWS
│   │   │ 
│   │   ├── schemas.py         # Файл с определением схем Pydantic для модуля aws
│   │   │ 
│   │   ├── config.py          # Файл с конфигурацией для модуля aws
│   │   │ 
│   │   ├── constants.py       # Файл с константами для модуля aws
│   │   │ 
│   │   ├── exceptions.py      # Файл с определением исключений для модуля aws
│   │   │ 
│   │   └── utils.py           # Файл с вспомогательными функциями для модуля aws
│   │   
│   │   
│   ├── 📁 posts/              # Модуль для работы с постами
│   │   │ 
│   │   ├── router.py          # Файл с определением маршрутов для модуля posts
│   │   │ 
│   │   ├── schemas.py         # Файл с определением схем Pydantic для модуля posts
│   │   │
│   │   ├── models.py          # Файл с определением моделей базы данных для модуля posts
│   │   │
│   │   ├── dependencies.py    # Файл с определением зависимостей для маршрутов модуля posts
│   │   │
│   │   ├── constants.py       # Файл с константами и кодами ошибок для модуля posts
│   │   │
│   │   ├── exceptions.py      # Файл с определением исключений для модуля posts
│   │   │
│   │   ├── service.py         # Файл с бизнес-логикой для модуля posts
│   │   │
│   │   └── utils.py           # Файл с вспомогательными функциями для модуля posts
│   │   
│   │   
│   ├── config.py              # Файл с глобальной конфигурацией приложения
│   │   
│   ├── models.py              # Файл с глобальными моделями базы данных
│   │   
│   ├── exceptions.py          # Файл с глобальными исключениями
│   │   
│   ├── pagination.py          # Файл с модулем для пагинации
│   │   
│   ├── database.py            # Файл для подключения к базе данных
│   │   
│   └── main.py                # Главный файл приложения, инициализирующий FastAPI
│   
│   
├── 📁 tests/                  # Директория для тестов
│   │  
│   ├── 📁 auth/               # Директория для тестов модуля auth
│   │   
│   ├── 📁 aws/                # Директория для тестов модуля aws
│   │   
│   └── 📁 posts/              # Директория для тестов модуля posts
│   
│   
├── 📁 templates/              # Директория для шаблонов HTML
│   │   
│   └── index.html             # Файл с шаблоном HTML
│   
│   
├── 📁 requirements/           # Директория для файлов с зависимостями
│   │  
│   ├── base.txt               # Файл с базовыми зависимостями
│   │   
│   ├── dev.txt                # Файл с зависимостями для разработки
│   │   
│   └── prod.txt               # Файл с зависимостями для продакшена
│   
│   
├── .env                       # Файл с переменными окружения
│
├── .gitignore                 # Файл с исключениями для Git
│
├── logging.ini                # Файл с конфигурацией логирования
│
├── requirements.txt           # Файл с перечнем зависимостей проекта
│
└── alembic.ini                # Файл с конфигурацией Alembic 
 ```
Учебный материал на Stepik - https://stepik.org/course/179694/syllabus