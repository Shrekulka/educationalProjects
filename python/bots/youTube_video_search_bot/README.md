**Project Description: YouTube Video Search Bot**

YouTube Video Search Bot is a Telegram bot developed using asynchronous programming with the `aiogram` library for 
interacting with the Telegram API and `aiohttp` for working with the YouTube API. The bot allows users to search for 
videos on YouTube based on various parameters and receive periodic updates with links to videos at designated times.

**Functionality:**

1. Video Search:
   - Users can choose a video category from a predefined list, including categories like news, movies, education, sports,
     comedy, and others.
   - Users provide search keywords (query) to perform the video search.
   - Users can select the sorting order of search results based on publish date, relevance, or view count.
   - Users have the option to specify the region for video search.

2. Displaying Results:
   - The bot sends users a list of videos with their titles, publish dates, and links to view on YouTube.
   - If available, the response may also include a brief description of the video and the publish date.

3. Periodic Video Sending:
   - If the video search (sending) time falls within the range of 7 AM to 10 PM (GMT), the bot periodically sends a single
     video link with a specified interval (3 hours).
   - The sending occurs as a simple text message with the video link.

**Project Settings:**

To run the bot, the following keys and settings are required:

1. YouTube API Key (`API_KEY`): The developer token (key) used to access the YouTube API and execute search queries. The
   API_KEY should be specified in the `.env` file.

2. Telegram Bot Token (`TELEGRAM_BOT_TOKEN`): The bot token for interacting with the Telegram API. This token is provided
   when creating a new bot using BotFather in Telegram. The token should be specified in the `.env` file.

3. Telegram Chat ID (`TELEGRAM_CHAT_ID`): The identifier of the chat where messages with search results and periodic 
   video links will be sent. The chat ID can be obtained by querying the bot `@userinfobot` in Telegram. The value of 
   `TELEGRAM_CHAT_ID` should also be specified in the `.env` file.

**Methods and Properties:**

1. `VideoSearch`:
   - `search_videos(q, order='relevance', max_results=5, published_after=None, category=None, region_code=None)`: Method
     for performing a video search on YouTube with specified parameters. It takes query, sorting order, maximum results,
     publish date, category, and region as parameters. Returns a list of found videos.

2. `TelegramBot`:
   - `send_video(video_id)`: Asynchronous method for sending a video with the given identifier to the Telegram chat.
   - `send_videos_periodically(videos)`: Asynchronous method for periodically sending a list of videos to Telegram. Waits
     for a specified time interval between sending.
   - `on_startup()`: Asynchronous method for starting the bot and listening for Telegram messages.
   - `on_shutdown()`: Asynchronous method for stopping the bot and closing the `aiohttp.ClientSession` session.

3. `Menu`:
   - `get_valid_input(prompt, options, default=None)`: Static method for obtaining valid input from the user. It takes a
     prompt, a list of valid options, and an optional default value. Returns the user's valid input.
   - `parse_date_input(date_input)`: Static method for parsing the user's date input and converting it to a `datetime.date`
     object or `None` if the date format is incorrect.
   - `show_menu()`: Asynchronous method for interacting with the user, providing a menu to choose category, keywords, 
     sorting, region, and date. Then it performs video search using `VideoSearch`, displays the results, and initiates 
     asynchronous video sending to Telegram.

**Conclusion:**

The "YouTube Video Search Bot" project offers users a convenient way to search for and view videos on YouTube, as well 
as receive periodic updates with interesting videos on Telegram. 




Описание проекта "YouTube Video Search Bot":

YouTube Video Search Bot - это Telegram бот, разработанный на основе асинхронного программирования с использованием 
библиотеки `aiogram` для взаимодействия с Telegram API и `aiohttp` для работы с YouTube API. Бот предоставляет 
пользователям возможность искать видео на YouTube по различным параметрам, а также получать периодические обновления с 
ссылками на видео в отведенные часы.

Функциональность бота:

