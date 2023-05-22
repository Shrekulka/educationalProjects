#include <iostream>
#include <cstring>
#include <iomanip>

using namespace std;

// Создайте класс employee, который содержит имя (объект класса string) и номер (типа long) служащего. Включите в него
// метод getdata(), предназначенный для получения данных от пользователя и помещения их в объект, и метод putdata(), для
// вывода данных. Предполагаем, что имя не может иметь внутренних пробелов.
// Напишите функцию main(), использующую этот класс. Вам нужно будет создать массив типа employee, а затем предложить
// пользователю ввести данные до 100 служащих. Наконец, вам нужно будет вывести данные всех служащих.

class employee
{
private:
	string mName;
	long mNumber;
public:
	void setData();

	void showData();
};


int main()
{
	employee emp[1000];
	int n = 0;
	char ch;
	do
	{
		cout << "Enter the date of employee with № " << n + 1 << '\n';
		emp[n++].setData();
		cout << "Continue (y/n)? ";
		cin >> ch;
	} while (ch != 'n');
	for (int i = 0; i < n; ++i)
	{
		cout << "Number employee " << i + 1 << '\n';
		emp[i].showData();
	}
	cout << '\n';
	return 0;
}

void employee::setData()
{
	cout << "Enter name -> ";
	cin >> mName;
	cout << "Enter number -> ";
	cin >> mNumber;
}

void employee::showData()
{
	cout << "The name is -> " << mName << '\n';
	cout << "The number is -> " << mNumber << '\n';
}