#include <stdio.h>

#define INSIDE_WORD 1   /* Состояние: внутри слова */
#define OUTSIDE_WORD 0  /* Состояние: вне слова */

int main()
{
	int currentChar = 0;        // Переменная для хранения текущего символа
	int state = OUTSIDE_WORD;   // Начинаем с состояния "вне слова"

	while ((currentChar = getchar()) != EOF)
	{
		// Если введен символ 'q', выходим из программы
		if (currentChar == 'q')
		{
			break;
		}

		// Проверяем, является ли текущий символ разделителем (пробел, новая строка или табуляция)
		if (currentChar == ' ' || currentChar == '\n' || currentChar == '\t')
		{
			// Если предыдущее состояние было "внутри слова", добавляем символ новой строки
			if (state == INSIDE_WORD)
			{
				putchar('\n');
				state = OUTSIDE_WORD;  // Переходим в состояние "вне слова"
			}
		}
		else if (state == OUTSIDE_WORD)
		{
			state = INSIDE_WORD;  // Если текущий символ не разделитель и предыдущее состояние было "вне слова", переходим в состояние "внутри слова"
			putchar(currentChar);  // Выводим текущий символ
		}
		else
		{
			putchar(currentChar);  // Выводим текущий символ слова
		}
	}

	return 0;
}
