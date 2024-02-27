# Book Bot

## Problem Statement

### What?
Book Bot

### Why?
To enable reading a book directly in the Telegram bot and practice working with inline buttons.

### What should the bot be able to do?
1. Load book pages from storage and send them to the chat as messages with buttons.
2. Save the page where the user stopped reading and load the book from that point.
3. Go to the beginning of the book.

### Additional functionality
1. Save bookmarks - pages of the book that the user wants to save.
2. Edit bookmarks (delete unnecessary ones).

### Interaction Description with the Bot
1. The user sends the /start command to the bot (or starts it by finding it in the search).
2. The bot greets the user, informs that the user can read the book directly in the chat with the bot, and also offers 
   the user to see the list of available commands by sending the /help command.
3. At this stage, the user can perform 5 actions:
    - Send the /help command to the chat.
    - Send the /beginning command to the chat.
    - Send the /continue command to the chat.
    - Send the /bookmarks command to the chat.
    - Send any other message to the chat.
4. The user sends the /help command to the chat:
    - The bot sends the user a list of available commands, informs that it's possible to save book pages as bookmarks,
      and wishes happy reading.
5. The user sends the /beginning command to the chat:
    a) The bot sends the first page of the book to the chat along with 3 inline buttons (back, current page number, and 
       forward).
    b) Accordingly, when interacting with the book message, the user can:
     - Click the "Forward" button, and then the bot will load the next page of the book if the current page is not the 
       last one. The current page number on the button will increase by 1. And if the current page is the last one in 
       the book, nothing will change.
     - Click the button with the current page number, and then the bot will save this page as a bookmark, informing the 
       user about it.
     - Click the "Back" button, and then the bot will load the previous page of the book if the current page is not the 
       first one. The current page number on the button will decrease by 1. And if the current page is the first one, 
       nothing will change.
6. The user sends the /continue command to the chat:
    - The bot sends the page of the book where the user stopped reading during the last interaction with the book 
      message.
    - If the user hasn't started reading the book yet, the bot sends a message with the first page of the book.
7. The user sends the /bookmarks command to the chat:
    a) If the user previously saved bookmarks, the bot sends a list of saved bookmarks to the chat as inline buttons, 
       as well as inline buttons "Edit" and "Cancel".
       1) If the user clicks on a bookmark button, the bot sends a message with the book on the page indicated by the 
          bookmark.
       2) If the user clicks "Cancel", the bot removes the list of bookmarks and sends a message suggesting to continue 
          reading by sending the /continue command.
       3) If the user clicks "Edit", the bot sends the list of saved bookmarks as inline buttons with a mark for 
          deletion, as well as the "Cancel" inline button.
          - If the user clicks on a bookmark marked for deletion, it disappears from the list of editable bookmarks.
          - If the list contains at least one bookmark, and the user clicks "Cancel", the bot removes the message with 
            the list of editable bookmarks and changes it to a message suggesting to continue reading by sending the 
            /continue command.
          - If, after deleting the next bookmark, there are no bookmarks left in the list, the bot informs the user that 
            they have no bookmarks and suggests to continue reading the book by sending the /continue command.
8. The user sends any other message to the chat:
    a) The bot reacts to such a message, for example, by echoing it.

