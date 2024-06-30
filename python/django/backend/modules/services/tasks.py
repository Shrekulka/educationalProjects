# backend/modules/services/tasks.py

from typing import Optional

from celery import shared_task
from django.core.management import call_command

from .email import send_activate_email_message, send_contact_email_message


@shared_task
def send_activate_email_message_task(user_id: int) -> Optional[str]:
    """
        Отправляет письмо активации для пользователя.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            Optional[str]: Результат отправки сообщения (обычно строка с статусом отправки).
                           Может вернуть None, если произошла ошибка.

        Notes:
            - Эта задача обычно используется в представлении UserRegisterView.
            - Использует функцию send_activate_email_message для отправки письма активации.
    """
    # Вызываем функцию для отправки письма активации и возвращаем результат
    return send_activate_email_message(user_id)


########################################################################################################################

@shared_task
def send_contact_email_message_task(subject: str, email: str, content: str, ip: str, user_id: int) -> Optional[str]:
    """
        Отправляет письмо из формы обратной связи.

        Args:
            subject (str): Тема письма.
            email (str): Адрес электронной почты получателя.
            content (str): Содержимое письма.
            ip (str): IP-адрес отправителя.
            user_id (int): Идентификатор пользователя, отправившего сообщение.

        Returns:
            Optional[str]: Результат отправки сообщения (обычно строка с статусом отправки).
                           Может вернуть None, если произошла ошибка.

        Notes:
            - Эта задача обычно используется в представлении FeedbackCreateView.
            - Использует функцию send_contact_email_message для отправки письма из формы обратной связи.
    """
    # Вызываем функцию для отправки письма из формы обратной связи и возвращаем результат
    return send_contact_email_message(subject, email, content, ip, user_id)


########################################################################################################################

# Этот декоратор указывает, что функция dbackup_task является задачей Celery. Это означает, что она может быть запущена
# асинхронно в фоновом режиме, независимо от основного потока выполнения приложения.
@shared_task
def dbackup_task() -> None:
    """
        Выполнение резервного копирования базы данных.

        Эта задача выполняет резервное копирование базы данных, вызывая команду `dbackup`.
    """
    # Вызываем команду 'dbackup' для выполнения резервного копирования базы данных.
    call_command('dbackup')
########################################################################################################################
