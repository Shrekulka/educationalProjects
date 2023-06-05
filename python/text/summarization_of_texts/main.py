import sys
import networkx as nx
import nltk
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from itertools import combinations


def calculate_similarity(set1, set2):
    """
    Вычисляет схожесть между двумя множествами слов.

    Args:
        set1 (set): Первое множество слов.
        set2 (set): Второе множество слов.

    Returns:
        float: Значение схожести между множествами.
    """
    if not set1 or not set2:  # Если одно из множеств пустое, возвращаем 0
        return 0.0

    return len(set1 & set2) / (len(set1) + len(set2))  # Вычисляем схожесть по формуле


def textrank(text, language='english'):
    """
    Применяет алгоритм TextRank для ранжирования предложений в тексте.

    Args:
        text (str): Текст, в котором необходимо выделить значимые предложения.
        language (str, optional): Язык текста. По умолчанию 'english'.

    Returns:
        list: Список предложений, отсортированных по значимости.
    """

    sentences = sent_tokenize(text)  # Разделяем текст на предложения
    tokenizer = RegexpTokenizer(r'\w+')  # Создаем токенизатор, чтобы разделить предложения на слова

    if language == 'english':
        stemmer = SnowballStemmer("english")  # Создаем стеммер для английского языка
    elif language == 'russian':
        nltk.download('punkt')  # Загружаем ресурсы для обработки русского языка, если необходимо
        stemmer = SnowballStemmer("russian")  # Создаем стеммер для русского языка
    elif language == 'ukrainian':
        nltk.download('punkt')  # Загружаем ресурсы для обработки украинского языка, если необходимо
        stemmer = SnowballStemmer("ukrainian")  # Создаем стеммер для украинского языка
    else:
        print("Неподдерживаемый язык/Unsupported language.")
        return []

    words = [set(stemmer.stem(word) for word in tokenizer.tokenize(sentence.lower()))
             # Приводим слова к основной форме и создаем множества слов для каждого предложения
             for sentence in sentences]

    # Создаем комбинации пар предложений
    pairs = combinations(range(len(sentences)), 2)

    # Вычисляем схожесть для каждой пары предложений
    scores = [(i, j, calculate_similarity(words[i], words[j])) for i, j in pairs]

    # Отфильтровываем пары с нулевой схожестью
    scores = filter(lambda x: x[2], scores)

    g = nx.Graph()  # Создаем пустой граф
    g.add_weighted_edges_from(scores)  # Добавляем взвешенные ребра в граф на основе схожести
    pr = nx.pagerank(g)  # Вычисляем PageRank для графа

    # Сортируем предложения по убыванию PageRank
    sorted_sentences = sorted(((i, pr[i], s) for i, s in enumerate(sentences) if i in pr),
                              key=lambda x: pr[x[0]], reverse=True)

    return sorted_sentences  # Возвращаем отсортированный список предложений


def extract_summary(text, language='english', num_sentences=5):
    """
    Извлекает краткое содержание из текста, используя алгоритм TextRank.

    Args:
        text (str): Текст, из которого необходимо извлечь краткое содержание.
        language (str, optional): Язык текста. По умолчанию 'english'.
        num_sentences (int, optional): Количество предложений в кратком содержании. По умолчанию 5.

    Returns:
        str: Краткое содержание текста.
    """
    ranked_sentences = textrank(text, language)  # Применяем алгоритм TextRank для ранжирования предложений
    top_n = sorted(ranked_sentences[:num_sentences])  # Выбираем топ-N предложений
    summary = ' '.join(x[2] for x in top_n)  # Объединяем предложения в одну строку

    return summary


def save_summary_to_file(summary, filename):
    """
    Сохраняет краткое содержание в файл.

    Args:
        summary (str): Краткое содержание текста.
        filename (str): Имя файла для сохранения.

    Returns:
        bool: True, если сохранение прошло успешно, иначе False.
    """
    try:
        with open(filename, 'w') as file:
            file.write(summary)
        print("Результат сохранен в файл:", filename)
        return True
    except IOError:
        print("Ошибка при сохранении файла/Error while saving the file.")
        return False


