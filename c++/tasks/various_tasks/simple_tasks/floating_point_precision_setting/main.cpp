#include <iostream>
#include <cmath>
#include <iomanip>

// Метод setprecision() библиотеки iomanip в C++ используется для установки точности с плавающей запятой библиотеки ios
// на основе точности, указанной в качестве параметра этого метода. fixed - Показывает, что установленная точность
// относится к количеству знаков после запятой

int main()
{
	double a {}, b {}, c {}, p {}, s {};
	std::cout << "Введите катет 'a' и 'b' : \n";
	std::cin >> a >> b;
	s = (a * b) / 2;
	c = sqrt(a * a + b * b);
	p = a + b + c;
	std::cout << "Площадь треугольника = " << std::setprecision(2) << std::fixed << s << '\n'
			  << "Периметр треугольника = " << p << '\n';

	std::cout << "Нажмите любую клавишу для продолжения...";
	std::cin.ignore();
	std::cin.get();

	return 0;
}
