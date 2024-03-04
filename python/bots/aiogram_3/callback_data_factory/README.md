# The essence of the Callback Data Factory is that we can specify the structure of callback_data, and a special class 
# will automatically build it - when forming a button, and then filter and parse it - when handling a press on this button.

### For example, a class describing the callback factory could be like this:
```bash
# Definition of the GoodsCallbackFactory class, which inherits CallbackData and sets the prefix 'goods' to create
# callback data.
class GoodsCallbackFactory(CallbackData, prefix='goods'):
    # Definition of the category_id attribute of type int to store the category identifier.
    category_id: int
    # Definition of the subcategory_id attribute of type int to store the subcategory identifier.
    subcategory_id: int
    # Definition of the item_id attribute of type int to store the item identifier.
    item_id: int
```

### Next, based on this class, we can already form inline buttons for the keyboard:
```bash
# ...
# Creating the first button for category 1.
button_1 = InlineKeyboardButton(
    text='Category 1',                   # Button text
    callback_data=GoodsCallbackFactory(  # Creating callback data using the GoodsCallbackFactory class
        category_id=1,                   # Setting the category identifier
        subcategory_id=0,                # Setting the subcategory identifier
        item_id=0                        # Setting the item identifier
    ).pack())                            # Calling the pack() method, which converts the class instance into a string of 
                                         # the form '<prefix>:<category_id>:<subcategory_id>:<item_id>'
                                         

# Creating the second button for category 2.
button_2 = InlineKeyboardButton(
    text='Category 2',                   # Button text
    callback_data=GoodsCallbackFactory(  # Creating callback data using the GoodsCallbackFactory class
        category_id=2,                   # Setting the category identifier
        subcategory_id=0,                # Setting the subcategory identifier
        item_id=0                        # Setting the item identifier
    ).pack())                            # Calling the pack() method, which converts the class instance into a string of
                                         # the form '<prefix>:<category_id>:<subcategory_id>:<item_id>'
                                         
# ...
```

### Then, we need to form a keyboard from these buttons. Inline keyboard is an array of arrays of inline buttons:
```bash
# Creating markup for an inline keyboard using buttons button_1 and button_2.
markup = InlineKeyboardMarkup(inline_keyboard=[[button_1],[button_2]])
```

### Next, let's send this keyboard to the user. Let's create a simple handler that will send it to the chat when
### the /start command is received:
```bash
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Here is the keyboard',
        reply_markup=markup)
```

### Let's create a handler that catches button clicks to inspect the update structure.
```bash
@router.callback_query()
async def process_any_inline_button_press(callback: CallbackQuery):
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))
```

### Run the bot and send it the start command. The expected result:
![img.png](images_for_readme/example_1.png)

The difference between the two handlers (@router.callback_query() and @router.callback_query(GoodsCallbackFactory.filter()))
is that the first handler uses a filter defined using GoodsCallbackFactory.filter(), which filters the callback_data so
that the handler responds only to specific types of callback_data corresponding to the specified criteria. The second 
handler does not use a filter and responds to all callback_data without restrictions.

### This handler will respond to pressing any inline button and print the update to the terminal
```bash
# Decorator with a filter indicating the handler for button clicks, filtered using GoodsCallbackFactory
@router.callback_query(GoodsCallbackFactory.filter())
# Asynchronous handler function with parameters callback and callback_data
async def process_category_press(callback: CallbackQuery, callback_data: GoodsCallbackFactory):
    await callback.message.answer(text=callback_data.pack())  # Sending a response message with data from callback_data
    await callback.answer()                              # Sending confirmation of handling the button press to the user
```

### If we need to catch only the press of the first button ("Category 1"), once again the magic filter can help us
### and the handler may look like this:
```bash
@router.callback_query(GoodsCallbackFactory.filter(F.category_id == 1))
async def process_category_press(callback: CallbackQuery,
                                 callback_data: GoodsCallbackFactory):
    await callback.message.answer(text=callback_data.pack())  # Sending a response message with data from callback_data
    await callback.answer()                              # Sending confirmation of handling the button press to the user
```

