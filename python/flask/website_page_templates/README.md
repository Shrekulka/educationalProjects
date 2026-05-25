# Flask Web Application Project
This is a simple web application built with Python and Flask that demonstrates creating a multi-page website using 
templates, routing, logging and error handling.

## Project Goals
1. Demonstrate using Flask for building web applications
2. Show organization of routes and HTTP request handlers
3. Configure working with templates and a base template for interface unification
4. Implement logging of errors and events into a file and console
5. Handle typical HTTP client and server errors

## Routes
/ - Home page
/about - About page
/contact - Contact page with form
/login - Login page
/profile/<username> - Personal profile page

## Templates
base.html - Base template with common layout
index.html - Home page
about.html - About page
contact.html - Contact page
404.html - 404 error page template

## Styles
Description of the CSS styles used for page elements.
File: static/css/styles.css

## Logging
Logger configuration in the logger.py module to output information to app.log file and console.
Uses DEBUG, INFO, ERROR levels.
Logs application errors, requests, events.

## Requirements File
Describes project dependencies and versions of used libraries.

## Running

## Installing dependencies:
```bash
pip install -r requirements.txt
```

## Starting:
```bash
python app.py
```

## Project Structure:
```bash
website_page_templates/              # Main project folder.
│
├── flsite.py                        # Main Flask application file.
│
├── static/                          # Folder with static resources (CSS, JS, etc.) directly accessible to clients.
│   ├── css/                         # Folder containing style files.
│   │   └── styles.css               # Style file for web pages.
│   └── js/                          # Folder containing JavaScript files.
│        
├── templates/                       # Folder for HTML templates used in the application.
│   ├── base.html                    # Base HTML template.
│   ├── about.html                   # HTML template for the "About" page.
│   ├── index.html                   # HTML template for the main page.
│   ├── contact.html                 # HTML template for the "Contact" page.
│   ├── login.html                   # HTML template for the "Login" page.
│   └── page404.html                 # HTML template for the 404 error page.
│
├── config.py                        # File with configuration for the Flask application.
│
├── README.md                        # File with project description, instructions, and other documentation.
│
├── logger.py                        # File with a module for logging.
│
├── val.log                          # Log file for recording application logs.
│
├── requirements.txt                 # File specifying dependencies (libraries and their versions) for the project. This
│                                    # can be used for easy deployment of the project on other systems.
├── venv/                            # Folder with a virtual environment to isolate project dependencies.
│
└── .env                             # File with environment variables (e.g., API keys).
```
# This sets the directory for Flask to look for static files.
1. import os
2. os.environ["FLASK_STATIC"] = "./static"
3. After initializing the Flask application (app: Flask = Flask(__name__)), specify that Flask should use the 'static'
   folder for static files (CSS, images, etc.) - app.static_folder = 'static'
```bash
import os
os.environ["FLASK_STATIC"] = "./static"
app: Flask = Flask(__name__)
app.static_folder = 'static'
```




# Проект веб-приложения на Flask
Это простое веб-приложение на Python и Flask, которое демонстрирует создание многостраничного сайта с использованием 
шаблонов, маршрутизации, логирования и обработки ошибок.

## Цели проекта
1. Продемонстрировать использование Flask для построения веб-приложений
2. Показать организацию маршрутов и обработчиков HTTP-запросов
3. Настроить работу с шаблонами и базовым шаблоном для унификации интерфейса
4. Реализовать логирование ошибок и событий в файл и консоль
5. Обработать типичные HTTP ошибки клиента и сервера

## Маршруты (routes)
/ - главная страница
/about - страница "О сайте"
/contact - страница "Обратная связь" c формой
/login - страница авторизации
/profile/<username> - личный профиль пользователя

## Шаблоны
base.html - базовый шаблон с общей разметкой
index.html - главная страница
about.html - страница "О сайте"
contact.html - страница "Обратная связь"
404.html - шаблон для ошибки 404

## Стили
Описание используемых CSS-стилей для элементов страницы.
Файл: static/css/styles.css

## Логирование
Настройка логгера в модуле logger.py для вывода информации в файл app.log и в консоль.
Используются уровни DEBUG, INFO, ERROR.
Логируются ошибки, запросы, события приложения.

## Файл requirements.txt
Описание зависимостей проекта. Содержит названия и версии используемых библиотек.

## Запуск

## Установка зависимостей:
```bash
pip install -r requirements.txt
```

## Запуск:
```bash
python app.py
```

## Структура проекта: 
```bash
website_page_templates/              # Основная папка проекта.
│
├── flsite.py                        # Основной файл Flask-приложения.
│
├── static/                          # Папка со статическими ресурсами (CSS, JS и т. д.), доступными напрямую клиентам.
│   ├── css/                         # Папка с файлами стилей.
│   │   └── styles.css               # Файл стилей для веб-страниц.
│   └── js/                          # Папка с файлами JavaScript.
│        
├── templates/                       # Папка для HTML-шаблонов, используемых в приложении.
│   ├── base.html                    # Базовый HTML-шаблон.
│   ├── about.html                   # HTML-шаблон для страницы "О сайте".
│   ├── index.html                   # HTML-шаблон для главной страницы.
│   ├── contact.html                 # HTML-шаблон для страницы "Обратная связь".
│   ├── login.html                   # HTML-шаблон для страницы "Авторизация".
│   └── page404.html                 # HTML-шаблон для страницы с ошибкой 404.
│
├── config.py                        # Файл с конфигурацией Flask-приложения.
│
├── README.md                        # Файл с описанием проекта, инструкциями и другой документацией.
│
├── logger.py                        # Файл с модулем для логирования.
│
├── val.log                          # Файл журнала для записи логов приложения.
│
├── requirements.txt                 # Файл, указывающий зависимости (библиотеки и их версии) для проекта. Это
│                                    # может использоваться для удобного развёртывания проекта на других системах.
├── venv/                            # Папка с виртуальным окружением для изоляции зависимостей проекта.
│
└── .env                             # Файл с переменными окружения (например, ключи API).
```

# Это укажет Flask где искать статику.
1. import os
2. os.environ["FLASK_STATIC"] = "./static"
3. После инициализации Flask-приложения app: Flask = Flask(__name__) указываем Flask использовать папку 'static' для 
   статических файлов (CSS, изображения и т. д.)- app.static_folder = 'static'
```bash
import os
os.environ["FLASK_STATIC"] = "./static"
app: Flask = Flask(__name__)
app.static_folder = 'static'
```