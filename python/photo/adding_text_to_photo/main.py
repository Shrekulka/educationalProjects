from PIL import Image, ImageDraw, ImageFont
import os
import re
import sys


def get_default_font_path():
    """
    Возвращает путь к шрифту по умолчанию в зависимости от операционной системы.

    Возвращает:
    - Путь к шрифту по умолчанию в формате строки.

    Примечание:
    - Для операционной системы Windows используется путь "C:/Windows/Fonts/Arial.ttf".
    - Для операционной системы Linux используется путь "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf".
    - Для операционной системы macOS используется путь "/System/Library/Fonts/Supplemental/Arial.ttf".
    - Если операционная система неизвестна, возвращается None.
    """
    # Определение операционной системы
    is_windows = sys.platform.startswith('win')
    is_linux = sys.platform.startswith('linux')
    is_mac = sys.platform.startswith('darwin')

    # Проверка операционной системы и возврат пути к шрифту по умолчанию
    if is_windows:
        return 'C:/Windows/Fonts/Arial.ttf'
    elif is_linux:
        return '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    elif is_mac:
        return '/System/Library/Fonts/Supplemental/Arial.ttf'
    else:
        # Если операционная система неизвестна, возвращаем путь по умолчанию вручную
        return None


def add_text_to_image(image, text, font_path, font_size, text_color, x, y):
    """
    Добавляет текст на изображение в указанных координатах.

    Аргументы:
    - image: объект изображения (PIL Image)
    - text: текст для добавления
    - font_path: путь к файлу шрифта (.ttf)
    - font_size: размер шрифта
    - text_color: цвет текста (например, 'красный', '#FF0000')
    - x: координата X для расположения текста
    - y: координата Y для расположения текста
    """
    # Создание объекта шрифта с заданным путем и размером
    font = ImageFont.truetype(font_path, font_size)
    # Создание объекта ImageDraw для рисования на изображении
    draw = ImageDraw.Draw(image)
    # Получение ограничивающего прямоугольника для текста
    text_bbox = draw.textbbox((x, y), text, font=font)
    # Добавление текста на изображение с заданными координатами и цветом
    draw.text((x, y), text, font=font, fill=text_color)
    # Вычисление ширины и высоты текста
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    return text_width, text_height  # Возврат ширины и высоты текста


def process_images(folder_path, font_path, font_size, text, text_color, x, y, output_folder_path):
    """
    Обрабатывает все изображения в указанной папке, добавляя текст на каждое изображение и сохраняя их.

    Аргументы:
    - folder_path: путь к папке с изображениями
    - font_path: путь к файлу шрифта (.ttf)
    - font_size: размер шрифта
    - text: текст для добавления
    - text_color: цвет текста (например, 'красный', '#FF0000')
    - x: координата X для расположения текста
    - y: координата Y для расположения текста
    - output_folder_path: путь к папке для сохранения измененных изображений
    """

    # Создание папки для сохранения измененных изображений, если путь не указан
    if not output_folder_path:
        output_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imported_photos")
    os.makedirs(output_folder_path, exist_ok=True)

    # Переменная для хранения количества измененных фотографий
    num_modified = 0

    # Перебор всех файлов в папке
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                # Проверка поддерживаемых форматов изображений
                if not any(filename.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif"]):
                    continue  # Пропустить файлы с неподдерживаемыми форматами

                # Открытие изображения
                image = Image.open(file_path)

                # Проверка правильности указанных координат
                image_width, image_height = image.size
                if x < 0 or x > image_width:
                    continue  # Пропустить изображение
                if y < 0 or y > image_height:
                    continue  # Пропустить изображение

                # Добавление текста на изображение и получение размеров текста
                text_width, text_height = add_text_to_image(image, text, font_path, font_size, text_color, x, y)

                # Сохранение измененного изображения
                output_path = os.path.join(output_folder_path, filename)
                image.save(output_path)

                # Увеличение счетчика измененных фотографий
                num_modified += 1

            except (OSError, Image.UnidentifiedImageError):
                pass  # Пропустить неподдерживаемые файлы или файлы, вызывающие ошибку

    # Вывод количества измененных фотографий
    print(f"Количество измененных фотографий: {num_modified}")


def validate_color(color):
    """
    Проверяет правильность формата цвета.
    Возвращает True, если цвет указан в правильном формате, иначе False.
    """
    # Проверка формата цвета в форме '#RRGGBB' или 'rgb(R, G, B)'
    hex_pattern = r'^#([A-Fa-f0-9]{6})$'
    rgb_pattern = r'^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$'

    if re.match(hex_pattern, color) or re.match(rgb_pattern, color):
        return True
    else:
        return False


# Взаимодействие с пользователем через консоль
if __name__ == '__main__':
    folder_path = input("Введите путь к папке с фотографиями: ")
    font_path = input("Введите путь к файлу шрифта (.ttf),\nили нажмите Enter для использования шрифта по умолчанию: ")
    if not font_path:
        default_font_path = get_default_font_path()

        if os.path.isfile(default_font_path):
            font_path = default_font_path
            print("Шрифт по умолчанию загружен.")
        else:
            print("Шрифт по умолчанию не найден.")
            sys.exit()
    font_size = int(input("Введите размер шрифта: "))
    text = input("Введите текст для добавления на фотографии: ")

    text_color = input("Введите цвет текста (например: '#FF0000' или 'rgb(R, G, B)': 255, 0, 0): ")
    while not validate_color(text_color):
        print("Неправильный формат цвета. Пожалуйста, введите цвет в правильном формате.")
        text_color = input("Введите цвет текста (например: '#FF0000' или 'rgb(R, G, B)': 255, 0, 0): ")

    print("""Координаты для расположения текста вводятся: 
    X от левого края и должна быть в диапазоне от 0 до ширины изображения, 
    Y от верхнего края и должна быть в диапазоне от 0 до высоты изображения.""")
    x = int(input("Введите координату X для расположения текста: "))
    y = int(input("Введите координату Y для расположения текста: "))
    output_folder_path = input("Введите путь к папке для сохранения измененных изображений,\n"
                               "или нажмите Enter для создания папки 'imported_photos' в текущей директории проекта: ")

    process_images(folder_path, font_path, font_size, text, text_color, x, y, output_folder_path)
