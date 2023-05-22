#include <iostream>

using namespace std;

// Напишите программу, предлагающую пользователю осуществить перевод температуры из шкалы Цельсия в шкалу Фаренгейта или
// наоборот, а затем осуществите преобразование. Используйте в программе переменные вещественного типа. Взаимодействие
// программы с пользователем может выглядеть следующим образом:
// Нажмите 1 для перевода шкалы Цельсия в шкалу Фаренгейта,
// 2 для перевода шкалы Фаренгейта в шкалу Цельсия:
// 2 Введите температуру по Фаренгейту: 70
// Значение по Цельсию: 21.111111

int main()
{
	int choice = 0;
	double temp = 0.0;
xyz:
	cout << "\n*****Temperature conversion from Celsius to Fahrenheit or vice versa*****\n\n";
	cout << "Press 1 to convert Celsius to Fahrenheit: \n" << "Press 2 to convert Fahrenheit to Celsius: \n";
	cin >> choice;
	switch (choice)
	{
	case 1:
	{
		cout << "Enter temperature in Celsius ->";
		cin >> temp;
		cout << "In degrees Fahrenheit, this is -> " << 9.0 / 5.0 * temp + 32.0 << '\n';
		break;
	}
	case 2:
	{
		cout << "Enter temperature in Fahrenheit ->";
		cin >> temp;
		cout << "In degrees Celsius, this is -> " << 5.0 / 9.0 * (temp - 32.0) << '\n';
		break;
	}
	default:
	{
		cout << "Wrong choice try again!!!\n";
		goto xyz;
	}
	}

	return 0;
}
