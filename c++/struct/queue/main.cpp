// Файл main.cpp
#include <iostream>
#include "queue.h"

using namespace std;

void loop();

int main()
{
	loop();

	return 0;
}

// Функция для взаимодействия с пользователем
void loop()
{
	Queue myQueue;
	int choice {};
	while (true)
	{
		do
		{
			// Выводим пользователю меню команд
			cout << "1) - Enter to create the element of the Queue ;\n"
					"2) - Enter for the pop data ;\n"
					"3) - Enter for fine the middle ;\n"
					"4) - To quite ;\n";
			cin >> choice;                      // Вводим выбор пользователя

		} while (choice < 1 || choice > 4);      // Проверяем, валиден ли выбор пользователя

		int tmp {};

		switch (choice)
		{
		case 1:
			cout << "Enter the data to create the element of the Queue ;\n";
			cin >> tmp;
			puch(myQueue, tmp);                 // Добавляем элемент в очередь
			break;
		case 2:
			tmp = pull(myQueue);                 // Удаляем элемент из очереди
			cout << "Removed the element with data " << tmp << '\n';
			break;
		case 3:
			cout << theMiddle(myQueue);          // Находим среднее значение элементов в очереди
		case 4:
			return;                             // Завершаем выполнение программы
		}

		print(myQueue);                          // Выводим содержимое очереди на экран
	}
}
