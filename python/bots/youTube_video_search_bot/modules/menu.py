import datetime
import json
from dateutil import parser


from modules.time_manager import TimeManager
from modules.video_search import VideoSearch
from modules.telegram_bot import TelegramBot

# Константы

CATEGORY_OPTIONS = {
    '1': {'name': 'News', 'code': 'news'},
    '2': {'name': 'Movies', 'code': 'movies'},
    '3': {'name': 'Educational', 'code': 'education'},
    '4': {'name': 'Sports', 'code': 'sports'},
    '5': {'name': 'Comedy', 'code': 'comedy'},
    '6': {'name': 'Science and Technology', 'code': 'science'},
    '7': {'name': 'Music', 'code': 'music'},
    '8': {'name': 'Travel', 'code': 'travel'},
    '9': {'name': 'Food and Cooking', 'code': 'food'},
    '10': {'name': 'Gardening', 'code': 'gardening'},
    '11': {'name': 'Other', 'code': 'other'}
}

ORDER_OPTIONS = {
    '1': {'name': 'Date', 'code': 'date'},
    '2': {'name': 'Relevance', 'code': 'relevance'},
    '3': {'name': 'View Count', 'code': 'viewCount'}
}

REGION_OPTIONS = {
    '1': {'name': 'Ukraine', 'code': 'ua'},
    '2': {'name': 'Russia', 'code': 'ru'},
    '3': {'name': 'USA', 'code': 'us'}
}


class Menu:
    """Класс Menu для обработки взаимодействия с пользователем и поиска видео.

    Атрибуты:
        api_key (str): Ключ API YouTube Data для доступа к API.
        bot_token (str): Токен Telegram бота для доступа к API.
        chat_id (int): Идентификатор чата Telegram, куда будут отправляться видео.
    """

    def __init__(self, api_key: str, bot_token: str, chat_id: int):
        """Инициализация объекта Menu.

        Args:
            api_key (str): Ключ API YouTube Data для доступа к API.
            bot_token (str): Токен Telegram бота для доступа к API.
            chat_id (int): Идентификатор чата Telegram, куда будут отправляться видео.
        """
        self.api_key = api_key
        self.video_search = VideoSearch(api_key)  # Создание экземпляра VideoSearch
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.telegram_bot = TelegramBot(self.bot_token, self.chat_id, self.video_search)

    @staticmethod
    def get_valid_input(prompt: str, options: dict, default=None) -> str:
        """Получает корректный ввод пользователя на основе доступных опций.

        Args:
            prompt (str): Подсказка для пользователя.
            options (dict): Словарь доступных опций с ключами в виде входных значений и значениями в виде описания опций.
            default: Значение по умолчанию, возвращаемое при пустом вводе пользователя.

        Returns:
            str: Корректный ввод пользователя или значение по умолчанию.
        """
        # Запрашиваем ввод пользователя
        user_input = input(prompt)

        # Если пользователь не ввел ничего, возвращаем значение по умолчанию
        if not user_input:
            return default

        # Проверяем, что введенное значение есть среди допустимых опций
        if user_input in options:
            return user_input

        # Выводим сообщение об ошибке, если введенное значение не является допустимой опцией
        print("Неверный ввод. Пожалуйста, выберите допустимую опцию.")

    @staticmethod
    def parse_date_input(date_input: str) -> datetime.datetime | None:
        """Преобразует введенную пользователем дату.

        Args:
            date_input (str): Введенная пользователем дата в формате ГГГГ-ММ-ДД.

        Returns:
            datetime.datetime | None: Преобразованная дата или None, если преобразование не удалось.
        """
        try:
            # Пытаемся распарсить введенную пользователем дату с помощью dateutil.parser
            parsed_date = parser.parse(date_input)

            # Проверяем, является ли полученный объект типом datetime.datetime
            # Если да, то возвращаем его, иначе возвращаем None
            return parsed_date if isinstance(parsed_date, datetime.datetime) else None
        except ValueError:
            # Если возникла ошибка при парсинге даты, возвращаем None
            return None

    async def show_menu(self) -> None:
        """Показывает меню пользователю и обрабатывает поиск видео и отправку."""
        # Показываем категории для поиска видео
        print("Choose a category for video search:")
        for key, value in CATEGORY_OPTIONS.items():
            print(f"{key}: {value['name']}")

        # Получаем от пользователя номер выбранной категории
        category_input = self.get_valid_input("Enter the category number: ", CATEGORY_OPTIONS, default=None)

        # Получаем код выбранной категории, используя словарь CATEGORY_OPTIONS
        category = CATEGORY_OPTIONS[category_input]['code'] if category_input else None

        # Получаем от пользователя тему для поиска видео
        q = input("\nEnter the search query: ")

        # Выводим опции сортировки для поиска видео
        print("Choose a sorting option for video search:")
        for key, value in ORDER_OPTIONS.items():
            print(f"{key}: {value['name']}")

        # Получаем от пользователя номер выбранной сортировки
        order_input = self.get_valid_input("Введите номер сортировки: ", ORDER_OPTIONS, default='2')

        # Получаем выбранный код сортировки, используя словарь ORDER_OPTIONS
        order = ORDER_OPTIONS[order_input]['code']

        # Выводим опции региона для поиска видео
        print("Choose a region for video search:")
        for key, value in REGION_OPTIONS.items():
            print(f"{key}: {value['name']}")

        # Получаем от пользователя номер выбранного региона
        region_input = self.get_valid_input("Enter the region number: ", REGION_OPTIONS, default='ua')

        # Получаем код выбранного региона, используя словарь REGION_OPTIONS
        region_code = REGION_OPTIONS[region_input]['code']

        # Получаем от пользователя максимальное количество результатов для поиска
        max_results = int(input("\nEnter the maximum number of results: "))

        # Получаем от пользователя дату публикации для поиска видео
        date_input = input(
            "\nEnter the publication date in the format YYYY-MM-DD (e.g., 2023-07-21), or leave it blank: ")

        # Парсим введенную дату с помощью функции parse_date_input
        published_after = self.parse_date_input(date_input)

        # Выполняем поиск видео с использованием экземпляра video_search
        response = self.video_search.search_videos(q=q, order=order, max_results=max_results,
                                                   published_after=published_after, category=category,
                                                   region_code=region_code)

        # Выводим ответ от YouTube API
        print("Response from YouTube API:")
        print(json.dumps(response, ensure_ascii=False))

        # Выводим значения nextPageToken для пагинации результатов поиска
        print(f"nextPageToken {response['nextPageToken']}")

        # Выводим информацию о каждом найденном видео в формате "Название, Дата публикации, URL на YouTube"
        [print("%s, %s, https://youtu.be/%s" % (
            item['snippet']['title'], item['snippet']['publishedAt'], item['id']['videoId'])) for item in
         response['items']]

        # Если текущее время входит в разрешенный временной диапазон, выполняем асинхронную отправку видеостатей
        # на Telegram
        if TimeManager.is_within_time_range():
            await self.telegram_bot.send_videos_periodically(response['items'])
        else:
            print("Not within the allowed time range.")
