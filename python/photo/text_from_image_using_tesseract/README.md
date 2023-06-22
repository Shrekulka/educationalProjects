This code is designed to recognize text in images using the pytesseract library and the 
Tesseract OCR tool. Here is a brief description of each part of the code:

Function definition:
choose_language(): allows the user to select the language for text recognition.
choose_file_option(): allows the user to choose a file or group of files to be recognized.
choose_save_location(): allows the user to enter the path for saving the recognition results.
choose_config(): allows the user to select a text recognition configuration or enter their own.
process_image(): processes the image using Tesseract OCR.

The main() function, which is called when running the script. Within it, other functions are called sequentially. 
functions to select parameters and process the image.
As a result, when running the script, the user is prompted to select a language, a file or group of files option, a path 
to save the result and configuration of the text recognition. The program then processes the selected files or images, 
recognizes OCR and displays the result on the screen and saves the results to files.

Instructions for installing tesseract and Tesseract language data on os mac:

1) In the terminal - brew install tesseract

2) Create a directory to store the Tesseract language data. Run the following command:
   sudo mkdir -p /usr/local/share/tessdata

3) Download the data files of Tesseract language packs: for Russian, Ukrainian and English languages download the file
   from the official Tesseract repository on GitHub. Run the following command:
   sudo curl -o /usr/local/share/tessdata/rus.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/rus.traineddata
   sudo curl -o /usr/local/share/tessdata/ukr.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/ukr.traineddata
   sudo curl -o /usr/local/share/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

4) Check that the language data files have been downloaded successfully by running the command:
   ls -l /usr/local/share/tessdata

5) Configure tesseract options:
   https://help.ubuntu.ru/wiki/tesseract




Данный код предназначен для распознавания текста на изображениях с использованием библиотеки pytesseract и инструмента 
Tesseract OCR. Вот краткое описание каждой части кода:

Определение функций:
choose_language(): позволяет пользователю выбрать язык для распознавания текста.
choose_file_option(): позволяет пользователю выбрать опцию файла или группы файлов для распознавания.
choose_save_location(): позволяет пользователю ввести путь для сохранения результатов распознавания.
choose_config(): позволяет пользователю выбрать конфигурацию распознавания текста или ввести свою собственную.
process_image(): обрабатывает изображение с использованием Tesseract OCR.

Основная функция main(), которая вызывается при запуске скрипта. Внутри нее происходит последовательный вызов других 
функций для выбора параметров и обработки изображений.
В итоге, при запуске скрипта, пользователю предлагается выбрать язык, опцию файла или группы файлов, путь для сохранения
результатов и конфигурацию распознавания текста. Затем программа обрабатывает выбранные файлы или изображения, распознает
на них текст с помощью Tesseract OCR и выводит результат на экран, а также сохраняет результаты в файлы.

Инструкция по установке tesseract и языковых данных Tesseract на os mac:

1) В терминале - brew install tesseract

2) Создайте каталог для хранения языковых данных Tesseract. Выполните следующую команду:
   sudo mkdir -p /usr/local/share/tessdata

3) Загрузите файлы данных языковых пакетов Tesseract. Для русского, украинского и английского языков скачайте файл
   с официального репозитория Tesseract на GitHub. Выполните следующую команду:
   sudo curl -o /usr/local/share/tessdata/rus.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/rus.traineddata
   sudo curl -o /usr/local/share/tessdata/ukr.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/ukr.traineddata
   sudo curl -o /usr/local/share/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

4) Проверьте, что файлы языковых данных были успешно загружены, выполните команду:
   ls -l /usr/local/share/tessdata

5) Опции конфига tesseract:
   https://help.ubuntu.ru/wiki/tesseract