### There are convenient ways to extract data from callback_data. Let's respond to pressing any button. And we'll
### send a formatted response with data extracted from callback_data to the chat.
```bash
# This handler will respond to pressing any inline button and send a formatted response with data
# from callback_data to the chat
# Decorator with a filter indicating the handler for button clicks, filtered using GoodsCallbackFactory
@router.callback_query(GoodsCallbackFactory.filter())  
# Asynchronous handler function with parameters callback and callback_data
async def process_category_press(callback: CallbackQuery, callback_data: GoodsCallbackFactory): 
    await callback.message.answer(                                   # Sending a response message
        text=f'Goods category: {callback_data.category_id}\n'        # Text with information about the goods category
             f'Goods subcategory: {callback_data.subcategory_id}\n'  # Text with information about the goods subcategory
             f'Item: {callback_data.item_id}')                       # Text with information about the item
    await callback.answer()                              # Sending confirmation of handling the button press to the user
```

## Features of Working with Callback Factory
Callback factories are convenient to use when you need to create dynamic keyboards that change during the project's lifecycle. For instance, if buttons depend on what is currently in a dynamically changing database.

It's also convenient to use a factory if you need to pass data through callback_data to a handler and then easily work with it by parsing the structure of callback_data into composite parts and accessing them as attributes of the factory class instance.

## When working with callback factories, keep in mind some peculiarities/limitations:

1. The length of callback_data for inline buttons is limited to 64 bytes. This is not much, but generally sufficient for implementing many ideas.
2. The colon ":" is used as the default data separator in callback_data. However, you can replace it with another symbol or group of symbols using the `sep` parameter. It makes sense to change the separator if you may have colons in the data from which you build callback_data.
3. If you're forming an inline keyboard as a list of button lists, you need to pack the instance of your factory class into a string using the `pack()` method.
4. If you're building an inline keyboard using a builder, adding arguments to the `button()` method, you don't need to pack the factory class instance into a string.
5. Using an insecure callback factory is a potential security threat to your service because malicious users can tamper with callback_data by sending requests to your bot through Telegram servers with button data that you didn't send to the user.

## Prefix in the Callback Factory Class is Needed to Uniquely Identify Callback Data Generated with this Class.
The reason is that your bot may have several different callback factory classes, each of which will generate its own callback_data for different purposes.

### Let's explore the usage of prefix in the callback factory with examples in more detail.
Suppose we have a bot for an online store. This store has categories of products, subcategories, and individual items.
To simplify user navigation through the catalog, we decided to use inline keyboards with callbacks.

### For this, we need 3 callback factories:
```bash
# Factory for category callbacks
class CategoriesCallbacks(CallbackData, prefix="categories"):
    category_id: int

# Factory for subcategory callbacks    
class SubcategoriesCallbacks(CallbackData, prefix="subcategories"):
    category_id: int
    subcategory_id: int

# Factory for item callbacks
class ItemsCallbacks(CallbackData, prefix="items"):
    category_id: int 
    subcategory_id: int
    item_id: int
```
### Note that each factory has its own prefix:
- categories
- subcategories
- items

This is done to distinguish callbacks from different factories.

### Now let's form callbacks for categories:
```bash
cat_1_cb = CategoriesCallbacks(category_id=1).pack()
# Result: categories:1

cat_2_cb = CategoriesCallbacks(category_id=2).pack() 
# Result: categories:2
```
Here, the callback data contains the "categories" prefix, indicating that the callback was created by the 
CategoriesCallbacks factory.

### Similarly for subcategories:
```bash
subcat_1_cb = SubcategoriesCallbacks(category_id=1, subcategory_id=5).pack()
# Result: subcategories:1:5 

subcat_2_cb = SubcategoriesCallbacks(category_id=2, subcategory_id=8).pack()
# Result: subcategories:2:8
```
In this case, the "subcategories" prefix indicates that the callbacks were created by the SubcategoriesCallbacks factory.

