# Task:

1. Create an HTML file (e.g., "index.html") with the following content:
   ```bash
   <!DOCTYPE html>
   
   <html lang="ru">
   <head>
   
   <meta charset="UTF-8">
   
   <title>Example of a simple HTML page</title>
   </head>
   
   <body>
   
   I AM UNBELIEVABLY COOL AND MY RESPECT IS IMMEASURABLE :)
   </body>
   
   </html>
   ```
2. Create a FastAPI application that accepts a GET request to the default endpoint (route, page address) "/" and returns
   an HTML page.
3. Save the file and run the application using uvicorn: uvicorn main:app --reload

Open 'http://localhost:8000' in your web browser.

To complete the task, you can read about the FastAPI "FileResponse" feature.

## Solution:

### First solution variant:
In this variant, we import FastAPI and FileResponse from fastapi. Then we create an instance of FastAPI with the title 
"my_first_startup_option". Next, we define a route handler for HTTP GET requests to the root URL "/". Inside this 
handler, we return a FileResponse with the file "index.html".

To run the application, execute the following command in the terminal:
```bash
uvicorn first_startup_option:app --reload
```
Then you can open http://localhost:8000 in a web browser to see the content of the index.html file.

### Second solution variant:
In this alternative approach, we create a function named create_app which initializes a FastAPI instance with the header
"my_second_startup_option" and defines route handlers for various URL paths. These route handlers return the content of 
the "index.html" file upon request.

#### Functionality:
- The root URL ("/") returns the content of the "index.html" file for display in the browser.
- The URL "/download" returns the content of the "index.html" file for downloading.
- The URL "/custom_filename" returns the content of the "index.html" file for downloading with a custom file name 
- "my_custom_file.html".

#### Inside the create_app() function, we define the following route handlers:
- @app.get("/"): Route handler for HTTP GET requests to the root URL "/". Returns the "index.html" file in response for 
  display in the browser.
- @app.get("/download"): Route handler for HTTP GET requests to the URL "/download". Returns the "index.html" file for 
  downloading, setting the "Content-Disposition" header to "attachment; filename=index.html".
- @app.get("/custom_filename"): Route handler for HTTP GET requests to the URL "/custom_filename". Returns the 
  "index.html" file for downloading with the custom file name "my_custom_file.html". This is achieved by setting the 
  "Content-Disposition" header where we specify the file name manually.

Then, in the if __name__ == "__main__": block, we start the application using uvicorn.run, specifying the path to the 
create_app function ("second_startup_option:create_app"), as well as the host and port.

To run the application, you need to execute this script (second_startup_option.py) in the terminal or IDE.

##### After running, you can open the respective URL paths in a web browser to observe different behaviors:
http://localhost:8000 - Displays the content of the index.html file in the browser.
http://localhost:8000/download - Prompts to download the index.html file.
http://localhost:8000/custom_filename - Prompts to download the file with the name "my_custom_file.html".

This solution variant demonstrates the flexibility of FastAPI in configuring route handlers and managing response 
behaviors, such as displaying files in the browser or offering them for download with different file names.

### Third Solution Variation:
In this variation, we utilize HTMLResponse to read and return the contents of the "index.html" file. The route handler
@app.get("/", response_class=HTMLResponse) opens the "index.html" file, reads its contents, and returns it as an 
HTMLResponse to be displayed in the browser.
This variation also includes route handlers /download and /custom_filename from the previous variation, which offer 
downloading the "index.html" file with different filenames.

## Differences between Variations:

#### First Variation (first_startup_option.py):
- The FastAPI instance is created directly in the module code.
- The route handler @app.get("/") is also declared in the same module.
- To run, the command uvicorn first_startup_option:app --reload is used in the terminal.

#### Second Variation (second_startup_option.py):
- A function create_app() is created, which creates and returns a FastAPI instance.
- Route handlers @app.get("/"), @app.get("/download"), @app.get("/custom_filename") are declared inside create_app().
- To run, the command uvicorn.run("second_startup_option:create_app", host="127.0.0.1", port=8000, reload=True) is used.

