import os
import sqlite3
import pyzipper
import zipfile
import getpass
from data import Data


class BD:
    def __init__(self, database_name):
        """
        Инициализирует объект базы данных SQLite.

        Аргументы:
        - database_name (str): Имя базы данных.
        """
        if not database_name:  # Проверка, если имя базы данных не указано
            return
        self.database_name = database_name  # Сохранение имени базы данных
        self.connection = None  # Инициализация соединения с базой данных
        self.create_database()  # Создание базы данных

    def create_database(self):
        """
        Метод создает базу данных SQLite, если она не существует.
        """
        if not os.path.isfile(self.database_name):  # Проверка, если файл базы данных не существует
            self.connection = sqlite3.connect(self.database_name)  # Установка соединения с базой данных
            cursor = self.connection.cursor()  # Создание курсора

            # Создание таблицы с полями ID, TYPE, ADDRESS, LOGIN, PASSWORD, NOTE
            cursor.execute('''CREATE TABLE IF NOT EXISTS data
                                 (ID INTEGER PRIMARY KEY,
                                  TYPE VARCHAR NOT NULL,
                                  ADDRESS VARCHAR NOT NULL, 
                                  LOGIN VARCHAR ,
                                  PASSWORD VARCHAR NOT NULL,
                                  NOTE TEXT)''')

            self.connection.commit()  # Сохранение изменений в базе данных
        else:
            print("Database already exists.")
            print(self.database_name)

    def delete_data_by_type(self, data_type):
        """
        Метод возвращает данные из базы данных по заданному типу.

        Аргументы:
        - data_type (str): Тип данных.

        Возвращает:
        - rows (list): Список с данными.
        """
        if self.connection is not None:  # Проверка, если есть соединение с базой данных
            cursor = self.connection.cursor()  # Создание курсора

            # Получение данных из таблицы по типу
            cursor.execute(f"DELETE FROM data WHERE TYPE=?", (data_type,))

            rows = cursor.fetchall()  # Получение всех строк результата запроса

            return rows
        else:
            print("There is no connection to the database.")
            return []

    def get_all_data(self):
        """
        Метод возвращает все данные из базы данных.

        Возвращает:
        - rows (list): Список со всеми данными.
        """
        if self.connection is not None:  # Проверка, если есть соединение с базой данных
            cursor = self.connection.cursor()  # Создание курсора

            # Получение всех данных из таблицы
            cursor.execute("SELECT * FROM data")
            rows = cursor.fetchall()  # Получение всех строк результата запроса

            return rows
        else:
            print("There is no connection to the database.")
            return []

    def get_data_by_type(self, data_type, data_name):
        """
        Метод возвращает данные из базы данных по заданному типу.

        Аргументы:
        - data_type (str): Тип данных.
        - data_name (str): Имя данных.

        Возвращает:
        - rows (list): Список с данными.
        """
        if self.connection is not None:  # Проверка, если есть соединение с базой данных
            cursor = self.connection.cursor()  # Создание курсора

            # Получение данных из таблицы по типу
            cursor.execute("SELECT * FROM data WHERE TYPE=? AND ADDRESS LIKE ?", (data_type, data_name))

            rows = cursor.fetchall()  # Получение всех строк результата запроса

            return rows
        else:
            print("There is no connection to the database.")
            return []

    def insert_data(self, data):
        """
        Метод вставляет данные в базу данных.

        Аргументы:
        - data (dict): Словарь с данными для вставки.
          (должен содержать ключи: 'type', 'address', 'login', 'password', 'note')
        """
        if self.connection is not None:  # Проверка, если есть соединение с базой данных
            cursor = self.connection.cursor()  # Создание курсора

            # Вставка данных в таблицу
            cursor.execute("INSERT INTO data (TYPE, ADDRESS, LOGIN, PASSWORD, NOTE) VALUES (?, ?, ?, ?, ?)",
                           (data['type'], data['address'], data['login'], data['password'], data['note']))

            self.connection.commit()  # Сохранение изменений в базе данных
        else:
            print("There is no connection to the database.")

    def update_data(self, data):
        """
        Метод обновляет данные в базе данных.

        Аргументы:
        - data (dict): Словарь с данными для обновления
          (должен содержать ключи: 'type', 'address', 'login', 'password', 'note', 'id')
        """
        if self.connection is not None:  # Проверка, если есть соединение с базой данных
            cursor = self.connection.cursor()  # Создание курсора

            cursor.execute("UPDATE data SET TYPE=?, ADDRESS=?, LOGIN=?, PASSWORD=?, NOTE=? WHERE ID=?",
                           (data['type'], data['address'], data['login'], data['password'], data['note'], data['id']))

            self.connection.commit()  # Сохранение изменений в базе данных
        else:
            print("There is no connection to the database.")

    def archive_database(self, archive_name):
        """
        Метод архивирует базу данных SQLite.

        Аргументы:
        - archive_name (str): Имя архива.

        Возвращает:
        - password (str): Пароль для архива.
        """
        encryption_choice = input("1. Encrypt archive\n2. Leave archive unencrypted\nEnter your choice: ")
        password = None  # Инициализация переменной пароля

        if encryption_choice == "1":
            password_choice = input("1. Want to use your password\n2. Generate password\nEnter your choice: ")
            if password_choice == "1":
                password = input("Enter the password to encrypt the archive: ")

                # Входим во вложенный контекстный блок, используя pyzipper для создания ZIP-архива.
                # Устанавливаем метод шифрования AES.
                # Создаем объект zipf, который представляет ZIP-архив для записи.
                with pyzipper.AESZipFile(archive_name, 'w', compression=zipfile.ZIP_DEFLATED,
                                         encryption=pyzipper.WZ_AES) as zipf:
                    # Устанавливаем пароль для архива, преобразуя его в байтовую строку.
                    zipf.setpassword(password.encode())
                    # Записываем файл базы данных в архив с использованием его базового имени в качестве имени файла в
                    # архиве.
                    zipf.write(self.database_name, os.path.basename(self.database_name))
            elif password_choice == "2":
                # Создаем объект класса Data с пустыми данными.
                password_data = Data('', '')

                # Проверяем сложность выбранного пользователем варианта пароля.
                password_choice = password_data.check_password_complexity(password_choice)

                # Генерируем пароль в соответствии с выбранным пользователем вариантом.
                password_data.generate_password(password_choice)

                # Сохраняем сгенерированный пароль.
                password = password_data.password

                # Входим во вложенный контекстный блок, используя pyzipper для создания ZIP-архива.
                # Устанавливаем метод шифрования AES.
                # Создаем объект zipf, который представляет ZIP-архив для записи.
                with pyzipper.AESZipFile(archive_name, 'w', compression=zipfile.ZIP_DEFLATED,
                                         encryption=pyzipper.WZ_AES) as zipf:
                    # Устанавливаем сгенерированный пароль для архива, преобразуя его в байтовую строку.
                    zipf.setpassword(password_data.password.encode())

                    # Записываем файл базы данных в архив с использованием его базового имени в качестве имени файла в
                    # архиве.
                    zipf.write(self.database_name, os.path.basename(self.database_name))
            else:
                print("Invalid choice.")
        elif encryption_choice == "2":
            if self.connection:  # Проверка, если есть соединение с базой данных
                # Входим в контекстный блок, используя zipfile для создания ZIP-архива.
                # Создаем объект zipf, который представляет ZIP-архив для записи.
                with zipfile.ZipFile(archive_name, 'w') as zipf:
                    zipf.write(self.database_name, os.path.basename(self.database_name))
            else:
                print(
                    "There is no connection to the database.")
        else:
            print("Invalid choice.")

        return password  # Возвращаем пароль

    @staticmethod
    def unzip_database(archive_name):
        """
        Метод извлекает архив базы данных SQLite.

        Аргументы:
        - archive_name (str): Имя файла архива.

        Возвращает:
        - details (dict): Словарь с информацией об извлеченной базе данных
          (содержит ключи 'Archive' и 'Password').
        """
        # Входим в контекстный блок, используя pyzipper для открытия ZIP-архива в режиме чтения.
        # Создаем объект zipf, который представляет ZIP-архив для чтения.
        with pyzipper.AESZipFile(archive_name, 'r', compression=zipfile.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as zipf:
            # Проверяем свойство flag_bits класса ZipInfo, чтобы узнать, зашифрован ли файл
            info_list = zipf.infolist()
            # Перебирается infolist() и проверяется, есть ли зашифрованные файлы в zip
            for info in info_list:
                # бит 0x1 — это файл зашифрован
                if info.flag_bits & 0x1:
                    while True:
                        password = getpass.getpass("Enter the password to unpack the archive: ")
                        try:
                            # Устанавливаем пароль для архива, преобразуя его в байтовую строку и извлекаем все файлы
                            zipf.extractall(pwd=password.encode())
                            # Возвращаем словарь с информацией об извлеченной базе данных:
                            # имя архива и пароль.
                            return {
                                "Archive": archive_name,
                                "Password": password
                            }
                        # Если пароль неверный, возникнет исключение RuntimeError.
                        except RuntimeError:
                            print("Incorrect password. Please try again.")
                else:
                    zipf.extractall()  # Извлечение всех файлов из архива
                    # Возвращаем словарь с информацией об извлеченной базе данных:
                    # имя архива и отсутствие пароля.
                    return {
                        "Archive": archive_name,
                        "Password": None
                    }
