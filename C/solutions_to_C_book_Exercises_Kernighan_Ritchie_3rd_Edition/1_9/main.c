// Упражнение 1.9. Напишите программу, копирующую символы ввода в выходной поток и заменяющую стоящие подряд пробелы на
// один пробел.

#include <stdio.h>

int main() {
	int c = 0;
	bool last_char_was_space = false; // Флаг для отслеживания последнего символа, который был пробелом

	// Чтение символов из входного потока до достижения конца файла (EOF)
	while ((c = getchar()) != EOF) {
		if (c == ' ') {
			// Если текущий символ - пробел
			if (!last_char_was_space) {
				putchar(c); // Если предыдущий символ не был пробелом, вывести текущий символ
				last_char_was_space = true; // Установить флаг, что текущий символ - пробел
			}
		} else {
			putchar(c); // Если текущий символ не пробел, вывести его
			last_char_was_space = false; // Сбросить флаг
		}

		// Выход из программы по символу 'q'
		if (c == 'q') {
			break;
		}
	}

	return 0;
}
