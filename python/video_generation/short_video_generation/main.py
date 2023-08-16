from gtts import gTTS
from moviepy.editor import *
import cv2 as cv
import os
from dotenv import load_dotenv


# pip install opencv-python==4.5.5.62
# pip install python-dotenv

# Класс для генерации текста с помощью GPT-3.5
class GPT3Generator:
    def __init__(self):
        pass

    def generate_audio_text(self, video_script=None):
        # Если video_script уже есть, попросим пользователя подтвердить его или ввести новый текст
        if video_script:
            print("Текущий текст для аудио:")
            print(video_script)
            choice = input("Использовать текущий текст? (y/n): ")
            if choice.lower() == "y":
                return video_script

        # Если video_script отсутствует или пользователь решил ввести новый текст
        audio_text = input("Введите текст для аудио: ")
        return audio_text


# Класс для синтеза речи из текста с помощью Google Text-to-Speech
class GoogleTextToSpeech:
    def generate_speech_from_text(self, text, lang="ru"):
        max_text_length = 500  # Вы можете изменить это значение по необходимости
        num_chunks = (len(text) + max_text_length - 1) // max_text_length

        # Генерация речи для каждого части текста
        for i in range(num_chunks):
            start_idx = i * max_text_length
            end_idx = (i + 1) * max_text_length
            chunk = text[start_idx:end_idx]

            tts = gTTS(text=chunk, lang=lang, slow=False)
            tts.save(f"temp_{i}.mp3")

        # Объединение всех аудиофрагментов в один файл
        audio_clips = [AudioFileClip(f"temp_{i}.mp3") for i in range(num_chunks)]
        final_audio = concatenate_audioclips(audio_clips)
        final_audio.write_audiofile("temp.mp3")

        # Удаление временных файлов
        for i in range(num_chunks):
            os.remove(f"temp_{i}.mp3")


# Класс для работы с видео с помощью OpenCV
class VideoEditor:
    def resize_video(self, input_video_filename, output_video_filename):
        cap = cv.VideoCapture(input_video_filename)

        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        size = (width, height)

        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out = cv.VideoWriter(output_video_filename, fourcc, 20.0, size)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv.resize(frame, size)
            out.write(frame)

        cap.release()
        out.release()


# Класс для создания уникального короткого видео на основе текста и аудио
class VideoCreator:
    def create_unique_video(self, topic, text, audio_text, output_video_filename):
        # Генерация речи из текста
        tts = GoogleTextToSpeech()
        tts.generate_speech_from_text(audio_text)

        # Создание текстового файла для добавления на видео
        with open("temp.txt", "w", encoding="utf-8") as f:
            f.write(text)

        # Загрузка аудио файлов
        audio = AudioFileClip("temp.mp3")

        # Добавление текста на видео
        txt_clip = TextClip(text, fontsize=50, color="white", bg_color="green")
        txt_clip = txt_clip.set_position(("center", "bottom"))

        # Set the fps attribute for the txt_clip
        txt_clip = txt_clip.set_duration(audio.duration).set_fps(30)

        video = CompositeVideoClip([txt_clip])

        # Добавление аудио к видео
        video = video.set_audio(audio)

        # Сохранение финального видео
        video.write_videofile(output_video_filename)

        # Очистка временных файлов
        audio.close()
        video.close()
        os.remove("temp.mp3")
        os.remove("temp.txt")


# Класс для меню
class Menu:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        self.gpt3_generator = GPT3Generator()
        self.video_creator = VideoCreator()
        self.video_topic = None
        self.video_script = None
        self.audio_text = None

    def run(self):
        # Запрос темы и скрипта видео
        self.video_topic = input("Введите тему видео: ")
        self.video_script = input("Введите скрипт для видео: ")

        # Запрос текста для аудио
        self.audio_text = self.gpt3_generator.generate_audio_text()

        # Создание уникального видеоролика
        output_filename = "output_video.mp4"
        self.video_creator.create_unique_video(self.video_topic, self.video_script, self.audio_text, output_filename)
        print(f"Уникальный видеоролик создан и сохранен в файл {output_filename}.")


