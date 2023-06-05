#include "pch.h"

// Программа из листинга предлагает пользователю ввести до 10 поговорок. Каждая поговорка считывается во временный
// символьный массив, а затем копируется в объект String. Если пользователь вводит пустую строку, оператор break завершает
// цикл ввода. После вывода введенных данных программа использует функции-члены length ( ) и operator< ( ) для нахождения
// самой короткой и самой первой в алфавитном порядке строки. Программа также применяет операцию индексации ( [ ] )
// для того, чтобы разместить перед каждой поговоркой ее начальный символ. Рассмотрим пример выполнения этой программы:
//
// Hi, what's your паmе? >> Мisty Gutz
// Misty Gutz, please enter up to 10 short sayings <empty line to quit>:
// 1: а fool and his money are soon parted
// 2: penny wise , pound foolish
// 3: the love of money is the root of much evil
// 4: out of siqht, out of mind
// 5: aЬsence makes the heart qrow fonder
// 6: aЬsinthe makes the hart qrow fonder
//
// Here are your sayings :
//а: а fool and his money are soon parted
//р: penny wise, pound foolish
//t: the love of money is the root of much evil out of sight, out of mind
//о: out of siqht, out of mind
//а: absence makes the heart grow fonder absinthe makes the hart grow fonder
//а: aЬsinthe makes the hart qrow fonder
// Shortest saying:
// penny wise, pound foolish First alphabetically:
// First alphabetically:
// а fool and his money are soon parted
// This program used 11 String objects. Вуе.

int main()
{
	String name;
// Ввод имени;
	cout << "Hi, what is your name ? \n >> ";
	cin >> name;
// Вывод сообщения с просьбой ввести до 10 фраз.
	cout << name << ", please enter up to " << ArSize << " short sayings <empty line to quit>:\n";
// Массив объектов;
	String sayings[ArSize];
// Временное хранилище для строки;
	char temp[MaxLen];
	int i;

// Цикл для ввода фраз, считывания их с помощью cin и сохранения в объекты sayings.
	for (i = 0; i < ArSize; i++)
	{
		cout << i + 1 << ": ";
		cin.get(temp, MaxLen);
		while (cin && cin.get() != '\n')
		{
			continue;
		}
		// пустая строка?
		if (!cin || temp[0] == '\n')
		{
			// прервать;
			break;
		}
		else
		{
			// Перегруженное присвоение;
			sayings[i] = temp;
		}
	}
// общее количество прочитанных строк;
	int total = i;
// 1) Вариант;
	if (total > 0)
	{
// вывод поговорок
		cout << "Here are your sayings:\n";
		for (i = 0; i < total; i++)
		{
			cout << sayings[i][0] << ": " << sayings[i] << '\n';
		}
		int shortest = 0;
		int first = 0;
		for (i = 1; i < total; i++)
		{
			if (sayings[i].length() < sayings[shortest].length())
			{ shortest = i; }
			if (sayings[i] < sayings[first])
			{ first = i; }
		}
		cout << "Shortest saying:\n" << sayings[shortest] << '\n';
		// Самая короткая поговорка
		cout << "First alphabetically:\n" << sayings[first] << '\n';
		// Первая по алфавиту
		cout << "This program used " << String::HowMany() << " String objects. Bуе.\n";
	}
	else
	{
		// Ничего не было введено;
		cout << "No input! Bуе.\n";
	}

	return 0;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 2) Вариант;
//
// Реализован этот подход с использованием двух указателей на объекты String. Первоначально указатель shortest указывает
// на первый объект в массиве. Всякий раз, когда программа находит объект с более короткой строкой, она устанавливает
// указатель shortest на этот объект. Аналогично, указатель first отслеживает самую первую в алфавитном порядке строку.
// Обратите внимание, что эти два указателя не создают новые объекты, они просто указывают на существующие объекты.
// Поэтому они не требуют применения операции new для выделения дополнительной памяти.
// Для разнообразия программа использует указатель, который отслеживает новые объекты:
// String * favorite = new String (sayings [choice] ) ;
// Здесь указатель favorite обеспечивает доступ к безымянному объекту, созданному операцией new. Этот синтаксис означает
// инициализацию нового объекта String с помощью объекта sayings [choice]. При этом вызывается конструктор копирования,
// поскольку тип аргумента для конструктора копирования (const String &) соответствует инициализирующему значению
// (sayings [ choice ] ). Для выбора случайных значений в программе используются функции s rand (), rand () и time ().

//	if (total > 0)
//	{
//// вывод поговорок
//// вывод пословиц for (i = О; i < total; i++)
//		cout << "Here are your sayings:\n";
//		cout << sayings[i] << "\n";
//// Указатели для отслеживания кратчайшей и первой строки
//		String* shortest = &sayings[0]; // инициализация первым объектом
//		String* first = &sayings[0];
//		for (i = 1; i < total; i++)
//		{
//			if (sayings[i].length() < shortest->length())
//			{
//				shortest = &sayings[i];
//			}
//			// сравнение значений
//			if (sayings[i] < *first)
//			{
//				// присваивание адреса
//				first = &sayings[i];
//			}
//		}
//		// вывод кратчайшей пословицы
//		cout << "Shortest saying:\n" << *shortest << endl;
//		// вывод первой пословицы по алфавиту
//		cout << "First alphabetically:\n" << *first << endl;
//		srand(time(nullptr));
//		// выбор случайного индекса
//		int choice = rand() % total;
//		// Создание и инициализация объекта String с помощью new
//		String* favorite = new String(sayings[choice]);
//		// вывод любимой пословицы
//		cout << "Му favorite saying:\n" << *favorite << endl;
//		delete favorite;
//	}
//	else
//	{
//		cout << "Not much to say, eh?\n"; // ничего не было введено
//		cout << "Буе.\n";
//	}


