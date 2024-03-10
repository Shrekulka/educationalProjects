# Editing Messages with Media Content

In the Telegram Bot API, there is a method called edit_message_media that allows you to modify most types of media 
content in a previously sent message.

## Types of media that can be edited using edit_message_media:
- Photo (photo) - InputMediaPhoto.
- Audio (audio) - InputMediaAudio.
- Documents (document) - InputMediaDocument.
- Video (video) - InputMediaVideo.
- Animation (animation) - InputMediaAnimation.

To edit, a new InputMedia object of the corresponding type with updated media content is passed.

For example, to change a photo in a message:
```bash
await bot.edit_message_media(
    chat_id=chat_id,
    message_id=message_id,
    media=InputMediaPhoto(media='new_photo.jpg'))
```
Additionally, you can update the caption and reply keyboard for the edited media message.

## Types of media that CANNOT be edited using edit_message_media:
- Voice messages (voice) - InputMediaVoice.
- Video messages (video_note) - InputMediaVideoNote.
- Stickers (sticker).

For these three types, you can only change the caption and reply keyboard, but not the media content itself. Another 
option is to delete the old content and send a new message with the desired data type.

Example of changing the caption for a voice message:
```bash
await bot.edit_message_caption(
    chat_id=chat_id,
    message_id=message_id,
    caption="New caption for the voice message")
```

If you try to change the actual voice/video message or sticker using edit_message_media, the bot will receive a 
TelegramBadRequest error.

Thus, the edit_message_media method allows easy updating of most types of media content, but has limitations for 
specific types that need to be considered when developing bots.

When editing text, we simply compared the old and new text for a complete match to avoid TelegramBadRequest exceptions,
as Telegram recognizes when there is no change and responds accordingly to the aiogram request.

How do we differentiate between photos if they have different file_ids all the time? By looking at the update with a 
photo, or any media update, you can see that the update not only has a file_id but also a file_unique_id. Media objects
are distinguished in Telegram by this unique id because it remains unchanged during object forwarding.

Why then do we specify file_id as the media parameter instead of file_unique_id? Using file_unique_id would prevent 
Telegram from changing the file_id. Unfortunately, specifying media=file_unique_id results in an error. Resending an 
object previously sent by us can only be done by specifying its file_id. However, objects can be distinguished from each
other by file_unique_id.

# Instructions for understanding how to use the code:
1. Start the Telegram bot and send two different files of the same data type (text, photo, video, audio, document, 
   animation, voice message) to the chat. For some examples, you need to send two different files of the same data type
   (the data type that changes and the data type it changes to). For example: 
  a) for mode = 2.1(2) - you need to send two different photos to the chat; 
  b) for mode = 6.1(2) - you need to send two different documents and two different videos to the chat.
2. Copy the file_id in response to your sent messages (for example, for photos and videos) and paste them into the 
   corresponding fields in the file editing_messages_of_different_types/lexicon/lexicon.py. This is necessary to 
   demonstrate the code operation. For example: 
  a) for mode = 3.1(2) - you need to send two different videos to the 
    chat. After sending a video to the chat, you will receive a response:
    ```bash
    Here's your video,
    file_id is:
    BAACAgIAAxkBAAIKJGXq7oPTxl68v1mXd6gpQM5DqpOxAAJ5QgAC329YSwGUIGrmTFQgNAQ
    file_unique_id is:
    AgADeUIAAt9vWEs
    ```
    Copy the file_id key value 'BAACAgIAAxkBAAIKJGXq7oPTxl68v1mXd6gpQM5DqpOxAAJ5QgAC329YSwGUIGrmTFQgNAQ' to the 
    video_id1 field in the LEXICON dictionary in the file located in the project at /lexicon/lexicon.py. Do the same for
    the second file and copy its file_id to video_id2. b) for mode = 6.1(2) - you need to send two different documents 
    and two different videos to the chat. After sending a document to the chat, you will receive a response:
    ```bash
    Here's your document,
    file_id is: 
    BQACAgIAAxkBAAIJ4WXpshECZEKbLppJXsfk-XThZ2KzAAJTRwAC329QSyriMv2jC0ZvNAQ
    file_unique_id is: 
    AgADU0cAAt9vUEs
    ```
    Copy the file_id key value 'BQACAgIAAxkBAAIJ4WXpshECZEKbLppJXsfk-XThZ2KzAAJTRwAC329QSyriMv2jC0ZvNAQ' to the 
    document_id1 field in the LEXICON dictionary in the file located in the project at /lexicon/lexicon.py. Do the same
    for the second file and copy its file_id to document_id2.