### And for items with the "items" prefix:
```bash
item_1_cb = ItemsCallbacks(category_id=1, subcategory_id=5, item_id=23).pack()
# Result: items:1:5:23
```
Thus, having a unique prefix allows us to differentiate callbacks from different factories.

### Then in the handlers, we can analyze the prefix and call the appropriate business logic:
```bash
@dp.callback_query(text_startswith="categories:") 
# Handling category callbacks
async def categories_callback_handler(callback: CallbackQuery):
    ...

@dp.callback_query(text_startswith="subcategories:")
# Handling subcategory callbacks
async def subcategories_callback_handler(callback: CallbackQuery):
   ...   

@dp.callback_query(text_startswith="items:")
# Handling item callbacks  
async def items_callback_handler(callback: CallbackQuery):
    ...
```
This is how using prefixes in callback factories helps structure the code and navigation through the bot's sections.


## Project Structure:
```bash
📁 callback_data_factory                    # Root directory of the entire project
 │
 ├── .env                                   # File with environment variables (secret data) for configuring the bot.
 │
 ├── .env.example                           # File with sample secrets for GitHub
 │
 ├── .gitignore                             # File that tells git which files and directories not to track
 │
 ├── bot.py                                 # Main executable file - entry point into the bot
 │
 ├── requirements.txt                       # File with project dependencies.
 │
 ├── logger_config.py                       # Logger configuration.
 │
 ├── README.md                              # File with project description.
 │
 ├── 📁 images_for_readme/                  # Directory for storing images for use in README.md.         
 │   └── example_1.png                      # Image used in README.md
 │
 ├── 📁 config_data/                        # Directory with the bot configuration module.
 │   ├── __init__.py                        # Package initializer file. 
 │   └── config_data.py                     # Module for bot configuration.
 │
 ├── 📁 database/                           # Package for working with the database.
 │   ├── __init__.py                        # Package initializer file.     
 │   └── database.py                        # Module with the database template.
 │
 ├── 📁 filters/                            # Package with custom filters.
 │   ├── __init__.py                        # Package initializer file.      
 │   └── filters.py                         # Module with custom filters.
 │ 
 ├── 📁 handlers/                           # Package with handlers.
 │   ├── __init__.py                        # Package initializer file.
 │   └── user_handlers.py                   # Module with user handlers. Main handlers for bot updates.
 │                                                 
 └── 📁 keyboards/                          # Package with bot keyboards.
     ├── __init__.py                        # Package initializer file.            
     └── keyboard_utils.py                  # Module with utilities for working with keyboards.
```
Educational material on Stepik - https://stepik.org/course/120924/syllabus





# Суть Callback Data Factory в том, что мы можем указать структуру callback_data, а специальный класс будет автоматически 
# ее собирать - при формировании кнопки, а затем фильтровать и разбирать - при обработке нажатия на эту кнопку.

### Например, класс, описывающий фабрику коллбэков, может быть таким:
```bash
# Определение класса GoodsCallbackFactory, который наследует CallbackData и устанавливает префикс 'goods' для создания 
# коллбэк-данных.
class GoodsCallbackFactory(CallbackData, prefix='goods'):
    # Определение атрибута category_id типа int для хранения идентификатора категории.
    category_id: int
    # Определение атрибута subcategory_id типа int для хранения идентификатора подкатегории.
    subcategory_id: int
    # Определение атрибута item_id типа int для хранения идентификатора товара.
    item_id: int
```

