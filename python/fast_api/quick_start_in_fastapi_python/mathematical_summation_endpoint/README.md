# Task:
Create a FastAPI application that accepts a POST request to the endpoint `/calculate` with two numbers (`num1` and 
`num2`) as input data. The application should respond with the sum of the two numbers.

For example, a request to `/calculate` with `num1=5` and `num2=10` should return `{"result": 15}` in the response.

(Note: You can use any method of your choice to run the FastAPI application for testing the endpoint. This task requires
knowledge from the following lessons / official documentation. We hope such an approach with increasing complexity will
motivate you to acquire additional information or to study the course as soon as possible).

# Solution:
## Solution 1: mathematical_summation_endpoint/first_mathematical_summation_option.py
This solution is a web application created using FastAPI that allows calculating the sum of two numbers.
#### Features of this solution:
1. *Using Pydantic for data validation*:
   The Numbers class from the Pydantic library is used for validating input data. This ensures simplicity and reliability
   in working with data, automatic type and field value checks.
2. *Working with static files*:
   The Starlette library is used to handle static files such as an HTML page with a form for entering numbers. The HTML
   file calculate_first_option.html is mounted at the root URL /templates.
3. *Handling forms*:
   The web application provides an HTML form for entering two numbers and calculating their sum. When the user enters
   numbers and clicks the "calculate" button, JavaScript code sends the data to the server using the fetch API.
4. *Handling POST requests*:
   The calculate_sum handler accepts data in JSON format, validates it with the Numbers model from Pydantic, calculates
   the sum, and returns the result in JSON format.
5. *Running the server*:
   The server is launched using uvicorn, and logging settings are imported from logger_config.

## Solution 2: mathematical_summation_endpoint/second_mathematical_summation_option.py
This solution is also a FastAPI web application for calculating the sum of two numbers.
#### Key features:
1. *Using FastAPI to create the web application*:
   The web application is created using FastAPI.
2. *Passing parameters through an HTML form*:
   The num1 and num2 parameters are passed through an HTML form using the POST method. The form is submitted to the URL
   /calculate.
3. *Handling parameters using Pydantic*:
   The num1 and num2 parameters are received in the calculate_sum handler using Pydantic, providing data validation and
   automatic API documentation.
4. *Returning the result as JSON*:
   The result of the sum calculation is returned as a JSON response with the key result.
5. *Using HTML templates*:
   An HTML page with a form for entering numbers is stored in the file calculate_second_option.html.
6. *Running the server*:
   The server is launched using uvicorn, and logging settings are imported from logger_config.

## Solution 3: mathematical_summation_endpoint/third_mathematical_summation_option.py
This solution differs from the previous two in that the num1 and num2 parameters are passed in the query string of a GET
request.
#### Features of this solution:
1. *Passing parameters in the query string*:
   The num1 and num2 parameters are passed in the query string of a GET request, for example: 
   http://127.0.0.1:5080/calculate?num1=5&num2=10.
2. *Handling parameters in the FastAPI handler*:
   The calculate handler accepts the num1 and num2 parameters directly in the function signature, without using Pydantic
   or an HTML form.
3. *Returning the result as a message*:
   The result of the sum calculation is returned as a message embedded in a string, rather than in JSON format.
4. *Absence of HTML template*:
   This solution does not use an HTML template, as it does not involve displaying a web page.
5. *Running the server*:
   The server is launched using uvicorn, and logging settings are imported from logger_config.

## The main difference between these solutions lies in the way parameters are passed and the presentation of the result:
1. The first solution uses an HTML form for data input and sends it to the server using JavaScript and the fetch API.
   The result is returned in JSON format.
2. The second solution also uses an HTML form, but data is sent directly to the server using the POST method.
   The result is returned in JSON format.
3. The third solution passes parameters in the query string of a GET request, without using an HTML form.
   The result is returned as a message, not JSON.

The choice of solution depends on specific requirements and preferences. The first and second solutions are more suitable
for web applications with a user interface where a form for entering data needs to be displayed. The third solution might
be preferable for simple API endpoints without a web interface.

## Project Structure:
```bash
📁 lesson_first_file_server_with_fastapi        # Root directory of the entire project
 │
 ├── first_mathematical_summation_option.py     # Main script for the first option of running the application.
 │ 
 ├── second_mathematical_summation_option.py    # Main script for the second option of running the application.
 │ 
 ├── third_mathematical_summation_option.py     # Main script for the third option of running the application.
 │
 ├── 📁 templates/                              # Directory with HTML templates for web pages.
 │   ├── calculate_first_option.html            # HTML template file for the first calculation option.
 │   └── calculate_second_option.html           # HTML template file for the second calculation option.
 │ 
 ├── logger_config.py                           # Logger configuration.
 │
 ├── README.md                                  # Project description file.
 │
 └── requirements.txt                           # Project dependencies file.                     
```
Educational material on Stepik - https://stepik.org/course/179694/syllabus.





# Задание:
Создайте приложение FastAPI, которое принимает POST-запрос к конечной точке (маршруту, адресу странички) `/calculate` с
двумя числами (`num1` и `num2`) в качестве входных данных. Приложение должно ответить суммой двух чисел.

Например, запрос на `/calculate` с `num1=5` и `num2=10` должен возвращать `{"result": 15}` в ответе.

(Примечание: Вы можете использовать любой метод по вашему выбору для запуска приложения FastAPI для тестирования 
конечной точки. Для выполнения задания потребуются знания из следующих уроков / из официальной документации. Надеемся, 
что такой подход с повышением сложности будет мотивировать на получение дополнительной информации или к скорейшему 
изучению курса). 


