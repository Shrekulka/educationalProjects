import os
import pytesseract
from PIL import Image


# 1) В терминале - brew install tesseract

# 2) Создайте каталог для хранения языковых данных Tesseract. Выполните следующую команду:
# sudo mkdir -p /usr/local/share/tessdata

# 3) Загрузите файлы данных языковых пакетов Tesseract. Для русского, украинского и английского языков скачайте файл
# с официального репозитория Tesseract на GitHub. Выполните следующую команду:
# sudo curl -o /usr/local/share/tessdata/rus.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/rus.traineddata
# sudo curl -o /usr/local/share/tessdata/ukr.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/ukr.traineddata
# sudo curl -o /usr/local/share/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

# 4) Проверьте, что файлы языковых данных были успешно загружены, выполните команду:
# ls -l /usr/local/share/tessdata

# Опции конфига tesseract:
# https://help.ubuntu.ru/wiki/tesseract

def choose_language():
    """
    Позволяет пользователю выбрать язык для распознавания текста.

    Возвращает выбранный язык в виде строки.
    """
    print("Выберите язык:")
    print("1) Русский")
    print("2) Украинский")
    print("3) Английский")
    language_choice = input("Введите номер выбранного языка: ")

    if language_choice == "1":
        return "rus"
    elif language_choice == "2":
        return "ukr"
    elif language_choice == "3":
        return "eng"
    else:
        print("Неверный выбор языка. Выбран русский язык по умолчанию.")
        return "rus"


def choose_file_option():
    """
    Позволяет пользователю выбрать опцию файла или группы файлов для распознавания.

    Возвращает выбранный вариант в виде числа (1 - один файл, 2 - группа файлов).
    """
    print("Выберите:")
    print("1) Один файл")
    print("2) Группа файлов")
    file_choice = input("Введите номер выбранного варианта: ")

    if file_choice == "1":
        return 1
    elif file_choice == "2":
        return 2
    else:
        print("Неверный выбор. Выбран вариант одного файла по умолчанию.")
        return 1


def choose_save_location():
    """
    Позволяет пользователю ввести путь для сохранения результатов распознавания.

    Возвращает введенный путь в виде строки.
    """

    while True:
        save_location = input("Введите путь для сохранения результатов: ")  # Ввод пути для сохранения результатов
        if os.path.isdir(save_location):  # Проверка, является ли путь действительной папкой
            return save_location  # Возвращаем введенный путь
        elif not save_location:  # Проверка, является ли путь пустым
            print("Путь не может быть пустым. Попробуйте снова.")  # Вывод сообщения об ошибке, если путь пустой
        else:
            try:
                os.makedirs(save_location)  # Попытка создания указанной папки
                return save_location  # Возвращаем введенный путь
            except OSError:
                print("Невозможно создать указанную папку. Попробуйте другой путь.")
                # Вывод сообщения об ошибке, если создание папки невозможно


