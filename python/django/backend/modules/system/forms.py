# backend/modules/system/forms.py
from typing import Any

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User

from backend.settings import CAPTCHA_CHALLENGE_FUNCT
from .models import Profile, Feedback


########################################################################################################################


########################################################################################################################
class UserRegisterForm(UserCreationForm):
    """
        Форма регистрации нового пользователя.

        Добавляет к стандартным полям для создания пользователя (username и password1, password2)
        поля для ввода email, имени и фамилии.
        Также реализует проверку уникальности email и настройку стилей форм.
        Включает поле reCAPTCHA для защиты от ботов.

        Наследуется от UserCreationForm.
    """

    captcha = CaptchaField(
        generator=CAPTCHA_CHALLENGE_FUNCT,
    )

    # Определяем метакласс для настройки полей формы
    class Meta(UserCreationForm.Meta):
        """
            Метакласс для определения полей формы.
        """
        # Добавляем к стандартным полям (username, password1, password2) поля email, first_name и last_name
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean_email(self) -> str:
        """
            Проверяет уникальность введенного email.

            Raises:
                forms.ValidationError: Если указанный email уже используется другим пользователем.

            Returns:
                str: Введенный email.
        """
        # Получаем email из cleaned_data формы
        email = self.cleaned_data.get('email')
        # Получаем username из cleaned_data формы
        username = self.cleaned_data.get('username')
        # Проверяем, что email не пустой и уже не используется другим пользователем
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            # Если email уже используется другим пользователем, вызываем исключение ValidationError
            raise forms.ValidationError('Такой email уже используется в системе')
        # В противном случае возвращаем введенный email
        return email

    def __init__(self, *args, **kwargs):
        """
            Конструктор класса, вызывается при создании экземпляра формы.

            Аргументы:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Обновляет стили формы регистрации, устанавливая атрибуты placeholder и class для полей формы.
        """
        # Вызываем конструктор родительского класса с передачей позиционных и именованных аргументов
        super().__init__(*args, **kwargs)
        # Проходимся по всем полям формы
        for field in self.fields:
            # Обновляем атрибуты виджета поля username
            self.fields['username'].widget.attrs.update({"placeholder": 'Придумайте свой логин'})
            # Обновляем атрибуты виджета поля email
            self.fields['email'].widget.attrs.update({"placeholder": 'Введите свой email'})
            # Обновляем атрибуты виджета поля first_name
            self.fields['first_name'].widget.attrs.update({"placeholder": 'Ваше имя'})
            # Обновляем атрибуты виджета поля last_name
            self.fields["last_name"].widget.attrs.update({"placeholder": 'Ваша фамилия'})
            # Обновляем атрибуты виджета поля password1
            self.fields['password1'].widget.attrs.update({"placeholder": 'Придумайте свой пароль'})
            # Обновляем атрибуты виджета поля password2
            self.fields['password2'].widget.attrs.update({"placeholder": 'Повторите придуманный пароль'})
            # Устанавливаем атрибуты class и autocomplete для каждого поля формы
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


########################################################################################################################
class UserLoginForm(AuthenticationForm):
    """
        Форма авторизации пользователя на сайте.
        Включает поле reCAPTCHA для защиты от ботов.

        Наследуется от AuthenticationForm.
    """
    # Добавляем поле CaptchaField для проверки капчи
    captcha = CaptchaField(
        generator=CAPTCHA_CHALLENGE_FUNCT,
    )

    def __init__(self, *args, **kwargs):
        """
            Конструктор класса, вызывается при создании экземпляра формы.

            Аргументы:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Обновляет стили формы авторизации, устанавливая атрибуты placeholder, label и class для полей формы.
        """
        # Вызываем конструктор родительского класса с передачей позиционных и именованных аргументов
        super().__init__(*args, **kwargs)
        # Проходимся по всем полям формы
        for field in self.fields:
            # Обновляем атрибут placeholder для поля username
            self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
            # Обновляем атрибут placeholder для поля password
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
            # Обновляем label для поля username
            self.fields['username'].label = 'Логин'
            # Устанавливаем атрибуты class и autocomplete для каждого поля формы
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


########################################################################################################################
class UserUpdateForm(forms.ModelForm):
    """
        Форма обновления данных пользователя.

        Атрибуты:
            username (str): Имя пользователя.
            email (str): Email пользователя.
            first_name (str): Имя пользователя.
            last_name (str): Фамилия пользователя.
    """

    class Meta:
        # Определение модели и полей, которые будут использоваться в форме
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        """
            Конструктор класса, вызывается при создании экземпляра формы.

            Аргументы:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Проходится по всем полям формы и обновляет их атрибуты для установки стилей под bootstrap.
        """
        # Вызываем конструктор родительского класса с передачей позиционных и именованных аргументов
        super().__init__(*args, **kwargs)
        # Проходимся по всем полям формы
        for field in self.fields:
            # Обновляем атрибуты виджета поля
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  # Устанавливаем класс для стилизации формы под bootstrap
                'autocomplete': 'off'  # Отключаем автозаполнение
            })

    def clean_email(self) -> str:
        """
            Проверяет уникальность email пользователя.

            Returns:
                str: Email пользователя.

            Raises:
                forms.ValidationError: Если email уже занят другим пользователем.
        """
        # Получаем введенный email из данных формы
        email = self.cleaned_data.get('email')
        # Получаем имя пользователя из данных формы
        username = self.cleaned_data.get('username')
        # Проверяем, что email не пустой и уже не используется другим пользователем
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            # Если email уже используется другим пользователем, вызываем исключение ValidationError
            raise forms.ValidationError('Email адрес должен быть уникальным')
        # Возвращаем введенный email
        return email


