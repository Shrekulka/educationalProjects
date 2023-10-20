//1.14. Напишите программу, печатающую гистограммы частот встречаемости вводимых символов.

#include <stdio.h>
#include <ctype.h>

#define SIZE 256

int main()
{
	int currentChar = 0;             // Переменная для хранения текущего символа
	int charFreq[SIZE] = { 0 };     // Массив для хранения частоты встречаемости символов
	int otherCharCount = 0;         // Счетчик других символов (не букв)

	while ((currentChar = getchar()) != EOF) // Читаем символы до конца файла
	{
		if (currentChar == 'q') break; // Если вводится 'q', завершаем программу

		if (currentChar >= 0 && currentChar < SIZE) // Убеждаемся, что текущий символ находится в допустимых пределах
		{
			if (isalpha(currentChar)) // Если символ является буквой
			{
				++charFreq[currentChar]; // Увеличиваем счетчик для данной буквы
			}
			else
			{
				++otherCharCount; // Иначе увеличиваем счетчик для других символов
			}
		}
		else
		{
			++otherCharCount; // Увеличиваем счетчик для других символов, если символ находится вне допустимых пределов
		}
	}
	printf("Histogram of frequency of occurrence of letters:\n");

	// Перебираем массив charFreq и выводим гистограмму
	for (int i = 0; i < SIZE; ++i)
	{
		if (charFreq[i] > 0)
		{
			printf("%c: ", i); // Выводим символ

			for (int j = 0; j < charFreq[i]; ++j)
			{
				putchar('*'); // Выводим звездочку для каждого встреченного символа
			}
			putchar('\n'); // Переходим на новую строку для следующего символа
		}
	}

	printf("Frequency of other symbols: %d\n", otherCharCount); // Выводим количество других символов

	return 0;
}
