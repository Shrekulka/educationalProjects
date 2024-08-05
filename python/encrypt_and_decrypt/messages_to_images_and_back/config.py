# messages_to_images_and_back/config.py

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    """
    Класс Settings для хранения конфигурационных данных приложения.

    Атрибуты:
       file_path (str): Путь к изображению, которое будет обрабатываться. Значение по умолчанию - "input_image/1.jpg".
       file_path_out (str): Путь к выходному изображению, куда будет сохранено изображение со скрытым сообщением.
                            Значение по умолчанию - "output_image/stego_20240726_087fdbad23f8b566.jpg".
       output_directory (str): Путь к директории, куда будут сохраняться выходные изображения.
       filename_prefix (str): Префикс для имени файла выходных изображений.
       default_payload (str): Сообщение по умолчанию, которое будет скрыто в изображениях.
       allowed_extensions (List[str]): Список разрешенных расширений файлов изображений.
       secret_key (str): Секретный ключ для шифрования и дешифрования сообщений.
       default_action (str): Действие по умолчанию (может быть "hide" или "extract").
       red_bold (str): Цвет для вывода текста с жирным красным начертанием.
       bright_blue (str): Цвет для вывода текста в ярко-синем цвете.
       reset (str): Цвет для сброса стиля текста в консоли.

    Конфигурация:
       env_file (str): Имя файла, из которого будут считываться переменные окружения.
       env_file_encoding (str): Кодировка файла переменных окружения.
    """
    # Путь к изображению, которое будет обрабатываться.
    file_path: str = "input_image/1.jpg"

    # Путь к выходному изображению, куда будет сохранено изображение со скрытым сообщением.
    file_path_out: str = "output_image/stego_20240726_087fdbad23f8b566.jpg"

    # Путь к директории, куда будут сохраняться выходные изображения
    output_directory: str = "output_image"

    # Префикс для имени файла, который будет использоваться для выходных изображений
    filename_prefix: str = "stego_"

    # Сообщение по умолчанию, которое будет скрыто в изображениях
    default_payload: str = "Беги, за тобой выехали!"

    # Список разрешенных расширений файлов изображений
    allowed_extensions: list[str] = [".jpg", ".jpeg", ".png"]

    # Секретный ключ для шифрования и дешифрования сообщений
    secret_key: str = "pink-bmw"

    # Действие по умолчанию (может быть "hide" или "extract")
    default_action: str = "extract"

    # Цвета для вывода сообщений в консоль
    red_bold: str = "\033[1;31m"     # Красный текст с жирным начертанием
    bright_blue: str = "\033[1;94m"  # Ярко-синий текст
    reset: str = "\033[0m"           # Сброс стиля (возвращает текст к нормальному виду)

    # Конфигурация для работы с переменными окружения
    class Config:
        env_file = ".env"            # Имя файла, из которого будут считываться переменные окружения
        env_file_encoding = "utf-8"  # Кодировка файла переменных окружения


# Создаем экземпляр класса Settings для хранения конфигурационных данных
config: Settings = Settings()