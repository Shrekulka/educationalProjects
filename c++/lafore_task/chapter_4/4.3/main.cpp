#include <iostream>

using namespace std;

// Создайте структуру с именем Volume, содержащую три поля типа Distance из примера englstrc, для хранения трех измерений
// помещения. Определите переменную типа Volume, инициализируйте ее, вычислите объем, занимаемый помещением, и выведите
// результат на экран. Для подсчета объема переведите каждое из значений типа Distance в значение типа float, равное
// соответствующей длине в футах и хранимое в отдельной переменной. Затем для вычисления объема следует перемножить три
// полученные вещественные переменные.

struct Distance
{
	int feet;
	float inches;
};
struct Volume
{
	Distance length;
	Distance width;
	Distance height;
};

int main()
{
	float l = 0, w = 0, h = 0;
	Volume room1{{ 12, 4.7 },
				 { 16, 2.56 },
				 { 9,  2.1 }};
	l = room1.length.feet + room1.length.inches / 12.0;
	w = room1.width.feet + room1.width.inches / 12.0;
	h = room1.height.feet + room1.height.inches / 12.0;
	cout << "\nОбъем = " << l * w * h << " кубических фунтов \n";
	return 0;
}