def main():
    """
    Главная функция программы, обеспечивает взаимодействие с пользователем.
    """
    print("Выберите язык/Choose a language:")
    print("1. English")
    print("2. Русский")
    print("3. Українська")

    stemmer_language = None  # Инициализируем переменную 'stemmer_language' со значением None
    language_choice = input("Выберите действие: 1 - English, 2 - Русский, 3 - Українська: ")

    if language_choice == '1':
        stemmer_language = 'english'
    elif language_choice == '2':
        stemmer_language = 'russian'
    elif language_choice == '3':
        stemmer_language = 'ukrainian'
        print("Некорректный выбор языка/Invalid language choice.")
        exit()

    input_choice = input("Выберите действие: 1 - считать из файла, 2 - ввести вручную: ")

    text = ""  # Инициализируем переменную 'text' со значением пустой строки

    if input_choice == '1':
        filename = input("Введите имя файла: ")
        try:
            with open(filename, 'r') as file:
                text = file.read()  # Читаем текст из файла и сохраняем его в переменную 'text'
        except FileNotFoundError:
            print("Файл не найден/File not found.")
            exit()
    elif input_choice == '2':
        end_symbol = input("Введите символ для завершения ввода: ")
        print("Введите текст (для завершения ввода введите символ для завершения): ")
        lines = []
        while True:
            line = sys.stdin.readline().strip()  # Считываем введенную строку и удаляем пробелы по краям
            if line == end_symbol:
                break
            lines.append(line)
        text = '\n'.join(lines)  # Объединяем строки в одну строку с разделителем '\n'
        if not text.strip():
            print("Ошибка: текст не может быть пустым. Повторите ввод.")
            return  # Возвращаемся из функции, если текст пустой
    else:
        print("Некорректный выбор действия/Invalid action choice.")
        exit()

    num_sentences_choice = input(
        "Введите количество предложений в кратком содержании (по умолчанию 5): ")
    if num_sentences_choice.strip():
        try:
            num_sentences = int(num_sentences_choice)
        except ValueError:
            print("Ошибка: введите корректное число. Будет использовано значение по умолчанию.")
            num_sentences = 5
    else:
        num_sentences = 5  # Если введенное значение пустое, устанавливаем значение по умолчанию равное 5
    # Вызываем функцию extract_summary с аргументами 'text', 'stemmer_language' и 'num_sentences' и сохраняем результат
    # в переменную 'summary'
    summary = extract_summary(text, stemmer_language, num_sentences)
    print(summary)

    if input_choice == '1':
        output_filename = input(
            "Введите имя файла для сохранения результата (оставьте пустым, если не хотите сохранять в файл): ").strip()
        output_filename = output_filename.strip()  # Удаляем лишние пробелы из имени файла
        if output_filename != "":
            save_summary_to_file(summary, output_filename)  # Сохраняем краткое содержание в файл
        else:
            print("Результат не сохранен в файл.")
    elif input_choice == '2':
        save_choice = input(
            "Хотите сохранить результат в файл? (y/n): ")
        if save_choice.lower() == 'y':
            output_filename = input(
                "Введите имя файла для сохранения результата: ").strip()
            output_filename = output_filename.strip()  # Удаляем лишние пробелы из имени файла
            if output_filename != "":
                save_summary_to_file(summary, output_filename)  # Сохраняем краткое содержание в файл
            else:
                print("Некорректное имя файла/Invalid filename.")
        else:
            print("Результат не сохранен в файл.")


if __name__ == "__main__":
    try:
        main()  # Вызываем функцию main
    except KeyboardInterrupt:
        print(
            "Программа завершена по запросу пользователя.")