1. Поиск видео:
   - Пользователь может выбрать категорию видео из предложенного списка, включающего такие категории, как новости, 
     фильмы, образовательные видео, спорт, юмор и другие.
   - Пользователь указывает ключевые слова (запрос), по которым будет выполняться поиск.
   - Возможность выбора сортировки результатов по дате публикации, рейтингу или количеству просмотров.
   - Пользователь может указать регион, в котором будет выполняться поиск видео.

2. Отображение результатов:
   - Бот отправляет пользователю список видео с их названиями, датами публикации и ссылками на просмотр на YouTube.
   - Если доступны, в ответе также присутствует краткое описание видео и дата публикации.

3. Периодическая отправка видео:
   - Если время поиска видео (отправки) попадает в интервал с 7 утра до 22 вечера (GMT), бот периодически отправляет 
     одну ссылку на видео с заданным интервалом (3 часа).
   - Отправка происходит в виде простого текстового сообщения с ссылкой на видео.

Настройки проекта:

Для работы бота требуется наличие следующих ключей и настроек:

1. YouTube API Key (API_KEY): Токен (ключ) разработчика, используемый для доступа к YouTube API и выполнения поисковых 
   запросов. API_KEY должен быть указан в файле .env.

2. Telegram Bot Token (TELEGRAM_BOT_TOKEN): Токен бота для взаимодействия с Telegram API. Этот токен выдается при 
   создании нового бота в Telegram BotFather. Токен должен быть указан в файле .env.

3. Telegram Chat ID (TELEGRAM_CHAT_ID): Идентификатор чата, в который будут отправляться сообщения с результатами поиска
   и периодическими ссылками на видео. Идентификатор чата можно получить, обратившись к боту @userinfobot в Telegram. 
   Значение TELEGRAM_CHAT_ID также должно быть указано в файле .env.

Методы и свойства:

1. `VideoSearch`:
   - `search_videos(q, order='relevance', max_results=5, published_after=None, category=None, region_code=None)`: Метод 
      для выполнения поиска видео на YouTube с заданными параметрами. Принимает параметры запроса, сортировки, 
      максимального количества результатов, даты публикации, категории и региона. Возвращает список найденных видео.

2. `TelegramBot`:
   - `send_video(video_id)`: Асинхронный метод для отправки видео с указанным идентификатором в чат Telegram.
   - `send_videos_periodically(videos)`: Асинхронный метод для периодической отправки списка видео в Telegram. Ожидает 
      определенный интервал времени между отправками.
   - `on_startup()`: Асинхронный метод для запуска бота и начала прослушивания сообщений Telegram.
   - `on_shutdown()`: Асинхронный метод для остановки бота и

 закрытия сессии `aiohttp.ClientSession`.

3. `Menu`:
   - `get_valid_input(prompt, options, default=None)`: Статический метод для получения допустимого ввода от пользователя.
      Принимает приглашение (подсказку), список допустимых вариантов и значение по умолчанию. Возвращает валидный 
      пользовательский ввод.
   - `parse_date_input(date_input)`: Статический метод для разбора пользовательского ввода даты и преобразования его в 
      объект `datetime.date` или `None`, если формат даты некорректен.
   - `show_menu()`: Асинхронный метод для взаимодействия с пользователем, предоставляет меню для выбора категории, 
      ключевых слов, сортировки, региона и даты. Затем выполняет поиск видео с использованием `VideoSearch`, выводит 
      результаты и запускает асинхронную отправку видео в Telegram.

4. Константы:
   - `CATEGORY_OPTIONS`: Словарь с опциями категорий видео для выбора пользователем.
   - `ORDER_OPTIONS`: Словарь с опциями сортировки результатов поиска.
   - `REGION_OPTIONS`: Словарь с опциями регионов для выбора пользователем.

Проект предоставляет пользователям удобный способ поиска и просмотра видео на YouTube, а также возможность получать 
периодические обновления с интересными видео на Telegram. 