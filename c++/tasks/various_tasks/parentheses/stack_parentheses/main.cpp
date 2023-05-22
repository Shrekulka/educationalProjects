#include <iostream>
#include <stack>

// Функция для проверки корректности последовательности скобок
bool isBracketsSequenceCorrect(const std::string& s)
{
	std::stack<char> stk;

	for (char c : s)
	{
		if (c == '(' || c == '[' || c == '{')
		{
			stk.push(c);
		}
		else if (c == ')')
		{
			if (!stk.empty() && stk.top() == '(')
			{
				stk.pop();
			}
			else
			{
				return false; // Некорректная последовательность скобок
			}
		}
		else if (c == ']')
		{
			if (!stk.empty() && stk.top() == '[')
			{
				stk.pop();
			}
			else
			{
				return false; // Некорректная последовательность скобок
			}
		}
		else if (c == '}')
		{
			if (!stk.empty() && stk.top() == '{')
			{
				stk.pop();
			}
			else
			{
				return false; // Некорректная последовательность скобок
			}
		}
	}

	return stk.empty(); // Если стек пуст, то последовательность скобок корректна
}

int main()
{
	std::string s = "()({}[])";

	if (isBracketsSequenceCorrect(s))
	{
		std::cout << "Последовательность скобок корректна!!!" << std::endl;
	}
	else
	{
		std::cout << "Последовательность скобок некорректна!!!" << std::endl;
	}

	return 0;
}
