// Программа запрашивает у пользователя количество треугольников и длины сторон каждого треугольника. Затем программа
// проверяет, является ли каждый из треугольников действительным с помощью проверки условий на соответствие неравенству
// треугольника. Результаты проверки сохраняются в векторе, который затем выводится на экран пользователю в виде
// сообщения о том, является ли каждый треугольник действительным или нет.

#include <iostream>
#include <vector>

int main()
{
	int size = 0;  // количество треугольников
	std::cout << "Enter the number of triangles: ";
	std::cin >> size;
	std::cin.ignore();

	std::vector<int> myVector(size);  // Вектор с результатами

	// Цикл для обработки каждого тестового случая
	for (int i = 0; i < size; ++i)
	{
		int firstSegment {}, secondSegment {}, thirdSegment {};
		std::cout << "Enter the lengths of the sides of the triangle separated by spaces #" << (i + 1) << ": ";
		std::cin >> firstSegment >> secondSegment >> thirdSegment;  // Чтение длин сторон треугольника из ввода

		// Проверка условия треугольника с использованием оператора тернарного условия
		bool answer = ((firstSegment + secondSegment > thirdSegment) && (secondSegment + thirdSegment > firstSegment) &&
					   (firstSegment + thirdSegment > secondSegment));

		myVector[i] = answer;  // Сохранение результата проверки в вектор
	}

	std::cout << "\nTriangle validity results:\n";

	// Цикл для вывода результатов
	for (int i: myVector)
	{
		std::cout << (i ? "Valid" : "Invalid") << ' ';  // Вывод каждого элемента вектора, разделенного пробелом
	}
	std::cout << std::endl;

	return 0;
}