#### Third Variation (third_startup_option.py):
- Uses HTMLResponse to read and return the contents of the "index.html" file in the browser.
- The route handler @app.get("/", response_class=HTMLResponse) opens the file, reads its contents, and returns 
  HTMLResponse.
- Also includes route handlers /download and /custom_filename from the second variation.

Second and third solution variations allow for more flexibility in configuring and structuring FastAPI applications, 
making them better suited for larger projects. The choice between them depends on specific requirements and preferences 
of the developer, as well as how you want to handle the file on the client side (display in the browser or offer for 
download).

## Project structure:
```bash
📁 lesson_first_file_server_with_fastapi    # Root directory of the entire project
 │
 ├── first_startup_option.py                # Main script for the first variant of launching the application.
 │ 
 ├── second_startup_option.py               # Main script for the second variant of launching the application.
 │ 
 ├── third_startup_option.py                # Main script for the third variant of launching the application.
 │
 ├── index.html                             # HTML file with an example of a simple page.
 │
 ├── logger_config.py                       # Logger configuration.
 │
 ├── README.md                              # File with project description.
 │
 └── requirements.txt                       # File with project dependencies.                     
```
Educational material on Stepik - https://stepik.org/course/179694/syllabus





# Задание:

1) Создайте html-файл (напр. "index.html"), в тексте которого напишите:
    ```bash
    <!DOCTYPE html>
    
    <html lang="ru">
    <head>
    
    <meta charset="UTF-8">
    
    <title> Пример простой страницы html</title>
    </head>
    
    <body>
    
    Я НЕРЕАЛЬНО КРУТ И МОЙ РЕСПЕКТ БЕЗ МЕРЫ :)
    </body>
    
    </html>
    ```
2) Создайте приложение FastAPI, которое принимает GET-запрос к дефолтной конечной точке (маршруту, адресу странички) `/`
   и возвращает html-страницу.
3) Сохраните файл и запустите приложение с помощью `uvicorn`: uvicorn main:app --reload

Откройте 'http://localhost:8000'в вашем веб-браузере. 

Для выполнения задания можно прочитать про возможность FastAPI "FileResponse". 

## Решение:

### Первый вариант решения:
В этом варианте мы импортируем FastAPI и FileResponse из fastapi. Затем создаем экземпляр FastAPI с заголовком 
"my_first_startup_option". Далее определяем обработчик маршрута для HTTP GET запросов на корневой URL "/". Внутри этого 
обработчика мы возвращаем FileResponse с файлом "index.html".

Чтобы запустить приложение, нужно выполнить следующую команду в терминале:
```bash
uvicorn first_startup_option:app --reload
```
Затем можно открыть http://localhost:8000 в веб-браузере, чтобы увидеть содержимое файла index.html.

### Второй вариант решения:
В этом варианте мы создаем функцию create_app, которая создает экземпляр FastAPI с заголовком "my_second_startup_option"
и определяет обработчики маршрутов для различных URL-адресов. Обработчики маршрутов возвращают содержимое файла 
"index.html" по запросу.

#### Функционал:
- Корневой URL-адрес ("/") возвращает содержимое файла "index.html" для отображения в браузере.
- URL-адрес "/download" возвращает содержимое файла "index.html" для скачивания.
- URL-адрес "/custom_filename" возвращает содержимое файла "index.html" для скачивания с пользовательским именем файла 
  "my_custom_file.html".

#### Внутри функции create_app() мы определяем следующие обработчики маршрутов:
- @app.get("/"): Обработчик маршрута для HTTP GET запросов на корневой URL "/". Возвращает файл "index.html" в ответ на 
  запрос для отображения в браузере.
- @app.get("/download"): Обработчик маршрута для HTTP GET запросов на URL "/download". Возвращает файл "index.html" для 
  скачивания, устанавливая заголовок "Content-Disposition" со значением "attachment; filename=index.html".
