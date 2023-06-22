TextRank to rank sentences

The program implements the TextRank algorithm for ranking sentences in text. The algorithm is based on similarity 
analysis between sentences based on sets of words reduced to the main form. According to the ranking results, offers 
with the most significant are highlighted in the summary.

Usage

The program offers the following features:

calculate_similarity(set1, set2): Calculates the similarity between two sets of words.
textrank(text, language='english'): Uses the TextRank algorithm to rank sentences in text.
extract_summary(text, language='english', num_sentences=5): Extracts the summary from the text using an algorithm
TextRank.
save_summary_to_file(summary, filename): Saves the summary to a file.
main(): The main function of the program, provides user interaction.
To use the program, follow the instructions provided during the execution. You will be prompted to select
language (English, Russian or Ukrainian), enter the text or specify the name of the file with the text, as well as set 
the number short sentences. The result will be displayed on the screen and can be saved to a file.

Dependencies

The program uses the following dependencies:

networkx: a library for working with graphs.
nltk: A library for natural language processing.
itertools: a module for working with iterations.
Please make sure all dependencies are installed before running the program.




TextRank для ранжирования предложений

Программа реализует алгоритм TextRank для ранжирования предложений в тексте. Алгоритм основывается на анализе схожести 
между предложениями на основе множеств слов, приведенных к основной форме. По результатам ранжирования, предложения с 
наибольшей значимостью выделены в краткое содержание.

Использование

Программа предлагает следующие функции:

calculate_similarity(set1, set2): Вычисляет схожесть между двумя множествами слов.
textrank(text, language='english'): Применяет алгоритм TextRank для ранжирования предложений в тексте.
extract_summary(text, language='english', num_sentences=5): Извлекает краткое содержание из текста, используя алгоритм 
TextRank.
save_summary_to_file(summary, filename): Сохраняет краткое содержание в файл.
main(): Главная функция программы, обеспечивает взаимодействие с пользователем.
Для использования программы, следуйте инструкциям, предоставляемым в процессе выполнения. Вам будет предложено выбрать 
язык (английский, русский или украинский), ввести текст или указать имя файла с текстом, а также задать количество 
предложений в кратком содержании. Результат будет отображен на экране и может быть сохранен в файл.

Зависимости

Программа использует следующие зависимости:

networkx: библиотека для работы с графами.
nltk: библиотека для обработки естественного языка.
itertools: модуль для работы с итерациями.
Пожалуйста, убедитесь, что все зависимости установлены перед запуском программы.