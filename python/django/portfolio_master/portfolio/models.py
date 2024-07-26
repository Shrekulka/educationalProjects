from ckeditor.fields import RichTextField
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Skill(models.Model):
    """
    Модель для представления навыков автора.

    Attributes:
        name (str): Название навыка.
        level (str): Уровень владения навыком.
    """
    # Название навыка, ограничено 30 символами
    name = models.CharField(max_length=30)
    # Уровень владения навыком, ограничено 3 символами
    level = models.CharField(max_length=3)

    class Meta:
        # Сортировка по id
        ordering = ['id']
        # Человекочитаемое название модели в единственном числе
        verbose_name = 'Навык'
        # Человекочитаемое название модели во множественном числе
        verbose_name_plural = 'Навыки'

    def __str__(self) -> str:
        # Строковое представление объекта (будет отображаться в админ-панели)
        return self.name


class Category(models.Model):
    """
    Модель для представления категорий работ в портфолио.

    Attributes:
        engname (str): Название категории на английском языке.
        rusname (str): Название категории на русском языке.
    """

    # Название категории на английском, ограничено 25 символами
    engname = models.CharField(max_length=25)
    # Название категории на русском, ограничено 25 символами
    rusname = models.CharField(max_length=25)

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        # Возвращает русское название категории
        return self.rusname


class Work(models.Model):
    """
    Модель для представления отдельных работ в портфолио.

    Attributes:
        title (str): Заголовок работы.
        slug (str): URL-совместимое имя работы.
        category (Category): Связанная категория работы.
        image (ImageField): Изображение работы.
        description (str): Описание работы.
        stack (str): Используемые технологии.
        link (str): Ссылка на работу.
    """

    # Заголовок работы, ограничен 150 символами
    title = models.CharField(max_length=150)
    # URL-совместимое имя, уникальное, ограничено 150 символами
    slug = models.SlugField(max_length=150, unique=True)
    # Связь с моделью Category (многие к одному)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='works')
    # Изображение работы, сохраняется в папку 'works'
    image = models.ImageField(upload_to='works')
    # Описание работы
    description = RichTextField()
    # Используемые технологии
    stack = RichTextField()
    # Ссылка на работу
    link = models.URLField(max_length=200)

    class Meta:
        # Сортировка по id в обратном порядке (новые работы первыми)
        ordering = ['-id']
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self) -> str:
        return self.title


class Service(models.Model):
    """
    Модель для представления услуг, предоставляемых автором.

    Attributes:
        name (str): Название услуги.
        icon (str): Название иконки для услуги.
        description (str): Краткое описание услуги.
    """
    # Название услуги, ограничено 25 символами
    name = models.CharField(max_length=25)
    # Название иконки для услуги, ограничено 50 символами
    icon = models.CharField(max_length=50)
    # Краткое описание услуги, ограничено 200 символами
    description = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']
        verbose_name = 'Сервис'
        verbose_name_plural = 'Виды сервиса'

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    """
    Модель для представления инструментов, связанных с услугами.

    Attributes:
        name (str): Название инструмента.
        service (Service): Связанная услуга.
    """
    # Название инструмента, ограничено 150 символами
    name = models.CharField(max_length=150)
    # Связь с моделью Service (многие к одному)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        # Сортировка по id в обратном порядке
        ordering = ['-id']
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    """
    Модель для представления информации об авторе портфолио.

    Attributes:
        name (str): Имя автора.
        lastname (str): Фамилия автора.
        about (str): Информация об авторе.
        skills (ManyToManyField): Связь с моделью Skill.
        image (ImageField): Фотография автора.
    """
    # Имя автора, ограничено 15 символами
    name = models.CharField(max_length=15)
    # Фамилия автора, ограничена 15 символами
    lastname = models.CharField(max_length=15)
    # Информация об авторе
    about = CKEditor5Field()
    # Связь многие-ко-многим с моделью Skill
    skills = models.ManyToManyField(Skill, related_name='author')
    # Фотография автора, сохраняется в папку 'author'
    image = models.ImageField(upload_to='author')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self) -> str:
        # Возвращает полное имя автора
        return f'{self.name} {self.lastname}'


class Message(models.Model):
    """
    Модель для представления сообщений, отправленных через форму обратной связи.

    Attributes:
        name (str): Имя отправителя.
        email (str): Email отправителя.
        subject (str): Тема сообщения.
        message (str): Текст сообщения.
        created_at (datetime): Дата и время создания сообщения.
    """
    # Имя отправителя, ограничено 100 символами
    name = models.CharField(max_length=100)
    # Email отправителя
    email = models.EmailField()
    # Тема сообщения, ограничена 100 символами
    subject = models.CharField(max_length=100)
    # Текст сообщения
    message = models.TextField()
    # Дата и время создания сообщения, заполняется автоматически
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Сортировка по дате создания в обратном порядке (новые сообщения первыми)
        ordering = ['-created_at']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self) -> str:
        # Возвращает краткую информацию о сообщении
        return f'Сообщение от {self.name}: {self.subject}'


class Testimony(models.Model):
    """
    Модель для представления отзывов заказчиков.

    Attributes:
        name (str): Имя заказчика.
        lastname (str): Фамилия заказчика.
        image (ImageField): Фотография заказчика.
        text (str): Текст отзыва.
    """

    # Имя заказчика, ограничено 15 символами
    name = models.CharField(max_length=15)
    # Фамилия заказчика, ограничена 15 символами
    lastname = models.CharField(max_length=15)
    # Фотография заказчика, сохраняется в папку 'clients'
    image = models.ImageField(upload_to='clients')
    # Текст отзыва
    text = models.TextField()

    class Meta:
        # Сортировка по id в обратном порядке
        ordering = ['-id']
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self) -> str:
        # Возвращает полное имя заказчика
        return f'{self.name} {self.lastname}'
