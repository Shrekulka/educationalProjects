# telegram_bot_book/database.py/database.py

# Создаем шаблон заполнения словаря с пользователями
user_dict_template = {
    'page': 1,
    'bookmarks': set()
}

# Инициализируем "базу данных"
users_db = {}