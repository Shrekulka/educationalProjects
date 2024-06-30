# backend/modules/services/email.py

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_contact_email_message(subject: str, email: str, content: str, ip: str, user_id: int) -> None:
    """
        Отправляет письмо с контактной формы сайта.

        Эта функция отправляет электронное письмо с данными, полученными из контактной формы сайта.
        Если указан идентификатор пользователя, то информация о пользователе включается в письмо.

        Аргументы:
            subject (str): Тема письма.
            email (str): Адрес электронной почты отправителя.
            content (str): Содержание письма.
            ip (str): IP-адрес отправителя.
            user_id (int): Идентификатор пользователя (если пользователь авторизован).

        Возвращает:
            None
    """
    # Получаем объект пользователя по ID, если указан user_id. Если пользователь не авторизован, user будет None.
    user = User.objects.get(id=user_id) if user_id else None

    # Генерируем сообщение письма из шаблона 'system/email/feedback_email_send.html'.
    # В шаблон передаем следующие данные: email, content, ip, user.
    message = render_to_string('system/email/feedback_email_send.html', {
        'email': email,
        'content': content,
        'ip': ip,
        'user': user,
    })

    # Создаем объект EmailMessage с указанной темой, сообщением, адресом электронной почты сервера и адресом
    # администратора.
    email_message = EmailMessage(
        subject=subject,  # Тема письма
        body=message,  # Содержание письма
        from_email=settings.EMAIL_SERVER,  # Адрес электронной почты сервера
        to=[settings.EMAIL_ADMIN],  # Адрес электронной почты администратора
    )

    # Отправляем письмо. Если отправка не удалась, будет выброшено исключение.
    email_message.send(fail_silently=False)


########################################################################################################################
def send_activate_email_message(user_id: int) -> None:
    """
        Функция отправки письма с подтверждением для аккаунта пользователя.

        Аргументы:
            user_id (int): Идентификатор пользователя.

        Возвращает:
            None
    """
    # Получаем объект пользователя по его идентификатору.
    user = get_object_or_404(User, id=user_id)

    # Получаем текущий домен сайта.
    current_site = Site.objects.get_current().domain

    # Генерируем токен для подтверждения аккаунта пользователя.
    token = default_token_generator.make_token(user)

    # Кодируем идентификатор пользователя для использования в URL.
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Генерируем URL для активации аккаунта с помощью reverse_lazy.
    activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})

    # Формируем тему письма.
    subject = f'Активируйте свой аккаунт, {user.username}!'

    # Генерируем сообщение письма из шаблона 'system/email/activate_email_send.html'.
    # В шаблон передаем следующие данные: user, activation_url.
    message = render_to_string('system/email/activate_email_send.html', {
        'user': user,
        'activation_url': f'http://{current_site}{activation_url}',
    })

    # Отправляем письмо пользователю, используя метод email_user объекта пользователя.
    # Метод email_user возвращает None, так как отправляет письмо напрямую.
    user.email_user(subject, message)
########################################################################################################################