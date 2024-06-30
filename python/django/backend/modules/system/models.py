# backend/modules/system/models.py
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from modules.services.utils import unique_slugify

# Получаем модель пользователя
User = get_user_model()


########################################################################################################################
class Profile(models.Model):
    """
        Модель профиля пользователя.

        Эта модель расширяет встроенную модель пользователя, предоставляя дополнительные поля,
        такие как URL (slug), аватар, биография и дата рождения.

        Атрибуты:
            user (OneToOneField): Ссылка на модель пользователя.
            slug (SlugField): Уникальный URL для профиля.
            avatar (ImageField): Аватар пользователя с валидацией расширений файлов.
            bio (TextField): Биография пользователя, ограниченная 500 символами.
            birth_date (DateField): Дата рождения пользователя.
            following (ManyToManyField): Пользователи, на которых подписан данный пользователь.


        Методы:
            save(self, *args, **kwargs) -> None:
                Переопределенный метод save, который генерирует и устанавливает уникальный slug для профиля перед
                сохранением.

            __str__(self) -> str:
                Возвращает строковое представление профиля (имя пользователя).

            get_absolute_url(self) -> str:
                Возвращает абсолютный URL профиля.

            create_user_profile(sender: type[User], instance: User, created: bool, **kwargs) -> None:
                Сигнальный обработчик, создающий профиль пользователя при создании нового пользователя.

            save_user_profile(sender: type[User], instance: User, **kwargs) -> None:
                Сигнальный обработчик, сохраняющий профиль пользователя при сохранении пользователя.

            is_online(self) -> bool:
                Проверяет, находится ли пользователь в онлайне.

            class Meta:
                Метаданные модели.

                Атрибуты:
                    db_table (str): Название таблицы в базе данных.
                    ordering (tuple): Порядок сортировки записей.
                    verbose_name (str): Человекочитаемое имя модели в единственном числе.
                    verbose_name_plural (str): Человекочитаемое имя модели во множественном числе.
    """

    # Ссылка на пользователя, при удалении пользователя профиль также будет удален.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Уникальный URL (slug) для профиля, с максимальной длиной 255 символов.
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)

    # Поле для загрузки аватара пользователя.
    avatar = models.ImageField(
        verbose_name='Аватар',  # Человекочитаемое имя для поля.
        upload_to='images/avatars/%Y/%m/%d/',  # Путь для сохранения загруженных аватаров.
        default='images/avatars/default.jpg',  # Значение по умолчанию.
        blank=True,  # Поле необязательно к заполнению.
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))]  # Валидация расширений файлов.
    )

    # Биография пользователя, ограниченная 500 символами, необязательное поле.
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')

    # Дата рождения пользователя, необязательное поле.
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    # Связь многие-ко-многим для отслеживания подписок пользователя
    following = models.ManyToManyField('self',
                                       verbose_name='Подписки',
                                       related_name='followers',
                                       symmetrical=False,  # Подписка в одну сторону (не означает взаимную подписку)
                                       blank=True)  # Поле может быть пустым

    class Meta:
        """
            Метаданные модели.

            Атрибуты:
                db_table (str): Название таблицы в базе данных.
                ordering (tuple): Порядок сортировки записей.
                verbose_name (str): Человекочитаемое имя модели в единственном числе.
                verbose_name_plural (str): Человекочитаемое имя модели во множественном числе.
        """
        db_table = 'app_profiles'  # Название таблицы в базе данных.
        ordering = ('user',)  # Порядок сортировки записей по полю 'user'.
        verbose_name = 'Профиль'  # Человекочитаемое имя модели в единственном числе.
        verbose_name_plural = 'Профили'  # Человекочитаемое имя модели во множественном числе.

    def save(self, *args, **kwargs) -> None:
        """
            Переопределенный метод save.

            Генерирует и устанавливает уникальный slug для профиля перед сохранением, если он не задан.
        """
        # Если поле slug не заполнено, генерируем его из имени пользователя.
        if not self.slug:
            self.slug = unique_slugify(self, str(self.user))
        # Вызываем метод родительского класса для сохранения объекта.
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
            Возвращает строковое представление профиля.

            Returns:
                str: Имя пользователя (получаемое через связанный экземпляр модели User).
        """
        return str(self.user)

    def get_absolute_url(self) -> str:
        """
            Возвращает абсолютный URL профиля.

            Returns:
                str: URL профиля.
        """
        return reverse('profile_detail', kwargs={'slug': self.slug})

    @receiver(post_save, sender=User)
    def create_user_profile(sender: type[User], instance: User, created: bool, **kwargs) -> None:
        """
            Сигнальный обработчик, создающий профиль пользователя при создании нового пользователя.

            Аргументы:
                sender (type[User]): Модель, пославшая сигнал.
                instance (User): Экземпляр модели, который был сохранен.
                created (bool): Флаг, указывающий на создание нового экземпляра.
        """
        # Если создан новый пользователь, создаем связанный профиль.
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender: type[User], instance: User, **kwargs) -> None:
        """
            Сигнальный обработчик, сохраняющий профиль пользователя при сохранении пользователя.

            Аргументы:
                sender (type[User]): Модель, пославшая сигнал.
                instance (User): Экземпляр модели, который был сохранен.
        """
        # Проверяем, существует ли профиль у пользователя
        if hasattr(instance, 'profile'):
            # Сохраняем связанный профиль при сохранении пользователя.
            instance.profile.save()
        else:
            # Если профиль не существует, создаем его перед сохранением.
            Profile.objects.create(user=instance)

    def is_online(self) -> bool:
        """
            Проверяет, находится ли пользователь в онлайне.

            Returns:
                bool: Возвращает True, если пользователь активен (время последнего действия меньше 300 секунд назад),
                      иначе False.
        """
        # Получаем время последнего визита из кэша по ключу 'last-seen-id-пользователя'
        last_seen: Optional[timezone.datetime] = cache.get(f'last-seen-{self.user.id}')

        # Проверяем, что время последнего визита определено и прошло менее 300 секунд с момента его последнего действия
        if last_seen is not None and timezone.now() < last_seen + timezone.timedelta(seconds=300):
            return True  # Пользователь активен
        return False  # Пользователь не активен

    @property
    def get_avatar(self) -> str:
        """
            Возвращает URL аватара пользователя.

            Если пользователь загрузил аватар, возвращается URL загруженного изображения.
            Если аватар не загружен, возвращается URL для аватара, сгенерированного с помощью сервиса UI Avatars.

            Returns:
                str: URL аватара пользователя.

            В шаблоне профиля вызывать аватарку через {{ profile.get_avatar }}, вместо {{ profile.avatar.url }}.
        """
        # Если аватар загружен, возвращаем URL загруженного изображения.
        if self.avatar:
            return self.avatar.url
        # Если аватар не загружен, возвращаем URL для сгенерированного аватара.
        return f"https://ui-avatars.com/api/?size=150&background=random&name={self.slug}"


########################################################################################################################
class Feedback(models.Model):
    """
        Модель обратной связи.

        Эта модель представляет запись обратной связи, отправленной пользователем. Она содержит информацию
        о теме, электронном адресе отправителя, содержимом письма, дате отправки, IP-адресе отправителя
        и связанном пользователе (если он был авторизован на сайте).

        Атрибуты:
            subject (CharField): Тема письма обратной связи, максимальная длина 255 символов.
            email (EmailField): Электронный адрес отправителя, максимальная длина 255 символов.
            content (TextField): Содержимое письма обратной связи.
            time_create (DateTimeField): Дата и время создания записи, устанавливается автоматически при создании.
            ip_address (GenericIPAddressField): IP-адрес отправителя, может быть пустым.
            user (ForeignKey): Связь с моделью пользователя, может быть пустой.

        Методы:
            __str__(): Возвращает строковое представление объекта для отображения в админке Django.

        Метаданные:
            verbose_name: Человекочитаемое название модели в единственном числе.
            verbose_name_plural: Человекочитаемое название модели во множественном числе.
            ordering: Порядок сортировки записей по убыванию даты создания.
            db_table: Название таблицы в базе данных.
    """
    # Тема письма, максимальная длина 255 символов
    subject = models.CharField(max_length=255, verbose_name='Тема письма')

    # Электронный адрес (email), максимальная длина 255 символов
    email = models.EmailField(max_length=255, verbose_name='Электронный адрес (email)')

    # Содержимое письма в текстовом формате
    content = models.TextField(verbose_name='Содержимое письма')

    # Дата и время создания записи, устанавливается автоматически при создании
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    # IP-адрес отправителя, может быть пустым
    ip_address = models.GenericIPAddressField(verbose_name='IP отправителя', blank=True, null=True)

    # Связь с моделью пользователя, может быть пустой
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        # Человекочитаемое название модели в единственном числе
        verbose_name = 'Обратная связь'

        # Человекочитаемое название модели во множественном числе
        verbose_name_plural = 'Обратная связь'

        # Порядок сортировки записей по убыванию даты создания
        ordering = ['-time_create']

        # Название таблицы в базе данных
        db_table = 'app_feedback'

    def __str__(self) -> str:
        # Строковое представление объекта, используется для отображения в админке Django
        return f'Вам письмо от {self.email}'
########################################################################################################################
