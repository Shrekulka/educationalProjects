This code is a simple programme for creating and storing logins and passwords. The programme uses a SQLite database
SQLite database to store the data.

The main classes are:

1. BD is a class representing the SQLite database. It contains methods for creating the database, inserting data, 
   update data, delete data and retrieve data from the database.
2. Data - a base class for different types of data (websites, files, applications, notes, games). It contains methods 
   for saving data to the database, generating a password and checking password complexity.
3. WebsiteData - a class for website data. It is inherited from Data.
4. FileData - a class for data about a file. Inherited from Data.
5. ApplicationData - class for application data. Inherited from Data.
6. NoteData - class for notes. Inherited from Data.
7. GameData - class for game data. Inherited from Data.
8. Menu - class representing the programme menu. It contains methods for displaying menus, performing user actions and 
   database management.

The following actions can be performed in the programme:

1) Create a new database.
2) Load an existing database.
3) Generate and save a new password.
4) Display all saved passwords.
5) Create a database archive.
6) Extract the database from the archive.
7) Exit the programme.

To run the programme, call the main() function.
File - with_password.zip - archive password: yEDhh=KS!-c&r.IhbuJ&T%Q]
File - no_password.zip - no password





Данный код представляет собой простую программу для создания и хранения логинов и паролей. В программе используется база
данных SQLite для хранения данных.

Основные классы:

1. BD - класс, представляющий базу данных SQLite. Он содержит методы для создания базы данных, вставки данных, 
   обновления данных, удаления данных и получения данных из базы.
2. Data - базовый класс для различных типов данных (веб-сайты, файлы, приложения, заметки, игры). Он содержит методы для
   сохранения данных в базу данных, генерации пароля и проверки сложности пароля.
3. WebsiteData - класс для данных о веб-сайте. Наследуется от Data.
4. FileData - класс для данных о файле. Наследуется от Data.
5. ApplicationData - класс для данных о приложении. Наследуется от Data.
6. NoteData - класс для заметок. Наследуется от Data.
7. GameData - класс для данных об игре. Наследуется от Data.
8. Menu - класс, представляющий меню программы. Он содержит методы для отображения меню, выполнения действий пользователя
   и управления базой данных.
В программе можно выполнить следующие действия:

1) Создать новую базу данных.
2) Загрузить существующую базу данных.
3) Сгенерировать и сохранить новый пароль.
4) Отобразить все сохраненные пароли.
5) Создать архив базы данных.
6) Извлечь базу данных из архива.
7) Выйти из программы.

Для запуска программы необходимо вызвать функцию main().
Файл - with_password.zip - пароль к архиву: yEDhh=KS!-c&r.IhbuJ&T%Q]
Файл - no_password.zip - без пароля