3. In the file editing_messages_of_different_types/handlers/user_handlers.py, find the variable mode and set its value
   depending on the functionality you want to test. Comments next to each mode value explain what the bot will do in that
   mode.
4. In the content_data directory, there are two samples of each type for uploading.

# Summary:

## There are three main ways to replace old messages with new ones when interacting with users:
- By sending new messages without deleting the old ones.
- By deleting the old message before sending the new one.
- By editing the old message.

#### All three methods are used in practice, but the last one does not always work.

### Editing messages will work in cases:
  a) When you need to edit a text message with a text message (Telegram Bot API method - editMessageText). 
  b) When you need to edit a message with media content with a message with media content (Telegram Bot API method - 
     editMessageMedia). Currently, this includes messages with media content types: 
    - Audio. 
    - Video. 
    - Document. 
    - Animation. 
    - Photo. 
  c) When you need to edit only the inline keyboard (Telegram Bot API method - editMessageReplyMarkup). 
  d) When you need to edit the caption of the message (Telegram Bot API method - editMessageCaption). 
  e) When editing, if the new message matches the old one completely, a TelegramBadRequest exception occurs: Telegram 
     server says Bad Request: there is no media in the message to edit.

#### If, during development, there is an understanding that such an exception may occur, there are three main ways:
- Compare the new message with the old one before sending and do not send the new one if they match.
- Catch the TelegramBadRequest exception using a try/except construct.
- Ensure the new message is changed guaranteed.

## Project Structure:
```bash
📁 editing_messages_of_different_types      # Root directory of the entire project.
 │
 ├── .env                                   # File with environment variables (secret data) for configuring the bot.
 │
 ├── .env.example                           # File with examples of secrets for GitHub.
 │
 ├── .gitignore                             # File that tells Git which files and directories not to track.
 │
 ├── bot.py                                 # Main executable file - entry point to the bot.
 │
 ├── requirements.txt                       # File with project dependencies.
 │
 ├── logger_config.py                       # Logger configuration.
 │
 ├── README.md                              # File with project description.
 │
 ├── 📁 config_data/                        # Directory with the bot configuration module.
 │   ├── __init__.py                        # Package initializer file. 
 │   └── config_data.py                     # Module for bot configuration.
 │
 ├── 📁 content_data/                       # Directory with content for loading into handlers.
 │   └── ...                                # Content for loading into handlers.
 │
 ├── 📁 handlers/                           # Package with handlers.
 │   ├── __init__.py                        # Package initializer file.
 │   └── user_handlers.py                   # Module with user handlers. Main update handlers for the bot.
 │                                              
 ├── 📁 keyboards/                          # Directory for storing keyboards sent to the user.
 │   ├── __init__.py                        # Package initializer file.                      
 │   └── keyboard.py                        # Module with keyboards.
 │                                                 
 └──📁 lexicon/                             # Directory for storing bot lexicons.      
     ├── __init__.py                        # Package initializer file.                      
     └── lexicon.py                         # File with dictionary mapping commands and requests to displayed texts.
```
Educational material on Stepik - https://stepik.org/course/120924/syllabus





# Редактирование сообщений с медиа-контентом. 

В Telegram Bot API есть метод *edit_message_media*, который позволяет изменять большинство типов загружаемых медиа в 
ранее отправленном сообщении.

## Типы медиа, которые можно отредактировать с помощью edit_message_media:
- Фото (photo) - InputMediaPhoto.
- Аудио (audio) - InputMediaAudio.
- Документы (document) - InputMediaDocument.
- Видео (video) - InputMediaVideo.
- Анимации (animation) - InputMediaAnimation.
- 
Для редактирования передается новый объект InputMedia соответствующего типа с обновленным медиа-контентом.

Например, для изменения фото в сообщении:
```bash
await bot.edit_message_media(
    chat_id=chat_id,
    message_id=message_id,
    media=InputMediaPhoto(media='новое_фото.jpg'))
```
Также можно дополнительно обновить описание (caption) и клавиатуру (reply_markup) для редактируемого медиа-сообщения.

## Типы медиа, которые НЕЛЬЗЯ отредактировать с помощью edit_message_media:
- Голосовые сообщения (voice) - InputMediaVoice.
- Видеосообщения (video_note) - InputMediaVideoNote.
- Стикеры (sticker)

Для этих трех типов можно только изменить описание (caption) и клавиатуру (reply_markup), но не сам медиа-контент. Или 
вариант с удалением старого и отправкой нового сообщения с выбранным типом данных.

