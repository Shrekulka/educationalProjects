import pikepdf
from pikepdf import Pdf
from tkinter import Tk, filedialog
from pyfiglet import Figlet
from colorama import init, Fore, Style
import os

# Инициализация colorama
init()


def encrypt_pdf():
    """
    Шифрует выбранный PDF-файл с использованием введенного пользователем пароля.
    """
    root = Tk()
    root.withdraw()

    # Запрос пользователя на выбор PDF-файла для шифрования
    file_path = filedialog.askopenfilename(filetypes=[("PDF Файлы", "*.pdf")])
    if not file_path:
        print(Fore.RED + "Файл не выбран. Завершение." + Style.RESET_ALL)
        return

    # Получить имя файла без пути
    file_name = os.path.basename(file_path)
    # Запрос пользователя на ввод пароля
    password = input("Введите пароль: ")
    if not password:
        print(Fore.RED + "Пароль не может быть пустым. Завершение." + Style.RESET_ALL)
        return

    try:
        # Запрос пользователя на ввод имени файла для сохранения
        encrypted_file_name = input("Введите имя файла для сохранения (без расширения .pdf): ")

        # Запрос пользователя на ввод директории для сохранения файла
        encrypted_file_directory = input("Введите директорию для сохранения файла (оставьте пустым для использования директории по умолчанию): ")

        # Проверка, если директория не указана, использовать директорию по умолчанию
        if not encrypted_file_directory:
            encrypted_file_directory = "data"

        # Объединение пути и имени файла
        encrypted_file_path = os.path.join(encrypted_file_directory, encrypted_file_name + ".pdf")

        with Pdf.new() as pdf:
            original_pdf = Pdf.open(file_path)
            for page in original_pdf.pages:
                pdf.pages.append(page)
            pdf.save(encrypted_file_path, encryption=pikepdf.Encryption(owner=password, user=password))

        print(Fore.GREEN + f"Создан зашифрованный файл: {encrypted_file_path}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "Произошла ошибка при шифровании:", str(e) + Style.RESET_ALL)



def decrypt_pdf():
    """
    Расшифровывает выбранный зашифрованный PDF-файл с использованием введенного пользователем пароля.
    """
    root = Tk()
    root.withdraw()

    # Запрос пользователя на выбор зашифрованного PDF-файла
    file_path = filedialog.askopenfilename(filetypes=[("PDF Файлы", "*.pdf")])
    if not file_path:
        print(Fore.RED + "Файл не выбран. Завершение." + Style.RESET_ALL)
        return

    # Получить имя файла без пути
    file_name = os.path.basename(file_path)
    # Запрос пользователя на ввод пароля
    password = input("Введите пароль для расшифровки: ")
    if not password:
        print(Fore.RED + "Пароль не может быть пустым. Завершение." + Style.RESET_ALL)
        return

    try:
        with Pdf.open(file_path, password=password) as pdf:
            # Запрос пользователя на ввод имени файла для сохранения
            decrypted_file_name = input("Введите имя файла для сохранения (без расширения .pdf): ")

            # Запрос пользователя на ввод директории для сохранения файла
            decrypted_file_directory = input("Введите директорию для сохранения файла (оставьте пустым для использования директории по умолчанию): ")

            # Проверка, если директория не указана, использовать директорию по умолчанию
            if not decrypted_file_directory:
                decrypted_file_directory = "data"

            # Объединение пути и имени файла
            decrypted_file_path = os.path.join(decrypted_file_directory, decrypted_file_name + ".pdf")

            pdf.save(decrypted_file_path)

            print(Fore.GREEN + f"Создан расшифрованный файл: {decrypted_file_path}" + Style.RESET_ALL)
    except pikepdf.PasswordError:
        print(Fore.RED + "Неверный пароль. Завершение." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "Произошла ошибка при расшифровке:", str(e) + Style.RESET_ALL)



def main():
    # Красивый вывод в консоль
    preview_text = Figlet(font='slant')
    print(Fore.CYAN + preview_text.renderText('MENU') + Style.RESET_ALL)
    print(Fore.YELLOW + "1. Зашифровать PDF-файл")
    print("2. Расшифровать зашифрованный PDF-файл")
    choice = input("Введите ваш выбор (1 или 2): ")

    if choice == "1":
        encrypt_pdf()
    elif choice == "2":
        decrypt_pdf()
    else:
        print(Fore.RED + "Неверный выбор. Завершение." + Style.RESET_ALL)


if __name__ == '__main__':
    main()
