This code solves the task of speech recognition using the SpeechRecognition library. It provides the user 
to record audio from a microphone, save it to a file and then perform speech recognition on that audio.

The main steps of the task solution are:

1) At the beginning of the programme, the user is prompted to select audio quality, sampling rate and input language 
   parameters.
2) A directory is then created to save the audio and text files, if they do not exist.
3) The user is prompted to enter a file name to save the audio, and specify the duration of the recording.
4) The audio is recorded using the sounddevice library and the audio file is saved using the soundfile.
5) An audio file is loaded and then passed to the SpeechRecognition library for speech recognition.
6) The resulting text is displayed and saved in a text file.
   
Thus, this code solves the task of converting speech into text, allowing the user to record and recognise 
audio in various languages.




Данный код решает задачу распознавания речи с помощью библиотеки SpeechRecognition. Он предоставляет пользователю 
возможность записать аудио с микрофона, сохранить его в файл и затем произвести распознавание речи в этом аудио.

Основные шаги решения задачи:

1) В начале программы пользователю предлагается выбрать параметры качества звука, частоты дискретизации и языка ввода.
2) Затем создается директория для сохранения аудио и текстовых файлов, если они не существуют.
3) Пользователю предлагается ввести имя файла для сохранения аудио, и указать длительность записи.
4) Происходит запись аудио с помощью библиотеки sounddevice и сохранение аудиофайла с помощью soundfile.
5) Загружается аудиофайл, который затем передается в библиотеку SpeechRecognition для распознавания речи.
6) Полученный текст выводится на экран и сохраняется в текстовом файле.
   
Таким образом, данный код решает задачу преобразования речи в текст, позволяя пользователю записывать и распознавать 
аудио на различных языках.