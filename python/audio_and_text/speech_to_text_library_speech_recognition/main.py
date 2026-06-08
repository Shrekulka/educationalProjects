import os
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr
from colorama import init, Fore, Style
from pyfiglet import Figlet

# Инициализация модуля colorama для автоматического сброса цвета
init()


def get_quality_choice():
    """
    Получает от пользователя выбор степени качества звука.

    :return: Выбранный пользователем вариант степени качества
    """
    quality_description = """
    Качество звука влияет на четкость и детализацию аудиозаписи.
    Данная программа предоставляет вам выбор следующих вариантов степени качества:
    1) Низкое качество (low): 8000 Гц - подходит для обычных речевых записей.
    2) Обычное качество (normal): 16000 Гц - подходит для большинства аудиозаписей.
    3) Высокое качество (high): 32000 Гц - для высококачественных аудиозаписей.
    """
    print(Fore.CYAN + quality_description.strip())

    while True:
        choice = input(Fore.MAGENTA + "\nВыберите степень качества (введите число от 1 до 3): ")

        if choice in ["1", "2", "3"]:
            return choice
        else:
            print(Fore.RED + "Некорректный выбор!!! Пожалуйста, повторите ввод.")


def get_sample_rate():
    """
    Получает от пользователя желаемое значение sample rate (частота дискретизации).

    :return: Выбранное пользователем значение sample rate
    """
    sample_rate_description = """
    Sample rate (частота дискретизации) определяет количество семплов аудиозаписи в секунду.
    Данная программа предоставляет вам выбор следующих вариантов sample rate:
    1) Низкое качество (low): 8000 Гц - подходит для обычных речевых записей.
    2) Обычное качество (normal): 16000 Гц - подходит для большинства аудиозаписей.
    3) Высокое качество (high): 32000 Гц - для высококачественных аудиозаписей.
    """
    print(Fore.CYAN + sample_rate_description.strip())

    while True:
        choice = input(Fore.MAGENTA + "\nВыберите желаемое значение sample rate (введите число от 1 до 3): ")

        if choice in ["1", "2", "3"]:
            return int(choice) * 8000
        else:
            print(Fore.RED + "Некорректный выбор!!! Пожалуйста, повторите ввод.")


def get_language():
    """
    Получает от пользователя выбор языка ввода.

    :return: Выбранный пользователем язык
    """
    language_description = """
    Данная программа поддерживает распознавание речи на следующих языках:
    1) Английский
    2) Русский
    3) Украинский
    """
    print(Fore.CYAN + language_description.strip())

    while True:
        choice = input(Fore.MAGENTA + "\nВыберите язык ввода (введите число от 1 до 3): ")

        if choice == "1":
            return "en-US"
        elif choice == "2":
            return "ru-RU"
        elif choice == "3":
            return "uk-UA"
        else:
            print(Fore.RED + "Некорректный выбор. Пожалуйста, повторите ввод.")


def record_audio(duration, sample_rate, file_path, language):
    """
       Записывает аудио с помощью микрофона и выполняет преобразование в текст.

       :param duration: Длительность записи в секундах
       :param sample_rate: Частота дискретизации (sample rate)
       :param file_path: Путь для сохранения аудио файла
       :param language: Язык ввода
       """
    # Запись аудио
    print(Fore.CYAN + "\nЗапись аудио началась, говорите ...")

    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Ожидание окончания записи

    # Сохранение аудио в файл
    sf.write(file_path, audio, sample_rate)
    print(Fore.MAGENTA + "\nАудиозапись сохранена в файле:", file_path)

    # Создание объекта Recognizer
    recognizer = sr.Recognizer()

    # Загрузка аудиофайла
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)

    # Распознавание речи
    try:
        text = recognizer.recognize_google(audio_data, language=language)
        print(Fore.CYAN + "\nРаспознанный текст:\n")

        print(Fore.GREEN + text)



    except sr.UnknownValueError:
        print(Fore.RED + "Не удалось распознать речь.")

    except sr.RequestError as e:
        print(Fore.RED + "Ошибка сервиса распознавания речи:", str(e))


def main():
    # Красивый вывод в консоль
    preview_text = Figlet(font='slant')
    print(preview_text.renderText('Speech to Text'))

    print(Fore.GREEN + "Добро пожаловать в программу Speech to Text!")

    print(Fore.YELLOW + "\nСейчас необходимо будет настроить несколько параметров.\n", Fore.MAGENTA + "Начнем:\n",
          sep="\n")

    # Получение выбора степени качества звука
    quality_choice = get_quality_choice()
    print(Fore.YELLOW + "\nВыбранная степень качества звука:", quality_choice, "\n")

    # Получение выбора sample rate
    sample_rate = get_sample_rate()
    print(Fore.YELLOW + "\nВыбранный sample rate:", sample_rate, "\n")

    # Получение выбора языка ввода
    language = get_language()
    print(Fore.YELLOW + "\nВыбранный язык ввода:", language)

    # Создание директории для сохранения аудио и текста
    audio_dir = "audio"
    text_dir = "text"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    if not os.path.exists(text_dir):
        os.makedirs(text_dir)

    # Получение имени файла для сохранения
    file_name = input(Fore.CYAN + "\nВведите имя файла для сохранения (без расширения): ") + ".wav"
    audio_file_path = os.path.join(audio_dir, file_name)
    text_file_path = os.path.join(text_dir, file_name.replace(".wav", ".txt"))

    # Получение длительности записи
    duration = float(input(Fore.MAGENTA + "\nВведите длительность записи (в секундах): "))

    # Запись аудио
    record_audio(duration, sample_rate, audio_file_path, language)

    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=language)

        # Сохранение распознанного текста в текстовый файл
        try:
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(text)
                print(Fore.YELLOW + "\nТекст сохранен в файле:", text_file_path)

        except IOError:
            print(Fore.RED + "Не удалось сохранить текст в файле:", text_file_path)

    except sr.UnknownValueError:
        print(Fore.RED + "Не удалось распознать речь.")

    except sr.RequestError as e:
        print(Fore.RED + "Ошибка сервиса распознавания речи:", str(e))


if __name__ == "__main__":
    main()
