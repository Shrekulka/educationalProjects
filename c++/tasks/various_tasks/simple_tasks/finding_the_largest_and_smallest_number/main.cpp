#include <iostream>

// Нахождение наибольшего и наименьшего числа

int main()
{
	int a{}, b{}, c{}, d{};
	std::cout << " Enter : \n" << "'A' = \n" << "'B' = \n" << "'C' = \n" << "'D' = \n";
	std::cin >> a >> b >> c >> d;
	int max1 = std::max(a, b);
	int max2 = std::max(c, d);
	int max3 = std::max(max1, max2);
	int min1 = std::min(a, b);
	int min2 = std::min(c, d);
	int min3 = std::min(min2, min1);
	std::cout << max3 << '\n' << min3 << '\n';
	return 0;
}