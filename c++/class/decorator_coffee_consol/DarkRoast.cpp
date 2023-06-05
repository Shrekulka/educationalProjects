//
// Created by Shrekulka on 31.05.2023.
//

#include "pch.h"
#include "DarkRoast.h"

// Определение конструктора класса DarkRoast.
DarkRoast::DarkRoast()
{

}

// Определение деструктора класса DarkRoast.
DarkRoast::~DarkRoast()
{

}

// Определение функции GetDescription() класса DarkRoast. Функция возвращает строку "Dark roast" в качестве описания для
// объектов класса DarkRoast.
string DarkRoast::GetDescription()
{
	// Возвращаем строку "Dark roast" и присваиваем ее переменной description.
	return description = "Dark roast";
}

// Определение функции Cost() класса DarkRoast. Функция возвращает число 2 в качестве стоимости для объектов класса
// DarkRoast.
double DarkRoast::Cost()
{
	// Возвращаем число 2 в качестве стоимости напитка.
	return 2;
}

// Определение конструктора класса DarkRoast, который принимает указатель на объект типа Beverage с именем bev.
DarkRoast::DarkRoast(Beverage* bev)
{
}