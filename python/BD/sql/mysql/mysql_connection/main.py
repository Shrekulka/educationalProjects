import pymysql
from config import host, user, password, db_name


def create_table(connection):
    """Создание таблицы users."""

    # Создем таблицу
    with connection.cursor() as cursor:
        # Создаем таблицу со следующими строками
        create_table_query = "CREATE TABLE IF NOT EXISTS `users` (id int AUTO_INCREMENT, " \
                             "name varchar(32), " \
                             "password varchar(32), " \
                             "email varchar(32)," \
                             "PRIMARY KEY (id));"
        # Выполняем запрос на создание таблицы
        cursor.execute(create_table_query)
        print("Таблица успешно создана")


def insert_data(connection):
    """Добавление данных в таблицу users."""

    name = input("Введите имя: ")
    password = input("Введите пароль: ")
    email = input("Введите адрес электронной почты: ")
    # Добавляем данные в таблицу
    with connection.cursor() as cursor:
        insert_query = "INSERT INTO `users` (name, password, email) VALUES (%s, %s, %s);"
        cursor.execute(insert_query, (name, password, email))
        # Для того, что бы наши данные занеслись в таблицу и сохранились нам нужно закоммитить или зафиксировать наш
        # запрос
        connection.commit()
        print("Данные успешно добавлены")


def update_data(connection):
    """Обновление данных в таблице users."""

    user_id = input("Введите идентификатор пользователя: ")
    password = input("Введите новый пароль: ")
    # Запрос на обновление данных
    with connection.cursor() as cursor:
        update_query = "UPDATE `users` SET password = %s WHERE id = %s;"
        cursor.execute(update_query, (password, user_id))
        connection.commit()
        print("Данные успешно обновлены")


def delete_data(connection):
    """Удаление данных из таблицы users."""

    user_id = input("Введите идентификатор пользователя: ")
    # Запрос на удаление данных
    with connection.cursor() as cursor:
        delete_query = "DELETE FROM `users` WHERE id = %s;"
        cursor.execute(delete_query, user_id)
        connection.commit()
        print("Данные успешно удалены")


def drop_table(connection):
    """Удаление таблицы users."""

    confirmation = input("Вы уверены, что хотите удалить таблицу? (yes/no): ")
    if confirmation.lower() == "yes":
        # Запрос на удаление всей таблицы (drop table)
        with connection.cursor() as cursor:
            drop_table_query = "DROP TABLE IF EXISTS `users`;"
            cursor.execute(drop_table_query)
            print("Таблица успешно удалена")
    else:
        print("Удаление таблицы отменено")


def select_all_data(connection):
    """Извлечение всех данных из таблицы users."""
    # Запрос на извлечение всех данных из таблицы
    with connection.cursor() as cursor:
        # * - забираем все
        select_all_rows = "SELECT * FROM `users`;"
        cursor.execute(select_all_rows)
        # Извлекаем из таблицы все строки
        rows = cursor.fetchall()
        for i in rows:
            print(i)
        print("#" * 50)


def main():
    # Создаем объект класса pymysql для подключения к базе
    try:
        connection = pymysql.connect(host=host,
                                     port=3306,
                                     user=user,
                                     password=password,
                                     database=db_name,
                                     cursorclass=pymysql.cursors.DictCursor)
        print("Успешное подключение...")
        print("#" * 50)
        # Выводим меню для пользователя
        while True:
            print("Выберите действие:")
            print("1. Создать таблицу")
            print("2. Добавить данные")
            print("3. Обновить данные")
            print("4. Удалить данные")
            print("5. Удалить таблицу")
            print("6. Извлечь все данные")
            print("0. Выход")

            choice = input("Введите ваш выбор: ")

            if choice == "1":
                create_table(connection)
            elif choice == "2":
                insert_data(connection)
            elif choice == "3":
                update_data(connection)
            elif choice == "4":
                delete_data(connection)
            elif choice == "5":
                drop_table(connection)
            elif choice == "6":
                select_all_data(connection)
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")

        # Закрываем соединение
        connection.close()

    except Exception as ex:
        print("Отказано в подключении...")
    print(ex)


if __name__ == "__main__":
    main()
