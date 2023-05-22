#include <iostream>

// Сумма последовательностей

int main()
{
	double a {}, b {};
	double summ {}, summSequence {};
	int n {};
	std::cout << "ВВедите числа : \n" << "Действительное число 'A' \n" << "Действительное число 'B' \n"
			  << "Натуральное число 'N' \n";
	std::cin >> a >> b >> n;

	for (int i = 0; i < n; i++)
	{
		summ = a + i * b;
		summSequence += summ;
		std::cout << "Сумма = " << summ << '\n';
	}
	std::cout << "Сумма последовательностей = " << summSequence << '\n';

	return 0;
}