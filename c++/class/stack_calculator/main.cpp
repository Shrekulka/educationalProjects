#include "pch.h"

int main()
{
	Stack<double> resultStack(100);  // Создаем стек для хранения результатов

	Calculator<double> calc;
	calc.Run();  // Запускаем калькулятор

	auto& calcStack = const_cast<Stack<double>&>(calc.getStack());  // Получаем ссылку на стек калькулятора

	if (!calcStack.isempty())  // Проверяем, не пуст ли стек калькулятора
	{
		double result = calcStack.pop();  // Извлекаем результат из стека калькулятора

		resultStack.push(result);  // Сохраняем результат в стеке

		// Вывод содержимого стека с результатами
		std::cout << "Результаты в стеке:\n";
		while (!resultStack.isempty())
		{
			std::cout << resultStack.pop() << '\n';
		}
	}
	else
	{
		std::cout << "Ошибка: Пустой стек калькулятора\n";
	}

	return 0;
}
