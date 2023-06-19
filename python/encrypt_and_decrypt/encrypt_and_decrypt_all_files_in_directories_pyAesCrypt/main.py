import encryption
import decryption


def menu():
    """
    Отображает меню и обрабатывает выбор пользователя.

    """
    print("Меню:")
    print("1. Шифрование файлов в директории")
    print("2. Дешифрование файлов в директории")
    print("3. Выход")

    choice = input("Выберите действие (1-3): ")

    if choice == "1":
        dir = input("Введите путь к директории для шифрования файлов: ")
        password = input("Введите пароль для шифрования: ")
        encryption.walking_by_dirs(dir, password)
        print("Шифрование завершено.")
    elif choice == "2":
        dir = input("Введите путь к директории для дешифрования файлов: ")
        password = input("Введите пароль для дешифрования: ")
        decryption.walking_by_dirs(dir, password)
        print("Дешифрование завершено.")
    elif choice == "3":
        print("Программа завершена.")
        return
    else:
        print("Неверный выбор. Пожалуйста, выберите действие от 1 до 3.")

    menu()


if __name__ == "__main__":
    # Запуск меню
    menu()
