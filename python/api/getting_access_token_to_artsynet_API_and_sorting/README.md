In this task you need to use the artsy.net API
The Artsy API provides information about some artists, their works and exhibitions.
For this task you will need information about artists (let's call them artists).
You are given artist identifiers in the Artsy database.
For each identifier get the artist's name and year of birth.
Output the artist names in the order of non-decreasing year of birth. In case they have the same year of birth, 
display their names in lexicographical order.
Working with the Artsy API
Few projects provide a fully open and free API. In most cases, in order to access the
API is accessed by registering with the project, creating your own application, and obtaining a unique key (or token). 
token to access the API.
To start working with the Artsy API you need to access the starting page of the API documentation 
https://developers.artsy.net/v2/start and perform the necessary steps, namely to register, create an application, and 
get a pair of Client Id and Client Secret IDs. Do not publish these IDs.
After that you need to get the API access token. On the start page of the documentation there are examples of how to 
request and what the server's response looks like. We will give you an example request in Python.

```python
import requests
import json

client_id = '...'.
client_secret = '...'.

# initiate a request to get a token
r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                  data={
                      "client_id": client_id,
                      "client_secret": client_secret
                  })

# parse server response
j = json.loads(r.text)

# get the token
token = j["token"]

# Now we're all set to retrieve artist information. On the start page of the documentation there is an example of how 
# request and what the server's response looks like. Example Python query.

# Create a header that contains our token
headers = {"X-Xapp-Token" : token}
# initiate the request with the header
r = requests.get("https://api.artsy.net/api/artists/4d8b92b34eb68a1b2c0003f4", headers=headers)

# parse server response
j = json.loads(r.text)

```

Note:
The sortable_name parameter in UTF-8 encoding is used as the artist name.
Example input data:
4d8b92b34eb68a1b2c0003f4
537def3c139b21353f0006a6
4e2ed576477cc70001006f99
Example output data:
Abbott Mary
Warhol Andy
Abbas Hamra
Note to Windows Users
The default character set for Windows is CP1251 when opening a writable file, but the site uses UTF-8 for writing names. 
website uses UTF-8 encoding, which may cause an error when trying to write a name in unusual characters to the file. 
You can use print, or the encoding argument of the open function.



Here are full instructions on how to create client_id, client_secret and use .env file:

1) Create a new file called .env in the root directory of your project. This can be done in a text editor 
   or through command line. Make sure the .env file is in the same directory as your project code.
2) Open the .env file in a text editor and add the lines client_id = 'your_client_id',client_secret = 
   'your_client_secret', where replace your_client_id,client_secret with your own data. For example:

```python
client_id = 'abc123xyz'
client_secret = 'abc123xyz'
```

3) Save the .env file.
4) Make sure you have the dotenv package installed. If it is not installed, run the command:

```
pip install python-dotenv
```

5) In your Python code, where you need to use client_id, client_secret, add the following lines to the beginning of the
   file:

```python
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

# Get API_KEY variable value
client_id = os.getenv('abc123xyz')
client_secret = os.getenv('abc123xyz')
```

6) Now the client_id, client_secret variables will contain the value from the client_id, client_secret variables from .env.
   Note that you have to import the dotenv module, load the environment variables from the .env file with 
   load_dotenv(), and then use os.getenv("your_information") to get the value of the client_id, 
   client_secret. Make sure that your code using client_id, client_secret is after loading environment variables 
   environment.

It is important to save the .env file in a safe place and not to publish it in public repositories. The .env file 
contains sensitive data such as client_id and client_secret keys and should not be shared with others.

Creating a .env file is important to keep the .env file out of the Git repository and prevent it from being accidentally 
publication. Here are the complete instructions for creating and adding a .gitignore file:

1) Create a .gitignore file in the root directory of your project. You can use any text editor to 
   to create this file.
2) In the .gitignore file, specify a pattern for excluding files. To exclude the .env file, add the following line to 
   the file .gitignore:

```
.env
```

   This line tells Git not to track or include the .env file in the repository.
3) Save the .gitignore file.
4) Open a terminal or command line and go to the root directory of your project.
5) Initialize the Git repository using the command:

```
git init
```

   This command will create an empty Git repository in the current project directory.
6) Add all project files to the Git index using the command:

```
git add .
```

   This command adds all files in the current directory and its subdirectories to the Git index.
7) Commit changes with a comment to commit them to the repository history:

```
git commit -m "Added .gitignore file"
```

   Replace ".gitignore file added" with your own comment.
