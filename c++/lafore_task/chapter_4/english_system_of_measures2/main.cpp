#include <iostream>

using namespace std;

// Структуры допускают вложенность, то есть использование структурной переменной в качестве поля какой-либо другой структуры.
// Внесем дополнения в программу ENGLSTRC, которые позволят это продемонстрировать. Пусть нам необходимо хранить данные о
// размерах комнаты, то есть ее ширину и длину. Поскольку мы работаем с английской системой мер, нам придется хранить эти
// величины с использованием типа Distance:

// длина в английской системе
struct Distance
{
	// футы
	int feet;
	// дюймы
	float inches;
};

// размеры прямоугольной комнаты
struct Room
{
	// длина
	Distance length;
	// ширина
	Distance width;
};

int main()
{
// переменная dining типа Room
	Room dining;
	// задание параметров комнаты
	dining.length.feet = 13;
	dining.length.inches = 6.5;
	dining.width.feet = 10;
	dining.width.inches = 0.0;
// преобразование длины и ширины в вещественный формат
// вычисление площади комнаты и вывод на экран
	float l = dining.length.feet + dining.length.inches / 12;
	float w = dining.width.feet + dining.width.inches / 12;
	cout << "Площадь комнаты равна " << l * w << " квадратных футов\n";
	return 0;
}