### Далее, на основе этого класса мы уже можем формировать инлайн-кнопки для клавиатуры:
```bash
# ...
# Создание первой кнопки для категории 1.
button_1 = InlineKeyboardButton(
    text='Категория 1',                  # Текст кнопки
    callback_data=GoodsCallbackFactory(  # Создание коллбэк-данных с помощью класса GoodsCallbackFactory
        category_id=1,                   # Установка идентификатора категории
        subcategory_id=0,                # Установка идентификатора подкатегории
        item_id=0                        # Установка идентификатора товара
    ).pack())                            # Вызов метода pack(), который преобразует экземпляр класса в строку вида
                                         # '<prefix>:<category_id>:<subcategory_id>:<item_id>'


# Создание второй кнопки для категории 2.
button_2 = InlineKeyboardButton(
    text='Категория 2',                  # Текст кнопки
    callback_data=GoodsCallbackFactory(  # Создание коллбэк-данных с помощью класса GoodsCallbackFactory
        category_id=2,                   # Установка идентификатора категории
        subcategory_id=0,                # Установка идентификатора подкатегории
        item_id=0                        # Установка идентификатора товара
    ).pack())                            # Вызов метода pack(), который преобразует экземпляр класса в строку вида
                                         # '<prefix>:<category_id>:<subcategory_id>:<item_id>'
# ...
```

### Далее, нужно из этих кнопок сформировать клавиатуру. Инлайн-клавиатура - это массив массивов инлайн-кнопок:
```bash
# # Создание разметки для инлайн-клавиатуры с использованием кнопок button_1 и button_2.
markup = InlineKeyboardMarkup(inline_keyboard=[[button_1],[button_2]])
```
### Далее отправим эту клавиатуру пользователю. Создадим простейший хэндлер, который будет ее отправлять в чат по 
### команде /start:
```bash
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Вот такая клавиатура',
        reply_markup=markup)
```
### Сделаем хэндлер, который будет ловить нажатия на кнопки, чтобы посмотреть на структуру апдейта.
```bash
@router.callback_query()
async def process_any_inline_button_press(callback: CallbackQuery):
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))
```
### Запустим бота и отправим ему команду старт. Результат ожидаемый:
![img.png](images_for_readme/example_1.png)

Отличие между двумя хэндлерами (@router.callback_query() и @router.callback_query(GoodsCallbackFactory.filter()))
заключается в том, что первый хэндлер использует фильтр, определенный с помощью GoodsCallbackFactory.filter(), который 
фильтрует callback_data, чтобы хэндлер реагировал только на определенные типы callback_data, соответствующие указанным 
критериям. Второй хэндлер не использует фильтр и реагирует на все callback_data без ограничений.

### Этот хэндлер будет срабатывать на нажатие любой инлайн кнопки и распечатывать апдейт в терминал
```bash
# Декоратор с фильтром, указывающий на обработчик нажатия кнопок, отфильтрованных с помощью GoodsCallbackFactory
@router.callback_query(GoodsCallbackFactory.filter())
# Асинхронная функция-обработчик с параметрами callback и callback_data
async def process_category_press(callback: CallbackQuery, callback_data: GoodsCallbackFactory):
    await callback.message.answer(text=callback_data.pack())  # Отправляем ответное сообщение с данными из callback_data
    await callback.answer()                               # Отправка подтверждения обработки нажатия кнопки пользователю
```

### Если нужно поймать только нажатие на первую кнопку ("Категория 1"), то нам в очередной раз может помочь магический 
### фильтр и хэндлер может быть таким:
```bash
@router.callback_query(GoodsCallbackFactory.filter(F.category_id == 1))
async def process_category_press(callback: CallbackQuery,
                                 callback_data: GoodsCallbackFactory):
    await callback.message.answer(text=callback_data.pack())  # Отправляем ответное сообщение с данными из callback_data
    await callback.answer()                               # Отправка подтверждения обработки нажатия кнопки пользователю
```

