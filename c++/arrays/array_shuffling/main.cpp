#include <iostream>
#include <random>

// Перемешивание массива
int main()
{
	// Инициализация объекта random_device для получения случайного значения семени
	std::random_device rd;
	// Инициализация генератора случайных чисел mt19937 с полученным значением семени
	std::mt19937 gen(rd());

	const int SIZE = 10;
	int mas[SIZE] {};
	int temp {};
	double ha {};
	unsigned int k = {};
	unsigned int l = {};
	size_t i {};

	// Заполнение массива значениями от 0 до SIZE-1
	for (i = 0; i < SIZE; i++)
	{
		mas[i] = i;
		std::cout << mas[i] << " ";
	}
	std::cout << '\n';

	// Перемешивание массива пока доля неправильно расположенных элементов не превысит 0.5
	while (ha < 0.5)
	{
		// Генерация случайных индексов k и l
		k = gen() % SIZE;
		l = gen() % SIZE;
		std::swap(mas[l], mas[k]);

		// Подсчет количества неправильно расположенных элементов
		for (i = 0; i < SIZE; i++)
		{
			if (mas[i] != i)
			{
				temp++;
			}
		}

		// Вычисление доли неправильно расположенных элементов
		ha = static_cast<double>(temp) / SIZE;
		temp = 0;
	}

	// Вывод перемешанного массива
	for (auto x: mas)
	{
		std::cout << x << " ";
	}
	std::cout << std::endl;

	return 0;
}
