// Упражнение 1.10. Напишите программу, копирующую вводимые символы в выходной поток с заменой символа табуляции на \t,
// символа забоя на \b и каждой обратной наклонной черты на \\. Это сделает видимыми все символы табуляции и забоя.

#include <stdio.h>

int main()
{
	int c;

	while ((c = getchar()) != EOF)
	{
		if (c == '\t')
		{
			putchar('\\');  // Вывод обратной косой черты для символа табуляции
			putchar('t');   // Вывод 't' после обратной косой черты
		}
		else if (c == '\b')
		{
			putchar('\\');  // Вывод обратной косой черты для символа забоя
			putchar('b');   // Вывод 'b' после обратной косой черты
		}
		else if (c == '\\')
		{
			putchar('\\');  // Вывод двух обратных косых черт для символа '\'
			putchar('\\');  // Вывод второй обратной косой черты
		}
		else if (c == 'q')
		{
			break;          // Выход из программы при вводе символа 'q'
		}
		else
		{
			putchar(c);      // Вывод остальных символов без изменений
		}
	}
	return 0;
}