### Есть удобные способы извлечения данных из callback_data. Будем принимать нажатие на любую кнопку. А пользователю мы
### отправим форматированный текст с данными, извлеченными из callback_data.
```bash
# Этот хэндлер будет срабатывать на нажатие любой инлайн кнопки и отправлять в чат форматированный ответ с данными
# из callback_data
# Декоратор с фильтром, указывающий на обработчик нажатия кнопок, отфильтрованных с помощью GoodsCallbackFactory
@router.callback_query(GoodsCallbackFactory.filter())  
# Асинхронная функция-обработчик с параметрами callback и callback_data
async def process_category_press(callback: CallbackQuery, callback_data: GoodsCallbackFactory): 
    await callback.message.answer(                                      # Отправляем ответное сообщение
        text=f'Категория товаров: {callback_data.category_id}\n'        # Текст с информацией о категории товаров
             f'Подкатегория товаров: {callback_data.subcategory_id}\n'  # Текст с информацией о подкатегории товаров
             f'Товар: {callback_data.item_id}')                         # Текст с информацией о товаре
    await callback.answer()                               # Отправка подтверждения обработки нажатия кнопки пользователю
```

## Особенности работы с фабрикой коллбэков
Фабрику коллбэков удобно использовать тогда, когда требуется создавать динамические клавиатуры, меняющиеся в ходе жизни 
проекта. Например, если кнопки зависят от того, что в данный момент лежит в динамически меняющейся базе данных.

Также удобно использовать фабрику, если через callback_data требуется передавать какие-то данные в хэндлер и затем 
удобно с ними работать, разбирая структуру callback_data на составные части и обращаясь к ним как к атрибутам экземпляра 
класса фабрики.

## При работе с фабрикой коллбэков нужно держать в голове некоторые особенности/ограничения:

1. Длина callback_data для инлайн-кнопок ограничена 64 байтами. Это не очень много, но в целом, достаточно для 
   реализации многих задумок.
2. В качестве разделителя данных в callback_data, по умолчанию используется двоеточие. Но можно заменить на другой 
   символ или группу символов. За это отвечает параметр sep. Имеет смысл менять разделитель в том случае, если у вас 
   могут оказаться двоеточия в данных, из которых вы строите callback_data.
3. Если вы формируете инлайн-клавиатуру как список списков кнопок, то экземпляр класса вашей фабрики необходимо 
   упаковать в строку с помощью метода pack().
4. Если вы формируете инлайн-клавиатуру с помощью билдера, добавляя аргументы в метод button() - упаковывать экземпляр 
   класса фабрики в строку не надо.
5. Использование незащищенной фабрики коллбэков - это потенциальная угроза безопасности для вашего сервиса, потому что 
   недобросовестные пользователи могут подменять callback_data, отправляя вашему боту запросы через сервера телеграм с 
   данными кнопок, которые вы пользователю не отправляли.

## Prefix в классе фабрики коллбэков нужен для того, чтобы однозначно идентифицировать callback_data, сформированные с 
## помощью этого класса.
Дело в том, что в боте может быть несколько разных классов фабрик коллбэков, каждый из которых будет формировать свои 
callback_data для разных целей.

### Давайте рассмотрим использование префикса в фабрике коллбэков на примерах поподробнее.
Допустим, у нас есть бот для интернет-магазина. В этом магазине есть категории товаров, подкатегории и сами товары.
Чтобы упростить навигацию пользователя по каталогу, мы решили использовать inline-клавиатуры с коллбэками.

### Для этого нам нужно 3 фабрики коллбэков:
```bash
# Фабрика для коллбэков категорий
class CategoriesCallbacks(CallbackData, prefix="categories"):
    category_id: int

# Фабрика для коллбэков подкатегорий    
class SubcategoriesCallbacks(CallbackData, prefix="subcategories"):
    category_id: int
    subcategory_id: int

# Фабрика для коллбэков товаров
class ItemsCallbacks(CallbackData, prefix="items"):
    category_id: int 
    subcategory_id: int
    item_id: int
```
### Обратите внимание, у каждой фабрики есть свой префикс:
- categories
- subcategories
- items

