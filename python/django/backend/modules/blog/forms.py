# backend/modules/blog/forms.py

from django import forms

from .models import Article, Comment


class ArticleCreateForm(forms.ModelForm):
    """
        Форма добавления статей на сайте.

        Атрибуты:
            model (Article): Модель статьи.
            fields (tuple): Поля модели, которые будут включены в форму.
    """
    class Meta:
        # Указываем, что данная форма будет работать с моделью Article
        model = Article
        # Определяем поля модели, которые будут включены в форму
        fields = ('title', 'slug', 'category', 'short_description', 'full_description', 'thumbnail', 'status')

    def __init__(self, *args, **kwargs):
        """
            Обновление стилей формы под Bootstrap.

            Args:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.
        """
        # Вызываем метод инициализации родительского класса
        super().__init__(*args, **kwargs)
        # Обновляем стили каждого поля формы
        for field in self.fields:
            # Добавляем класс 'form-control' для стилей Bootstrap
            # Отключаем автозаполнение для всех полей формы
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class ArticleUpdateForm(ArticleCreateForm):
    """
    Форма обновления статьи на сайте.

    Атрибуты:
        model (Article): Модель статьи.
        fields (tuple): Поля формы для обновления статьи.
    """

    class Meta:
        model = Article  # Указываем модель, с которой будет работать форма

        # Добавляем поля 'updater' и 'fixed' к полям формы создания статьи (title, slug, category, short_description,
        # full_description, thumbnail, status)
        fields = ArticleCreateForm.Meta.fields + ('updater', 'fixed')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap.

        Args:
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.
        """
        super().__init__(*args, **kwargs)  # Вызываем метод __init__ родительского класса для инициализации формы

        # Обновляем атрибуты виджета поля 'fixed' для применения стилей Bootstrap
        self.fields['fixed'].widget.attrs.update({
            'class': 'form-check-input'  # Применяем класс Bootstrap для чекбоксов
        })


class CommentCreateForm(forms.ModelForm):
    """
    Форма для добавления новых комментариев к статьям.

    Attributes:
        parent (int): Идентификатор родительского комментария. Поле скрыто от пользователя, так как
                      оно заполняется автоматически, если комментарий является ответом на другой комментарий.
        content (str): Содержание комментария. Пользователь вводит текст комментария в это поле.
    """

    # Идентификатор родительского комментария.
    # Поле скрыто от пользователя, так как оно заполняется автоматически, если комментарий является ответом
    # на другой комментарий.
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)

    # Содержание комментария. Пользователь вводит текст комментария в это поле.
    content = forms.CharField(
        label='',  # Убираем метку, чтобы поле было без заголовка
        widget=forms.Textarea(  # Используем виджет Textarea для многострочного ввода текста
            attrs={  # Задаем атрибуты виджета для управления его внешним видом
                'cols': 30,  # Ширина поля в символах
                'rows': 5,  # Высота поля в строках
                'placeholder': 'Напишите комментарий здесь...',  # Текст-подсказка внутри поля
                'class': 'form-control'  # CSS-класс для стилизации поля (Bootstrap)
            }
        )
    )

    class Meta:
        """
            Мета-класс для определения особых параметров формы.

            Attributes:
                model (Comment): Модель, с которой связана данная форма (Comment).
                fields (tuple): Поля модели, которые должны быть представлены в форме.
                                В данном случае, форма будет содержать только поле 'content'.
        """
        model = Comment  # Указываем модель, с которой работает форма
        fields = ('content',)  # Указываем, какие поля модели будут представлены в форме
