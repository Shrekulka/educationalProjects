import pyAesCrypt
import os


# Функция дешифрования файла
def decryption(file, password):
    """
       Дешифрует указанный файл с использованием заданного пароля.

       Аргументы:
       file (str): Путь к файлу, который нужно дешифровать.
       password (str): Пароль для дешифрования файла.

    """
    # Задаем размер буфера
    buffer_size = 512 * 1024

    # Вызываем метод дешифровки
    pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]), password, buffer_size)

    # Выводим на консоль имя зашифрованного файла
    print("[Файл '" + str(os.path.splitext(file)[0]) + "' дешифрован]")

    # Удаляем исходный файл
    os.remove(file)


# Функция сканирования директорий
def walking_by_dirs(dir, password):
    """
        Рекурсивно дешифрует все файлы в указанной директории и ее поддиректориях с использованием заданного пароля.

        Аргументы:
        dir (str): Путь к директории, в которой нужно дешифровать файлы.
        password (str): Пароль для дешифрования файлов.

    """
    # Перебираем все поддиректории в указанной директории
    for name in os.listdir(dir):
        path = os.path.join(dir, name)

        # Если находим файл,то дешифруем его
        if os.path.isfile(path):
            try:
                decryption(path, password)
            except Exception as ex:
                print(ex)
        # Если находим директорию, то повторяем цикл в поисках файлов
        else:
            walking_by_dirs(path, password)
