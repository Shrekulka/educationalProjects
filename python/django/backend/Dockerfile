# Dockerfile для создания образа Docker, используемого для запуска Django-приложения.
# Основан на Python с Alpine Linux для минимального размера образа и быстрого запуска.

FROM python:alpine

# Устанавливаем переменные окружения для Python, чтобы ускорить запуск и избежать создания скомпилированных файлов.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Обновляем пакеты и устанавливаем библиотеку libpq, необходимую для подключения к PostgreSQL.
RUN apk update && apk add libpq

# Устанавливаем временные зависимости, необходимые для компиляции Python-модулей.
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev libffi-dev openssl-dev

# Обновляем pip до последней версии.
RUN pip install --upgrade pip

# Копируем файл requirements.txt внутрь контейнера и устанавливаем зависимости Python-приложения.
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Удаляем временные зависимости после установки пакетов.
RUN apk del .build-deps

# Задаем рабочую директорию внутри контейнера.
WORKDIR /app

# Копируем все файлы из текущей локальной директории внутрь контейнера.
COPY . .

# Устанавливаем права доступа 777 для всех файлов внутри контейнера (не рекомендуется для продакшн среды).
RUN chmod -R 777 ./
