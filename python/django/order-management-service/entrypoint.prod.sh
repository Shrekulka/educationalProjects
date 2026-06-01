#!/bin/sh

# Production entrypoint для Docker-контейнера.
# Запускает Gunicorn — надёжный WSGI-сервер для реальной эксплуатации.

echo "==> Запуск міграцій..."
python manage.py migrate --noinput

echo "==> Збір статичних файлів..."
python manage.py collectstatic --noinput

echo "==> Запуск Gunicorn (production)..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level info \
    --access-logfile -