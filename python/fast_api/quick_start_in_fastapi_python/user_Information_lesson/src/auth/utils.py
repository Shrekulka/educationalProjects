# user_Information_lesson/src/auth/utils.py
import random
from typing import Union, Generator, Iterator

from src.models import User

# Начальный идентификатор для данных
STARTING_ID = 1

FIRST_NAMES = [
    'Алексей', 'Александра', 'Андрей', 'Анна', 'Борис', 'Валентина', 'Василий', 'Виктор', 'Галина', 'Дмитрий', 'Елена',
    'Жанна', 'Захар', 'Иван', 'Ирина', 'Константин', 'Ксения', 'Лариса', 'Максим', 'Марина', 'Николай', 'Оксана',
    'Павел', 'Петр', 'Раиса', 'Роман', 'Руслан', 'Светлана', 'Сергей', 'Татьяна', 'Ульяна', 'Федор', 'Христина',
    'Цветана', 'Чеслав', 'Шарлотта', 'Щек', 'Эдуард', 'Юлия', 'Юрий', 'Яна', 'Ярослав'
]

LAST_NAMES = [
    'Абрамов', 'Беляев', 'Волков', 'Григорьев', 'Дмитриев', 'Егоров', 'Жуков', 'Иванов', 'Козлов', 'Лебедев',
    'Макаров', 'Никитин', 'Орлов', 'Павлов', 'Романов', 'Смирнов', 'Тарасов', 'Устинов', 'Федоров', 'Харитонов',
    'Цветков', 'Чернов', 'Шарапов', 'Щербаков', 'Эдуардов', 'Юдин', 'Яковлев', 'Яромеев', 'Антоненко', 'Бондаренко',
    'Волочков', 'Гаврилов', 'Данилов', 'Ефимов', 'Жигалов', 'Захаров', 'Исаев', 'Карпов', 'Лисов', 'Михайлов',
    'Назаров', 'Осипов', 'Поляков', 'Родионов', 'Соболев', 'Тимофеев', 'Устинов', 'Филатов', 'Хмельнов', 'Цой'
]

EMAIL = [
    'alex@example.com', 'anna@example.com', 'andrey@example.com', 'boris@example.com', 'valentina@example.com',
    'vasily@example.com', 'viktor@example.com', 'galina@example.com', 'dmitry@example.com', 'elena@example.com',
    'zhanna@example.com', 'zakhar@example.com', 'ivan@example.com', 'irina@example.com', 'konstantin@example.com',
    'ksenia@example.com', 'larisa@example.com', 'maxim@example.com', 'marina@example.com', 'nikolay@example.com',
    'oksana@example.com', 'pavel@example.com', 'petr@example.com', 'raisa@example.com', 'roman@example.com',
    'ruslan@example.com', 'svetlana@example.com', 'sergey@example.com', 'tatiana@example.com', 'ulyana@example.com',
    'fedor@example.com', 'kristina@example.com', 'tsetana@example.com', 'cheslav@example.com', 'charlotte@example.com',
    'shek@example.com', 'eduard@example.com', 'yulia@example.com', 'yuri@example.com', 'yana@example.com',
    'yaroslav@example.com'
]


def id_generator(num_users: int) -> Generator[int, None, None]:
    """
    Генератор уникальных идентификаторов пользователей.

    Args:
        num_users (int): Количество уникальных идентификаторов пользователей, которые нужно сгенерировать.

    Returns:
        Generator[int, None, None]: Генератор уникальных идентификаторов пользователей.
    """
    # Начинаем с генерации идентификатора, который соответствует начальному идентификатору
    # Например, если STARTING_ID = 1, начинаем с 1
    for i in range(STARTING_ID, STARTING_ID + num_users):
        # Используем цикл for для генерации идентификаторов от STARTING_ID до STARTING_ID + num_users
        # Применяем оператор yield для возврата каждого идентификатора по мере его генерации
        yield i


def generate_users(num_users: int) -> list:
    """
    Генерирует пользователей.

    Args:
        num_users (int): Количество пользователей, которые нужно сгенерировать.

    Returns:
        list: Список объектов пользователей, содержащих сгенерированные данные.

    """
    users = []  # Создаем пустой список для хранения сгенерированных пользователей
    # Создаем генератор уникальных идентификаторов
    id_gen: Iterator[int] = id_generator(num_users)
    # Цикл проходит size раз, создавая новых пользователей.
    for _ in range(num_users):
        # Получаем следующий уникальный идентификатор
        user_id = next(id_gen)
        # Генерируем полное имя пользователя
        full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        # Генерируем случайный возраст от 10 до 120 лет
        age = random.choice(range(10, 120))
        # Генерируем случайный адрес электронной почты из списка EMAIL
        email = random.choice(EMAIL)

        # Создаем нового пользователя с сгенерированными данными и добавляем его в список пользователей
        new_user = User(user_id=user_id, full_name=full_name, age=age, email=email)
        users.append(new_user)
    # Возвращаем список сгенерированных пользователей
    return users


def find_user_by_id(user_id: int, users: list) -> Union[User, dict]:
    """
    Функция для поиска пользователя по идентификатору.

    Args:
        user_id (int): Идентификатор пользователя, которого нужно найти.
        users (list): Список пользователей, в котором осуществляется поиск.

    Returns:
        Union[User, dict]: Если пользователь найден, возвращается объект пользователя.
                          В противном случае возвращается словарь с сообщением об ошибке.
    """
    # Перебираем каждого пользователя в списке пользователей
    for user in users:
        # Проверяем идентификатор каждого пользователя в списке
        if user.user_id == user_id:
            # Если идентификатор совпадает, возвращаем пользователя
            return user
    # Если пользователь не найден, возвращаем словарь с сообщением об ошибке
    return {"error": "User not found"}
