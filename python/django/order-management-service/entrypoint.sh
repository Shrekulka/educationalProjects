#!/bin/sh

# Development entrypoint (без Docker или docker-compose.override.yml).
# Запускает Django runserver с авто-перезагрузкой.

echo "==> Запуск міграцій..."
python manage.py migrate --noinput

echo "==> Збір статичних файлів..."
python manage.py collectstatic --noinput

echo "==> Запуск development-сервера..."
exec python manage.py runserver 0.0.0.0:8000