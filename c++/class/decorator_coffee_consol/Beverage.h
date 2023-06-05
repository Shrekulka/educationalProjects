//
// Created by Shrekulka on 31.05.2023.
//

#pragma once

#include "pch.h"

#ifndef DECORATORCOFFEE_CONSOL_BEVERAGE_H
#define DECORATORCOFFEE_CONSOL_BEVERAGE_H

// Определение класса Beverage, который является абстрактным базовым классом для напитков.
class Beverage
{
public:

	// Объявление чисто виртуальной функции, которая должна быть переопределена в производных классах. Эта функция
	// возвращает стоимость напитка в виде числа с плавающей запятой.
	virtual double Cost() = 0;

	// Объявление чисто виртуальной функции, которая должна быть переопределена в производных классах. Эта функция
	// возвращает описание напитка в виде строки.
	virtual string GetDescription() = 0;

	// Определение конструктора и деструктора класса.
	Beverage();

	virtual ~Beverage();
};


#endif //DECORATORCOFFEE_CONSOL_BEVERAGE_H
