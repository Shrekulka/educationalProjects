# backend/modules/services/email.py

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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
