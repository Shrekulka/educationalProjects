#include <iostream>
#include <iomanip>
using namespace std;

// Вы хотите создать таблицу умножения на заданное число. Напишите программу, которая позволяет пользователю ввести это
// число, а затем генерирует таблицу размером 20 строк на 10 столбцов. Первые строки результата работы программы должны
// выглядеть примерно следующим образом:
// Введите число: 7
// 7142128354249566370
// 77849198105112119126133140
// 147154161168175182189196203210

int main()
{
	int value = 0;
	cout << "\n********** Multiplication table for a given number **********\n\n";
	cout << "Enter the number -> ";
	cin>>value;
	for (int i = 1; i < 200; ++i)
	{
		cout <<setw(5)<<i*value <<' ';
		if(i%10==0)
			cout << '\n';
	}
	return 0;
}
