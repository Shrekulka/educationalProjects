#include <iostream>

// Подсчет, сколько траекторий из города А в город В; Идентична функции Фибаначи;
int number_of_trajectories(int);

int main()
{
	int finish;
	std::cout << "Enter the destination city (a positive integer): ";

	if (!(std::cin >> finish)) // Проверка ввода пользователя
	{
		std::cout << "Invalid input. Please enter a positive integer." << std::endl;
		return 1; // Завершаем программу с кодом возврата 1, указывающим на ошибку
	}

	if (finish <= 0) // Проверка, что введенное число является положительным
	{
		std::cout << "Invalid input. Please enter a positive integer." << std::endl;
		return 1; // Завершаем программу с кодом возврата 1, указывающим на ошибку
	}

	std::cout << "Grasshopper has " << number_of_trajectories(finish) << " trajectories from 1 to " << finish
			  << std::endl; // Выводим количество траекторий на экран

	return 0;
}

int number_of_trajectories(int n)
{
	int K[n + 1]; // Объявление массива для хранения количества траекторий
	K[0] = 0; // Начальное значение количества траекторий для города 0
	K[1] = 1; // Начальное значение количества траекторий для города 1

	for (int i = 2; i <= n; ++i) // Цикл для вычисления количества траекторий от города 2 до целевого города
	{
		K[i] = K[i - 1] + K[i - 2]; // Вычисление количества траекторий на основе предыдущих значений
	}

	return K[n]; // Возвращаем количество траекторий до целевого города
}