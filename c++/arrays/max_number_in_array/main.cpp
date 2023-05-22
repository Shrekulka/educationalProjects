#include <iostream>
#include <random>

// Максимальное число в массиве

int main()
{
	// Инициализация объекта random_device для получения случайного значения семени
	std::random_device rd;
	// Инициализация генератора случайных чисел mt19937 с полученным значением семени
	std::mt19937 gen(rd());
	// Инициализация распределения для генерации случайных чисел в заданном диапазоне
	std::uniform_int_distribution<int> dis(10, 99);

	int mas[10] {};
	int i {};

	// Генерация случайного числа с использованием генератора и распределения
	for (i = 0; i < 10; i++)
	{
		mas[i] = dis(gen);
		std::cout << mas[i] << " ";
	}
	std::cout << '\n';

	int ind(0);
	int maxx = mas[0];

	// Поиск максимального числа в массиве
	for (i = 1; i < 10; i++)
	{
		if (maxx < mas[i])
		{
			maxx = mas[i];
			ind = i;
		}
	}
	std::cout << "Max = " << maxx << '\t' << "Index = " << ind << '\n';

	return 0;
}
