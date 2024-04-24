# Task:
# Your task is to create a FastAPI application that handles requests related to products. 
## The application should have two endpoints:
1. Endpoint for getting information about a product:
   - Route: `/product/{product_id}`
   - Method: GET
   - Path parameter:
     - `product_id`: the identifier of the product (integer)
   - Response: Returns a JSON object containing information about the product based on the provided `product_id`.
2. Endpoint for searching for products:
   - Route: `/products/search`
   - Method: GET
   - Query parameters:
     - `keyword` (string, required): keyword for searching products.
     - `category` (string, optional): category for filtering products.
     - `limit` (integer, optional): maximum number of products to return (default 10 if not specified).
   - Response: Returns a JSON array containing information about the products that match the search criteria.
3. For example, you can use the following data for subsequent response direction:
```bash
sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]
```
Example:
A GET request to /product/123 should return:
```bash
{
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}
```
In response to a GET request to /products/search?keyword=phone&category=Electronics&limit=5, the following should be 
returned:
```bash
[
    {
        "product_id": 123,
        "name": "Smartphone",
        "category": "Electronics",
        "price": 599.99
    },
    {
        "product_id": 789,
        "name": "Iphone",
        "category": "Electronics",
        "price": 1299.99
    }
]
```
Note that if the routes are the same (for example, /products/{product_id} and /products/search), the second route will 
not work because FastAPI will try to convert the word "search" to an integer, processing the first route and resulting 
in an error. Routes are processed in the order handlers are declared.
Please implement the FastAPI application and test the endpoints using tools such as "curl", Postman, or any other API 
client.

# Solution Description:

1. Creating the FastAPI application:
    a) In the main.py module, defined the create_app() function, which creates an instance of the FastAPI application.
    b) Inside this function, defined two route handlers:
       - get_product() for handling requests to retrieve product information by its identifier (/product/{product_id}).
       - search_product() for handling requests to search for products by keyword, category, and limit
         (/products/search).
2. Handler get_product():
    - This handler takes product_id as a path parameter.
    - It searches for the product in the sample_products list using a list comprehension and the next() function.
    - If the product is found, it creates an instance of Product and returns it.
    - If the product is not found, it raises an HTTPException with status code 404 Not Found and the appropriate message.
3. Handler search_product():
    a) This handler takes the following query parameters:
       - keyword (required) - keyword for searching products.
       - category (optional) - category for filtering products.
       - limit (optional, default 10) - maximum number of products to return.
    b) First, it creates a results list containing products whose name contains the keyword (case-insensitive).
    c) If a category is specified, it filters the results list to include only products with the specified category.
    d) It returns a list of Product instances created from the filtered data, with a limit applied.
4. Running the application:
    - In the if name == 'main' block, the application is run using uvicorn.run(), specifying the path to the
      create_app() function, as well as the host and port.
    - Exception handling for KeyboardInterrupt and other errors is implemented using try/except blocks.
5. Testing:
    a) Getting product information
       - Route: /product/{product_id}
       - Method: GET
To test this route, create a new GET request in Postman and specify the URL http://localhost:5080/product/123
(assuming the application is running on localhost and port 5080).
Upon sending this request, you should receive a response with status 200 OK and the following body:
```bash
{
    "product_id": 123,
    "name": "Смартфон",
    "category": "Электроника",
    "price": 599.99
}
```
If you specify a non-existing product_id, for example, http://localhost:5080/product/999, you will receive a response
with status 404 Not Found and the message "Product not found".
    b) Searching for products
    - Route: /products/search
    - Method: GET
    - Query parameters:
      - keyword (required)
      - category (optional)
      - limit (optional, default 10)
To test this route, create a new GET request in Postman and specify the URL
http://localhost:5080/products/search?keyword=phone&category=Электроника&limit=5.
Upon sending this request, you should receive a response with status 200 OK and the following body:
```bash
[
    {
        "product_id": 123,
        "name": "Смартфон",
        "category": "Электроника",
        "price": 599.99
    },
    {
        "product_id": 789,
        "name": "iPhone",
        "category": "Электроника",
        "price": 1299.99
    }
]
```
Note that the results are filtered by the keyword "phone" and the category "Electronics", and the number of returned
products is limited to 5.
If you omit the category parameter, the results will be filtered only by the keyword. For example, for the request
http://localhost:5080/products/search?keyword=phone, you will get:
```bash
[
    {
        "product_id": 123,
        "name": "Смартфон",
        "category": "Электроника",
        "price": 599.99
    },
    {
        "product_id": 456,
        "name": "Чехол для телефона",
        "category": "Аксессуары",
        "price": 19.99
    },
    {
        "product_id": 789,
        "name": "iPhone",
        "category": "Электроника",
        "price": 1299.99
    }
]
```
Thus, this solution has been successfully tested using Postman, checking both endpoints and various combinations of 
query parameters.

## Project Structure:
```bash
📁 feedback_service/              # Root directory of the entire project
│
├── README.md                     # File containing project description
│
├── requirements.txt              # File listing project dependencies
│
└── 📁 src/                       # Main directory containing source code of the application
    │
    ├── database.py               # Module for working with the database
    │
    ├── logger_config.py          # Module for configuring logging
    │
    ├── main.py                   # Main module containing the FastAPI application code
    │
    └── models.py                 # Module containing the Pydantic model for product
```




# Задача:
Ваша задача - создать приложение FastAPI, которое обрабатывает запросы, связанные с продуктами (товарами). 
## Приложение должно иметь две конечные точки:
1. Конечная точка для получения информации о продукте:
   - Маршрут: `/product/{product_id}`
   - Метод: GET
   - Параметр пути:
     - `product_id`: идентификатор продукта (целое число)
   - Ответ: Возвращает объект JSON, содержащий информацию о продукте, основанную на предоставленном `product_id`.