- @app.get("/custom_filename"): Обработчик маршрута для HTTP GET запросов на URL "/custom_filename". Возвращает файл 
  "index.html" для скачивания с пользовательским именем файла "my_custom_file.html". Это достигается с помощью заголовка
  "Content-Disposition", где мы указываем имя файла вручную.

Затем, в блоке if name == "main":, мы запускаем приложение с помощью uvicorn.run, указывая путь к функции create_app 
("second_startup_option:create_app"), а также хост и порт.
Чтобы запустить приложение, нужно выполнить этот скрипт (second_startup_option.py) в терминале или IDE. 

##### После запуска можно открыть соответствующие URL-адреса в веб-браузере, чтобы увидеть различное поведение:
http://localhost:8000 - отобразит содержимое файла index.html в браузере.
http://localhost:8000/download - предложит скачать файл index.html.
http://localhost:8000/custom_filename - предложит скачать файл с именем "my_custom_file.html".
Этот вариант решения демонстрирует гибкость FastAPI в настройке обработчиков маршрутов и управлении поведением ответов,
таких как отображение файлов в браузере или предложение их для скачивания с различными именами файлов.

### Третий вариант решения:
В этом варианте мы используем HTMLResponse для чтения и возврата содержимого файла "index.html". Обработчик маршрута 
@app.get("/", response_class=HTMLResponse) открывает файл "index.html", читает его содержимое и возвращает его в виде 
HTMLResponse для отображения в браузере.
Этот вариант также включает обработчики маршрутов /download и /custom_filename из предыдущего варианта, которые 
предлагают скачать файл "index.html" с различными именами файлов.

## Различия между вариантами:

#### Первый вариант (first_startup_option.py):
- Экземпляр FastAPI создается непосредственно в коде модуля.
- Обработчик маршрута (@app.get("/")) также объявляется в этом же модуле.
- Для запуска используется команда uvicorn first_startup_option:app --reload в терминале.

#### Второй вариант (second_startup_option.py):
- Создается функция create_app(), которая создает и возвращает экземпляр FastAPI.
- Обработчики маршрутов (@app.get("/"), @app.get("/download"), @app.get("/custom_filename")) объявляются внутри 
  create_app().
- Для запуска используется команда uvicorn.run("second_startup_option:create_app", host="127.0.0.1", port=8000, 
  reload=True).

#### Третий вариант (third_startup_option.py):
- Использует HTMLResponse для чтения и возврата содержимого файла "index.html" в браузере.
- Обработчик маршрута @app.get("/", response_class=HTMLResponse) открывает файл, читает его содержимое и возвращает 
  HTMLResponse.
- Также включает обработчики маршрутов /download и /custom_filename из второго варианта.

Второй и третий варианты решения позволяют более гибко настраивать и конфигурировать приложение FastAPI, а также лучше 
подходят для структурирования крупных проектов. Выбор между ними зависит от конкретных требований и предпочтений 
разработчика, а также от того, как вы хотите обрабатывать файл на стороне клиента (отображать в браузере или предлагать 
для скачивания).

## Структура проекта:
```bash
📁 lesson_first_file_server_with_fastapi    # Корневая директория всего проекта
 │
 ├── first_startup_option.py                # Основной скрипт для первого варианта запуска приложения.
 │ 
 ├── second_startup_option.py               # Основной скрипт для второго варианта запуска приложения.
 │ 
 ├── third_startup_option.py                # Основной скрипт для третьего варианта запуска приложения.
 │
 ├── index.html                             # HTML файл с примером простой страницы.
 │
 ├── logger_config.py                       # Конфигурация логгера.
 │
 ├── README.md                              # Файл с описанием проекта. │
 │
 └── requirements.txt                       # Файл с зависимостями проекта.                     
 ```
Учебный материал на Stepik - https://stepik.org/course/179694/syllabus