########################################################################################################################
class UserPasswordChangeForm(SetPasswordForm):
    """
        Форма для изменения пароля пользователя.

        Наследуется от SetPasswordForm.

        Методы:
            __init__(self, *args, **kwargs): Конструктор класса, обновляющий стили формы.
    """

    def __init__(self, *args, **kwargs):
        """
            Конструктор класса, обновляющий стили формы.

            Аргументы:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Проходится по всем полям формы и обновляет их атрибуты для установки стилей под bootstrap.
        """
        # Вызываем конструктор родительского класса с передачей позиционных и именованных аргументов
        super().__init__(*args, **kwargs)
        # Проходимся по всем полям формы
        for field in self.fields:
            # Обновляем атрибуты виджета поля
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  # Устанавливаем класс для стилизации формы под bootstrap
                'autocomplete': 'off'  # Отключаем автозаполнение
            })


########################################################################################################################
class UserForgotPasswordForm(PasswordResetForm):
    """
        Форма запроса на восстановление пароля.
        Включает поле reCAPTCHA для защиты от ботов.

        Наследует стандартную форму PasswordResetForm и добавляет обновление стилей для полей формы.
    """
    # Добавляем поле CaptchaField для проверки капчи
    captcha = CaptchaField(
        generator=CAPTCHA_CHALLENGE_FUNCT,
    )

    def __init__(self, *args, **kwargs):
        """
            Конструктор класса, вызывается при создании экземпляра формы.

            Аргументы:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Обновляет стили формы восстановления пароля, устанавливая атрибуты class и autocomplete для полей формы.
        """
        # Вызываем конструктор родительского класса с передачей позиционных и именованных аргументов
        super().__init__(*args, **kwargs)
        # Проходимся по всем полям формы
        for field in self.fields:
            # Обновляем атрибуты виджета поля
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  # Устанавливаем класс для стилизации формы под bootstrap
                'autocomplete': 'off'  # Отключаем автозаполнение
            })


########################################################################################################################
class UserSetNewPasswordForm(SetPasswordForm):
    """
        Форма изменения пароля пользователя после подтверждения.

        Наследует стандартную форму SetPasswordForm и добавляет обновление стилей для полей формы.
    """

    def __init__(self, *args, **kwargs):
        """
            Конструктор класса, вызывается при создании экземпляра формы.

            Аргументы:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Обновляет стили формы установки нового пароля, устанавливая атрибуты class и autocomplete для полей формы.
        """
        # Вызываем конструктор родительского класса с передачей позиционных и именованных аргументов
        super().__init__(*args, **kwargs)
        # Проходимся по всем полям формы
        for field in self.fields:
            # Обновляем атрибуты виджета поля
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  # Устанавливаем класс для стилизации формы под bootstrap
                'autocomplete': 'off'  # Отключаем автозаполнение
            })


########################################################################################################################
class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя.

    Атрибуты:
        slug (str): Уникальный URL профиля.
        birth_date (date): Дата рождения пользователя.
        bio (str): Биография пользователя.
        avatar (File): Аватар пользователя.
    """

    class Meta:
        # Определяем модель, с которой связана форма, и список полей, которые будут отображаться в форме
        model = Profile
        fields = ('slug', 'birth_date', 'bio', 'avatar')

    def __init__(self, *args, **kwargs):
        """
            Конструктор класса, вызывается при создании экземпляра формы.

            Аргументы:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Проходится по всем полям формы и обновляет их атрибуты для установки стилей и отключения автозаполнения.
        """
        # Вызываем конструктор родительского класса с передачей позиционных и именованных аргументов
        super().__init__(*args, **kwargs)
        # Проходимся по всем полям формы
        for field in self.fields:
            # Обновляем атрибуты виджета поля
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  # Устанавливаем класс для стилизации формы под bootstrap
                'autocomplete': 'off'  # Отключаем автозаполнение
            })


########################################################################################################################
class FeedbackCreateForm(forms.ModelForm):
    """
    Форма для создания обратной связи.

    Эта форма наследуется от `forms.ModelForm` и связана с моделью `Feedback`.
    Она позволяет создавать и редактировать экземпляры модели `Feedback`.

    Атрибуты:
        Meta (класс): Метакласс, содержащий параметры формы.

    Методы:
        __init__(self, *args, **kwargs): Инициализирует экземпляр формы и обновляет стили полей.
    """

    class Meta:
        """
        Метакласс, содержащий параметры формы.

        Атрибуты:
            model (Model): Модель Django, связанная с формой.
            fields (tuple): Кортеж полей, которые должны быть включены в форму.
        """
        model = Feedback  # Модель Django, связанная с формой
        fields = ('subject', 'email', 'content')  # Кортеж полей, которые должны быть включены в форму

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Инициализирует экземпляр формы и обновляет стили полей.

        Этот метод вызывается при создании экземпляра формы.
        Он вызывает конструктор родительского класса, а затем обновляет стили виджетов полей,
        устанавливая CSS-класс 'form-control' и отключая автозаполнение.
        """
        super().__init__(*args, **kwargs)  # Вызов конструктора родительского класса

        # Обновление стилей полей формы
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  # Устанавливает CSS-класс 'form-control'
                'autocomplete': 'off'  # Отключает автозаполнение
            })
########################################################################################################################
