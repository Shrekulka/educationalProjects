"""
Решение данного кода позволяет создать комбинированное аудио, сочетая заданный фрагмент музыки с текстом.
Пользователю предлагается выбрать источник текста: либо из файла, либо ввести текст с клавиатуры.
Комбинированное аудио сохраняется в указанном месте и может быть проиграно.
"""

from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup

import subprocess


class AudioCombiner:
    def __init__(self, music_path):
        """
        Инициализация объекта AudioCombiner.

        Параметры:
        - music_path (str): Путь к файлу с музыкой.
        """
        self.music = AudioSegment.from_file(music_path, format='mp3')  # Загрузка музыкального фрагмента
        self.text_audio = None
        self.combined_audio = None

    def add_text_from_file(self, text_file):
        """
        Добавление текста из файла в комбинированное аудио.

        Параметры:
        - text_file (str): Путь к файлу с текстом.
        """
        try:
            with open(text_file, 'r') as file:
                text = file.read()  # Чтение текста из файла
                self.add_text(text)
        except IOError:
            print("Ошибка чтения файла с текстом.")

    def add_text(self, text):
        """
        Добавление текста в комбинированное аудио.

        Параметры:
        - text (str): Текст для добавления.
        """
        language = 'ru'
        tts = gTTS(text=text, lang=language, slow=False)  # Создание аудио из текста
        tts.save('audio_text.mp3')
        self.text_audio = AudioSegment.from_file('audio_text.mp3', format='mp3')

    def combine_audio(self):
        """
        Объединение музыки и текстового аудио.
        """
        if self.text_audio is None:
            print("Аудио с текстом не было добавлено.")
            return

        self.text_audio = self.text_audio.apply_gain(5)  # Увеличение громкости текстового аудио
        self.text_audio = speedup(self.text_audio, playback_speed=1.2)  # Ускорение воспроизведения текстового аудио

        while len(self.text_audio) < len(self.music):  # Повторение текстового аудио, чтобы его длина совпала с музыкой
            self.text_audio += self.text_audio

        self.text_audio = self.text_audio[:len(self.music)]  # Обрезание текстового аудио до длины музыки
        self.combined_audio = self.music.overlay(self.text_audio)  # Объединение музыки и текстового аудио

    def save_combined_audio(self, save_path):
        """
        Сохранение комбинированного аудио.

        Параметры:
        - save_path (str): Путь и имя файла для сохранения комбинированного аудио.
        """
        if self.combined_audio is None:
            print("Комбинированное аудио не было создано.")
            return

        self.combined_audio.export(save_path, format='mp3')  # Экспорт комбинированного аудио в файл
        print("Комбинированное аудио сохранено в", save_path)

    def play_combined_audio(self):
        """
        Проигрывание комбинированного аудио.
        """
        if self.combined_audio is None:
            print("Комбинированное аудио не было создано.")
            return

        try:
            subprocess.call(["afplay", "combined_audio.mp3"])  # Проигрывание комбинированного аудио
        except KeyboardInterrupt:
            print("\nПроигрывание комбинированного аудио прервано.")


def main():
    music_path = input("Введите путь к файлу с музыкой: ")
    audio_combiner = AudioCombiner(music_path)

    print("Выберите источник текста:")
    print("1. Файл")
    print("2. Ввод с клавиатуры")
    source_choice = input("Ваш выбор: ")

    if source_choice == '1':
        text_file = input("Введите путь к файлу с текстом: ")
        audio_combiner.add_text_from_file(text_file)
    elif source_choice == '2':
        text = input("Введите текст: ")
        audio_combiner.add_text(text)

    save_path = input("Введите путь и имя файла для сохранения комбинированного аудио (в формате 'путь/имя.mp3'): ")
    audio_combiner.combine_audio()
    audio_combiner.save_combined_audio(save_path)

    play_choice = input("Хотите проиграть комбинированное аудио? (y/n): ")
    if play_choice.lower() == 'y':
        audio_combiner.play_combined_audio()


if __name__ == '__main__':
    main()