1. ## Helper Function _get_part_text()
    Before sending book pages to users in the chat, it is necessary to format the book text for convenient processing. 
    We will store book pages in a dictionary, where the key will be the page number, and the value will be a string with 
    the text of that page, as shown in the previous step. And before writing the main function that will prepare such a 
    dictionary from the text file, we need to write a helper function _get_part_text(), which will take as input the 
    text from the file, the pointer to the start of the page in the text, and the maximum size of the page to return. 
    And the function should return the text of the page and its size (in characters). At the same time, the resulting 
    page must necessarily end with some punctuation mark, so that the text of the page does not end with a half-word.
    
    The implementation of the _get_part_text() function, which takes three arguments in the following order:
    
    text - a string with the full text from which to get a page no larger than the specified size
    start - the index of the first character in the text from which the page should start (indexing starts from 0)
    page_size - the maximum size of the page to be returned
    The function should return the text of the page (type str) and its resulting size in characters (type int).
    
    The list of punctuation marks that can be the end of the page text consists of the following symbols:
    , - comma
    . - period
    ! - exclamation mark
    : - colon
    ; - semicolon
    ? - question mark

    Note 1. It is guaranteed that the text passed to the function is not empty, and punctuation marks from the list 
            above will definitely be encountered in the text of the page.
    
    Note 2. It is also guaranteed that the starting character will be less than the length of the text passed to the 
            function.
    
    Note 3. If an ellipsis (as well as other combinations of consecutive punctuation marks, such as ?!, ?.., !.., etc.) 
            is encountered in the text - it should either completely fall into the current page, or not fall into the 
            page at all. Such a sequence cannot be split because the next book page will then start with a period, 
            periods, or other punctuation marks, which will look like incorrect text formatting to the user.
    
    Note 4. There is no need to trim invisible characters (newline, space, etc.) to the left of the text. We will do 
            this inside the next function.

    ```bash
    Sample Input 1:
    text = 'One. Two. Three. Four. Five. Reception!'
    print(*_get_part_text(text, 5, 9), sep='\n')
    
    Sample Output 1:
    Two. Three.
    9
    
    Sample Input 2:
    text = 'Yes? Are you sure? Maybe you imagined it?.. Well, alright, come tomorrow, then we'll see what can be done. 
    And no objections! So, tomorrow!'
    print(*_get_part_text(text, 22, 145), sep='\n')
    
    Sample Output 2:
    Maybe you imagined it?.. Well, alright, come tomorrow, then we'll see what can be done. And no objections! So, 
    tomorrow!
    139
    
    Sample Input 3:
    text = '— I've checked everything very carefully, — said the computer, — and I state with all certainty that this is
    the answer. It seems to me, if I may be absolutely honest with you, the whole point is that you yourself didn't know
    what the question was.'
    print(*_get_part_text(text, 54, 70), sep='\n')
    
    Sample Output 3:
    — and I state with all certainty that this is the answer.
    58
    """
2. ## Function prepare_book()
    We have access to the text file of the book named book.txt. We need to write a function prepare_book() that takes 1 
    argument:
    path - a string - the path to the book file.
    
    The function should read the file book.txt and transform it into a dictionary using the _get_part_text() function 
    written in the previous step. The keys in the dictionary will be consecutive page numbers, and the values will be 
    the texts of these pages. So, for example, if the text of the book is as follows:
    
    The vulgarity of her own dream was so noticeable that Tanya understood: she even had to dream and grieve with stamps
    stuffed into her head, and it couldn't be otherwise because a rusty narrow-gauge railway has long been laid through 
    all female heads on the planet, and these thoughts - are not her own hopes at all, but just a rumbling commercial 
    stuff in her brain.
    
    As if she herself did not really think and dream, but in the empty autumn square, a huge panel burned on the wall of
    the house, showing indifferent fat ravens an advertisement for budget cosmetics.

    With a page size of PAGE_SIZE = 100, the book dictionary will look like this:
    
    book = {
    1: 'The vulgarity of her own dream was so noticeable that Tanya understood:',
    2: 'she even had to dream and grieve with stamps stuffed into her head, and it couldn't be otherwise because,',
    3: 'a rusty narrow-gauge railway has long been laid through all female heads on the planet,',
    4: 'and these thoughts - are not her own hopes at all,',
    5: 'but just a rumbling commercial stuff in her brain.',
    6: 'As if she herself did not really think and dream,',
    7: 'but in the empty autumn square, a huge panel burned on the wall of the house,',
    8: 'showing indifferent fat ravens an advertisement for budget cosmetics.'}
    
    Note 1. Do not call the prepare_book() function - just write it. The function should not return anything.
    Note 2. You don't need to create the book dictionary - it already exists, just fill it.
    Note 3. You don't need to insert the code of the _get_part_text() function. Assume that you already have it and can 
            call it by passing the appropriate parameters.
    Note 4. The PAGE_SIZE parameter is already set to 1050, just use it as a variable declared earlier.
    Note 5. Before placing the page text in the dictionary, remove unnecessary characters from the beginning of this 
            text. These could be spaces, line breaks, tabs, etc. Just in case, I remind you about the lstrip() string 
            method. 
    Note 6. The book.txt text file is available at the link. The resulting dictionary for this text is available at the 
            link.
    Note 7. When opening the file, explicitly specify the encoding encoding='utf-8'.

## Project Structure:
```bash
📁 Bookbot                                  # Root directory of the entire project
 │
 ├── .env                                   # File with environment variables (secret data) for bot configuration.
 │
 ├── .env.example                           # File with examples of secrets for GitHub
 │
 ├── .gitignore                             # File informing git which files and directories to ignore
 │
 ├── bot.py                                 # Main executable file - entry point for the bot
 │
 ├── requirements.txt                       # File with project dependencies.
 │
 ├── logger_config.py                       # Logger configuration.
 │
 ├── README.md                              # File with project description.
 │
 ├── 📁 book/                               # Directory with the book file book.txt
 │   └── book.txt                           # Text file of the book
 │
 ├── 📁 config_data/                        # Directory with the bot configuration module.
 │   ├── __init__.py                        # Package initializer file. 
 │   └── config_data.py                     # Module for bot configuration.
 │
 ├── 📁 database/                           # Package for working with the database.
 │   ├── __init__.py                        # Package initializer file.     
 │   └── database.py                        # Module with the database template.
 │
 ├── 📁 filters/                            # Package with custom filters.
 │   ├── __init__.py                        # Package initializer file.      
 │   └── filters.py                         # Module with filters that we will write for specific bot tasks.
 │ 
 ├── 📁 handlers/                           # Package with handlers.
 │   ├── __init__.py                        # Package initializer file.
 │   ├── user_handlers.py                   # Module with user handlers. Main update handlers for the bot.
 │   └── other_handlers.py                  # Module with handlers for other user messages.
 │                                                 
 ├── 📁 keyboards/                          # Package with bot keyboards.
 │   ├── __init__.py                        # Package initializer file.            
 │   ├── bookmarks_kb.py                    # Module with keyboards for working with user bookmarks.
 │   ├── main_menu.py                       # Module for forming the main menu of the bot.
 │   └── pagination_kb.py                   # Module for forming pagination buttons to control the book.     
 │ 
 ├── 📁 lexicon/                            # Directory for storing bot lexicons.      
 │   ├── __init__.py                        # Package initializer file.                      
 │   └── lexicon_ru.py                      # File with a dictionary of command and query mappings to displayed texts.
 │ 
 └── 📁 services/                           # Directory for auxiliary tools.     
     ├── __init__.py                        # Package initializer file.                       
     └── file_handling.py                   # Module for preparing the book for bot processing.      