if __name__ == "__main__":
    menu = Menu()
    menu.run()

# import openai
# from gtts import gTTS
# from moviepy.editor import *
# import numpy as np
# import cv2 as cv
# import os
# from dotenv import load_dotenv
#
#
# # pip install opencv-python==4.5.5.62
# # pip install python-dotenv
#
# # Класс для генерации текста с помощью GPT-3.5
# class GPT3Generator:
#     def __init__(self, api_key):
#         self.api_key = api_key
#
#     def generate_text(self, prompt):
#         response = openai.Completion.create(
#             engine="text-davinci-002",
#             prompt=prompt,
#             max_tokens=100,
#             temperature=0.7,
#             stop=None,
#             frequency_penalty=0.0,
#             presence_penalty=0.0,
#             n=1,
#             stop_sequence=None,
#             api_key=self.api_key  # Передаем ключ API в запрос
#         )
#         return response.choices[0].text.strip()
#
#     def generate_audio_text(self, video_script):
#         response = openai.Completion.create(
#             engine="text-davinci-002",
#             prompt=video_script,
#             max_tokens=100,
#             temperature=0.7,
#             stop=None,
#             frequency_penalty=0.0,
#             presence_penalty=0.0,
#             n=1,
#             stop_sequence=None,
#             api_key=self.api_key  # Передаем ключ API в запрос
#         )
#         return response.choices[0].text.strip()
#
#
# # Класс для синтеза речи из текста с помощью Google Text-to-Speech
# class GoogleTextToSpeech:
#     def generate_speech_from_text(self, text, lang="ru"):
#         tts = gTTS(text=text, lang=lang, slow=False)
#         tts.save("temp.mp3")
#
#
# # Класс для работы с видео с помощью OpenCV
# class VideoEditor:
#     def resize_video(self, input_video_filename, output_video_filename):
#         cap = cv.VideoCapture(input_video_filename)
#
#         width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
#         size = (width, height)
#
#         fourcc = cv.VideoWriter_fourcc(*'mp4v')
#         out = cv.VideoWriter(output_video_filename, fourcc, 20.0, size)
#
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#
#             frame = cv.resize(frame, size)
#             out.write(frame)
#
#         cap.release()
#         out.release()
#
#
# # Класс для создания уникального короткого видео на основе текста и аудио
# class VideoCreator:
#     def create_unique_video(self, text, audio_text, output_video_filename):
#         # Генерация речи из текста
#         tts = GoogleTextToSpeech()
#         tts.generate_speech_from_text(audio_text)
#
#         # Создание текстового файла для добавления на видео
#         with open("temp.txt", "w", encoding="utf-8") as f:
#             f.write(text)
#
#         # Загрузка аудио файлов
#         audio = AudioFileClip("temp.mp3")
#
#         # Добавление текста на видео
#
#         # Добавление текста на видео
#         txt_clip = TextClip(text, fontsize=50, color="white", bg_color="black")
#         txt_clip = txt_clip.set_position(("center", "bottom")).set_duration(audio.duration)
#         video = CompositeVideoClip([txt_clip])
#
#         # Добавление аудио к видео
#         video = video.set_audio(audio)
#
#         # Сохранение финального видео
#         video.write_videofile(output_video_filename)
#
#         # Очистка временных файлов
#         audio.close()
#         video.close()
#         os.remove("temp.mp3")
#         os.remove("temp.txt")
#
#
# def main():
#     # Загрузка переменных среды из файла .env
#     load_dotenv()
#
#     # Получение ключа API, токена Telegram бота и идентификатора чата из переменных окружения
#
#     api_key = os.getenv('API_KEY')
#     print(api_key)
#     gpt3_generator = GPT3Generator(api_key)  # Передаем ключ API
#     video_creator = VideoCreator()
#
#     # Генерация текста для создания видео
#     video_topic = "Тема видео"
#     video_script = gpt3_generator.generate_text(
#         f"Создайте скрипт для короткого видеоролика на тему: {video_topic}."
#     )
#
#     # Генерация текста для создания аудио
#     audio_script = gpt3_generator.generate_audio_text(video_script)
#
#     # Генерация уникального видеоролика
#     output_filename = "output_video.mp4"
#     video_creator.create_unique_video(video_script, audio_script, output_filename)
#     print(f"Уникальный видеоролик создан и сохранен в файл {output_filename}.")
#
#
# if __name__ == "__main__":
#     main()

