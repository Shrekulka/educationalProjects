#include <iostream>
#include <random>
#include <algorithm>

// Вывод массива в порядке возрастания

int main()
{
	// Инициализация объекта random_device для получения случайного значения семени
	std::random_device rd;
	// Инициализация генератора случайных чисел mt19937 с полученным значением семени
	std::mt19937 gen(rd());
	// Инициализация распределения для генерации случайных чисел в заданном диапазоне
	std::uniform_int_distribution<int> dis(0, 99);

	const int SIZE = 10;
	int mas[SIZE] {};
	size_t i {};

	// Генерация случайных чисел и вывод их на экран
	for (i = 0; i < SIZE; i++)
	{
		mas[i] = dis(gen);
		std::cout << mas[i] << " ";
	}
	std::cout << '\n';

	bool flag;

	// Сортировка массива в порядке возрастания
	do
	{
		flag = false;
		for (i = 0; i < SIZE - 1; i++)
		{
			if (mas[i] > mas[i + 1])
			{
				// Обмен элементов массива при несоблюдении порядка сортировки
				std::swap(mas[i], mas[i + 1]);
				flag = true;
			}
		}
	} while (flag);

	// Вывод отсортированного массива на экран
	for (i = 0; i < SIZE; i++)
	{
		std::cout << mas[i] << " ";
	}
	std::cout << '\n';

	return 0;
}