Пример изменения описания для голосового сообщения:
```bash
await bot.edit_message_caption(
    chat_id=chat_id,
    message_id=message_id,
    caption="Новое описание для голосового")
```
Если попытаться изменить сами голосовое/видеосообщение или стикер с помощью edit_message_media, бот получит ошибку 
TelegramBadRequest.

Таким образом, метод *edit_message_media* позволяет легко обновлять большинство типов медиа-контента, но имеет 
ограничения для нескольких специфических типов, которые нужно учитывать при разработке ботов.

Когда мы редактировали текст - мы просто сравнивали на полное совпадение старый и новый текст, чтобы избежать 
исключения TelegramBadRequest, потому что, как мы уже неоднократно убеждались, такое исключение возникает, когда новое 
сообщение полностью повторяет старое. Телеграм понимает, что менять нечего и соответствующим образом отвечает на запрос
от aiogram. 
Почему же в примере с фото мы просто не проверяем на соответствие id старого фото новому? Если не совпадают - берем одно
фото, если совпадают - берем другое. Почему не так? Дело в том, что file_id меняется с каждым новым апдейтом. То есть,
мы отправляем фото в чат по одному file_id, а апдейт приходит уже с другим file_id. file_id зависит от чата, в котором 
такой файл был получен, но еще он зависит от времени отправки. Ну, вот, так это устроено.

А как тогда различать фото между собой, если у них все время разный file_id? Если посмотреть на апдейт с фото, да и на 
самом деле, на любой апдейт с медиа, можно увидеть, что у апдейта есть не только поле file_id, но и *file_unique_id*. 
Вот по этому уникальному id медиа-объекты и различаются в Telegram, потому что он остается неизменным при пересылках 
объекта.
Почему же тогда мы, в качестве параметра media, указываем file_id, а не file_unique_id? Ведь тогда можно будет избежать 
того, что телеграм меняет file_id. К сожалению, нет. Указав media=file_unique_id мы получим ошибку. Это, увы, не 
работает. Отправить объект еще раз из уже отправленных нами ранее, можно только указав его file_id. А, вот, отличить 
объекты друг от друга можно по file_unique_id.

# Инструкция для понимания, как пользоваться кодом:
1. Запустите телеграм-бота и отправьте в чат два разных файла одного и того же типа данных (текст, фото, видео, аудио, 
   документ, анимация, голосовое сообщение). Для некоторых примеров надо отправить по два разных файла одного и того же 
   типа данных (тип данных который меняется и тип данных на который меняется). 
   Например: 
  a) для mode = 2.1(2) - нужно отправить в чат два разных фото;
  b) для mode = 6.1(2) - нужно отправить в чат два разных документа и два разных видео.
2. Скопируйте file_id в ответе на ваши отправленные сообщения (например, для фото и видео) и вставьте их в 
   соответствующие поля в файле editing_messages_of_different_types/lexicon/lexicon.py. Это необходимо для демонстрации 
   работы кода.
   Например: 
  a) для mode = 3.1(2) - нужно отправить в чат два разных видео. Отправив видео в чате нам возратится ответ:
   ```bash
   Here's your video,
   file_id is:
   BAACAgIAAxkBAAIKJGXq7oPTxl68v1mXd6gpQM5DqpOxAAJ5QgAC329YSwGUIGrmTFQgNAQ
   file_unique_id is:
   AgADeUIAAt9vWEs
   ```
   копируем в словарь LEXICON в поле video_id1 значение ключа file_id - 'BAACAgIAAxkBAAIKJGXq7oPTxl68v1mXd6gpQM5DqpOxAA
   J5QgAC329YSwGUIGrmTFQgNAQ' в файл расположенный в проекте по пути /lexicon/lexicon.py. Tоже самое проделываем со 
   вторым файлом и копируем его file_id в video_id2
  b) для mode = 6.1(2) - нужно отправить в чат два разных документа и два разных видео. 
   Отправив документ в чате нам возратится ответ:
   ```bash
   Here's your document,
   file_id is: 
   BQACAgIAAxkBAAIJ4WXpshECZEKbLppJXsfk-XThZ2KzAAJTRwAC329QSyriMv2jC0ZvNAQ
   file_unique_id is: 
   AgADU0cAAt9vUEs
   ```
   копируем в словарь LEXICON в поле document_id1 значение ключа file_id - BQACAgIAAxkBAAIJ4WXpshECZEKbLppJXsfk-XThZ2Kz
   AAJTRwAC329QSyriMv2jC0ZvNAQ в файл расположенный в проекте по пути /lexicon/lexicon.py. Tоже самое проделываем со 
   вторым файлом и копируем его file_id в document_id2.

   Отправив видео в чате нам возратится ответ:
   ```bash
   Here's your video,
   file_id is:
   BAACAgIAAxkBAAIKJGXq7oPTxl68v1mXd6gpQM5DqpOxAAJ5QgAC329YSwGUIGrmTFQgNAQ
   file_unique_id is:
   AgADeUIAAt9vWEs
   ```
   копируем в словарь LEXICON в поле video_id1 значение ключа file_id -    BAACAgIAAxkBAAIKJGXq7oPTxl68v1mXd6gpQM5DqpOx
   AAJ5QgAC329YSwGUIGrmTFQgNAQ в файл расположенный в проекте по пути /lexicon/lexicon.py. Tоже самое проделываем со 
   вторым файлом и копируем его file_id в video_id2.

