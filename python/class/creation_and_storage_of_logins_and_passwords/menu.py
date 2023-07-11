import os
import sqlite3
from bd import BD
from data import (WebsiteData, FileData, ApplicationData, NoteData, GameData)


class Menu:
    def __init__(self, database):
        """
        Инициализирует объект класса Menu.

        Аргументы:
        - database (BD): Объект базы данных SQLite.
        """
        self.unzip_data_structure = None
        self.archive_data_structure = None
        self.database = database

    def display_passwords(self):
        """
        Метод отображает все сохраненные пароли.
        """
        # Получаем все данные из базы данных
        rows = self.database.get_all_data()
        # Перебираем строки данных
        for row in rows:
            info = [f"{field}: {value}" for field, value in
                    zip(["ID", "Type", "Name", "Login", "Password", "Note"], row[0:6]) if value is not None]
            print("\n".join(info))  # Выводим информацию о пароле
            print()

    def archive(self):
        """
        Метод создает архив базы данных.
        """
        archive_name = input("Enter the path and name of the archive without extension (for example: /Users/base): ")
        archive_name = os.path.splitext(archive_name)[0] + ".zip"  # Добавляем расширение .zip к имени архива

        # Создаем архив базы данных и сохраняем возвращаемое значение пароля
        password = self.database.archive_database(archive_name)

        print("\nThe database was successfully archived.")
        print(f"Archive: {archive_name}")
        # Если пароль не None выводим пароль
        if password is not None:
            print(f"Password: {password}\n")

    def unzip(self):
        """
        Метод извлекает архив базы данных.
        """
        archive_name = input("Enter the path and name of the archive without extension (for example: /Users/base): ")
        archive_name = os.path.splitext(archive_name)[0] + ".zip"  # Добавляем расширение .zip к имени архива

        # Извлекаем базу данных из архива и сохраняем информацию о деталях
        details = self.database.unzip_database(archive_name)
        if details is not None:
            print("The database was successfully retrieved.")
            print(f"Archive: {details['Archive']}")
            if details['Password'] is not None:
                print(f"Password: {details['Password']}")
        else:
            print("Failed to retrieve database.")

    @staticmethod
    def print_menu_options(options):
        """
        Выводит на экран список опций меню.

        Аргументы:
        - options (dict): Словарь с опциями меню, где ключ - код опции, значение - кортеж с описанием опции.
        """
        # Перебираем опции меню
        for key, value in options.items():
            # Выводим код и описание опции
            print(f"{key}. {value[0]}")

    def run(self):
        """
        Метод запускает основное меню программы.
        """
        print("""                       ********** Hello user! **********
        This program is designed for managing and storing login credentials and passwords.
        You have the following options:
        1. Create a new database - to create a new database for storing your passwords.
        2. Load an existing database - to load an existing database to manage your passwords.
        0. Exit - to exit the program.\n""")
        action_options = {
            "1": ("Create new database", self.create_new_database),
            "2": ("Load existing database", self.load_existing_database),
            "0": ("Exit", self.exit_program)
        }

        while True:
            # Выводим опции основного меню
            self.print_menu_options(action_options)
            action_choice = input("Enter your choice: ")

            # Если выбор существует в опциях
            if action_choice in action_options:
                # Выполняем соответствующую функцию
                action_options[action_choice][1]()
                break
            else:
                print("Invalid choice. Please try again.")

        if self.database is not None:
            print("""                        ********** Main Menu **********
                   You are now in the main menu.
                   Here are your options:
                   1. Generate and save password - to generate and save a new password.
                   2. Display passwords - to display all stored passwords.
                   3. Archive data structure - to create an archive of the database.
                   4. Unzip data structure - to extract and load a database from an archive.
                   0. Exit - to exit the program.\n""")
            print()
            menu_options = {
                "1": ("Generate and save password", self.generate_and_save_password),
                "2": ("Display passwords", self.display_passwords),
                "3": ("Archive data structure", self.archive),
                "4": ("Unzip data structure", self.unzip),
                "0": ("Exit", self.exit_program)
            }

            while True:
                # Выводим опции главного меню
                self.print_menu_options(menu_options)
                choice = input("Enter your choice: ")
                # Если выбор существует в опциях
                if choice in menu_options:
                    # Выполняем соответствующую функцию
                    menu_options[choice][1]()
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("No database available. Exiting.")
            Menu.exit_program()

    def create_new_database(self):
        """
        Метод создает новую базу данных.
        """
        database_name = input(
            "Enter the path and name of the new database without extension (for example: /Users/new_database): ")
        # Создаем объект базы данных
        self.database = BD(database_name)
        # Устанавливаем соединение с базой данных
        self.database.connection = sqlite3.connect(database_name)

    def load_existing_database(self):
        """
        Метод загружает существующую базу данных.
        """
        database_name = input("Enter the location of the existing database: ")
        if os.path.exists(database_name):
            try:
                # Создаем объект базы данных
                self.database = BD(database_name)
                # Устанавливаем соединение с базой данных
                self.database.connection = sqlite3.connect(self.database.database_name)
                print("Database loaded.")
                print(self.database.database_name)

            except sqlite3.OperationalError:
                print("Invalid database file. Please try again.")
                self.database = None
        else:
            print("Invalid database file. Please try again.")
            self.database = None
            self.run()

    def generate_and_save_password(self):
        print("""This option allows you to generate and save a new password.
        Please select a category for the password.
        You will be prompted to enter the following information:
        - Name: Enter the name of the password item.
        - Login: Enter the login associated with the password (if applicable).
        - Password: A random password will be generated and displayed.
        - Notes: You can enter any additional notes or information (optional).
        """)
        # Словарь, содержащий отображение кода категории на класс данных и соответствующие промпты для имени и логина
        category_mapping = {
            "1": (WebsiteData, WebsiteData.get_name_prompt(), WebsiteData.get_login_prompt()),
            "2": (FileData, FileData.get_name_prompt(), None),
            "3": (ApplicationData, ApplicationData.get_name_prompt(), ApplicationData.get_login_prompt()),
            "4": (GameData, GameData.get_name_prompt(), GameData.get_login_prompt()),
            "5": (NoteData, NoteData.get_name_prompt(), None)
        }
        # Проходимся по каждой паре ключ-значение в словаре category_mapping
        for k, v in category_mapping.items():
            name = v[0].__name__.replace("Data", "")  # Получаем имя категории путем удаления "Data" из имени класса
            print(f"{k}. {name}")  # Выводим код категории и имя категории

        category_choice = input("Введите код категории: ")
        # Получаем выбранную категорию из словаря category_mapping
        category = category_mapping.get(category_choice)

        if category is None:
            print("Неверный код категории.")
            return
        # Распаковываем значения из выбранной категории
        class_name, name_prompt, login_prompt = category
        # Создаем объект данных пароля со значениями по умолчанию
        password_data = class_name(address="", login=None, password="")

        while True:
            name = input(name_prompt)
            try:
                password_data.name = name
                # Если выбрана категория "ApplicationData" или "GameData"
                if category_choice == "3" or category_choice == "4":
                    break
                else:
                    password_data.validate_name()  # Проверка правильности имени
                break
            except ValueError as e:
                print(str(e))
                continue

        password_data.name = name
        # Проверяем, существуют ли данные с таким же именем и типом
        data_exists = self.database.get_data_by_type(class_name.__name__, name)

        # Если данные с таким же именем и типом существуют заходим
        if data_exists:
            update_choice = input(
                "Data with the same name already exists. Do you want to update it?\n1) Yes\n2) No\nEnter your choice: ")
            # Обновление данных по имени
            if update_choice == "1":
                # Флаг, указывающий на то, были ли данные обновлены
                updated = False
                # Проходимся по каждому элементу данных
                for data_item in data_exists:
                    # Если имя элемента данных совпадает с введенным именем (регистронезависимое сравнение)
                    if data_item[2].lower() == name.lower():
                        # Опции для полей данных
                        field_options = {
                            "login": {
                                # Вопрос для ввода нового логина
                                "question": "Enter new login (leave blank to keep the current login): ",
                                # Значение по умолчанию для логина (текущий логин)
                                "default": data_item[3],
                                # Функция преобразования значения логина (не требуется для FileData и NoteData)
                                "conversion_func": None if class_name in [FileData, NoteData] else lambda x: x
                            },
                            "notes": {
                                # Вопрос для ввода новых заметок
                                "question": "Enter new notes (leave blank to keep the current notes): ",
                                # Значение по умолчанию для заметок (текущие заметки)
                                "default": data_item[5],
                                # Функция преобразования значения заметок (не требуется)
                                "conversion_func": None
                            },
                            "password": {
                                # Вопрос для ввода нового пароля
                                "question": "Enter new password:\n1) Keep the current password\n2) Generate a new password\nEnter your choice: ",
                                # Значение по умолчанию для пароля (отсутствует)
                                "default": None,
                                # Функция преобразования значения пароля в зависимости от выбора (2 - сгенерировать
                                # новый пароль, иначе текущий пароль)
                                "conversion_func": lambda x: self.choose_password_complexity() if x == "2" else
                                data_item[4]
                            }

                        }
                        # Словарь для хранения значений полей
                        field_values = {}

                        for field, options in field_options.items():
                            # Просим пользователя ввести значение поля
                            value = input(options["question"])
                            # Если значение не пустое, используем введенное значение, иначе используем значение по
                            # умолчанию
                            field_values[field] = value if value != "" else options["default"]

                            # Если есть функция преобразования, применяем ее к значению поля
                            if options["conversion_func"]:
                                field_values[field] = options["conversion_func"](field_values[field])

                        password_data.login = field_values["login"]  # Устанавливаем новое значение логина
                        password_data.password = field_values["password"]  # Устанавливаем новое значение пароля
                        password_data.notes = field_values["notes"]  # Устанавливаем новое значение заметок

                        # Обновляем данные в базе данных
                        self.database.update_data({
                            'type': password_data.__class__.__name__,
                            'address': password_data.name,
                            'login': password_data.login,
                            'password': password_data.password,
                            'note': password_data.notes,
                            'id': data_item[0]
                        })
                        updated = True
                        break

                # Если данные были обновлены
                if updated:
                    print("Data updated.")
                    # Выводим информацию о сгенерированном пароле
                    self.print_generated_password_details(class_name, password_data)
                # Если не найдено данных с указанным именем
                else:
                    print("No data with the specified name found.")
            # Если данные не были обновлены (не вошли в цикл по обновлению данных)
            else:
                print("Data not updated.")
        else:
            # Если у поля login_prompt есть значение
            if login_prompt is not None:
                login = input(login_prompt)  # Запрашиваем у пользователя логин
                # Если введен пустой логин, присваиваем ему значение None
                if login == "":
                    login = None
                # Присваиваем полю login объекта password_data значение логина
                password_data.login = login
            # Получаем сложность пароля от пользователя
            complexity_choice = self.choose_password_complexity()
            # Генерируем пароль
            password_data.generate_password(complexity_choice)

            notes = input("Enter notes: ")
            # Если введена пустая заметка, присваиваем ей значение None
            if notes == "":
                notes = None
            # Присваиваем полю notes объекта password_data значение логина
            password_data.notes = notes
            # Вставляем данные в базу данных
            self.database.insert_data({
                'type': password_data.__class__.__name__,
                'address': password_data.name,
                'login': password_data.login,
                'password': password_data.password,
                'note': password_data.notes
            })

            self.print_generated_password_details(class_name, password_data)

    @staticmethod
    def choose_password_complexity():
        """
        Метод запрашивает у пользователя сложность пароля.

        Возвращает:
        - complexity_choice (str): Выбор сложности пароля.
        """
        while True:
            complexity_prompt = "Choose password complexity:\n1. Normal\n2. Complex\n3. Very complex\nEnter your choice: "
            complexity_choice = input(complexity_prompt)

            valid_complexities = ["1", "2", "3"]  # Список допустимых вариантов сложности пароля
            # Если выбранная сложность присутствует в списке допустимых вариантов
            if complexity_choice in valid_complexities:
                break  # Прерываем цикл

            print("Invalid complexity choice. Please try again.")

        return complexity_choice  # Возвращаем выбранный вариант сложности

    @staticmethod
    def print_generated_password_details(class_name, password_data):
        """
        Выводит на экран информацию о сгенерированном пароле.

        Аргументы:
        - class_name (class): Класс данных пароля.
        - password_data (Data): Объект данных пароля.
        """
        print("Password generated and saved successfully.")
        print("Generated password details:")

        print(f"{class_name.__name__}: {password_data.name}")  # Выводим имя класса данных и имя пароля

        if password_data.login:  # Если есть логин
            print(f"Login: {password_data.login}")

        print(f"Password: {password_data.password}")  # Выводим пароль

        if password_data.notes:  # Если есть заметки
            print(f"Notes: {password_data.notes}")  # Выводим заметки
        print("\n")

    @staticmethod
    def exit_program():
        """
        Выходит из программы.
        """
        print("Goodbye!")
        return
