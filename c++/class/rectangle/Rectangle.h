//
// Created by Shrekulka on 23.05.2023.
//
#pragma once  // Директива препроцессора, обеспечивающая однократное включение файла в процессе компиляции.
#include "pch.h"  // Включение пользовательского заголовочного файла pch.h.

#ifndef RECTANGLE_RECTANGLE_H
#define RECTANGLE_RECTANGLE_H


class Rectangle // Объявление класса Rectangle
{
public: // Область доступа public

	Rectangle(int w = 1, int h = 1); // Конструктор класса Rectangle с параметрами w и h (по умолчанию 1)


	// Конструктор копирования для класса Rectangle
	Rectangle(const Rectangle& src);

	// Оператор присваивания
	Rectangle& operator=(const Rectangle& src);


	~Rectangle(); // Деструктор класса Rectangle


	void display() const; // Метод display для вывода ширины и высоты прямоугольника


	int setWidth(int w); // Метод setWidth для установки значения ширины


	int setHeight(int h); // Метод setHeight для установки значения высоты

private: // Область доступа private

	int* width, * height; // Указатели на переменные width и height
};



#endif //RECTANGLE_RECTANGLE_H
