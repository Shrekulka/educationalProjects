# backend/modules/blog/models.py

from datetime import date
from typing import Optional, Any

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from taggit.managers import TaggableManager

from modules.services.utils import unique_slugify, image_compress

# Это удобный способ получить модель пользователя, определенную в проекте Django. Вместо того, чтобы явно импортировать
# модель пользователя (from django.contrib.auth.models import User), get_user_model() возвращает модель пользователя,
# которая настроена в настройках проекта (AUTH_USER_MODEL).
User = get_user_model()


########################################################################################################################

# Вложенная категория, наследуемся от MPTTModel
class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    # Название категории
    title = models.CharField(max_length=255, verbose_name='Название категории')

    # Слаг категории (человеко-понятный URL)
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)

    # Описание категории
    description = models.TextField(verbose_name='Описание категории', max_length=300)

    # Родительская категория (для создания древовидной структуры)
    parent: TreeForeignKey = TreeForeignKey(
        'self',  # Ссылка на себя для создания древовидной структуры
        on_delete=models.CASCADE,  # При удалении родительской категории, удаляются также все дочерние категории
        null=True,  # Разрешает значение NULL в поле
        blank=True,  # Поле не обязательно для заполнения
        db_index=True,  # Индексирует поле для ускорения запросов
        related_name='children',  # Имя обратной связи для доступа к дочерним категориям
        verbose_name='Родительская категория'  # Человекочитаемое имя поля
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        # Порядок сортировки по заголовку
        order_insertion_by = ('title',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self) -> str:
        """
            Возвращает строковое представление категории (название).

            Возвращает:
                str: Название категории.
        """
        return self.title

    def get_absolute_url(self) -> str:
        """
            Возвращает абсолютный URL-адрес для отображения списка статей определенной категории.

            Этот метод используется для генерации URL-адреса, по которому можно перейти
            для просмотра списка статей, относящихся к данной категории. Он принимает
            slug категории (self.slug) в качестве аргумента для формирования URL-адреса.

            Returns:
                str: Абсолютный URL-адрес для отображения списка статей данной категории.

            Example:
                Допустим, имя маршрута для отображения списка статей категории - 'articles_by_category',
                и slug категории - 'news'. Тогда этот метод вернет URL-адрес вида:
                '/category/news/'
        """
        return reverse('articles_by_category', kwargs={'slug': self.slug})


########################################################################################################################
class Article(models.Model):
    """
        Модель для представления статей на сайте.

        Эта модель описывает структуру и поведение статей в блоге или на информационном сайте.
        Она включает в себя различные поля для хранения информации о статье, такие как заголовок,
        содержание, статус публикации, автор и т.д.

        Атрибуты:
            title (models.CharField): Заголовок статьи, ограниченный 255 символами.
            slug (models.SlugField): URL-совместимый идентификатор статьи, уникальный, до 255 символов.
            short_description (CKEditor5Field): Краткое описание статьи, ограниченное 500 символами, с поддержкой
                                                форматирования.
            full_description (CKEditor5Field): Полное содержание статьи, без ограничений по длине, с поддержкой
                                               форматирования.
            thumbnail (models.ImageField): Изображение-превью для статьи, необязательное.
            status (models.CharField): Статус публикации статьи ('published' или 'draft').
            time_create (models.DateTimeField): Дата и время создания статьи.
            time_update (models.DateTimeField): Дата и время последнего обновления статьи.
            author (models.ForeignKey): Ссылка на пользователя-автора статьи.
            updater (models.ForeignKey): Ссылка на пользователя, который последним обновил статью.
            fixed (models.BooleanField): Флаг, указывающий, закреплена ли статья.
            category (TreeForeignKey): Категория статьи, с поддержкой иерархической структуры.
            tags (TaggableManager): Теги, связанные со статьей.

        Методы:
            save(*args, **kwargs): Переопределенный метод сохранения, автоматически генерирует slug
                                   и обрабатывает thumbnail при необходимости.
            get_absolute_url(): Возвращает абсолютный URL статьи.
            get_sum_rating(): Возвращает суммарный рейтинг статьи.
            __str__(): Возвращает строковое представление статьи.
            get_view_count(): Возвращает количество просмотров для данной статьи.
            get_today_view_count() -> int: Возвращает количество просмотров для данной статьи за сегодняшний день.



        Менеджеры:
            objects (ArticleManager): Кастомный менеджер для выполнения запросов к модели.

        Мета:
            db_table (str): Имя таблицы в базе данных.
            ordering (list): Порядок сортировки статей по умолчанию.
            indexes (list): Индексы для оптимизации запросов.
            verbose_name (str): Человекочитаемое имя модели в единственном числе.
            verbose_name_plural (str): Человекочитаемое имя модели во множественном числе.

        Примечание:
            - Модель использует CKEditor5 для полей с расширенным форматированием текста.
            - Реализована возможность автоматического создания уникального slug.
            - Thumbnail автоматически сжимается при сохранении.
            - Используется древовидная структура для категорий (MPTT).
            - Поддерживается система тегов с использованием django-taggit.
            - Реализована система рейтингов для статей.
    """

    class ArticleManager(models.Manager):
        """
        Кастомный менеджер для модели статей.

        Методы:
            all(): Возвращает queryset опубликованных статей с предвыборкой связанных объектов author и category.
            detail(): Возвращает queryset для детальной страницы статьи с предвыборкой связанных объектов author,
                      category, комментариев, тегов и рейтингов.
        """

        def all(self) -> models.QuerySet:
            """
                Возвращает QuerySet всех опубликованных статей.

                Предварительно загружает (select_related) связанные объекты 'author' и 'category',
                чтобы избежать дополнительных запросов к базе данных при последующем обращении к этим связям.

                Возвращает:
                    models.QuerySet: QuerySet всех опубликованных статей с предзагруженными связями 'author',
                    'category', 'ratings' и 'views'
            """
            # Получаем QuerySet всех опубликованных статей
            queryset = (self.get_queryset().select_related('author', 'category').
                        prefetch_related('ratings', 'views').filter(status='published'))
            # Возвращаем QuerySet всех опубликованных статей
            return queryset

        def detail(self) -> models.QuerySet:
            """
                Возвращает queryset всех опубликованных статей с детальной информацией.

                Предварительно загружает (select_related) связанные объекты 'author' и 'category'.
                Предварительно загружает (prefetch_related) связанные объекты 'comments', 'comments__author' и
                'comments__author__profile', а также 'tags' и 'ratings',
                чтобы избежать дополнительных запросов к базе данных при последующем обращении к этим связям.

                Возвращает:
                    models.QuerySet: Queryset всех опубликованных статей с предзагруженными связями 'author', 'category',
                    'comments', 'comments__author', 'comments__author__profile', 'tags' и 'ratings'.
            """
            # Получаем queryset всех опубликованных статей
            # Предварительно загружаем связанные объекты 'author' и 'category'
            # Предварительно загружаем связанные объекты 'comments', 'comments__author' и 'comments__author__profile'
            # Предварительно загружаем связанные объекты 'tags' и 'ratings'
            return self.get_queryset() \
                .select_related('author', 'category') \
                .prefetch_related('comments', 'comments__author', 'comments__author__profile', 'tags', 'ratings') \
                .filter(status='published')

    # Опции для статуса статьи
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )
    # Заголовок, с максимальным количеством символов 255
    title = models.CharField(verbose_name='Заголовок', max_length=255)

    # Ссылка на материал (латиница), или в простонародии ЧПУ-человеко-понятный урл, с максимальным количеством символов
    # 255, blank (необязательно к заполнению)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)

    # Краткое описание статьи с использованием CKEditor5, ограниченное 500 символами
    short_description = CKEditor5Field(max_length=500, verbose_name='Краткое описание', config_name='extends')

    # Полное описание статьи с использованием CKEditor5, без ограничений по длине
    full_description = CKEditor5Field(verbose_name='Полное описание', config_name='extends')

    # Определяем поле модели для хранения изображения превью поста.
    thumbnail = models.ImageField(
        verbose_name='Превью поста',  # Определяем человекочитаемое имя для этого поля.
        blank=True,  # Позволяет оставить поле пустым (необязательное).
        # Задаем путь, куда будут сохраняться загруженные изображения, используя динамическую структуру директорий
        # согласно текущей дате.
        upload_to='images/thumbnails/%Y/%m/%d/',
        # Добавляем валидатор для проверки расширений файлов (допустимые расширения: png, jpg, webp, jpeg, gif).
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )

    # Опубликована статья, или черновик.
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)

    # Время создания.
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

    # Время обновления статьи.
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    # Ключ ссылаемый на пользователя из другой таблицы (пользователей) c on_delete=models.PROTECT (при удалении
    # происходит защита, что не позволяет так просто удалить пользователя с его статьями, чтоб вы могли передать статьи
    # другому человеку)
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts',
                               default=1)

    # Аналогично, только если при обновлении статьи выводить того, кто редактировал (добавлять, если вам это нужно) c
    # on_delete=models.CASCADE (при удалении просто убирается значение того, кто обновил у статей каскадно)
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True,
                                related_name='updater_posts', blank=True)

    # Булево значение, по умолчанию False (не закреплено)
    fixed = models.BooleanField(verbose_name='Зафиксировано', default=False)

    # Подключаем категории в модель статей, используем вместо отношения: ForeignKey импортированное отношение
    # вложенности из модуля MPTT: TreeForeignKey
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')

    # Подключаем кастомный менеджер для модели статей.
    objects = ArticleManager()

    # Менеджер для управления тегами статьи с помощью библиотеки django-taggit.
    # Позволяет добавлять, удалять и фильтровать статьи по тегам.
    tags = TaggableManager()

    class Meta:
        # Название таблицы в БД. (можно не добавлять, будет создано автоматически)
        db_table = 'app_articles'
        # Сортировка, ставим -created_at, чтобы выводились статьи в обратном порядке (сначала новые, потом старые).
        ordering = ['-fixed', '-time_create']
        # Индексирование полей, чтобы ускорить результаты сортировки.
        indexes = [models.Index(fields=['-fixed', '-time_create', 'status'])]
        # Название модели в админке в ед.ч
        verbose_name = 'Статья'
        # Во множественном числе
        verbose_name_plural = 'Статьи'

    def __init__(self, *args, **kwargs) -> None:
        """
            Инициализация объекта статьи.

            Эта функция выполняет следующие действия:
            1. Вызывает конструктор родительского класса для инициализации объекта.
            2. Сохраняет текущее значение поля thumbnail в атрибуте __thumbnail для последующего сравнения.
               Это позволяет определить, было ли изменено изображение статьи при сохранении.

            Args:
                *args: Позиционные аргументы, передаваемые в конструктор родительского класса.
                **kwargs: Именованные аргументы, передаваемые в конструктор родительского класса.

            Returns:
                None
        """
        # Вызов конструктора родительского класса для инициализации объекта
        super().__init__(*args, **kwargs)

        # Сохраняем текущее значение thumbnail в атрибуте __thumbnail, если объект уже существует (имеет pk)
        # или None, если объект новый (не имеет pk)
        self.__thumbnail: Optional[str] = self.thumbnail if self.pk else None

    def __str__(self) -> str:
        """
            Возвращает строковое представление статьи (заголовок).

            Возвращает:
                str: Заголовок статьи.
        """
        return self.title

    # Данный метод позволяет получать прямую ссылку на статью, без вызова {% url '' %}
    # Также мы импортировали reverse для формирования правильной ссылки.
    def get_absolute_url(self) -> str:
        """
            Получение абсолютного URL-адреса статьи.

            Возвращает:
                str: Абсолютный URL-адрес статьи.
        """
        return reverse('articles_detail', kwargs={'slug': self.slug})

    def get_sum_rating(self) -> int:
        """
            Возвращает суммарное значение всех рейтингов (лайков/дизлайков) для статьи.

            Возвращает:
                int: Сумма значений всех рейтингов статьи.
        """
        # Суммируем значения всех рейтингов для статьи
        return sum([rating.value for rating in self.ratings.all()])

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
            Переопределение метода сохранения объекта модели.

            Этот метод выполняет следующие действия:
            1. Генерирует уникальный slug, если он не указан.
            2. Сохраняет объект модели.
            3. Сжимает изображение thumbnail, если оно было изменено.

            Аргументы:
                *args: Позиционные аргументы для передачи в метод save родительского класса.
                **kwargs: Именованные аргументы для передачи в метод save родительского класса.

            Возвращает:
                None
        """
        # Проверяем, есть ли у объекта slug
        if not self.slug:
            # Если slug отсутствует, генерируем его на основе заголовка
            self.slug = unique_slugify(self, self.title)

        # Вызываем метод save родительского класса для сохранения объекта
        super().save(*args, **kwargs)

        # Проверяем, было ли изменено изображение thumbnail и существует ли оно
        if self.__thumbnail != self.thumbnail and self.thumbnail:
            # Если изображение изменилось и существует, сжимаем его
            image_compress(self.thumbnail.path, width=500, height=500)

    def get_view_count(self) -> int:
        """
            Возвращает количество просмотров для данной статьи.

            Returns:
                int: Количество просмотров статьи.
        """
        # Возвращает количество просмотров для данной статьи
        return self.views.count()

    def get_today_view_count(self) -> int:
        """
            Возвращает количество просмотров для данной статьи за сегодняшний день.

            Returns:
                int: Количество просмотров статьи за сегодняшний день.
        """
        # Получаем текущую дату (без времени)
        today = date.today()
        # Фильтруем QuerySet 'views' для текущей статьи по дате просмотра 'viewed_on', равной сегодняшней дате,
        # затем подсчитываем количество объектов в результате.
        return self.views.filter(viewed_on__date=today).count()


########################################################################################################################
class Comment(MPTTModel):
    """
    Модель древовидных комментариев.

    Атрибуты:
        article (ForeignKey): Ссылка на статью, к которой привязан комментарий.
        author (ForeignKey): Ссылка на автора комментария.
        content (TextField): Текст комментария.
        time_create (DateTimeField): Время добавления комментария.
        time_update (DateTimeField): Время обновления комментария.
        status (CharField): Статус комментария (опубликовано или черновик).
        parent (TreeForeignKey): Родительский комментарий (для древовидной структуры).
    """

    # Опции для статуса комментария
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    # Ссылка на статью, к которой привязан комментарий.
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments')
    # Ссылка на автора комментария.
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE,
                               related_name='comments_author')
    # Текст комментария.
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    # Время добавления комментария.
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    # Время обновления комментария.
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    # Статус комментария (опубликовано или черновик).
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)
    # Родительский комментарий (для древовидной структуры).
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True,
                            related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        """
            Метакласс для управления порядком вставки комментариев в древовидной структуре.

            Атрибуты:
                order_insertion_by (tuple): Кортеж для определения порядка вставки комментариев.
                                             Значение '-time_create' указывает на сортировку по времени создания
                                             в убывающем порядке.
        """
        # Определяет порядок вставки новых комментариев по времени создания, чтобы новые комментарии отображались
        # первыми.
        order_insertion_by: tuple = ('-time_create',)

    class Meta:
        """
            Класс Meta для определения метаданных модели Comment.

            Атрибуты:
                db_table (str): Название таблицы в базе данных для хранения комментариев.
                indexes (list): Список индексов для ускорения поиска комментариев.
                                Индекс создается для полей '-time_create', 'time_update', 'status', 'parent'.
                ordering (list): Порядок сортировки комментариев в запросах к базе данных.
                                 Комментарии сортируются по времени создания в убывающем порядке.
                verbose_name (str): Человекочитаемое название модели Comment в единственном числе.
                verbose_name_plural (str): Человекочитаемое название модели Comment во множественном числе.
        """
        db_table: str = 'app_comments'  # Название таблицы в базе данных для хранения комментариев.

        # Создание индексов для ускорения поиска комментариев.
        indexes: list = [models.Index(fields=['-time_create', 'time_update', 'status', 'parent'])]

        ordering: list = ['-time_create']  # Сортировка комментариев по времени добавления.

        verbose_name: str = 'Комментарий'  # Человекочитаемое название модели Comment в единственном числе.

        verbose_name_plural: str = 'Комментарии'  # Человекочитаемое название модели Comment во множественном числе.

    def __str__(self) -> str:
        """
        Возвращает строковое представление комментария (автор: текст).

        Возвращает:
            str: Строковое представление комментария.
        """
        # Возвращает строку, состоящую из имени автора и содержимого комментария, разделенных двоеточием.
        return f'{self.author}:{self.content}'


########################################################################################################################
class Rating(models.Model):
    """
        Модель рейтинга: Лайк - Дизлайк

        Attributes:
            article (ForeignKey): Ссылка на связанную статью.
            user (ForeignKey): Ссылка на пользователя, который оставил рейтинг. Может быть пустым.
            value (IntegerField): Значение рейтинга (1 - лайк, -1 - дизлайк).
            time_create (DateTimeField): Время создания рейтинга.
            ip_address (GenericIPAddressField): IP адрес пользователя, оставившего рейтинг.
    """

    # Ссылка на связанную статью. При удалении статьи все связанные рейтинги также будут удалены.
    article = models.ForeignKey(
        to=Article,
        verbose_name='Статья',
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    # Ссылка на пользователя, который оставил рейтинг. Поле может быть пустым.
    user = models.ForeignKey(
        to=User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    # Значение рейтинга (1 - лайк, -1 - дизлайк).
    value = models.IntegerField(
        verbose_name='Значение',
        choices=[(1, 'Нравится'), (-1, 'Не нравится')]
    )

    # Время создания рейтинга. Значение устанавливается автоматически при создании объекта.
    time_create = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True
    )

    # IP адрес пользователя, оставившего рейтинг.
    ip_address = models.GenericIPAddressField(
        verbose_name='IP Адрес'
    )

    class Meta:
        # Уникальность комбинации статьи и IP адреса, чтобы пользователь не мог оставлять несколько рейтингов с одного IP.
        unique_together = ('article', 'ip_address')

        # Сортировка по времени создания в обратном порядке (от новых к старым).
        ordering = ('-time_create',)

        # Индекс для ускорения поиска по времени создания и значению рейтинга.
        indexes = [
            models.Index(fields=['-time_create', 'value'])
        ]

        # Название модели в единственном числе.
        verbose_name = 'Рейтинг'
        # Название модели во множественном числе.
        verbose_name_plural = 'Рейтинги'

    def __str__(self) -> str:
        # Строковое представление объекта модели.
        return self.article.title


########################################################################################################################
class ViewCount(models.Model):
    """
        Модель для отслеживания просмотров статей.

        Поля:
        - article: Связь с моделью Article, которая представляет статью.
        - ip_address: IP-адрес, с которого был произведен просмотр.
        - viewed_on: Дата и время просмотра.

        Метаданные:
        - ordering: Сортировка по дате просмотра в убывающем порядке.
        - indexes: Индекс для поля viewed_on.
        - verbose_name: Человеко-читаемое имя модели.
        - verbose_name_plural: Человеко-читаемое множественное число для модели.
    """

    # Связь с моделью Article, которая представляет статью
    article: models.ForeignKey = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='views')

    # Поле для хранения IP-адреса, с которого был произведен просмотр
    ip_address: models.GenericIPAddressField = models.GenericIPAddressField(verbose_name='IP адрес')

    # Поле для хранения даты и времени просмотра, автоматически устанавливается при создании
    viewed_on: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        # Указывает на сортировку по дате просмотра в убывающем порядке
        ordering: tuple[str] = ('-viewed_on',)

        # Индекс для поля viewed_on
        indexes: list[models.Index] = [models.Index(fields=['-viewed_on'])]

        # Человеко-читаемое имя модели
        verbose_name: str = 'Просмотр'

        # Человеко-читаемое множественное число для модели
        verbose_name_plural: str = 'Просмотры'

    def __str__(self) -> str:
        """
            Возвращает строковое представление модели.

            Возвращаемое значение:
            - str: Название статьи, к которой относится данный просмотр.
        """
        return self.article.title  # Возвращает название статьи, связанной с просмотром
########################################################################################################################
