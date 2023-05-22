#include <iostream>

using namespace std;

// Создайте эквивалент калькулятора, выполняющего четыре основных арифметических операции. Программа должна запрашивать
// ввод пользователем первого операнда, знака операции и второго операнда. Для хранения операндов следует использовать
// переменные вещественного типа. Выбрать операцию можно при помощи оператора switch. В конце программа должна отображать
// результат на экране. Результат работы программы с пользователем может выглядеть следующим образом:
// Введите первый операнд, операцию и второй операнд: 10 / 3 Результат равен 3.333333
// Выполнить еще одну операцию (y/n)? y
// Введите первый операнд, операцию и второй операнд: 12 + 100 Результат равен 112
// Выполнить еще одну операцию (y/n)? n

int main()
{
	double value1 = 0.0, value2 = 0.0, ans = 0.0;
	char oper = '\0', ch = '\0';
	cout << "\n********** Calculator **********\n\n";
	do
	{
		cout << "Enter first operand, operation, second operand -> ";
		cin >> value1 >> oper >> value2;
		switch (oper)
		{
		case '+':
			ans = value1 + value2;
			break;
		case '-':
			ans = value1 - value2;
			break;
		case '/':
		{
			if (value2 == 0)
			{
				cout << "\nDivision by zero!!!\n\n";
			}
			else
			{
				ans = value1 / value2;
			}
			break;
		}
		case '*':
			ans = value1 * value2;
			break;
		default:
			ans = 0.0;
		}
		cout << "Answer = " << ans << "\n\n";
		cout << "To continue type - 'Y', abort type - 'N' -> ";
		cin >> ch;
		cout << '\n';
	} while ((ch != 'n') && (ch != 'N'));
	return 0;
}
