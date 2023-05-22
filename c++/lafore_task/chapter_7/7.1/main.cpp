#include <iostream>

using namespace std;

// Напишите функцию reversit(), которая переворачивает строку (массив типа char). Используйте цикл for, который меняет
// местами первый и последний символы, затем следующие и т. д. до предпоследнего. Строка должна передаваться в функцию
// reversit() как аргумент.
// Напишите программу для выполнения функции reversit(). Программа должна принимать строку от пользователя, вызывать
// функцию reversit(), а затем выводить полученный результат. Используйте метод ввода, который позволяет использовать
// внутренние пробелы. Протестируйте программу на примере фразы «Аргентина манит негра».

void reversit(char*);

int main()
{
	const int SIZE = 80;
	char strok[80];
	cout << "Enter str: ";
	cin.get(strok, SIZE);
	reversit(strok);
	cout << "You enter: " << strok << '\n';

	return 0;
}

void reversit(char s[])
{
	int len = strlen(s);
	for (int i = 0; i < len / 2; ++i)
	{
		char tem = s[i];
		s[i] = s[len - i - 1];
		s[len - i - 1] = tem;
	}
}