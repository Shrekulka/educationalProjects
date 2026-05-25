// Упражнение 1.15. Перепишите программу преобразования температур, выделив само преобразование в отдельную функцию.
#include <stdio.h>

// Макрос для преобразования Фаренгейтовых градусов в Цельсии
#define FAHRENHEIT_TO_CELSIUS(f) ((5.0 / 9.0) * ((f) - 32))

// Нижний предел температуры в Фаренгейтах
#define LOWER_LIMIT 0

// Верхний предел температуры в Фаренгейтах
#define UPPER_LIMIT 300

// Шаг изменения температуры в Фаренгейтах
#define STEP_SIZE 20

// Прототип функции для вывода таблицы температур
void printTemperatureTable();

int main(void)
{
	// Вызываем функцию для вывода таблицы температур
	printTemperatureTable();
	return 0;
}

// Функция для вывода таблицы температур
void printTemperatureTable()
{
	// Выводим заголовок таблицы
	printf("Temperature Conversion Table:\n");
	printf("Fahrenheit\tCelsius\n");

	// Цикл для перебора температур в Фаренгейтах
	for (int fahr = LOWER_LIMIT; fahr <= UPPER_LIMIT; fahr += STEP_SIZE)
	{
		// Вычисляем температуру в Цельсиях с использованием макроса FAHRENHEIT_TO_CELSIUS
		double celsius = FAHRENHEIT_TO_CELSIUS(fahr);

		// Выводим температуру в Фаренгейтах и Цельсиях
		printf("%-12d %.1f\n", fahr, celsius);
	}
}
