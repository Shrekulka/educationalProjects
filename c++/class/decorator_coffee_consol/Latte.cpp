//
// Created by Shrekulka on 31.05.2023.
//

#include "pch.h"
#include "Latte.h"

// Определение конструктора класса Latte.
Latte::Latte()
{

}

// Определение деструктора класса Latte.
Latte::~Latte()
{

}

// Определение функции GetDescription() класса Latte, которая возвращает значение типа string. Внутри функции
// устанавливается значение переменной description равное строке "Latte", а затем это значение возвращается.
string Latte::GetDescription()
{
	return description = "Latte";
}

// Определение функции Cost() класса Latte, которая возвращает значение типа double. Внутри функции возвращается
// значение 2.15, которое представляет стоимость напитка Latte.
double Latte::Cost()
{
	return 2.15;
}