```
Educational material on Stepik - https://stepik.org/course/120924/syllabus





# Бот-книга

## Постановка задачи

### Что?
Бот-книга

### Чтобы что?
Чтобы можно было читать книгу прямо в телеграм-боте и попрактиковаться в работе с инлайн-кнопками

### Что бот должен уметь?
1. Загружать страницы книги из хранилища и присылать их в чат в виде сообщений с кнопками
2. Сохранять страницу, на которой остановился пользователь и загружать книгу на этом месте
3. Переходить в начало книги

### Дополнительный функционал
1. Сохранять закладки - страницы книги, которые пользователь пожелал сохранить
2. Редактировать закладки (удалять ненужные)

### Описание взаимодействия с ботом
1. Пользователь отправляет команду /start боту (или стартует его, найдя в поиске).
2. Бот приветствует пользователя, сообщает, что пользователь может прочитать книгу прямо в чате с ботом, а также 
   предлагает пользователю посмотреть список доступных команд, отправив команду /help.
3. На этом этапе пользователь может совершить 5 действий:
    - Отправить в чат команду /help
    - Отправить в чат команду /beginning
    - Отправить в чат команду /continue
    - Отправить в чат команду /bookmarks
    - Отправить в чат любое другое сообщение
4. Пользователь отправляет в чат команду /help:
    - Бот присылает пользователю список доступных команд, сообщает о том, что можно сохранять страницы книги в закладки
      и желает приятного чтения.
5. Пользователь отправляет в чат команду /beginning:
    a) Бот отправляет в чат первую страницу книги и 3 инлайн-кнопки (назад, текущий номер страницы и вперед).
    b) Соответственно, при взаимодействии с сообщением-книгой пользователь может:
     - Нажать на кнопку "Вперед" и тогда бот загрузит следующую страницу книги, если текущая страница не последняя. 
       Номер текущей страницы на кнопке увеличится на 1. А если текущая страница последняя в книге, то ничего не 
       изменится.
     - Нажать на кнопку с текущим номером страницы и тогда бот сохранит эту страницу в закладки, сообщив пользователю 
       об этом.
     - Нажать на кнопку "Назад" и тогда бот загрузит предыдущую страницу книги, если текущая страница не первая. Номер 
       текущей страницы на кнопке уменьшится на 1. А если текущая страница первая, то ничего не изменится.
6. Пользователь отправляет в чат команду /continue:
    - Бот отправляет в чат страницу книги, на которой пользователь остановил чтение во время последнего взаимодействия с
      сообщением-книгой.
    - Если пользователь еще не начинал читать книгу - бот отправляет сообщение с первой страницей книги.
7. Пользователь отправляет в чат команду /bookmarks:
    a) Если пользователь сохранял закладки ранее, то бот отправляет в чат список сохраненных закладок в виде 
       инлайн-кнопок, а также инлайн-кнопки "Редактировать" и "Отменить".
       1) Если пользователь нажимает на кнопку с закладкой - бот отправляет сообщение с книгой на той странице, куда 
          указывала закладка
       2) Если пользователь нажимает на кнопку "Отменить", то бот убирает список закладок и отправляет сообщение с 
          предложением продолжить чтение, отправив команду /continue
       3) Если пользователь нажимает на кнопку "Редактировать", то бот отправляет список сохраненных закладок в виде 
          инлайн-кнопок с пометкой на удаление, а также инлайн-кнопку "Отменить"
          - Если пользователь нажимает на закладку с пометкой на удаление - она пропадает из списка редактируемых 
            закладок
          - Если список содержит хотя бы одну закладку и пользователь нажимает "Отменить" - бот убирает сообщение со 
            списком редактируемых закладок и меняет его на сообщение с предложением продолжить чтение, отправив команду 
            /continue
          - Если в списке, после очередного удаления закладки, не остается ни одной закладки - бот сообщает пользователю, 
            что у него нет ни одной закладки и предлагает продолжить чтение книги, отправив команду /continue
8. Пользователь отправляет в чат любое другое сообщение:
    a) Бот как-то реагирует на такое сообщение, например, эхом


1. ## Вспомогательная функция _get_part_text()
    Перед тем, как отправлять пользователям в чат страницы книги, нужно привести текст книги к удобному для работы 
    формату. Мы будем хранить страницы книги в словаре, где ключом будет номер страницы, а значением - строка с текстом 
    этой страницы, как показано на предыдущем шаге. И прежде, чем написать основную функцию, которая подготовит такой 
    словарь из текстового файла, нам потребуется написать вспомогательную функцию _get_part_text(), которая будет 
    получать на вход текст из файла, указатель на начало страницы в тексте и максимальный размер страницы, которую нужно
    вернуть. А возвращать функция должна текст страницы и ее размер (в символах). При этом, получившаяся страница, 
    обязательно должна заканчиваться на какой-нибудь знак препинания, чтобы текст страницы не обрывался на полуслове.
    
    Реализция функции _get_part_text(), которая принимает три аргумента в следующем порядке:
    
    text - строка с полным текстом, из которого нужно получить страницу не больше заданного размера
    start - номер первого символа в тексте, с которого должна начинаться страница (нумерация идет с нуля)
    page_size - максимальный размер страницы, которая должна получиться на выходе
    Функция должна вернуть текст страницы (тип str) и ее получившийся размер в символах (тип int).
    
    Список знаков препинания, которые могут быть окончанием текста страницы, состоит из знаков:
    , - запятая
    . - точка
    ! - восклицательный знак
    : - двоеточие
    ; - точка с запятой
    ? - вопросительный знак

    Примечание 1. Гарантируется, что подаваемый в функцию текст, не пустой, а в тексте страницы обязательно встретятся 
                  знаки препинания из списка выше
    
    Примечание 2. Также гарантируется, что стартовый символ будет меньше, чем длина подаваемого в функцию текста.
    
    Примечание 3. Если в тексте встречается многоточие (а также другие сочетания идущих подряд знаков препинания, типа, 
                  ?!, ?.., !.. и т.п.) - они либо целиком должны попасть в текущую страницу, либо не попасть в страницу 
                  вообще. Нельзя разорвать такую последовательность, потому что следующая страница книги тогда начнется 
                  с точки, точек или других знаков препинания, что для пользователя будет смотреться, как неправильное 
                  форматирование текста.
    
    Примечание 4. Обрезать невидимые символы (перенос строки, пробел и т.п.), получившиеся слева от текста, не надо. Мы 
                  это будем делать внутри следующей функции.
    
    Примечание 5. В тестирующую систему сдайте программу, содержащую только необходимую функцию _get_part_text(), но не 
                  код, вызывающий ее.
    ```bash
    Sample Input 1:
    text = 'Раз. Два. Три. Четыре. Пять. Прием!'
    print(*_get_part_text(text, 5, 9), sep='\n')
   
    Sample Output 1:
    Два. Три.
    9
   
    Sample Input 2:
    text = 'Да? Вы точно уверены? Может быть, вам это показалось?.. Ну, хорошо, приходите завтра, тогда и посмотрим, что
    можно сделать. И никаких возражений! Завтра, значит, завтра!'
    print(*_get_part_text(text, 22, 145), sep='\n')
   
    Sample Output 2:
    Может быть, вам это показалось?.. Ну, хорошо, приходите завтра, тогда и посмотрим, что можно сделать. И никаких 
    возражений! Завтра, значит,
    139
   
    Sample Input 3:
    text = '— Я всё очень тщательно проверил, — сказал компьютер, — и со всей определённостью заявляю, что это и есть 
    ответ. Мне кажется, если уж быть с вами абсолютно честным, то всё дело в том, что вы сами не знали, в чём вопрос.'
    print(*_get_part_text(text, 54, 70), sep='\n')
   
    Sample Output 3:
    — и со всей определённостью заявляю, что это и есть ответ.
    58
    ```
2. ## Функция подготовки книги prepare_book()
    Нам доступен текстовый файл книги book.txt. Нужно написать функцию prepare_book(), которая будет принимать 1 аргумент:
    path - строка - путь к файлу с книгой.
    
    Функция должна будет читать файл book.txt и, с помощью функции _get_part_text(), написанной на предыдущем шаге, 
    преобразовывать его в словарь. Ключами в словаре будут идущие подряд номера страниц, а значениями - тексты этих 
    страниц. То есть, если, например, текст книги будет таким:
    
    Пошлость собственной мечты была так заметна, что Таня понимала: даже мечтать и горевать ей приходится закачанными в 
    голову штампами, и по другому не может быть, потому что через все женские головы на планете давно проложена ржавая 
    узкоколейка, и эти мысли — вовсе не ее собственные надежды, а просто грохочущий у нее в мозгу коммерческий товарняк.
    
    Словно бы на самом деле думала и мечтала не она, а в пустом осеннем сквере горела на стене дома огромная панель, 
    показывая равнодушным жирным воронам рекламу бюджетной косметики.
    При размере страницы PAGE_SIZE = 100, словарь book будет таким:
    
    book = {1: 'Пошлость собственной мечты была так заметна, что Таня понимала:',
            2: 'даже мечтать и горевать ей приходится закачанными в голову штампами, и по-другому не может быть,',
            3: 'потому что через все женские головы на планете давно проложена ржавая узкоколейка,',
            4: 'и эти мысли — вовсе не ее собственные надежды,',
            5: 'а просто грохочущий у нее в мозгу коммерческий товарняк.',
            6: 'Словно бы на самом деле думала и мечтала не она,',
            7: 'а в пустом осеннем сквере горела на стене дома огромная панель,', 
            8: 'показывая равнодушным жирным воронам рекламу бюджетной косметики.'}

    Примечание 1. Функцию prepare_book() вызывать не надо - только написать. Функция не должна ничего возвращать.
    
    Примечание 2. Словарь book создавать не надо - он уже есть, просто заполняйте его.
    
    Примечание 3. Код функции _get_part_text() вставлять не надо. Считайте, что она у вас уже есть и вы можете ее 
                  вызвать, передав ей соответствующие параметры.
    
    Примечание 4. Параметр PAGE_SIZE уже задан, равным 1050, просто используйте его, как переменную, которая объявлена 
                  ранее.
    
    Примечание 5. Перед помещением текста страницы в словарь, удалите лишние символы из начала этого текста. Это мотут 
                  быть пробелы, переводы строк, табуляции и т.п. На всякий случай напоминаю про строковый метод lstrip().
    
    Примечание 6. Текстовый файл book.txt доступен по ссылке. Получающийся словарь по этому тексту доступен по ссылке.
    
    Примечание 7. При открытии файла, явно указывайте кодировку encoding='utf-8'.


## Структура проекта:
```bash
📁 Bookbot                                  # Корневая директория всего проекта
 │
 ├── .env                                   # Файл с переменными окружения (секретными данными) для конфигурации бота.
 │
 ├── .env.example                           # Файл с примерами секретов для GitHub
 │
 ├── .gitignore                             # Файл, сообщающий гиту какие файлы и директории не отслеживать
 │
 ├── bot.py                                 # Основной исполняемый файл - точка входа в бот
 │
 ├── requirements.txt                       # Файл с зависимостями проекта.
 │
 ├── logger_config.py                       # Конфигурация логгера.
 │
 ├── README.md                              # Файл с описанием проекта.
 │
 ├── 📁 book/                               # Директория с файлом книги book.txt
 │   └── book.txt                           # Текстовый файл книги
 │
 ├── 📁 config_data/                        # Директория с модулем конфигурации бота.
 │   ├── __init__.py                        # Файл-инициализатор пакета. 
 │   └── config_data.py                     # Модуль для конфигурации бота.
 │
 ├── 📁 database/                           # Пакет для работы с базой данных.
 │   ├── __init__.py                        # Файл-инициализатор пакета.     
 │   └── database.py                        # Модуль с шаблоном базы данных.
 │
 ├── 📁 filters/                            # Пакет с пользовательскими фильтрами.
 │   ├── __init__.py                        # Файл-инициализатор пакета.      
 │   └── filters.py                         # Модуль с фильтрами, которые мы напишем для конкретных задач бота.
 │ 
 ├── 📁 handlers/                           # Пакет с обработчиками.
 │   ├── __init__.py                        # Файл-инициализатор пакета.
 │   ├── user_handlers.py                   # Модуль с обработчиками пользователя. Основные обработчики обновлений бота.
 │   └── other_handlers.py                  # Модуль с обработчиком остальных сообщений пользователя.
 │                                                 
 ├── 📁 keyboards/                          # Пакет с клавиатурами бота.
 │   ├── __init__.py                        # Файл-инициализатор пакета.            
 │   ├── bookmarks_kb.py                    # Модуль с клавиатурами для работы с закладками пользователя.
 │   ├── main_menu.py                       # Модуль для формирования главного меню бота.
 │   └── pagination_kb.py                   # Модуль для формирования кнопок пагинации для управления книгой.     
 │ 
 ├── 📁 lexicon/                            # Директория для хранения словарей бота.      
 │   ├── __init__.py                        # Файл-инициализатор пакета.                      
 │   └── lexicon_ru.py                      # Файл со словарем соответствий команд и запросов отображаемым текстам.
 │ 
 └── 📁 services/                           # Директория для вспомогательных инструментов.     
     ├── __init__.py                        # Файл-инициализатор пакета.                       
     └── file_handling.py                   # Модуль для подготовки книги для обработки ботом.      
 ```
Учебный материал на Stepik - https://stepik.org/course/120924/syllabus