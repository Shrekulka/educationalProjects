//
// Created by Shrekulka on 31.05.2023.
//
#pragma once

#include "pch.h"

#ifndef DECORATORCOFFEE_CONSOL_ADDITIVES_H
#define DECORATORCOFFEE_CONSOL_ADDITIVES_H

// Определение класса Additives, который является абстрактным базовым классом для добавок к напиткам.
class Additives : public Beverage
{
public:
	// Объявление чисто виртуальной функции, которая должна быть переопределена в производных классах. Она возвращает
	// описание добавки к напитку в виде строки.
	virtual string GetDescription() = 0;

	// Объявление чисто виртуальной функции, которая должна быть переопределена в производных классах. Она возвращает
	// стоимость добавки к напитку в виде числа с плавающей запятой.
	virtual double Cost() = 0;

// Определение конструктора и деструктора класса.
	Additives();

	virtual ~Additives();

};


#endif //DECORATORCOFFEE_CONSOL_ADDITIVES_H