def choose_config():
    """
    Позволяет пользователю выбрать конфигурацию распознавания текста или ввести свою собственную.

    Возвращает выбранную конфигурацию в виде строки.
    """
    custom_configs = {
        "0": r'--oem 1 --psm 0 - Ориентация и скрипт не определены. Tesseract попытается самостоятельно определить ориентацию текста и скрипт',
        "1": r'--oem 1 --psm 1 - Распознавание страницы с одним блоком текста.',
        "2": r'--oem 1 --psm 2 - Распознавание страницы с одним блоком текста и возможностью распознавания текста в нескольких колонках.',
        "3": r'--oem 1 --psm 3 - Этот режим предполагает, что входное изображение содержит текст, ориентированный по вертикали, без разделения на блоки, и пытается распознать текст как непрерывную последовательность. Это может быть полезно для одиночных столбцов текста.',
        "4": r'--oem 1 --psm 4 - Распознавание страницы с одним блоком текста, содержащим только цифры.',
        "5": r'--oem 1 --psm 5 - Распознавание страницы с одним блоком текста с возможностью распознавания текста в нескольких колонках и с использованием улучшенного распознавания шрифтов в сложных условиях.',
        "6": r'--oem 1 --psm 6 - Этот режим предполагает, что входное изображение содержит текст, разделенный на блоки, и пытается распознать каждый блок независимо. Это наиболее распространенный режим и подходит для большинства случаев.',
        "7": r'--oem 1 --psm 7 - Распознавание страницы с текстом, разделенным на линии, без разделения на блоки.',
        "8": r'--oem 1 --psm 8 - Распознавание страницы с текстом, разделенным на слова.',
        "9": r'--oem 1 --psm 9 - Распознавание страницы с текстом, разделенным на слова с возможностью распознавания текста в нескольких колонках.',
        "10": r'--oem 1 --psm 10 - Распознавание страницы с текстом, разделенным на символы.',
        "11": r'--oem 1 --psm 11 - Распознавание страницы с текстом, разделенным на символы с возможностью распознавания текста в нескольких колонках.',
        "12": r'--oem 1 --psm 12 - Распознавание страницы с текстом, содержащимся в сплошном блоке, с разделением на линии.',
        "13": r'--oem 1 --psm 13 - Этот режим предполагает, что входное изображение содержит текст, разделенный на абзацы, и пытается распознать каждый абзац независимо. Он полезен, когда текст на изображении разделен на отдельные блоки абзацев.',
    }

    print("Выберите конфигурацию распознавания:")
    for key, config in custom_configs.items():
        print(f"{key}) {config}")
    config_choice = input("Введите номер выбранной конфигурации: ")

    custom_config = custom_configs.get(config_choice)

    if not custom_config:
        print("Неверный выбор конфигурации. Выбрана конфигурация по умолчанию.")
        custom_config = r'--oem 1 --psm 13'

    return custom_config


def process_image(img, language, custom_config, save_location):
    """
    Обрабатывает изображение с использованием Tesseract OCR.

    img: Объект изображения PIL.
    language: Выбранный язык для распознавания текста.
    custom_config: Выбранная конфигурация распознавания текста.
    save_location: Путь для сохранения результатов.

    Выводит распознанный текст на экран и сохраняет результаты в файл.
    """

    # Используем Tesseract OCR для распознавания текста на изображении
    text = pytesseract.image_to_string(img, lang=language, config=custom_config)

    # Выводим распознанный текст на экран
    print(text)

    # Получаем имя файла без расширения
    file_name = os.path.splitext(os.path.basename(img.filename))[0]

    # Формируем путь для сохранения файла с результатами
    output_file_path = os.path.join(save_location, f"{file_name}.txt")

    # Сохраняем результаты в файл
    with open(output_file_path, "w") as text_file:
        text_file.write(text)
        print(f"Результат сохранен в файл: {output_file_path}")


def main():
    language = choose_language()  # Выбор языка для распознавания текста
    file_option = choose_file_option()  # Выбор опции файла или группы файлов
    save_location = os.path.join(os.getcwd(), choose_save_location())  # Выбор пути для сохранения результатов
    custom_config = choose_config().split(' - ')[1]  # Выбор конфигурации распознавания текста

    # Если выбрана опция одного файла
    if file_option == 1:
        while True:
            file_path = input("Введите путь к файлу: ")  # Ввод пути к файлу
            if os.path.isfile(file_path):  # Проверка, является ли путь действительным файлом
                img = Image.open(file_path)  # Открываем файл с помощью PIL
                process_image(img, language, custom_config, save_location)  # Обрабатываем изображение
                break
            else:
                print("Указан недопустимый путь. Попробуйте снова.")


    # Если выбрана опция группы файлов
    elif file_option == 2:
        while True:
            file_folder = input("Введите путь к папке с файлами: ")  # Ввод пути к папке с файлами
            if os.path.isdir(file_folder):  # Проверка, является ли путь действительной папкой
                file_names = os.listdir(file_folder)  # Получаем список имен файлов в папке
                for file_name in file_names:
                    img = Image.open(f"{file_folder}/{file_name}")  # Открываем каждый файл из списка
                    process_image(img, language, custom_config, save_location)  # Обрабатываем изображение
                break
            else:
                print("Указан недопустимый путь. Попробуйте снова.")


# Запуск основной программы
if __name__ == "__main__":
    main()

