#include <stdio.h>
#include <ctype.h>

#define INSIDE_WORD 1   /* Состояние: внутри слова */
#define OUTSIDE_WORD 0  /* Состояние: вне слова */

int main()
{
	int currentChar = 0;        // Переменная для хранения текущего символа
	int numberOfLines = 0;      // Счетчик строк
	int numberOfWords = 0;      // Счетчик слов
	int numberOfCharacters = 0; // Счетчик символов
	int state = OUTSIDE_WORD;    // Начинаем с состояния "вне слова"

	while ((currentChar = getchar()) != EOF)
	{
		// Если введен символ 'q', выходим из программы
		if (currentChar == 'q')
		{
			break;
		}

		// Увеличиваем счетчик символов при каждом вводе символа
		++numberOfCharacters;

		// Если введен символ новой строки, увеличиваем счетчик строк
		if (currentChar == '\n')
		{
			++numberOfLines;
		}

		// Проверяем, является ли текущий символ буквой и не цифрой
		if (isalnum(currentChar) && !isdigit(currentChar))
		{
			// Если предыдущее состояние было "вне слова", увеличиваем счетчик слов и переходим в состояние "внутри слова"
			if (state == OUTSIDE_WORD)
			{
				++numberOfWords;
			}
			state = INSIDE_WORD;
		}
		else
		{
			state = OUTSIDE_WORD;  // Если текущий символ - разделитель, переходим в состояние "вне слова"
		}
	}

	// Выводим результаты подсчета
	printf("Number of Lines: %d\nNumber of Words: %d\nNumber of Characters: %d\n", numberOfLines, numberOfWords,
			numberOfCharacters);

	return 0;
}
