#include <stdio.h>
#include <stdlib.h>

int get_line(char** current_line);

void copy_string(char to[], const char from[]);

int main()
{
	int current_length = 0;             // Переменная для хранения длины текущей строки
	int max_length = 0;                 // Переменная для хранения длины самой длинной строки
	char* current_line = NULL;          // Указатель на текущую строку (динамический массив)
	char* longest_line = NULL;          // Указатель на самую длинную строку (динамический массив)

	// Читаем строки из ввода
	while ((current_length = get_line(&current_line)) > 0)
	{
		// Если введено "q" и новая строка, выходим из цикла
		if (current_length == 2 && current_line[0] == 'q' && current_line[1] == '\n') break;

		if (current_length > max_length)
		{
			max_length = current_length;  // Обновляем значение max_length
			if (longest_line != NULL)
			{
				free(longest_line);      // Освобождаем предыдущую longest_line, если она существует
			}
			// Выделяем память для новой longest_line и проверяем успешность выделения
			longest_line = (char*)malloc(current_length + 1);
			if (longest_line == NULL)
			{
				fprintf(stderr, "Ошибка выделения памяти\n"); // Выводим сообщение об ошибке
				exit(1); // Завершаем программу с кодом ошибки
			}
			copy_string(longest_line, current_line); // Копируем текущую строку в longest_line
		}
	}

	if (max_length > 0)
	{
		printf("%s", longest_line);     // Выводим самую длинную строку
	}

	free(longest_line); // Освобождаем память, выделенную для longest_line
	free(current_line); // Освобождаем память, выделенную для current_line

	return 0; // Возвращаем код завершения
}

/* get_line: читает строку в current_line и возвращает длину */
int get_line(char** current_line)
{
	int character = 0;
	int i = 0;
	int size = 1024; // Начальный размер буфера

	// Выделяем начальную память для текущей строки и проверяем успешность выделения
	*current_line = (char*)malloc(size);

	if (*current_line == NULL)
	{
		fprintf(stderr, "Ошибка выделения памяти\n"); // Выводим сообщение об ошибке
		exit(1); // Завершаем программу с кодом ошибки
	}

	while ((character = getchar()) != EOF && character != '\n')
	{
		if (character == 'q' && i == 0)
		{
			free(*current_line); // Освобождаем выделенную память перед выходом
			*current_line = NULL; // Устанавливаем указатель на NULL
			return -1; // Возвращаем -1, чтобы указать на завершение по 'q'
		}
		if (i == size - 1)
		{
			size *= 2; // Увеличиваем размер буфера по мере необходимости
			// Перераспределяем память для буфера и проверяем успешность выделения
			*current_line = (char*)realloc(*current_line, size);

			if (*current_line == NULL)
			{
				fprintf(stderr, "Ошибка выделения памяти\n"); // Выводим сообщение об ошибке
				exit(1); // Завершаем программу с кодом ошибки
			}
		}

		(*current_line)[i++] = (char)character; // Записываем символ в текущую строку
	}

	(*current_line)[i] = '\0'; // Добавляем завершающий нулевой символ

	return i; // Возвращаем длину строки
}

/* copy_string: копирует строку from в to */
void copy_string(char to[], const char from[])
{
	// Копируем символы из from в to, пока не достигнем нулевого символа
	for (int i = 0; from[i] != '\0'; ++i)
	{
		to[i] = from[i];
	}
}