8) Git will now ignore the .env file and will not include it in the repository.

Make sure that the .gitignore file excludes sensitive files such as .env, and save it in a safe place. 
Also make sure you don't add the .env file to the Git repository.

Note that if you've already initialized a Git repository and added an .env file, you'll also need to remove it from
repository with git rm --cached .env and then commit the changes.




В этой задаче вам необходимо воспользоваться API сайта artsy.net
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

```python
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

# Теперь все готово для получения информации о художниках. На стартовой странице документации есть пример того, как 
# осуществляется запрос и как выглядит ответ сервера. Пример запроса на Python.

# создаем заголовок, содержащий наш токен
headers = {"X-Xapp-Token" : token}
# инициируем запрос с заголовком
r = requests.get("https://api.artsy.net/api/artists/4d8b92b34eb68a1b2c0003f4", headers=headers)

# разбираем ответ сервера
j = json.loads(r.text)

```

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



Вот полная инструкция по созданию client_id, client_secret и использованию файла .env:

1) Создайте новый файл с названием .env в корневой директории вашего проекта. Это можно сделать в текстовом редакторе 
   или через командную строку. Убедитесь, что файл .env находится в той же директории, где находится ваш код проекта.
2) Откройте файл .env в текстовом редакторе и добавьте строки client_id = 'your_client_id',client_secret = 
   'your_client_secret', где your_client_id, client_secret замените на ваш собственный данные. Например:

```python
client_id = 'abc123xyz'
client_secret = 'abc123xyz'
```

3) Сохраните файл .env.
4) Убедитесь, что у вас установлен пакет dotenv. Если он не установлен, выполните команду:

```
pip install python-dotenv
```

5) В вашем коде Python, где вам нужно использовать client_id, client_secret, добавьте следующие строки в начало файла:

```python
from dotenv import load_dotenv
import os

# Загрузка переменных среды из файла .env
load_dotenv()

# Получение значения переменной API_KEY
client_id = os.getenv('abc123xyz')
client_secret = os.getenv('abc123xyz')
```

6) Теперь переменные client_id, client_secret будут содержать значение из переменных client_id, client_secret из .env.
   Обратите внимание, что вы должны импортировать модуль dotenv, загрузить переменные среды из файла .env с помощью 
   load_dotenv(), а затем использовать os.getenv("your_information"), чтобы получить значение переменных client_id, 
   client_secret. Убедитесь, что ваш код, использующий client_id, client_secret, находится после загрузки переменных 
   среды.

Важно сохранять файл .env в безопасном месте и не публиковать его в публичных репозиториях. Файл .env содержит 
конфиденциальные данные, такие как ключи client_id, client_secret и не должен быть доступны другим людям.

Cоздание файла .gitignore очень важно для исключения файла .env из репозитория Git и предотвращения его случайной 
публикации. Вот полная инструкция по созданию и добавлению файла .gitignore:

1) Создайте файл .gitignore в корневом каталоге вашего проекта. Вы можете использовать любой текстовый редактор для 
   создания этого файла.
2) В файле .gitignore укажите паттерн для исключения файлов. Для исключения файла .env добавьте следующую строку в файл 
   .gitignore:

```
.env
```

   Эта строка указывает Git не отслеживать и не включать в репозиторий файл .env.
3) Сохраните файл .gitignore.
4) Откройте терминал или командную строку и перейдите в корневой каталог вашего проекта.
5) Инициализируйте репозиторий Git с помощью команды:

```
git init
```

   Эта команда создаст пустой репозиторий Git в текущем каталоге проекта.
6) Добавьте все файлы проекта в индекс Git с помощью команды:

```
git add .
```

   Эта команда добавляет все файлы в текущем каталоге и его подкаталогах в индекс Git.
7) Выполните коммит изменений с комментарием, чтобы закрепить их в истории репозитория:

```
git commit -m "Добавлен файл .gitignore"
```

   Замените "Добавлен файл .gitignore" на свой собственный комментарий.
8) Теперь Git будет игнорировать файл .env и не будет его включать в репозиторий.

Убедитесь, что файл .gitignore исключает конфиденциальные файлы, такие как .env, и сохраните его в безопасном месте. 
Убедитесь также, что вы не добавляете файл .env в репозиторий Git.

Обратите внимание, что если вы уже инициализировали репозиторий Git и добавили файл .env, вам также нужно удалить его из
репозитория с помощью команды git rm --cached .env, а затем выполнить коммит изменений.