Это сделано для того, чтобы можно было отличать коллбэки от разных фабрик.

### Теперь сформируем коллбэки для категорий:
```bash
cat_1_cb = CategoriesCallbacks(category_id=1).pack()
# получится: categories:1

cat_2_cb = CategoriesCallbacks(category_id=2).pack() 
# получится: categories:2
```
Видно, что в данных коллбэка присутствует префикс "categories", который указывает, что коллбэк сформирован фабрикой 
CategoriesCallbacks.

### Аналогично для подкатегорий:
```bash
subcat_1_cb = SubcategoriesCallbacks(category_id=1, subcategory_id=5).pack()
# получится: subcategories:1:5 

subcat_2_cb = SubcategoriesCallbacks(category_id=2, subcategory_id=8).pack()
# получится: subcategories:2:8
```
Здесь префикс "subcategories" показывает, что коллбэки созданы фабрикой SubcategoriesCallbacks.

### И для товаров с префиксом "items":
```bash
item_1_cb = ItemsCallbacks(category_id=1, subcategory_id=5, item_id=23).pack()
# получится: items:1:5:23
```
Таким образом, наличие уникального префикса позволяет нам различать коллбэки от разных фабрик.

### А далее в обработчиках мы можем анализировать префикс и вызывать нужную бизнес-логику:
```bash
@dp.callback_query(text_startswith="categories:") 
# обработка коллбэков категорий
async def categories_callback_handler(callback: CallbackQuery):
    ...

@dp.callback_query(text_startswith="subcategories:")
# обработка коллбэков подкатегорий
async def subcategories_callback_handler(callback: CallbackQuery):
   ...   

@dp.callback_query(text_startswith="items:")
# обработка коллбэков товаров  
async def items_callback_handler(callback: CallbackQuery):
    ...
```
Вот как использование префиксов в фабриках коллбэков помогает структурировать код и навигацию по разделам бота.

## Структура проекта:
```bash
📁 callback_data_factory                    # Корневая директория всего проекта
 │
 ├── .env                                   # Файл с переменными окружения (секретными данными) для конфигурации бота.
 │
 ├── .env.example                           # Файл с примерами секретов для GitHub
 │
 ├── .gitignore                             # Файл, сообщающий гиту какие файлы и директории не отслеживать
 │
 ├── bot.py                                 # Основной исполняемый файл - точка входа в бот
 │
 ├── requirements.txt                       # Файл с зависимостями проекта.
 │
 ├── logger_config.py                       # Конфигурация логгера.
 │
 ├── README.md                              # Файл с описанием проекта.
 │
 ├── 📁 images_for_readme/                  # Директория для хранения изображений для использования в README.md.         
 │   └── example_1.png                      # Изображение, используемое в README.md
 │
 ├── 📁 config_data/                        # Директория с модулем конфигурации бота.
 │   ├── __init__.py                        # Файл-инициализатор пакета. 
 │   └── config_data.py                     # Модуль для конфигурации бота.
 │
 ├── 📁 database/                           # Пакет для работы с базой данных.
 │   ├── __init__.py                        # Файл-инициализатор пакета.     
 │   └── database.py                        # Модуль с шаблоном базы данных.
 │
 ├── 📁 filters/                            # Пакет с пользовательскими фильтрами.
 │   ├── __init__.py                        # Файл-инициализатор пакета.      
 │   └── filters.py                         # Модуль с пользовательскими фильтрами.
 │ 
 ├── 📁 handlers/                           # Пакет с обработчиками.
 │   ├── __init__.py                        # Файл-инициализатор пакета.
 │   └── user_handlers.py                   # Модуль с обработчиками пользователя. Основные обработчики обновлений бота.
 │                                                 
 └── 📁 keyboards/                          # Пакет с клавиатурами бота.
     ├── __init__.py                        # Файл-инициализатор пакета.            
     └── keyboard_utils.py                  # Модуль с утилитами для работы с клавиатурами.
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus