import os
import time
import json
import requests


def text_to_speech(text="Hello"):
    """
    Преобразует текст в речь и сохраняет аудиофайл.

    Args:
        text (str): Текст для преобразования в речь. По умолчанию - "Hello".
    """

    # Создаем словарь с заголовками
    headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}

    # Адрес API, которому будем отправлять запрос
    url = 'https://api.edenai.run/v2/audio/text_to_speech'

    # Основной словарь с настройками
    payload = {
        'providers': 'lovoai',
        'language': 'ru-RU',
        'option': 'MALE',
        'lovoai': 'ru-RU_Alexei Syomin',
        'text': text
    }

    try:
        # Отправляем POST-запрос на API
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Проверка на ошибки при запросе

        # Получаем результат в формате JSON
        result = response.json()
        unx_time = int(time.time())

        # Получаем URL аудио ресурса из ответа API
        audio_url = result.get('lovoai', {}).get('audio_resource_url')
        if audio_url:
            # Загружаем аудиофайл
            r = requests.get(audio_url)
            r.raise_for_status()  # Проверка на ошибки при загрузке аудио

            # Сохраняем аудиофайл
            with open(f'{unx_time}.wav', 'wb') as file:
                file.write(r.content)

        else:
            print('Не удалось получить URL аудио ресурса.')

    except requests.exceptions.RequestException as e:
        print(f'Произошла ошибка при выполнении запроса: {e}')


def main():
    """
    Точка входа в программу.
    """
    text_to_speech(
        text='Что умеет Python-фрилансер. Учимся собирать информацию в интернете.')


if __name__ == '__main__':
    main()
