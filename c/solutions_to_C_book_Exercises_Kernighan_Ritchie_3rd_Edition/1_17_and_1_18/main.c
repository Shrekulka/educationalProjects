// Упражнение 1.18. Напишите программу, которая будет в каждой вводимой строке заменять стоящие подряд символы пробелов
// и табуляций на один пробел и удалять пустые строки.
#include <stdio.h>
#include <stdlib.h>

#define MINIMUM_CHARACTERS 80 			// Макрос, для определения минимальной длины строки - 80

int main()
{
	int character = 0;                 // Переменная для хранения текущего символа
	int previous_char = 0;             // Переменная для отслеживания предыдущего символа
	int i = 0;                         // Счетчик символов в текущей строке
	int size = 1024;                   // Начальный размер буфера
	char* current_line = malloc(size); // Указатель на текущую строку (динамический массив)

	// Считываем символы до конца файла
	while ((character = getchar()) != EOF)
	{
		// Если встречена 'q' в начале строки
		if (character == 'q' && i == 0)
		{
			free(current_line);  // Освобождаем выделенную память перед выходом
			current_line = NULL; // Устанавливаем указатель на NULL
			return 0;
		}
		// Если текущая строка достигла предела размера буфера
		if (i == size - 1)
		{
			size *= 2; // Увеличиваем размер буфера вдвое

			// Перераспределяем память для буфера и проверяем успешность выделения
			current_line = (char*)realloc(current_line, size);

			// Если не удалось выделить память
			if (current_line == NULL)
			{
				fprintf(stderr, "Ошибка выделения памяти\n");
				exit(1);
			}
		}
		// Если встречен символ новой строки
		if (character == '\n')
		{
			// Проверяем, имеет ли строка более 80 символов
			current_line[i] = '\0'; // Добавляем завершающий нулевой символ
			if (i > MINIMUM_CHARACTERS)
			{
				printf("%s", current_line);
			}
			else
			{
				printf("The line does not contain more than 80 characters!!!\n");
			}
			i = 0; // Сбрасываем счетчик символов для новой строки
		}
		else
		{
			// Пропускаем лишние пробелы и табуляции
			if ((character == ' ' || character == '\t') && (previous_char == ' ' || previous_char == '\t'))
			{
				continue;
			}
			current_line[i++] = (char)character; // Записываем символ в текущую строку
		}
		previous_char = character; 				 // Сохраняем текущий символ как предыдущий
	}

	free(current_line);
	return 0;
}