########################################################################################################################
# import openai
# import torch
# import taming.models
# from nuwa_pytorch import VQGanVAE, NUWA
# from vqvae.vqvae import VQVAE
# from taming.models import vqgan
# from taming.models.vqgan import VQModel
# from taming.models.vqgan_config import VQGAN_DEFAULT_CONFIG
#
# class GPT3Generator:
#     def __init__(self, api_key):
#         openai.api_key = api_key
#
#     def generate_text(self, prompt, engine="text-davinci-002", max_tokens=150, temperature=0.7):
#         response = openai.Completion.create(
#             engine=engine,
#             prompt=prompt,
#             max_tokens=max_tokens,
#             temperature=temperature,
#             stop=None,
#             frequency_penalty=0.0,
#             presence_penalty=0.0,
#         )
#         return response.choices[0].text.strip()
#
#
# class VideoCreator:
#     def __init__(self, vae_path, vqgan_config, vqgan_ckpt):
#         self.gpt3_generator = GPT3Generator(api_key="ВАШ_API_КЛЮЧ")
#
#         # Загрузка предварительно обученной модели VQGAN
#         model = taming.models.vqgan.VQModel(**taming.models.vqgan.DEFAULT_CONFIG)
#         model.eval().requires_grad_(False)
#         model.init_from_ckpt(vqgan_ckpt)
#
#         # Создание экземпляра VQGanVAE и загрузка весов с предварительно обученной модели
#         self.vae = VQGanVAE()
#         self.vae.load_state_dict(model.state_dict())
#
#         # Инициализация Nuwa с помощью предварительно обученного VAE
#         self.nuwa = NUWA(vae=self.vae)
#
#     def create_video(self, video_topic, num_frames=30):
#         # Генерируем текст с помощью GPT-3.5 на основе темы видео
#         video_script = self.gpt3_generator.generate_text(
#             f"Создайте сценарий для короткого видеоролика на тему: {video_topic}.")
#
#         # Преобразуем сгенерированный текст в видео с помощью NUWA
#         text = torch.tensor([[self.nuwa.text_encoder.tokenizer.encode(video_script)]])
#         video = self.nuwa.generate(text=text, num_frames=num_frames)
#
#         return video
#
#
# if __name__ == "__main__":
#     # Пути к предварительно обученным моделям VQGAN
#     vqgan_config = 'model.yaml'
#     vqgan_ckpt = 'last.ckpt'
#
#     # Создаем экземпляр VideoCreator
#     video_creator = VideoCreator(vae_path="vqvae/vqvae_560.pt",
#                                  vqgan_config=vqgan_config,
#                                  vqgan_ckpt=vqgan_ckpt)
#
#     # Получаем текстовую подсказку для видео от пользователя
#     video_topic = input("Введите тему видео: ")
#
#     # Генерируем уникальное видео на основе сгенерированного текста
#     output_filename = "output_video.mp4"
#     video = video_creator.create_video(video_topic, num_frames=30)
#
#     if video is not None:
#         # Сохраняем видео в файл
#         with open(output_filename, "wb") as f:
#             f.write(video)
#         print("Видео успешно создано:", output_filename)
#     else:
#         print("Ошибка при создании видео.")


########################################################################################################################
# import openai
# from gtts import gTTS
# from moviepy.editor import *
# import subprocess
# import cv2
# import os
# import lavis


