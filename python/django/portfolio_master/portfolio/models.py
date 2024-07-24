from django.core.exceptions import ValidationError
from django.db import models


# Базовая модель для отслеживания времени создания и обновления объектов
class TimestampedModel(models.Model):
    # Поле для автоматического добавления времени создания
    created_at = models.DateTimeField(auto_now_add=True)
    # Поле для автоматического обновления времени последнего изменения
    updated_at = models.DateTimeField(auto_now=True)

    # Указываем, что это абстрактная модель и не будет создана в базе данных
    class Meta:
        abstract = True


# Модель для описания навыков (например, программирование, дизайн)
class Skill(models.Model):
    # Поле для названия навыка (например, Python, JavaScript)
    name = models.CharField(max_length=30)
    # Поле для уровня владения навыком с выбором значений
    LEVEL_CHOICES = [
        ('BEG', 'Beginner'),
        ('INT', 'Intermediate'),
        ('ADV', 'Advanced'),
        ('EXP', 'Expert'),
    ]
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)

    # Метод для валидации уровня навыка
    def clean(self):
        if self.level not in dict(self.LEVEL_CHOICES):
            raise ValidationError(f'Invalid level: {self.level}')

    class Meta:
        # Сортировка по id по умолчанию
        ordering = ['id']
        # Человекочитаемое имя модели в единственном числе
        verbose_name = 'Навык'
        # Человекочитаемое имя модели во множественном числе
        verbose_name_plural = 'Навыки'

    # Метод для строкового представления объекта
    def __str__(self):
        return self.name


# Модель для описания категорий работ (например, веб-разработка, графический дизайн)
class Category(models.Model):
    # Поле для английского названия категории с уникальным значением
    engname = models.CharField(max_length=25, unique=True)
    # Поле для русского названия категории с уникальным значением
    rusname = models.CharField(max_length=25, unique=True)

    class Meta:
        # Сортировка по id по умолчанию
        ordering = ['id']
        # Человекочитаемое имя модели в единственном числе
        verbose_name = 'Категория'
        # Человекочитаемое имя модели во множественном числе
        verbose_name_plural = 'Категории'

    # Метод для строкового представления объекта
    def __str__(self):
        return self.rusname


# Модель для описания выполненных работ (например, проекты, задачи)
class Work(models.Model):
    # Поле для названия работы
    title = models.CharField(max_length=150)
    # Поле для уникального slug (например, для URL)
    slug = models.SlugField(max_length=150, unique=True)
    # Поле для связи с категорией (ForeignKey)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='works')
    # Поле для изображения работы
    image = models.ImageField(upload_to='works')
    # Поле для описания работы
    description = models.TextField()
    # Поле для указания технологий, использованных в работе
    stack = models.TextField()
    # Поле для ссылки на работу
    link = models.URLField(max_length=200)

    class Meta:
        # Сортировка по id в обратном порядке по умолчанию
        ordering = ['-id']
        # Человекочитаемое имя модели в единственном числе
        verbose_name = 'Работа'
        # Человекочитаемое имя модели во множественном числе
        verbose_name_plural = 'Работы'

    # Метод для строкового представления объекта
    def __str__(self):
        return self.title


# Модель для описания сервисов (например, консультации, обучение)
class Service(models.Model):
    # Поле для названия сервиса
    name = models.CharField(max_length=25)
    # Поле для иконки сервиса
    icon = models.CharField(max_length=50)
    # Поле для описания сервиса
    description = models.CharField(max_length=200)

    class Meta:
        # Сортировка по id по умолчанию
        ordering = ['id']
        # Человекочитаемое имя модели в единственном числе
        verbose_name = 'Сервис'
        # Человекочитаемое имя модели во множественном числе
        verbose_name_plural = 'Виды сервиса'

    # Метод для строкового представления объекта
    def __str__(self):
        return self.name


# Модель для описания инструментов, использующихся в сервисах (например, инструменты разработки, ПО)
class Item(models.Model):
    # Поле для названия инструмента
    name = models.CharField(max_length=150)
    # Поле для связи с сервисом (ForeignKey)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        # Сортировка по id в обратном порядке по умолчанию
        ordering = ['-id']
        # Человекочитаемое имя модели в единственном числе
        verbose_name = 'Инструмент'
        # Человекочитаемое имя модели во множественном числе
        verbose_name_plural = 'Инструменты'

    # Метод для строкового представления объекта
    def __str__(self):
        return self.name


# Модель для описания авторов (например, сотрудники, исполнители)
class Author(models.Model):
    # Поле для имени автора
    name = models.CharField(max_length=15)
    # Поле для фамилии автора
    lastname = models.CharField(max_length=15)
    # Поле для описания автора
    about = models.TextField()
    # Поле для связи с навыками (ManyToManyField)
    skills = models.ManyToManyField(Skill, related_name='author')
    # Поле для изображения автора
    image = models.ImageField(upload_to='author')

    class Meta:
        # Сортировка по id в обратном порядке по умолчанию
        ordering = ['-id']
        # Человекочитаемое имя модели в единственном числе
        verbose_name = 'Автор'
        # Человекочитаемое имя модели во множественном числе
        verbose_name_plural = 'Авторы'

    # Метод для строкового представления объекта
    def __str__(self):
        return f'{self.name} {self.lastname}'


# Модель для описания сообщений, наследуется от TimestampedModel
class Message(TimestampedModel):
    # Поле для имени отправителя сообщения
    name = models.CharField(max_length=100)
    # Поле для email отправителя
    email = models.EmailField()
    # Поле для темы сообщения
    subject = models.CharField(max_length=100)
    # Поле для текста сообщения
    message = models.TextField()

    class Meta:
        # Сортировка по дате создания в обратном порядке по умолчанию
        ordering = ['-created_at']
        # Человекочитаемое имя модели в единственном числе
        verbose_name = 'Сообщение'
        # Человекочитаемое имя модели во множественном числе
        verbose_name_plural = 'Сообщения'

    # Метод для строкового представления объекта
    def __str__(self):
        return f'Сообщение от {self.name}: {self.subject}'


# Модель для описания отзывов заказчиков (например, отзывы клиентов)
class Testimony(models.Model):
    # Поле для имени заказчика
    name = models.CharField(max_length=15)
    # Поле для фамилии заказчика
    lastname = models.CharField(max_length=15)
    # Поле для изображения заказчика
    image = models.ImageField(upload_to='clients')
    # Поле для текста отзыва
    text = models.TextField()

    class Meta:
        # Сортировка по id в обратном порядке по умолчанию
        ordering = ['-id']
        # Человекочитаемое имя модели в единственном числе
        verbose_name = 'Заказчик'
        # Человекочитаемое имя модели во множественном числе
        verbose_name_plural = 'Заказчики'

    # Метод для строкового представления объекта
    def __str__(self):
        return f'{self.name} {self.lastname}'
