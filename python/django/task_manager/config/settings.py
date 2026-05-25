# task_manager/config/settings.py

import os
from pathlib import Path

import environ

# Инициализация environ
env = environ.Env()

# Путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Чтение .env (файл должен быть в корне проекта)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

PROJECT_ROOT = BASE_DIR.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# ⚠️ SECURITY: храните SECRET_KEY в .env, а не в коде
SECRET_KEY = env('SECRET_KEY')

# DEBUG читается как булево значение
DEBUG = env.bool('DEBUG', default=True)

# ALLOWED_HOSTS — список через запятую
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Если нужны доверенные источники для CSRF (например, при работе через прокси)
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_htmx',  # HTMX интеграция
    'django.contrib.sites',
    'allauth',  # Аутентификация
    'allauth.account',
    'allauth.socialaccount',

    # Local apps
    'apps.projects.apps.ProjectsConfig',
    'apps.tasks.apps.TasksConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# База данных
DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{env("DB_ENGINE", default="postgresql")}',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# EMAIL_BACKEND из .env
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# Тип автоинкремента для первичных ключей
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Аутентификация и авторизация
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Минимум 8 символов для безопасности
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

# django-allauth настройки
AUTHENTICATION_BACKENDS = [
    # Django backend
    'django.contrib.auth.backends.ModelBackend',
    # allauth backend для email/username
    'allauth.account.auth_backends.AuthenticationBackend',
]

# allauth конфигурация
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Опциональная верификация для dev
LOGIN_REDIRECT_URL = '/'  # Редирект после логина
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_AUTO_SIGNUP = True

# Интернационализация
USE_I18N = True
USE_TZ = True
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ===== ПРОДАКШН-НАСТРОЙКИ БЕЗОПАСНОСТИ =====
if not DEBUG:
    # Принудительный HTTPS
    SECURE_SSL_REDIRECT = True
    # Обязательно для прокси (если за nginx/ngrok)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Куки только по HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS (заставляет браузеры использовать HTTPS)
    SECURE_HSTS_SECONDS = 31536000  # 1 год
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Защита от кликджекинга
    X_FRAME_OPTIONS = 'DENY'
