FROM python:3.13-slim

# Установка рабочей директории
WORKDIR /app

# Установка переменной для вывода логов Python без буферизации
ENV PYTHONUNBUFFERED=1

# Установка зависимостей системы (только postgresql-client для отладки, gcc удалён)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements.txt и установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .



# Запуск Gunicorn сервера
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]