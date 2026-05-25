// Упражнение 1.8. Напишите программу для подсчета пробелов, табуляций и новых строк.

#include <stdio.h>

int main()
{
	int c = 0, count_spaces = 0, count_tabulation = 0, count_new_line = 0;

	// Чтение символов из входного потока до достижения конца файла (EOF)
	while ((c = getchar()) != EOF)
	{
		// Проверка на символ новой строки
		if (c == '\n') ++count_new_line;
			// Проверка на символ табуляции
		else if (c == '\t') ++count_tabulation;
			// Проверка на пробел
		else if (c == ' ') ++count_spaces;
			// Выход из программы по символу 'q'
		else if (c == 'q') break;
		else printf("Unsupported character: '%c'\n", c);
	}

	// Вывод результатов подсчета на экран
	printf("Spaces: %d\n", count_spaces);
	printf("Tabulations: %d\n", count_tabulation);
	printf("New Lines: %d\n", count_new_line);

	return 0;
}
