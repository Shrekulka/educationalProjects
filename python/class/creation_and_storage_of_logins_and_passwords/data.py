import random
import string


class Data:
    def __init__(self, name, password, login="", notes=""):
        """
        Инициализирует объект данных.

        Аргументы:
        - name (str): Имя данных.
        - password (str): Пароль.
        - login (str, optional): Логин. По умолчанию - "".
        - notes (str, optional): Заметки. По умолчанию - "".
        """
        self.name = name
        self.password = password
        self.login = login
        self.notes = notes

    def save_to_database(self, database):
        """
        Метод генерирует пароль.

        Аргументы:
        - complexity_choice (str): Выбор сложности пароля.
        """
        # Проверяем, если есть соединение с базой данных.
        if database.connection is not None:
            # Если заметки пустые, присваиваем значение None.
            if self.notes == "":
                self.notes = None
            # Вставляем данные в базу данных с использованием словаря self.__dict__,
            # который содержит атрибуты объекта Data.
            database.insert_data(self.__dict__)
        else:
            print("No database connection.")

    # Определяем длину пароля в зависимости от выбранной сложности.
    def generate_password(self, complexity_choice):
        """
        Метод генерирует пароль.

        Аргументы:
        - complexity_choice (str): Выбор сложности пароля.
        """
        if complexity_choice == "1":
            length = 10
        elif complexity_choice == "2":
            length = 16
        elif complexity_choice == "3":
            length = 20
        else:
            length = 24
        # Определяем набор символов, из которых будет состоять пароль.
        characters = string.ascii_letters + string.digits + string.punctuation
        # Генерируем список случайных символов длиной length из заданного набора символов.
        password_list = random.choices(characters, k=length)
        # Преобразуем список символов в строку и присваиваем ее атрибуту password объекта Data.
        self.password = ''.join(password_list)

    @staticmethod
    def check_password_complexity(password):
        """
        Метод проверяет сложность пароля.

        Аргументы:
        - password (str): Пароль.

        Возвращает:
        - complexity (str): Сложность пароля.
        """
        is_lowercase = any(char.islower() for char in password)
        is_uppercase = any(char.isupper() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_punctuation = any(char in string.punctuation for char in password)
        # Если пароль содержит строчные и заглавные буквы, цифры и специальные символы, возвращаем сложность "ultra".
        if all([is_lowercase, is_uppercase, has_digit, has_punctuation]):
            return "ultra"
        # Если пароль содержит строчные и заглавные буквы и цифры, но не содержит специальных символов,
        # возвращаем сложность "complex".
        elif all([is_lowercase, is_uppercase, has_digit]):
            return "complex"
        else:
            # Если пароль не соответствует ни одной из вышеперечисленных сложностей, возвращаем сложность "normal".
            return "normal"


class WebsiteData(Data):
    def __init__(self, address, login, password, notes=""):
        """
        Инициализирует объект данных для веб-сайта.

        Аргументы:
        - address (str): Адрес веб-сайта.
        - login (str): Логин.
        - password (str): Пароль.
        - notes (str, optional): Заметки. По умолчанию - "".
        """
        super().__init__(name=address, login=login, password=password, notes=notes)

    @staticmethod
    def get_name_prompt():
        """
        Возвращает приглашение для ввода имени веб-сайта.

        Возвращает:
        - prompt (str): Приглашение для ввода имени веб-сайта.
        """
        return "Enter website name (website name should start with 'http://', 'https://' or 'ftp://'): "

    @staticmethod
    def get_login_prompt():
        """
        Возвращает приглашение для ввода логина веб-сайта.

        Возвращает:
        - prompt (str): Приглашение для ввода логина веб-сайта.
        """
        return "Enter login for website: "

    def validate_name(self):
        """
        Проверяет правильность URL-адреса веб-сайта.
        Выбрасывает исключение ValueError, если URL-адрес некорректен.
        """
        # Определяем допустимые префиксы URL-адреса.
        prefixes = ("http://", "https://", "ftp://")
        # Если URL-адрес не начинается ни с одного из допустимых префиксов, выбрасываем исключение с сообщением о
        # некорректном URL-адресе.
        if not any(self.name.startswith(prefix) for prefix in prefixes):
            raise ValueError("Invalid website URL. Website name should start with 'http://', 'https://' or 'ftp://'")


class FileData(Data):
    def __init__(self, address, password, login=None, notes=""):
        """
        Инициализирует объект данных для файла.

        Аргументы:
        - address (str): Имя файла.
        - password (str): Пароль.
        - login (str, optional): Логин. По умолчанию - None.
        - notes (str, optional): Заметки. По умолчанию - "".
       """
        super().__init__(name=address, password=password, login=login, notes=notes)

    @staticmethod
    def get_name_prompt():
        """
        Возвращает приглашение для ввода имени файла.

        Возвращает:
        - prompt (str): Приглашение для ввода имени файла.
        """
        return "Enter a file name (the file name must not contain punctuation marks): "

    @staticmethod
    def get_login_prompt():
        """
        Возвращает приглашение для ввода логина файла.

        Возвращает:
        - prompt (str): Приглашение для ввода логина файла.
        """
        return None

    def validate_name(self):
        """
        Проверяет правильность имени файла.
        Выбрасывает исключение ValueError, если имя файла некорректно.
        """
        # Определяем недопустимые символы для имени файла "!"#$%&'()*+,-./:;<=>?@[\]^_{|}~".
        invalid_characters = string.punctuation
        # Если имя файла содержит недопустимые символы, выбрасываем исключение с сообщением о некорректном имени файла.
        if any(char in invalid_characters for char in self.name):
            raise ValueError("Invalid filename. The file name must not contain punctuation marks.")


class ApplicationData(Data):
    def __init__(self, address, password, login="", notes=""):
        """
        Инициализирует объект данных для приложения.

        Аргументы:
        - address (str): Название приложения.
        - password (str): Пароль.
        - login (str, optional): Логин. По умолчанию - "".
        - notes (str, optional): Заметки. По умолчанию - "".
        """
        super().__init__(name=address, password=password, login=login, notes=notes)

    @staticmethod
    def get_name_prompt():
        """
        Возвращает приглашение для ввода имени приложения.

        Возвращает:
        - prompt (str): Приглашение для ввода имени приложения.
        """
        return "Enter application name: "

    @staticmethod
    def get_login_prompt():
        """
        Возвращает приглашение для ввода логина приложения.

        Возвращает:
        - prompt (str): Приглашение для ввода логина приложения.
        """
        return "Enter login for application: "


class NoteData(Data):
    def __init__(self, address, password, login=None, notes=""):
        """
        Инициализирует объект данных для заметки.

        Аргументы:
        - address (str): Имя заметки.
        - password (str): Пароль.
        - login (str, optional): Логин. По умолчанию - None.
        - notes (str, optional): Заметки. По умолчанию - "".
        """
        super().__init__(name=address, password=password, login=login, notes=notes)

    @staticmethod
    def get_name_prompt():
        """
        Возвращает приглашение для ввода имени заметки.

        Возвращает:
        - prompt (str): Приглашение для ввода имени заметки.
        """
        return "Enter note name (имя записи не должно содержать знаков пунктуации): "

    @staticmethod
    def get_login_prompt():
        """
        Возвращает приглашение для ввода логина заметки.

        Возвращает:
        - prompt (str): Приглашение для ввода логина заметки.
        """
        return None

    def validate_name(self):
        """
        Проверяет правильность имени заметки.
        Выбрасывает исключение ValueError, если имя заметки некорректно.
        """
        # Определяем недопустимые символы для имени заметки "!"#$%&'()*+,-./:;<=>?@[\]^_{|}~".
        invalid_characters = string.punctuation
        # Если имя заметки содержит недопустимые символы, выбрасываем исключение с сообщением о некорректном имени.
        if any(char in invalid_characters for char in self.name):
            raise ValueError("Invalid filename. The file name must not contain punctuation marks.")


class GameData(Data):
    def __init__(self, address, login, password, notes=""):
        """
        Инициализирует объект данных для игры.

        Аргументы:
        - address (str): Название игры.
        - login (str): Логин.
        - password (str): Пароль.
        - notes (str, optional): Заметки. По умолчанию - "".
        """
        super().__init__(name=address, login=login, password=password, notes=notes)

    @staticmethod
    def get_name_prompt():
        """
        Возвращает приглашение для ввода имени игры.

        Возвращает:
        - prompt (str): Приглашение для ввода имени игры.
        """
        return "Enter game name: "

    @staticmethod
    def get_login_prompt():
        """
        Возвращает приглашение для ввода логина игры.

        Возвращает:
        - prompt (str): Приглашение для ввода логина игры.
        """
        return "Enter login for game: "