# Решение:
## Решение 1: mathematical_summation_endpoint/first_mathematical_summation_option.py
Данное решение представляет собой веб-приложение, созданное с помощью FastAPI, которое позволяет вычислять сумму двух 
чисел. 
#### Особенности этого решения:
1. *Использование Pydantic для валидации данных*: 
   Для валидации входных данных используется класс Numbers из библиотеки Pydantic. Это обеспечивает простоту и 
   надежность работы с данными, автоматическую проверку типов и значений полей.
2. *Работа со статическими файлами*: 
   Для обработки статических файлов, таких как HTML-страница с формой для ввода чисел, используется библиотека Starlette.
   HTML-файл calculate_first_option.html монтируется на корневой URL /templates.
3. *Обработка форм*:
   Веб-приложение предоставляет HTML-форму для ввода двух чисел и вычисления их суммы. Когда пользователь вводит числа и
   нажимает кнопку "вычислить", JavaScript-код отправляет данные на сервер с помощью fetch API.
4. *Обработчик POST-запроса*: 
   Обработчик calculate_sum принимает данные в формате JSON, валидирует их с помощью модели Numbers от Pydantic, 
   вычисляет сумму и возвращает результат в виде JSON-ответа.
5. *Запуск сервера*: 
   Запуск сервера осуществляется с использованием uvicorn, а настройки логирования импортируются из logger_config.

## Решение 2: mathematical_summation_endpoint/second_mathematical_summation_option.py
Это решение также представляет собой веб-приложение на FastAPI для вычисления суммы двух чисел. 
#### Ключевые особенности:
1. *Использование FastAPI для создания веб-приложения*: 
   Веб-приложение создается с помощью FastAPI.
2. *Передача параметров через HTML-форму*: 
   Параметры num1 и num2 передаются через HTML-форму с использованием метода POST. Форма отправляется на URL /calculate.
3. *Обработка параметров с использованием Pydantic*: 
   Параметры num1 и num2 принимаются в обработчике calculate_sum с помощью Pydantic, что обеспечивает валидацию данных и
   автоматическую документацию API.
4. *Возвращение результата в виде JSON*: 
   Результат вычисления суммы возвращается в виде JSON-ответа с ключом result.
5. *Использование шаблонов HTML*: 
   HTML-страница с формой для ввода чисел хранится в файле calculate_second_option.html.
6. *Запуск сервера*: 
   Запуск сервера осуществляется с использованием uvicorn, а настройки логирования импортируются из logger_config.

## Решение 3: mathematical_summation_endpoint/third_mathematical_summation_option.py
Это решение отличается от двух предыдущих тем, что параметры num1 и num2 передаются в строке запроса (query parameters)
GET-запроса. 
#### Особенности данного решения:
1. *Передача параметров в строке запроса*: 
   Параметры num1 и num2 передаются в строке запроса GET-запроса, например: http://127.0.0.1:5080/calculate?num1=5&num2=10.
2. *Обработка параметров в обработчике FastAPI*: 
   Обработчик calculate принимает параметры num1 и num2 напрямую в сигнатуре функции, без использования Pydantic или 
   HTML-формы.
3. *Возвращение результата в виде сообщения*: 
   Результат вычисления суммы возвращается в виде сообщения, вставленного в строку, а не в формате JSON.
4. *Отсутствие HTML-шаблона*: 
   В этом решении не используется HTML-шаблон, так как не предполагается отображение веб-страницы.
5. *Запуск сервера*: 
   Запуск сервера осуществляется с использованием uvicorn, а настройки логирования импортируются из logger_config.

## Основное различие между этими решениями заключается в способе передачи параметров и представлении результата:
1. Первое решение использует HTML-форму для ввода данных и отправляет их на сервер с помощью JavaScript и fetch API. 
   Результат возвращается в формате JSON.
2. Второе решение также использует HTML-форму, но данные отправляются напрямую на сервер с помощью метода POST. 
   Результат возвращается в формате JSON.
3. Третье решение передает параметры в строке запроса GET-запроса, без использования HTML-формы. Результат возвращается
   в виде сообщения, а не JSON.

Выбор решения зависит от конкретных требований и предпочтений. Первое и второе решения более подходят для веб-приложений
с интерфейсом, где требуется отображать форму для ввода данных. Третье решение может быть более предпочтительным для 
простых API-эндпойнтов без веб-интерфейса.

## Структура проекта:
```bash
📁 lesson_first_file_server_with_fastapi        # Корневая директория всего проекта
 │
 ├── first_mathematical_summation_option.py     # Основной скрипт для первого варианта запуска приложения.
 │ 
 ├── second_mathematical_summation_option.py    # Основной скрипт для второго варианта запуска приложения.
 │ 
 ├── third_mathematical_summation_option.py     # Основной скрипт для третьего варианта запуска приложения.
 │
 ├── 📁 templates/                              # Директория с шаблонами HTML-файлов для веб-страниц.
 │   ├── calculate_first_option.html            # Шаблон HTML-файла для первого варианта вычислений.
 │   └── calculate_second_option.html           # Шаблон HTML-файла для второго варианта вычислений.
 │ 
 ├── logger_config.py                           # Конфигурация логгера.
 │
 ├── README.md                                  # Файл с описанием проекта. │
 │
 └── requirements.txt                           # Файл с зависимостями проекта.                     
 ```
Учебный материал на Stepik - https://stepik.org/course/179694/syllabus