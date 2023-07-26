import aiohttp
import logging
from datetime import datetime
from googleapiclient.discovery import build


class VideoSearch:
    """Класс VideoSearch для поиска видео на YouTube.

    Этот класс использует YouTube API для поиска видео по заданным параметрам и получения информации о видео.

    Атрибуты:
        api_key (str): Ключ API для доступа к YouTube API.

    Методы:
        search_videos(q: str, order: str = 'relevance', max_results: int = 5, published_after: datetime = None,
                      category: str = None, region_code: str = None) -> dict:
            Осуществляет поиск видео на YouTube по заданным параметрам.

        get_category_id_by_name(category_name: str, region_code: str) -> str:
            Возвращает идентификатор категории по её названию и коду региона.

        async get_video_info(video_id: str) -> dict:
            Асинхронно получает информацию о видео по его идентификатору.

        async get_video_url(video_id: str) -> str:
            Асинхронно получает URL видео по его идентификатору.
    """

    def __init__(self, api_key: str):
        """Инициализация объекта VideoSearch.

        Args:
            api_key (str): Ключ API для доступа к YouTube API.
        """
        self.api_key = api_key
        # Создаем сервис YouTube API с помощью функции build.
        # Параметры функции: 'youtube' - имя API, 'v3' - версия API, developerKey - ключ API.
        self.service = build('youtube', 'v3', developerKey=api_key)

    def search_videos(self, q: str, order: str = 'relevance', max_results: int = 5,
                      published_after: datetime = None, category: str = None,
                      region_code: str = None) -> dict:
        """Осуществляет поиск видео на YouTube по заданным параметрам.

        Args:
            q (str): Тема для поиска видео.
            order (str, optional): Сортировка результатов. По умолчанию используется 'relevance'.
            max_results (int, optional): Максимальное количество результатов. По умолчанию 5.
            published_after (datetime, optional): Ограничение по дате публикации. По умолчанию None.
            category (str, optional): Категория видео. По умолчанию None.
            region_code (str, optional): Код региона для поиска. По умолчанию None.

        Returns:
            dict: Результаты поиска в виде словаря.
        """
        def format_timestamp(dt: datetime) -> str:
            """Преобразует дату и время в строку в формате ISO 8601.

            Args:
                dt (datetime): Дата и время.

            Returns:
                str: Строка с датой и временем в формате ISO 8601.
            """
            return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        # Преобразуем объект datetime в строку в формате ISO 8601, если задан параметр published_after,
        # иначе присваиваем переменной published_after_iso значение None.
        published_after_iso = format_timestamp(published_after) if published_after else None

        # Создаем запрос к YouTube API, используя метод search().list().
        # Передаем параметры для поиска видео, такие как q (тема), order (сортировка),
        # maxResults (максимальное количество результатов), publishedAfter (ограничение по дате публикации)
        # и regionCode (код региона для поиска).
        request = self.service.search().list(
            q=q,
            part="snippet",
            type='video',
            order=order,
            maxResults=max_results,
            publishedAfter=published_after_iso,
            regionCode=region_code
        )
        # Выполняем запрос и получаем ответ от YouTube API.
        response = request.execute()

        # Если задана категория, получаем идентификатор категории по названию и коду региона
        # с помощью метода get_category_id_by_name() и фильтруем ответ от API по идентификатору категории.
        if category is not None:
            category_id = self.get_category_id_by_name(category, region_code)  # Передаем region_code в метод
            if category_id:
                filtered_response = [item for item in response.get('items', []) if 'snippet' in item
                                     and 'categoryId' in item['snippet']
                                     and item['snippet']['categoryId'] == category_id]
                # Обновляем поле 'items' в ответе на отфильтрованные результаты.
                response['items'] = filtered_response
        # Возвращаем результаты поиска в виде словаря.
        return response

    def get_category_id_by_name(self, category_name: str, region_code: str) -> str:
        """Возвращает идентификатор категории по её названию и коду региона.

        Args:
            category_name (str): Название категории.
            region_code (str): Код региона.

        Returns:
            str: Идентификатор категории или пустая строка, если категория не найдена.
        """
        # Создаем запрос к YouTube API, используя метод videoCategories().list().
        # Передаем параметры запроса, включая regionCode (код региона).
        request = self.service.videoCategories().list(part="snippet", regionCode=region_code)

        # Выполняем запрос и получаем ответ от YouTube API.
        response = request.execute()

        # Получаем список категорий из ответа.
        items = response.get('items', [])

        # Итерируем по списку категорий.
        for item in items:
            # Проверяем, что в элементе 'snippet' есть поле 'title' с заданным названием категории.
            # Если такая категория найдена, возвращаем её идентификатор.
            if 'snippet' in item and 'title' in item['snippet'] and item['snippet']['title'] == category_name:
                return item['id']

        # Если категория не найдена, возвращаем пустую строку.
        return ""

    async def get_video_info(self, video_id: str) -> dict:
        """Асинхронно получает информацию о видео по его идентификатору.

        Args:
            video_id (str): Идентификатор видео.

        Returns:
            dict: Информация о видео в виде словаря или пустой словарь, если видео не найдено.
        """
        # Формируем URL для запроса к YouTube API с использованием идентификатора видео и ключа API.
        url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={self.api_key}&part=snippet"

        try:
            # Создаем асинхронную сессию aiohttp.ClientSession() для отправки HTTP-запроса.
            async with aiohttp.ClientSession() as session:
                # Отправляем GET-запрос по указанному URL и получаем ответ.
                async with session.get(url) as response:
                    # Проверяем статус ответа на наличие ошибок.
                    response.raise_for_status()

                    # Получаем данные ответа в формате JSON.
                    data = await response.json()

                    # Проверяем, что в ответе есть элемент "items" и его длина больше 0.
                    if "items" in data and len(data["items"]) > 0:
                        # Извлекаем информацию о видео из первого элемента "items".
                        item = data["items"][0]
                        snippet = item.get("snippet")

                        # Проверяем наличие необходимых полей в информации о видео.
                        title = snippet.get("title")
                        description = snippet.get("description")
                        publish_time = snippet.get("publishTime")

                        if title and description and publish_time:
                            # Убедимся, что длина подписи не превышает максимально допустимую
                            max_caption_length = 1024
                            title = title[:max_caption_length]
                            description = description[:max_caption_length]
                            publish_time = publish_time[:max_caption_length]

                            # Формируем словарь с информацией о видео и его URL.
                            video_info = {
                                "title": title,
                                "description": description,
                                "publishTime": publish_time,
                                "url": f"https://www.youtube.com/watch?v={video_id}",
                            }
                            return video_info

                        else:
                            # Выводим предупреждение, если не хватает данных о видео.
                            logging.warning(f"Insufficient data for video with identifier {video_id}.")
                    else:
                        # Выводим предупреждение, если видео с заданным идентификатором не найдено.
                        logging.warning(f"Video with identifier {video_id} not found.")

        except aiohttp.ClientError as e:
            # Выводим ошибку, если возникла проблема с HTTP-запросом.
            logging.error(f"Error retrieving video information: {e}")

        except Exception as e:
            # Выводим неизвестную ошибку, если что-то пошло не так.
            logging.error(f"Unknown error while retrieving video information: {e}")

        # Возвращаем пустой словарь, если не удалось получить информацию о видео.
        return {}

    async def get_video_url(self, video_id: str) -> str:
        """Асинхронно получает URL видео по его идентификатору.

        Аргументы:
            video_id (str): Идентификатор видео.

        Возвращает:
            str: URL видео или None, если видео не найдено.
        """
        # Строим URL для запроса к YouTube API, используя идентификатор видео и ключ API.
        url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={self.api_key}"

        try:
            # Создаем асинхронную сессию aiohttp.ClientSession() для отправки HTTP-запроса.
            async with aiohttp.ClientSession() as session:
                # Отправляем GET-запрос по указанному URL и получаем ответ.
                async with session.get(url) as response:
                    # Проверяем статус ответа на наличие ошибок.
                    response.raise_for_status()

                    # Получаем данные ответа в формате JSON.
                    data = await response.json()

                    # Проверяем, есть ли элемент "items" в ответе и его длина больше 0.
                    if "items" in data and len(data["items"]) > 0:
                        # Извлекаем информацию о видео из первого элемента "items".
                        video_info = data["items"][0]

                        # Получаем URL видео из поля "contentDetails".
                        video_url = video_info.get("contentDetails", {}).get("videoUrl")

                        # Возвращаем URL видео.
                        return video_url
        except aiohttp.ClientError as e:
            # Регистрируем ошибку, если возникла проблема с HTTP-запросом.
            logging.error(f"Error retrieving video URL: {e}")
        except Exception as e:
            # Регистрируем неизвестную ошибку, если что-то пошло не так.
            logging.error(f"Unknown error while retrieving video URL: {e}")

        # Возвращаем пустую строку, если URL видео не был получен.
        return ""