# # Установите ваш ключ API GPT-3.5 здесь
# openai.api_key = "YOUR_OPENAI_API_KEY"
#
#
# # Класс для генерации текста с помощью GPT-3.5
# class GPT3Generator:
#     def generate_text(self, prompt):
#         response = openai.Completion.create(
#             # Этот параметр указывает, какую модель движка GPT-3 использовать для выполнения запроса. Номер 002
#             # относится к конкретной версии движка.
#             engine="text-davinci-002",
#             # Это текстовая строка, которая содержит ваш запрос или начальную часть текста, с которой модель начнет
#             # генерацию продолжения.
#             prompt=prompt,
#             # Этот параметр ограничивает максимальное количество токенов (частей текста) в ответе модели. Например,
#             # если max_tokens=100, то ответ модели будет состоять из не более чем 150 токенов.
#             max_tokens=100,
#             # Параметр температуры контролирует степень случайности и разнообразия ответов модели. Значение 0.7 означает
#             # умеренную температуру, что приводит к разнообразным ответам с сохранением некоторой логичности.
#             temperature=0.7,
#             # Этот параметр позволяет указать текстовую последовательность, которая остановит генерацию текста. Если
#             # stop=None, модель будет генерировать текст до достижения максимального количества токенов или до
#             # завершения предложения.
#             stop=None,
#             # Этот параметр контролирует частоту использования слов в ответах. Значение 0.0 означает, что частота не
#             # регулируется, и модель может повторять слова из запроса.
#             frequency_penalty=0.0,
#             # Этот параметр влияет на вероятность использования разных слов в ответах. Значение 0.0 означает, что все
#             # слова равны и вероятность их использования не регулируется.
#             presence_penalty=0.0,
#             # позволяет указать, сколько различных ответов вы хотите получить от модели. Если n не указан, модель вернет
#             # только один ответ по умолчанию.
#             n=1,
#             # Этот параметр позволяет указать свою собственную последовательность символов, которая остановит генерацию
#             # текста, вместо использования параметра stop, который просто останавливает текст на основе подстроки.
#             stop_sequence=None
#         )
#         return response.choices[0].text.strip()
#
#     def generate_audio_text(self, video_script):
#         response = openai.Completion.create(
#             # Этот параметр указывает, какую модель движка GPT-3 использовать для выполнения запроса. Номер 002
#             # относится к конкретной версии движка.
#             engine="text-davinci-002",
#             # Это текстовая строка, которая содержит ваш запрос или начальную часть текста, с которой модель начнет
#             # генерацию продолжения.
#             prompt=video_script,
#             # Этот параметр ограничивает максимальное количество токенов (частей текста) в ответе модели. Например,
#             # если max_tokens=100, то ответ модели будет состоять из не более чем 150 токенов.
#             max_tokens=100,
#             # Параметр температуры контролирует степень случайности и разнообразия ответов модели. Значение 0.7 означает
#             # умеренную температуру, что приводит к разнообразным ответам с сохранением некоторой логичности.
#             temperature=0.7,
#             # Этот параметр позволяет указать текстовую последовательность, которая остановит генерацию текста. Если
#             # stop=None, модель будет генерировать текст до достижения максимального количества токенов или до
#             # завершения предложения.
#             stop=None,
#             # Этот параметр контролирует частоту использования слов в ответах. Значение 0.0 означает, что частота не
#             # регулируется, и модель может повторять слова из запроса.
#             frequency_penalty=0.0,
#             # Этот параметр влияет на вероятность использования разных слов в ответах. Значение 0.0 означает, что все
#             # слова равны и вероятность их использования не регулируется.
#             presence_penalty=0.0,
#             # позволяет указать, сколько различных ответов вы хотите получить от модели. Если n не указан, модель вернет
#             # только один ответ по умолчанию.
#             n=1,
#             # Этот параметр позволяет указать свою собственную последовательность символов, которая остановит генерацию
#             # текста, вместо использования параметра stop, который просто останавливает текст на основе подстроки.
#             stop_sequence=None
#         )
#         return response.choices[0].text.strip()
#
#
# # Класс для синтеза речи из текста с помощью Google Text-to-Speech
# class GoogleTextToSpeech:
#     def generate_speech_from_text(self, text, lang="uk"):
#         tts = gTTS(text=text, lang=lang, slow=False)
#         tts.save("temp.mp3")
#
#
# # Класс для использования FFmpeg
# class FFmpegProcessor:
#     def combine_audio_and_video(self, input_video_filename, input_audio_filename, output_video_filename):
#         cmd = ["ffmpeg", "-i", input_video_filename, "-i", input_audio_filename, "-c:v", "copy", "-c:a", "aac",
#                "-strict", "experimental", output_video_filename]
#         subprocess.run(cmd)
#
#
# # Класс для управления скриптами After Effects через Python (предполагается, что After Effects установлен на вашем
# # компьютере и его путь прописан в PATH)
# class AfterEffectsController:
#     def run_script(self, ae_script_filename):
#         cmd = ["afterfx", "-r", ae_script_filename]
#         subprocess.run(cmd)
#
#
# # Класс для работы с видео с помощью OpenCV
# class VideoEditor:
#     def resize_video(self, input_video_filename, output_video_filename, width, height):
#         cap = cv2.VideoCapture(input_video_filename)
#         fourcc = cv2.VideoWriter_fourcc(*"XVID")
#         out = cv2.VideoWriter(output_video_filename, fourcc, 20.0, (width, height))
#
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             frame = cv2.resize(frame, (width, height))
#             out.write(frame)
#
#         cap.release()
#         out.release()
#         cv2.destroyAllWindows()
#
#
# # Класс для создания уникального короткого видео на основе текста и аудио
# class VideoCreator:
#     def create_unique_video(self, text, output_video_filename):
#         # Генерация речи из текста
#         tts = GoogleTextToSpeech()
#         tts.generate_speech_from_text(text)
#
#         # Создание текстового файла для добавления на видео
#         with open("temp.txt", "w") as f:
#             f.write(text)
#
#         # Загрузка аудио файлов
#         audio = AudioFileClip("temp.mp3")
#
#         # Добавление текста на видео
#         txt_clip = TextClip(text, fontsize=50, color="white", bg_color="black")
#         txt_clip = txt_clip.set_pos("bottom").set_duration(audio.duration)
#         video = CompositeVideoClip([txt_clip])
#
#         # Добавление аудио к видео
#         video = video.set_audio(audio)
#
#         # Сохранение финального видео
#         video.write_videofile(output_video_filename)
#
#         # Очистка временных файлов
#         audio.close()
#         video.close()
#         os.remove("temp.mp3")
#         os.remove("temp.txt")
#
#
# # Класс для создания аудио файлов на основе текста
# class AudioCreator:
#     def create_audio_file(self, text, output_audio_filename):
#         tts = GoogleTextToSpeech()
#         tts.generate_speech_from_text(text)
#         os.rename("temp.mp3", output_audio_filename)
#
#
# class Menu:
#     def __init__(self):
#         self.gpt3_generator = GPT3Generator()
#         self.video_creator = VideoCreator()
#
#     def show_menu(self):
#         print("Меню:")
#         print("1. Создать уникальный видеоролик")
#         print("2. Завершить работу")
#
#     def handle_user_choice(self, choice):
#         if choice == "1":
#             video_topic = input("Введите тему для видео: ")
#             video_script = self.gpt3_generator.generate_text(
#                 f"Создайте скрипт для короткого видеоролика на тему: {video_topic}."
#             )
#             output_filename = input("Введите имя файла для сохранения видео: ")
#             self.video_creator.create_unique_video(video_script, output_filename)
#             print(f"Уникальный видеоролик создан и сохранен в файл {output_filename}.")
#         elif choice == "2":
#             print("Работа завершена.")
#             exit()
#         else:
#             print("Некорректный выбор. Пожалуйста, введите 1 или 2.")
#
#     def run(self):
#         while True:
#             self.show_menu()
#             choice = input("Выберите действие (введите 1 или 2): ")
#             self.handle_user_choice(choice)
#
#
# def main():
#     menu = Menu()
#     menu.run()
#
#
# if __name__ == "__main__":
#     main()
