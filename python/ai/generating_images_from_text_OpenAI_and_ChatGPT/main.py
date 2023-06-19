# Для того чтобы успешно запустить код, убедитесь, что вы выполнили следующие шаги:
#
# Установите библиотеку OpenAI с помощью команды: pip install openai.
# Установите переменную окружения OPENAI_API_KEY со значением вашего ключа API. Это можно сделать из командной строки
# следующим образом:
# 1) Для Linux/Mac:
# export OPENAI_API_KEY='ваш_ключ_api'
# 2) Для Windows (PowerShell):
# $env:OPENAI_API_KEY='ваш_ключ_api'
# Для Windows (командная строка):
# set OPENAI_API_KEY='ваш_ключ_api'
# Убедитесь, что переменная окружения OPENAI_API_KEY доступна из вашей среды выполнения (например, из вашей IDE). Если
# вы запускаете код из командной строки или скрипта, проверьте, что переменная окружения установлена в текущей сессии.
# После выполнения этих шагов код должен успешно работать и сохранять сгенерированное изображение в формате PNG с
# именем, основанным на введенном описании.

import openai
import os
import json
from base64 import b64decode
from dotenv import load_dotenv

# Загрузка переменных среды из файла .env
load_dotenv()

# Запрашиваем описание изображения, которое будем генерировать
prompt = input("The prompt: ")
# Сохраняем ключ от API - импортируя его воспользовавшись переменной окружения что бы его никому не передавать
openai.api_key = os.getenv('API_KEY')
print(openai.api_key)

# Приступаем к генерации изображения: передаем описание, количество сгенерированных изображений от 1 до 10, размер
# изображения (256х256, 512х512, 1024х1024 pix),
response = openai.Image.create(prompt=prompt, n=1, size='256x256')

with open('data.json', 'w') as file:
    json.dump(response, file, indent=4, ensure_ascii=False)

# Декодируем данные из словаря
image_data = b64decode(response['data'][0]['b64_json'])

# Составляем имя файла
file_name = '_'.join(prompt.split(' '))

# Сохраняем данные в изображение
with open(f'{file_name}.png', 'wb') as file:
    file.write(image_data)
