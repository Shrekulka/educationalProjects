#include <iostream>

// Произведение четырехзначного числа = 1234 -> 1*2*3*4 = 24

int main()
{
	int f {};
	int j {};
	int i {};
	int p(1);

	std::cout << "Введите четырехзначное число: \n";
	std::cin >> f;

	while (f < 1000 || f > 9999)
	{
		std::cout << "Некорректный ввод. Пожалуйста, введите четырехзначное число: \n";
		std::cin >> f;
	}

	for (i = 0; i < 4; i++)
	{
		j = f % 10;
		f = f / 10;
		p = p * j;
	}

	std::cout << p << std::endl;

	std::cin.ignore();

	return 0;
}