#include "pch.h"

int main()
{
	vector<Beverage*> orders; // Создаем вектор для хранения заказов

	// Меню напитков
	cout << "Welcome to the Coffee Shop!" << endl;
	cout << "Menu:" << endl;
	cout << "1. Dark Roast" << endl;
	cout << "2. Latte" << endl;
	cout << "3. Dark Mocha" << endl;
	cout << "4. White Mocha" << endl;
	cout << "0. Exit" << endl;

	int choice;
	do
	{
		cout << "Enter your choice (0-4): ";
		cin >> choice;

		switch (choice)
		{
		case 0: // Выход из программы
			break;
		case 1: // Dark Roast
		{
			Beverage* darkRoast = new DarkRoast();
			orders.push_back(darkRoast);
			cout << "Dark Roast added to the order." << endl;
		}
			break;
		case 2: // Latte
		{
			Beverage* latte = new Latte();
			orders.push_back(latte);
			cout << "Latte added to the order." << endl;
		}
			break;
		case 3: // Dark Mocha
		{
			Beverage* darkMocha = new DarkMocha(new DarkRoast());
			orders.push_back(darkMocha);
			cout << "Dark Mocha added to the order." << endl;
		}
			break;
		case 4: // White Mocha
		{
			Beverage* whiteMocha = new WhiteMocha(new Latte());
			orders.push_back(whiteMocha);
			cout << "White Mocha added to the order." << endl;
		}
			break;
		default:
			cout << "Invalid choice. Please try again." << endl;
			break;
		}
	} while (choice != 0);

	// Выводим информацию о заказах
	cout << "Order details:" << endl;
	for (const auto& order: orders)
	{
		cout << "Description: " << order->GetDescription() << endl;
		cout << "Cost: $" << order->Cost() << endl;
		cout << endl;
	}

	// Вычисляем общую сумму заказа
	double totalCost = 0;
	for (const auto& order : orders)
	{
		totalCost += order->Cost();
	}

// Выводим общую сумму заказа
	cout << "Total cost of the order: $" << totalCost << endl;

	// Освобождаем память
	for (auto order: orders)
	{
		delete order;
	}

//// 2-й вариант
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//	// Создаем напиток DarkRoast
//	Beverage* darkRoast = new DarkRoast();
//	cout << "Description: " << darkRoast->GetDescription() << endl;
//	cout << "Cost: $" << darkRoast->Cost() << endl;
//
//	// Добавляем к DarkRoast молоко
//	Beverage* darkRoastWithMilk = new Milk(darkRoast);
//	cout << "Description: " << darkRoastWithMilk->GetDescription() << endl;
//	cout << "Cost: $" << darkRoastWithMilk->Cost() << endl;
//
//	// Добавляем к DarkRoast молоко и шоколад
//	Beverage* darkRoastWithMilkAndMocha = new Mocha(darkRoastWithMilk);
//	cout << "Description: " << darkRoastWithMilkAndMocha->GetDescription() << endl;
//	cout << "Cost: $" << darkRoastWithMilkAndMocha->Cost() << endl;
//
//	// Создаем напиток Latte
//	Beverage* latte = new Latte();
//	cout << "Description: " << latte->GetDescription() << endl;
//	cout << "Cost: $" << latte->Cost() << endl;
//
//	// Добавляем к Latte взбитые сливки
//	Beverage* latteWithWhip = new Whip(latte);
//	cout << "Description: " << latteWithWhip->GetDescription() << endl;
//	cout << "Cost: $" << latteWithWhip->Cost() << endl;
//
//	// Добавляем к Latte молоко и шоколад
//	Beverage* latteWithMilkAndMocha = new Mocha(new Milk(latte));
//	cout << "Description: " << latteWithMilkAndMocha->GetDescription() << endl;
//	cout << "Cost: $" << latteWithMilkAndMocha->Cost() << endl;
//
//	// Создаем напиток DarkMocha
//	Beverage* darkMocha = new DarkMocha(new DarkRoast());
//	cout << "Description: " << darkMocha->GetDescription() << endl;
//	cout << "Cost: $" << darkMocha->Cost() << endl;
//
//	// Добавляем к DarkMocha молоко и шоколад
//	Beverage* darkMochaWithMilkAndMocha = new Mocha(new Milk(darkMocha));
//	cout << "Description: " << darkMochaWithMilkAndMocha->GetDescription() << endl;
//	cout << "Cost: $" << darkMochaWithMilkAndMocha->Cost() << endl;
//
//	// Создаем напиток WhiteMocha
//	Beverage* whiteMocha = new WhiteMocha(new Latte());
//	cout << "Description: " << whiteMocha->GetDescription() << endl;
//	cout << "Cost: $" << whiteMocha->Cost() << endl;
//
//	// Добавляем к WhiteMocha взбитые сливки
//	Beverage* whiteMochaWithWhip = new Whip(whiteMocha);
//	cout << "Description: " << whiteMochaWithWhip->GetDescription() << endl;
//	cout << "Cost: $" << whiteMochaWithWhip->Cost() << endl;
//
//	// Добавляем к WhiteMocha молоко и шоколад
//	Beverage* whiteMochaWithMilkAndMocha = new Mocha(new Milk(whiteMocha));
//	cout << "Description: " << whiteMochaWithMilkAndMocha->GetDescription() << endl;
//	cout << "Cost: $" << whiteMochaWithMilkAndMocha->Cost() << endl;
//
//	// Освобождаем память
//	delete darkRoast;
//	delete darkRoastWithMilk;
//	delete darkRoastWithMilkAndMocha;
//	delete latte;
//	delete latteWithWhip;
//	delete latteWithMilkAndMocha;
//	delete darkMocha;
//	delete darkMochaWithMilkAndMocha;
//	delete whiteMocha;
//	delete whiteMochaWithWhip;
//	delete whiteMochaWithMilkAndMocha;
	return 0;
}
