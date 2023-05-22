#include "pch.h"

int main()
{
	Rectangle rect1(5, 7); // Создание объекта rect1 класса Rectangle с шириной 5 и высотой 7
	Rectangle rect2 = rect1; // Создание объекта rect2 путем копирования rect1

	rect1.setHeight(10); // Изменение высоты rect1 на 10

	cout << "First Rectangle: " << endl;
	rect1.display(); // Вывод информации о rect1 (ширина и высота) на экран

	cout << "Second Rectangle: " << endl;
	rect2.display(); // Вывод информации о rect2 (ширина и высота) на экран

	return 0;
}
