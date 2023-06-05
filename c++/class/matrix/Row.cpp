//
// Created by Shrekulka on 31.05.2023.
//

#include "Row.h"

// Конструктор по-умолчанию
Row::Row() :
// Устанавливаем размер строки по-умолчанию
		_size(1)
{
	// Выделяем память под строку
	_row = new double[_size];

	// Заполняем строку нулевыми значениями
	for (unsigned i = 0; i < _size; ++i)
		_row[i] = 0.0;
}

// Конструктор с параметрами
// size - размер строки
// fill - значение, которым изначально будет заполнена строка (по-умолчанию 0)
Row::Row(unsigned size, double fill) :
// Устанавливаем размер строки
		_size(size)
{
	// Выделяем память под строку
	_row = new double[_size];

	// Заполняем строку желаемыми значениями
	for (unsigned i = 0; i < _size; ++i)
		_row[i] = fill;
}

// Конструктор копирования
Row::Row(const Row& original) :
// Устанавливаем размер строки
		_size(original._size)
{
	// Выделяем память под строку
	_row = new double[_size];

	// Инициализируем элементы новой строки
	// элементами строки original
	for (unsigned i = 0; i < _size; ++i)
		_row[i] = original._row[i];
}

// Деструктор
Row::~Row()
{
	// Освобождаем память, отведённую под строку
	delete[] _row;
}

// Функция, возвращающая размер строки
unsigned Row::size() const
{
	// Возвращаем размер строки
	return _size;
}

// Функция изменения размера строки
void Row::resize(unsigned size, double fill)
{
	// Если исходный размер строки не
	// совпадает с желаемым
	if (_size != size)
	{
		// Устанавливаем размер строки
		// равным желаемому
		_size = size;

		// Освобождаем память из-под исходной строки
		delete[] _row;

		// Выделяем память под строку нового размера
		_row = new double[_size];
	}

	// Заполняем строку желаемыми значениями
	for (unsigned i = 0; i < _size; ++i)
		_row[i] = fill;
}

// Перегруженный оператор взятия значения по индексу
double& Row::operator[](unsigned index)
{
	// Возвращаем ссылку на желаемое значение
	return _row[index];
}

// Перегруженный оператор взятия значения по индексу (константный)
const double& Row::operator[](unsigned index) const
{
	// Возвращаем константную ссылку на желаемое значение
	return _row[index];
}

// Перегруженный оператор вывода из потока input
std::istream& operator>>(std::istream& input, Row& rhs)
{
	// Идём по элементам очередной строки
	for (unsigned i = 0; i < rhs._size; ++i)
		// Выводим значение из потока
		// input в очередной элемент
		// строки
		input >> rhs._row[i];

	// Возвращаем ссылку на поток input
	return input;
}

// Перегруженный оператор ввода в поток output
std::ostream& operator<<(std::ostream& output, const Row& rhs)
{
	// Идём по элементам очередной строки
	for (unsigned i = 0; i < rhs._size; ++i)
	{
		// Если очередной элемент
		// отрицательный - выводим
		// в поток output знак "минус"
		if (rhs._row[i] < 0.0)
		{
			output << '-';
			// Иначе - выводим пробел
		}
		else
		{
			output << ' ';
		}

		// Выводим модуль элемента в поток output
		output << (rhs._row[i] < 0.0 ? -rhs._row[i] : rhs._row[i]) << "\t";
	}

	// Возвращаем ссылку на поток output
	return output;
}

// Перегруженный оператор сравнения строк
bool Row::operator==(const Row& rhs) const
{
	// Если размеры строк не совпадают, то строки заведомо не равны
	if (_size != rhs._size)
	{
		return false;
	}

	// Если на какие-либо значения строк различаются,
	// то строки не равны
	for (unsigned i = 0; i < _size; ++i)
		if (_row[i] != rhs._row[i])
		{
			return false;
		}

	// Если как размеры, так и все элементы строк совпадают,
	// то строки равны
	return true;
}

// Перегруженный оператор неравенства строк
bool Row::operator!=(const Row& rhs) const
{
	// Используется уже реализованный оператор сравнения строк
	return !(*this == rhs);
}

// Перегруженный оператор присваивания одной строки другой
const Row& Row::operator=(const Row& rhs)
{
	// Проверка на самоприсваивание
	if (this != &rhs)
	{
		// Если размеры строк не совпадают
		if (_size != rhs._size)
		{
			// Очищаем память из-под старой строки
			delete[] _row;

			// Устанавливаем новый размер
			_size = rhs._size;

			// Выделяем память под новую строку
			_row = new double[_size];
		}

		// Заполняем новую строку элементами из
		// присваиваемой
		for (unsigned i = 0; i < _size; ++i)
			_row[i] = rhs._row[i];
	}

	return *this;
}
