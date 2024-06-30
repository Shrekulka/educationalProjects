# backend/celery.py

import os

from celery import Celery

# Устанавливаем модуль настроек Django по умолчанию для программы 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Создаем экземпляр Celery с именем приложения 'backend'.
app = Celery('backend')

# Использование строки здесь означает, что рабочему процессу не нужно сериализовать
# объект конфигурации для дочерних процессов.
# - namespace='CELERY' означает, что все ключи конфигурации, связанные с Celery, должны иметь префикс `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загружаем модули задач из всех зарегистрированных Django-приложений.
app.autodiscover_tasks()
