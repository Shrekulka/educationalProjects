#include <iostream>

// Числа в порядке возрастания

int main()
{
	int x {}, y {}, z {};
	std::cout << "Enter inte three integer : \n" << "The first = ";
	std::cin >> x;
	std::cout << "The second = ";
	std::cin >> y;
	std::cout << "The third = ";
	std::cin >> z;

	if (x > y)
	{ std::swap(x, y); }
	if (y > z)
	{ std::swap(y, z); }
	if (x > y)
	{ std::swap(x, y); }

	std::cout << "Numbers in ascending order : \n" << x << " -> " << y << " -> " << z << std::endl << std::endl;

	system("pause");

	return 0;
}
