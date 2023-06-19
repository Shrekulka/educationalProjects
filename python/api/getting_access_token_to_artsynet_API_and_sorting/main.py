import requests
import json
import time
import os
from dotenv import load_dotenv



"""В этой задаче вам необходимо воспользоваться API сайта artsy.net
API проекта Artsy предоставляет информацию о некоторых деятелях искусства, их работах, выставках.
В рамках данной задачи вам понадобятся сведения о деятелях искусства (назовем их, условно, художники).
Вам даны идентификаторы художников в базе Artsy.
Для каждого идентификатора получите информацию о имени художника и годе рождения.
Выведите имена художников в порядке неубывания года рождения. В случае если у художников одинаковый год рождения, 
выведите их имена в лексикографическом порядке.
Работа с API Artsy
Полностью открытое и свободное API предоставляют совсем немногие проекты. В большинстве случаев, для получения доступа к
API необходимо зарегистрироваться в проекте, создать свое приложение, и получить уникальный ключ (или токен), и в 
дальнейшем все запросы к API осуществляются при помощи этого ключа.
Чтобы начать работу с API проекта Artsy, вам необходимо пройти на стартовую страницу документации к API 
https://developers.artsy.net/v2/start и выполнить необходимые шаги, а именно зарегистрироваться, создать приложение, и 
получить пару идентификаторов Client Id и Client Secret. Не публикуйте эти идентификаторы.
После этого необходимо получить токен доступа к API. На стартовой странице документации есть примеры того, как можно 
выполнить запрос и как выглядит ответ сервера. Мы приведем пример запроса на Python.

import requests
import json

client_id = '...'
client_secret = '...'

# инициируем запрос на получение токена
r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                  data={
                      "client_id": client_id,
                      "client_secret": client_secret
                  })

# разбираем ответ сервера
j = json.loads(r.text)

# достаем токен
token = j["token"]

Теперь все готово для получения информации о художниках. На стартовой странице документации есть пример того, как 
осуществляется запрос и как выглядит ответ сервера. Пример запроса на Python.

# создаем заголовок, содержащий наш токен
headers = {"X-Xapp-Token" : token}
# инициируем запрос с заголовком
r = requests.get("https://api.artsy.net/api/artists/4d8b92b34eb68a1b2c0003f4", headers=headers)

# разбираем ответ сервера
j = json.loads(r.text)

Примечание:
В качестве имени художника используется параметр sortable_name в кодировке UTF-8.
Пример входных данных:
4d8b92b34eb68a1b2c0003f4
537def3c139b21353f0006a6
4e2ed576477cc70001006f99
Пример выходных данных:
Abbott Mary
Warhol Andy
Abbas Hamra
Примечание для пользователей Windows
При открытии файла для записи на Windows по умолчанию используется кодировка CP1251, в то время как для записи имен на 
сайте используется кодировка UTF-8, что может привести к ошибке при попытке записать в файл имя с необычными символами. 
Вы можете использовать print, или аргумент encoding функции open.
"""

# Загрузка переменных среды из файла .env
load_dotenv()
########################################################################################################################
# 1) Решение:

# Ваши идентификаторы клиента (поесле регистрации на сайте вписываем свои данные)
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

# инициируем запрос на получение токена
print("Запрос на получение токена...")
r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                  data={
                      "client_id": client_id,
                      "client_secret": client_secret
                  })

# разбираем ответ сервера
j = json.loads(r.text)

# достаем токен
token = j["token"]
# создаем заголовок, содержащий наш токен
headers = {"X-Xapp-Token": token}
# инициируем запрос с заголовком
print("Запрос к API Artsy...")
r = requests.get("https://api.artsy.net/api/artists/4d8b92b34eb68a1b2c0003f4", headers=headers)

# разбираем ответ сервера
j = json.loads(r.text)
res = []  # Создаем пустой список res, в котором будем хранить информацию о художниках

# Открываем файл dataset_24476_4.txt для чтения и файл result.txt для записи с кодировкой UTF-8
with open('artists.txt', 'r') as f, open('result.txt', 'w', encoding='utf-8') as w:
    print("Чтение файла artists.txt и отправка запросов к API Artsy...")
    for i in f:  # Читаем файл dataset_24476_4.txt построчно
        req_str = 'https://api.artsy.net/api/artists/' + i.rstrip()  # Формируем URL для запроса к API Artsy
        print(f"Запрос {i}: {req_str}")
        j = requests.get(req_str, headers=headers).json()  # Отправляем GET-запрос к API и получаем ответ в формате JSON
        res.append(j['birthday'] + j['sortable_name'])  # Добавляем информацию о художнике в список res

    print("Сортировка и запись результатов в файл result.txt...")
    for i in sorted(res):  # Сортируем список res по возрастанию
        w.write(i[4:] + '\n')  # Записываем отсортированные имена художников в файл result.txt (без года рождения)

print("Готово! Результаты записаны в файл result.txt.")
########################################################################################################################
# 2) Решение:

# Ваши идентификаторы клиента (после регистрации на сайте вписываем свои данные)
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

# Инициируем запрос на получение токена
print("Запрос на получение токена...")
response = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                         data={
                             "client_id": client_id,
                             "client_secret": client_secret
                         })

# Разбираем ответ сервера
data = response.json()

# Достаем токен
token = data.get('token')

# Проверяем, удалось ли получить токен
if token is None:
    print("Ошибка при получении токена доступа.")
    exit()

# Создаем заголовок, содержащий наш токен
headers = {"X-Xapp-Token": token}

# Читаем идентификаторы художников из файла
print("Чтение файла artists.txt...")
with open("artists.txt", "r") as file:
    artist_ids = file.read().splitlines()

# Словарь для хранения информации о художниках
artist_info = {}

# Получаем информацию о художниках
print("Получение информации о художниках...")
for i, artist_id in enumerate(artist_ids, start=1):
    print(f"Запрос {i}: https://api.artsy.net/api/artists/{artist_id}")

    # Инициируем запрос с заголовком
    response = requests.get(f"https://api.artsy.net/api/artists/{artist_id}", headers=headers)

    # Разбираем ответ сервера
    data = response.json()

    # Извлекаем имя и год рождения художника
    name = data.get("sortable_name", "")
    birthday = data.get("birthday", "")

    # Добавляем информацию в словарь
    artist_info[artist_id] = {
        "name": name,
        "birthday": birthday
    }

    # Делаем паузу перед отправкой следующего запроса (2 секунды)
    time.sleep(2)

# Сортируем художников по возрастанию года рождения
print("Сортировка художников...")
sorted_artists = sorted(artist_info.values(), key=lambda x: (x["birthday"], x["name"]))

# Выводим имена художников
print("Имена художников:")
for artist in sorted_artists:
    print(artist["name"])
########################################################################################################################
