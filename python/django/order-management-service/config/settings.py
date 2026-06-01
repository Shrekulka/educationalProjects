# order-management-service/config/settings.py

import os
from pathlib import Path

from dotenv import load_dotenv

# Завантажуємо змінні з .env файлу
load_dotenv()

# BASE_DIR — корінь проєкту, від нього будуємо всі шляхи
BASE_DIR = Path(__file__).resolve().parent.parent


def get_env(key, default=None, required=False):
    """
    Вспомогательная функция для чтения переменных окружения.

    Почему не просто os.getenv везде?
    Потому что os.getenv без дефолта вернёт None и приложение
    упадёт позже с непонятной ошибкой типа:
    "NoneType has no attribute split"

    С этой функцией при required=True падение происходит сразу
    при старте с понятным сообщением что именно не настроено.
    """
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(
            f"Обов'язкова змінна середовища '{key}' не задана. "
            f"Перевірте .env файл."
        )
    return value


# SECURITY
# Секретний ключ Django — використовується для підпису сесій, токенів тощо
# Береться з .env, ніколи не хардкодиться
SECRET_KEY = get_env('DJANGO_SECRET_KEY', required=True)

# Debug режим — з .env, в продакшені має бути False
DEBUG = get_env('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = get_env('DJANGO_ALLOWED_HOSTS', '*').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_spectacular',
    'rest_framework',  # Django REST Framework
    'modules.orders.apps.OrdersConfig',  # наш модуль замовлень
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASE
# Читаємо всі параметри з .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env('DB_NAME', 'k2_erp', required=True),
        'USER': get_env('DB_USER', 'k2_user', required=True),
        'PASSWORD': get_env('DB_PASSWORD', required=True),
        'HOST': get_env('DB_HOST', 'localhost'),
        'PORT': get_env('DB_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'uk'  # Ukrainian
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

# STATIC FILES (для Django Admin)
STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_ROOT = BASE_DIR / 'staticfiles'

# PRIMARY KEY
# BigAutoField — 64-bit int, краще ніж AutoField (32-bit)
# для великої системи де може бути багато записів
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    # Формат відповіді за замовчуванням — JSON
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # зручний браузерний інтерфейс
    ],
    # Пагінація — важливо для ERP де може бути багато записів
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# DRF SPECTACULAR (Swagger)
SPECTACULAR_SETTINGS = {
    'TITLE': 'K2 ERP API',
    'DESCRIPTION': 'API модуля обліку замовлень для K2 ERP',
    'VERSION': '1.0.0',
}

CSRF_COOKIE_HTTPONLY = False
