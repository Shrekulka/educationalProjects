This program is designed to encrypt and decrypt files in a specified directory using the `pyAesCrypt` library. 

It provides the user with a simple text menu where one of two actions can be selected:

1. encrypt files in a directory: The user is prompted to enter the path to the directory containing the files to be 
   encrypted, as well as a password for encryption. The program then recursively searches all the subdirectories and 
   encrypts every file, saving the encrypted files with the extension `.crp`. The original files are deleted after 
   encryption.

2. In-directory decryption: The user is prompted for the path to the directory containing the files to be decrypted, as 
   well as the Decryption directory: The user is prompted to enter the path to the directory containing the files to be 
   decrypted and the password for decryption. The program recursively looks through all the subdirectories and decrypts 
   each found file with the extension `.crp`, saving the decrypted files without the extension `.crp`. The original 
   encrypted files are deleted after decryption.

The user can select one of these actions or terminate the programme. The program re-displays a menu after each completed
action, allowing the user to perform multiple actions in succession if needed.




Данная программа предназначена для шифрования и дешифрования файлов в указанной директории с использованием библиотеки 
`pyAesCrypt`. 

Она предоставляет пользователю простое текстовое меню, в котором можно выбрать одно из двух действий:

1. Шифрование файлов в директории: Пользователю предлагается ввести путь к директории, содержащей файлы для шифрования, 
   а также пароль для шифрования. Затем программа рекурсивно просматривает все поддиректории и шифрует каждый найденный 
   файл, сохраняя зашифрованные файлы с расширением `.crp`. Исходные файлы удаляются после шифрования.

2. Дешифрование файлов в директории: Пользователю предлагается ввести путь к директории, содержащей файлы для 
   дешифрования, а также пароль для дешифрования. Программа рекурсивно просматривает все поддиректории и дешифрует каждый
   найденный файл с расширением `.crp`, сохраняя дешифрованные файлы без расширения `.crp`. Исходные зашифрованные файлы
   удаляются после дешифрования.

Пользователь может выбрать одно из этих действий или завершить программу. Программа повторно отображает меню после 
каждого выполненного действия, позволяя пользователю выполнять несколько операций подряд, если требуется.