# backend/modules/services/utils.py

import os
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin
from uuid import uuid4

from PIL import Image, ImageOps
from django.core.files.storage import FileSystemStorage
from django.db.models import Model
from django.http import HttpRequest
from pytils.translit import slugify

from backend import settings


########################################################################################################################
def unique_slugify(instance: Model, slug: str) -> str:
    """
        Функция для генерации уникальных SLUG для объектов модели.

        Args:
            instance (Model): Экземпляр модели, для которой генерируется SLUG.
            slug (str): Исходный SLUG.

        Returns:
            str: Уникальный SLUG.
    """
    model = instance.__class__  # Получаем класс модели из экземпляра
    unique_slug = slugify(slug)  # Преобразуем исходный SLUG в URL-подобный формат

    # Проверяем, существует ли объект с таким SLUG в базе данных
    while model.objects.filter(slug=unique_slug).exists():
        # Если SLUG уже занят, генерируем новый с использованием уникального идентификатора
        unique_slug = f"{unique_slug}-{uuid4().hex[:8]}"

    return unique_slug  # Возвращаем уникальный SLUG


########################################################################################################################
def get_client_ip(request: HttpRequest) -> Optional[str]:
    """
        Получает IP-адрес клиента из заголовков HTTP-запроса.

        Если запрос был проксирован, функция пытается получить оригинальный IP-адрес клиента из заголовка
        'HTTP_X_FORWARDED_FOR'. В противном случае, она возвращает IP-адрес из заголовка 'REMOTE_ADDR'.

        Аргументы:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            Optional[str]: IP-адрес клиента в виде строки, или None, если IP-адрес не был найден.
    """
    # Получаем IP-адрес из заголовка 'HTTP_X_FORWARDED_FOR', если запрос был проксирован
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    # Если заголовок 'HTTP_X_FORWARDED_FOR' присутствует, берем первый IP-адрес из списка
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        # Иначе, берем IP-адрес из заголовка 'REMOTE_ADDR'
        ip = request.META.get('REMOTE_ADDR')

    return ip


########################################################################################################################
class CkeditorCustomStorage(FileSystemStorage):
    """
        Кастомное хранилище для медиа-файлов CKEditor.

        Этот класс расширяет FileSystemStorage, чтобы изменить расположение и имена файлов,
        сохраняемых через CKEditor. Файлы будут сохраняться в подкаталоги, основанные на дате сохранения.

        Attributes:
            location (str): Полный путь к директории, где будут храниться файлы.
            base_url (str): Базовый URL, по которому можно получить доступ к сохраненным файлам.
    """
    # Путь к директории для хранения файлов
    location: str = os.path.join(settings.MEDIA_ROOT, 'uploads/')

    # Базовый URL для доступа к сохраненным файлам
    base_url: str = urljoin(settings.MEDIA_URL, 'uploads/')

    def get_folder_name(self) -> str:
        """
            Генерирует имя папки для хранения файлов на основе текущей даты.

            Returns:
                str: Имя папки в формате 'YYYY/MM/DD'.
        """
        # Возвращает строку с текущей датой в формате 'YYYY/MM/DD'
        return datetime.now().strftime('%Y/%m/%d')

    def get_valid_name(self, name: str) -> str:
        """
            Возвращает корректное имя файла без изменений.

            Args:
                name (str): Исходное имя файла.

            Returns:
                str: Имя файла без изменений.
        """
        # Возвращает переданное имя файла без изменений
        return name

    def _save(self, name: str, content) -> str:
        """
            Сохраняет файл в кастомное хранилище с использованием уникальной структуры папок.

            Args:
                name (str): Имя файла.
                content: Содержимое файла.

            Returns:
                str: Путь к сохраненному файлу.
        """
        # Получаем имя папки на основе текущей даты
        folder_name = self.get_folder_name()

        # Формируем полный путь к файлу, включая папку и имя файла
        name = os.path.join(folder_name, self.get_valid_name(name))

        # Сохраняем файл, используя родительский метод _save, и возвращаем путь к сохраненному файлу
        return super()._save(name, content)


########################################################################################################################
def image_compress(image_path: str, height: int, width: int) -> None:
    """
        Оптимизирует изображение, сжимая его до указанных размеров и уменьшая качество для уменьшения размера файла.

        Args:
            image_path (str): Путь к изображению.
            height (int): Максимальная высота изображения.
            width (int): Максимальная ширина изображения.
    """
    # Открываем изображение
    img = Image.open(image_path)

    # Преобразуем изображение в RGB, если оно в другом формате
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Если размеры изображения превышают указанные, изменяем его размер
    if img.height > height or img.width > width:
        output_size = (height, width)
        img.thumbnail(output_size)

    # Корректируем ориентацию изображения на основе данных EXIF
    img = ImageOps.exif_transpose(img)

    # Сохраняем изображение с оптимизацией и сжатием качества до 90%
    img.save(image_path, format='JPEG', quality=90, optimize=True)
########################################################################################################################
