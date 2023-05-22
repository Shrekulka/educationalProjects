//
// Created by Shrekulka on 23.05.2023.
//

#include "Rectangle.h"

Rectangle::Rectangle(int w, int h) // Конструктор класса Rectangle с параметрами w и h (по умолчанию 1)
{
	width = new int; // Выделение памяти для переменной width
	height = new int; // Выделение памяти для переменной height
	*width = w; // Присваивание значение w переменной width
	*height = h; // Присваивание значение h переменной height
}

// Конструктор копирования для класса Rectangle
Rectangle::Rectangle(const Rectangle& src)
{
	// Выделение памяти для нового объекта
	width = new int;
	height = new int;

	// Копирование значений из исходного объекта
	*width = *(src.width);
	*height = *(src.height);
}

Rectangle& Rectangle::operator=(const Rectangle& src)
{
	// Проверка на самоприсваивание
	if (this == &src)
	{
		return *this;
	}

	// Освобождение занятой памяти
	delete width;
	delete height;

	// Выделение памяти
	width = new int;
	height = new int;

	// Копирование значений из исходного объекта
	*width = *(src.width);
	*height = *(src.height);

	// Возвращение ссылки на перезаписанный объект
	return *this;
}

Rectangle::~Rectangle() // Деструктор класса Rectangle
{
	delete width; // Освобождение памяти, занятой переменной width
	delete height; // Освобождение памяти, занятой переменной height
}

void Rectangle::display() const // Метод display для вывода ширины и высоты прямоугольника
{
	cout << "Width: " << *width << endl; // Вывод ширины
	cout << "Height: " << *height << endl; // Вывод высоты
}

int Rectangle::setWidth(int w) // Метод setWidth для установки значения ширины
{
	*width = w; // Присваивание нового значения ширины
}

int Rectangle::setHeight(int h) // Метод setHeight для установки значения высоты
{
	*height = h; // Присваивание нового значения высоты
}