3. В файле editing_messages_of_different_types/handlers/user_handlers.py найдите переменную mode и установите ее 
   значение в зависимости от того, какой функционал вы хотите протестировать. Комментарии рядом с каждым значением mode 
   поясняют, что будет делать бот в этом режиме.

4. По директории content_data находятся по два образца каждого типа для загрузки.

# Итоги:

## Есть три основных способа заменять старые сообщения новыми при взаимодействии бота с пользователем:

- Через отправку новых сообщений без удаления старых.
- Через удаление старого сообщения перед отправкой нового.
- Через редактирование старого сообщения.

#### Все три способа используются на практике, однако, последний работает не всегда.

### Редактирование сообщений сработает в случаях:
a) Когда нужно отредактировать текстовое сообщение текстовым (метод Telegram Bot API - editMessageText).
b) Когда нужно отредактировать сообщение с медиа-контентом сообщением с медиа-контентом (метод Telegram Bot API - 
  editMessageMedia). На текущий момент это сообщения с медиа-контентом типов:
    - Audio.
    - Video.
    - Document.
    - Animation.
    - Photo.
c) Когда нужно отредактировать только инлайн-клавиатуру (метод Telegram Bot API - editMessageReplyMarkup).
d) Когда нужно отредактировать подпись (caption) к сообщению (метод Telegram Bot API - editMessageCaption).
e) При редактировании, если новое сообщение полностью совпадает со старым, возникает исключение TelegramBadRequest: 
   Telegram server says Bad Request: there is no media in the message to edit.

#### Если, в процессе разработки, возникает понимание, что может возникать такое исключение, то есть три основных пути:
- Сравнивать перед отправкой новое сообщение со старым и не отправлять новое при их совпадении
- Перехватывать исключение TelegramBadRequest с помощью конструкции try/except
- Гарантированно изменять новое сообщение



## Структура проекта:
```bash
📁 editing_messages_of_different_types      # Корневая директория всего проекта.
 │
 ├── .env                                   # Файл с переменными окружения (секретными данными) для конфигурации бота.
 │
 ├── .env.example                           # Файл с примерами секретов для GitHub.
 │
 ├── .gitignore                             # Файл, сообщающий гиту какие файлы и директории не отслеживать.
 │
 ├── bot.py                                 # Основной исполняемый файл - точка входа в бот.
 │
 ├── requirements.txt                       # Файл с зависимостями проекта.
 │
 ├── logger_config.py                       # Конфигурация логгера.
 │
 ├── README.md                              # Файл с описанием проекта.
 │
 ├── 📁 config_data/                        # Директория с модулем конфигурации бота.
 │   ├── __init__.py                        # Файл-инициализатор пакета. 
 │   └── config_data.py                     # Модуль для конфигурации бота.
 │
 ├── 📁 conеtent_data/                      # Директория с контентом для загрузки в хендлеры.
 │   └── ...                                # Контентом для загрузки в хендлеры.
 │
 ├── 📁 handlers/                           # Пакет с обработчиками.
 │   ├── __init__.py                        # Файл-инициализатор пакета.
 │   └── user_handlers.py                   # Модуль с обработчиками пользователя. Основные обработчики обновлений бота.
 │                                              
 ├── 📁 keyboards/                          # Директория для хранения клавиатур отправляемые пользователю.
 │   ├── __init__.py                        # Файл-инициализатор пакета.                      
 │   └── keyboard.py                        # Модуль с клавиатурами.
 │                                                 
 └──📁 lexicon/                            # Директория для хранения словарей бота.      
     ├── __init__.py                       # Файл-инициализатор пакета.                      
     └── lexicon.py                        # Файл со словарем соответствий команд и запросов отображаемым текстам.
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus