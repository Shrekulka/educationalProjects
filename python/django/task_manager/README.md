# 📋 Task Manager

Привет! Это веб-приложение для управления задачами и проектами, которое я написал на Django. Оно помогает не забывать о делах, расставлять приоритеты и следить за дедлайнами. Всё обновляется без перезагрузки страницы — благодаря HTMX ⚡

---

## 🚀 Возможности

- ✅ Создание, редактирование и удаление проектов
- ✅ Добавление, изменение и удаление задач внутри проекта
- ✅ Приоритеты задач (Low / Medium / High)
- ✅ Дедлайны и подсветка просроченных задач
- ✅ Быстрое изменение статуса задачи через checkbox
- ✅ Drag & Drop сортировка задач
- ✅ Фильтрация задач по статусу
- ✅ Поиск проектов в реальном времени
- ✅ Регистрация и авторизация пользователей
- ✅ Изоляция данных пользователей (каждый видит только свои проекты)
- ✅ Работа без перезагрузки страницы через HTMX + Alpine.js

---

## 🛠️ Технологии

### Backend
- Python 3.13
- Django 5.2
- PostgreSQL
- Gunicorn

### Frontend
- Bootstrap 5
- HTMX
- Alpine.js
- Hyperscript

### DevOps / Infrastructure
- Docker
- Docker Compose
- Ruff
- Black
- Pre-commit

---

## 📦 Быстрый запуск через Docker

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd task_manager
```

### 2. Создание `.env`

```bash
cp .env.example .env
```

Для локального запуска значения по умолчанию подходят.

---

### 3. Запуск контейнеров

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

---

### 4. Применение миграций

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

---

### 5. Создание суперпользователя

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

---

### 6. Открытие проекта

```text
http://localhost:8000
```

🚀 Готово! Приложение работает.

---

# 🧑‍💻 Локальный запуск (без Docker)

## 1. Создание виртуального окружения

```bash
python -m venv venv
```

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## 3. Настройка базы данных

Можно использовать:
- PostgreSQL
- SQLite

Если используется PostgreSQL — создай базу данных и укажи параметры подключения в `.env`.

---

## 4. Применение миграций

```bash
python manage.py migrate
```

---

## 5. Сбор статики

```bash
python manage.py collectstatic
```

---

## 6. Запуск сервера

```bash
python manage.py runserver
```

Открыть:

```text
http://127.0.0.1:8000
```

---

# 🔐 Переменные окружения

Пример `.env` уже находится в `.env.example`.

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_ENGINE=postgresql
POSTGRES_DB=task_manager
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# CSRF
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

---

## ⚠️ Для production

При `DEBUG=False` обязательно укажи:

- домен в `ALLOWED_HOSTS`
- домен в `CSRF_TRUSTED_ORIGINS`

Пример для ngrok:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,*.ngrok-free.app

CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,https://*.ngrok-free.app
```

---

# 🧪 Ruff, Black и Pre-commit

## Установка pre-commit

```bash
pip install pre-commit
```

---

## Установка git hooks

```bash
pre-commit install
```

Теперь перед каждым коммитом код автоматически проверяется линтерами 🚀

---

# 🗂️ Структура проекта

```text
task_manager/
├── config/                            # Конфиг Django проекта
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/                              # Пользовательские приложения
│   ├── projects/                      # Приложение "Проекты"
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── templates/
│   │       └── projects/
│   │           ├── project_list.html
│   │           ├── project_detail.html
│   │           ├── project_form.html
│   │           ├── project_confirm_delete.html
│   │           └── project_list_partial.html
│   │
│   └── tasks/                         # Приложение "Задачи"
│       ├── migrations/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── forms.py
│       ├── urls.py
│       ├── admin.py
│       └── templates/
│           └── tasks/
│               ├── task_form.html
│               ├── task_confirm_delete.html
│               ├── task_item.html
│               ├── task_list_container.html
│               └── task_form_quick.html
│
├── templates/                         # Общие шаблоны
│   └── base.html
│
├── static/                            # Кастомные статические файлы
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── staticfiles/                       # Собранная статика
├── media/                             # Загружаемые файлы
│
├── Dockerfile
├── docker-compose.dev.yml             # Docker Compose для разработки
├── docker-compose.prod.yml            # Docker Compose для production
│
├── .env.example                       # Пример env переменных
├── .env                               # Реальные env переменные
│
├── requirements.txt
├── manage.py
├── pyproject.toml                     # Конфиг Ruff и Black
├── .pre-commit-config.yaml
├── .gitignore
└── README.md
```

---

# 🌐 Деплой

Проект готов к деплою на любой сервер с поддержкой Docker.

## Пример запуска через ngrok

Добавь в `.env`:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,*.ngrok-free.app

CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,https://*.ngrok-free.app
```

Запуск:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

После этого можно открыть публичный URL от ngrok 🌍

---

# 📬 Обратная связь

Если есть вопросы, предложения или найден баг — пиши 🙂

---

# 📜 Лицензия

Проект выполнен в рамках технического задания.

Можно использовать в учебных и личных целях с указанием авторства.