2. Конечная точка для поиска товаров:
   - Маршрут: `/products/search`
   - Метод: GET
   - Параметры запроса:
     - `keyword` (строка, обязательна): ключевое слово для поиска товаров.
     - `category` (строка, необязательно): категория для фильтрации товаров.
     - `limit` (целое число, необязательно): максимальное количество товаров для возврата (по умолчанию 10, если не указано иное).
   - Ответ: Возвращает массив JSON, содержащий информацию о продукте, соответствующую критериям поиска.
3. Для примера можете использовать следующие данные с целью последующего направления ответа:
```bash
sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]
```
Пример:
Запрос GET на `/product/123` должен возвращать:
```bash
{
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}
```
В ответ на GET-запрос на `/products/search?keyword=phone&category=Electronics&limit=5` должно вернуться:
```bash
[
    {
        "product_id": 123,
        "name": "Smartphone",
        "category": "Electronics",
        "price": 599.99
    },
    {
        "product_id": 789,
        "name": "Iphone",
        "category": "Electronics",
        "price": 1299.99
    },
    ...
]
```
Обратите внимание, что если маршруты будут одинаковыми (например, /products/{product_id} и /products/search), то у нас 
второй маршрут будет не рабочим, тк слово search FastAPI будет пытаться привести к int, то есть обработать первый 
маршрут, и выдаст ошибку). Маршруты обрабатываются в порядке объявления хендлеров). 

Пожалуйста, внедрите приложение FastAPI и протестируйте конечные точки с помощью таких инструментов, как "curl", Postman
или любой другой клиент API.

# Описание решения:

1. Создание FastAPI приложения:
    a) В модуле main.py определили функцию create_app(), которая создает экземпляр FastAPI приложения.
    b) Внутри этой функции определили два обработчика маршрутов:
       - get_product() для обработки запросов на получение информации о продукте по его идентификатору 
         (/product/{product_id}).
       - search_product() для обработки запросов на поиск продуктов по ключевому слову, категории и ограничению 
         количества результатов (/products/search).
2. Обработчик get_product():
    - Этот обработчик принимает product_id в качестве параметра пути.
    - Он ищет продукт в списке sample_products с помощью генератора списков и функции next().
    - Если продукт найден, создается экземпляр Product и возвращается.
    - Если продукт не найден, возбуждается исключение HTTPException со статусом 404 Not Found и соответствующим 
      сообщением.
3. Обработчик search_product():
    a) Этот обработчик принимает следующие параметры запроса:
       - keyword (обязательный) - ключевое слово для поиска товаров.
       - category (необязательный) - категория для фильтрации товаров.
       - limit (необязательный, по умолчанию 10) - максимальное количество товаров для возврата.
    b) Сначала создается список results, содержащий продукты, в названии которых содержится ключевое слово (с учетом 
       регистра).
    с) Если указана категория, список results фильтруется, оставляя только продукты с указанной категорией.
    d) Возвращается список экземпляров Product, созданных из отфильтрованных данных, с ограничением по limit.
4. Запуск приложения:
    - В блоке if __name__ == '__main__' запускаем приложение с помощью uvicorn.run(), указывая путь к функции 
      create_app(), а также хост и порт.
    - Обработка исключений KeyboardInterrupt и других ошибок реализована с помощью блоков try/except.
5. Тестирование:
    a) Получение информации о продукте
       - Маршрут: /product/{product_id}
       - Метод: GET
Для тестирования этого маршрута создадим новый запрос GET в Postman, а в адресной строке укажем URL-адрес 
http://localhost:5080/product/123 (предполагая, что приложение запущено на локальном хосте и порту 5080).
При отправке этого запроса вы должны получить ответ со статусом 200 OK и следующим телом:
```bash
{
    "product_id": 123,
    "name": "Смартфон",
    "category": "Электроника",
    "price": 599.99
}
```
Если укажем несуществующий product_id, например, http://localhost:5080/product/999, то получим ответ со статусом 
404 Not Found и сообщением "Product not found".
    b) Поиск товаров
       - Маршрут: /products/search
       - Метод: GET
       - Параметры запроса:
         - keyword (обязательный)
         - category (необязательный)
         - limit (необязательный, по умолчанию 10)
Для тестирования этого маршрута создадим новый запрос GET в Postman и укажем URL-адрес 
http://localhost:5080/products/search?keyword=phone&category=Электроника&limit=5.
При отправке этого запроса должны получить ответ со статусом 200 OK и следующим телом:
```bash
[
    {
        "product_id": 123,
        "name": "Смартфон",
        "category": "Электроника",
        "price": 599.99
    },
    {
        "product_id": 789,
        "name": "iPhone",
        "category": "Электроника",
        "price": 1299.99
    }
]
```
Обратите внимание, что результаты отфильтрованы по ключевому слову "phone" и категории "Электроника", а количество 
возвращаемых продуктов ограничено 5.
Если не укажем параметр category, то результаты будут отфильтрованы только по ключевому слову. Например, для запроса 
http://localhost:5080/products/search?keyword=phone получим:
```bash
[
    {
        "product_id": 123,
        "name": "Смартфон",
        "category": "Электроника",
        "price": 599.99
    },
    {
        "product_id": 456,
        "name": "Чехол для телефона",
        "category": "Аксессуары",
        "price": 19.99
    },
    {
        "product_id": 789,
        "name": "iPhone",
        "category": "Электроника",
        "price": 1299.99
    }
]
```
Таким образом, было успешно протестировано данное решение с помощью Postman, проверив обе конечные точки и различные 
комбинации параметров запроса.

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
    └── models.py                 # Модуль, содержащий Pydantic модель для отзыва
```