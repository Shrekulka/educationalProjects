// Индекс искомого элемента;

// Данный код создает динамический массив заданного пользователем размера, заполняет его случайными числами от 0 до 49
// с помощью генератора псевдослучайных чисел std::mt19937 и std::uniform_int_distribution<int>, после чего ищет в
// массиве значение, заданное пользователем, и выводит индексы найденного значения (если таковые имеются) в векторе.
// Если значение не найдено, то выводится соответствующее сообщение. Для работы с вектором используется стандартный
// класс std::vector.

#include <iostream>
#include <random>
#include <vector>

int main()
{
	// Инициализация генератора случайных чисел с использованием std::random_device
	std::random_device rd;
	std::mt19937 gen(rd());

	// Создание распределения случайных чисел от 0 до 49
	std::uniform_int_distribution<int> dist(0, 49);

	int size {};
	size_t i {};
	std::cout << "Enter the size of the array = ";
	std::cin >> size;
	int* pmas = new int[size] {}; // Создание динамического массива размером size и инициализация нулями

	// Заполнение массива случайными числами
	for (i = 0; i < size; i++)
	{
		pmas[i] = dist(gen);
	}

	// Вывод содержимого массива
	for (i = 0; i < size; i++)
	{
		std::cout << pmas[i] << ' ';
	}
	int value {};
	std::cout << "\n\nEnter the value you want to find = ";
	std::cin >> value;

	std::vector<int> indices;  // Вектор для хранения индексов найденного значения

	// Проверка, совпадает ли текущий элемент с искомым значением
	for (i = 0; i < size; i++)
	{
		if (value == pmas[i])
		{
			indices.push_back(i);  // Если совпадает, добавляем индекс в вектор indices
		}
	}

	if (indices.empty())  // Если вектор indices пуст, значит значение не найдено в массиве
	{
		std::cout << "The value was not found in the array.\n";
	}
	else  // Иначе выводим индексы, где было найдено значение
	{
		std::cout << "\nThe value was found at indices: ";
		for (i = 0; i < indices.size(); i++)
		{
			std::cout << indices[i] << ' ';
		}
		std::cout << '\n';
	}

	delete[] pmas;  // Освобождение памяти, выделенной для массива

	return 0;
}
