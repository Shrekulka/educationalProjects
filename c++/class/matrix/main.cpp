#include "pch.h"

int main()
{
	// Взаимодействие с пользователем для создания и заполнения матрицы
	unsigned rows, cols;
	std::cout << "Введите количество строк матрицы: ";
	std::cin >> rows;
	std::cout << "Введите количество столбцов матрицы: ";
	std::cin >> cols;

	Matrix matrix(rows, cols);

	std::cout << "Введите элементы матрицы:\n";
	std::cin >> matrix;

	std::cout << "Введенная матрица:\n" << matrix << '\n';

	// Пример использования методов класса Matrix
	std::cout << "Выполняется копирование матрицы...\n";
	Matrix copy = matrix;  // Копирование матрицы
	std::cout << "Копирование завершено.\n";
	std::cout << "Скопированная матрица:\n" << copy << '\n';

	std::cout << "Выполняется транспонирование матрицы...\n";
	Matrix transposed = matrix.transpose();  // Транспонирование матрицы
	std::cout << "Транспонирование завершено.\n";
	std::cout << "Транспонированная матрица:\n" << transposed << '\n';

	// Взаимодействие с пользователем для доступа к элементам матрицы через оператор []
	unsigned rowIndex, colIndex;
	std::cout << "Введите индекс строки элемента, к которому хотите получить доступ: ";
	std::cin >> rowIndex;
	std::cout << "Введите индекс столбца элемента, к которому хотите получить доступ: ";
	std::cin >> colIndex;

	double value = matrix[rowIndex][colIndex];
	std::cout << "Значение элемента: " << value << '\n';

	// Пример использования операций над матрицами
	std::cout << "Выполняется сложение матриц...\n";
	Matrix sum = matrix + copy;  // Сложение матриц
	std::cout << "Сложение завершено.\n";
	std::cout << "Сумма матриц:\n" << sum << '\n';

	std::cout << "Выполняется вычитание матриц...\n";
	Matrix difference = matrix - copy;  // Вычитание матриц
	std::cout << "Вычитание завершено.\n";
	std::cout << "Разность матриц:\n" << difference << '\n';

	std::cout << "Выполняется умножение матриц...\n";
	Matrix product = matrix * copy;  // Умножение матриц
	std::cout << "Умножение завершено.\n";
	std::cout << "Произведение матриц:\n" << product << '\n';

	std::cout << "Выполняется возведение матрицы в степень...\n";
	Matrix power = matrix ^ 2;  // Возведение матрицы в степень 2
	std::cout << "Возведение в степень завершено.\n";
	std::cout << "Матрица, возведенная в степень 2:\n" << power << '\n';

	// Вычисление определителя матрицы
	std::cout << "Выполняется вычисление определителя матрицы...\n";
	double determinant = matrix.det();
	std::cout << "Определитель матрицы: " << determinant << '\n';
	std::cout << "Вычисление определителя завершено.\n";

	// Вычисление обратной матрицы
	std::cout << "Выполняется вычисление обратной матрицы...\n";
	Matrix inverseMatrix = matrix.inverse();
	std::cout << "Обратная матрица:\n" << inverseMatrix << '\n';
	std::cout << "Вычисление обратной матрицы завершено.\n";

	// Вычисление ранга матрицы
	std::cout << "Выполняется вычисление ранга матрицы...\n";
	int rank = matrix.rang();
	std::cout << "Ранг матрицы: " << rank << '\n';
	std::cout << "Вычисление ранга матрицы завершено.\n";

	// Вычисление произведения матрицы на скаляр
	double scalar = 2.0;
	std::cout << "Выполняется умножение матрицы на скаляр " << scalar << "...\n";
	Matrix scaledMatrix = matrix * scalar;
	std::cout << "Умножение на скаляр завершено.\n";

	// Вычисление деления матрицы на скаляр
	std::cout << "Выполняется деление матрицы на скаляр " << scalar << "...\n";
	Matrix dividedMatrix = matrix / scalar;
	std::cout << "Деление на скаляр завершено.\n";

	// Использование операций с присваиванием
	std::cout << "Выполняется сложение с присваиванием...\n";
	Matrix resultMatrix = matrix;
	resultMatrix += copy;  // Сложение с присваиванием
	std::cout << "Сложение с присваиванием завершено.\n";

	std::cout << "Выполняется вычитание с присваиванием...\n";
	resultMatrix -= copy;  // Вычитание с присваиванием
	std::cout << "Вычитание с присваиванием завершено.\n";

	std::cout << "Выполняется умножение с присваиванием...\n";
	resultMatrix *= copy;  // Умножение с присваиванием
	std::cout << "Умножение с присваиванием завершено.\n";

	std::cout << "Выполняется деление с присваиванием...\n";
	resultMatrix /= copy;  // Деление с присваиванием
	std::cout << "Деление с присваиванием завершено.\n";

	// Использование операторов сравнения матриц
	std::cout << "Выполняется проверка на равенство матриц...\n";
	bool isEqual = (matrix == copy);  // Проверка на равенство матриц
	std::cout << "Результат проверки на равенство: " << (isEqual ? "Матрицы равны" : "Матрицы не равны") << '\n';

	std::cout << "Выполняется проверка на неравенство матриц...\n";
	bool isNotEqual = (matrix != copy);  // Проверка на неравенство матриц
	std::cout << "Результат проверки на неравенство: " << (isNotEqual ? "Матрицы не равны" : "Матрицы равны") << '\n';

	// Демонстрация возведения матрицы в степень
	int exponent = 3;
	std::cout << "Выполняется возведение матрицы в степень " << exponent << "...\n";
	Matrix poweredMatrix = matrix ^ exponent;
	std::cout << "Возведение в степень завершено.\n";

	std::cout << "Матрица, возведенная в степень " << exponent << ":\n" << poweredMatrix << '\n';

	return 0;
}