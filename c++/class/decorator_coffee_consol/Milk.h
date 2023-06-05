//
// Created by Shrekulka on 31.05.2023.
//

#pragma once

#include "pch.h"

#ifndef DECORATORCOFFEE_CONSOL_MILK_H
#define DECORATORCOFFEE_CONSOL_MILK_H

// Определение класса Milk, который является производным классом от Additives.
class Milk : public Additives
{
protected:

// Объявление указателя на объект beverage.
	Beverage* beverage;

public:

	// Определение функции Cost() класса Milk, которая возвращает значение типа double. Внутри функции будет реализован
	// расчет стоимости добавки "молоко" к напитку.
	double Cost();

	// Определение функции GetDescription() класса Milk, которая возвращает значение типа string. Внутри функции будет
	// возвращаться описание добавки "молоко".
	string GetDescription();

	// Определение виртуального деструктора класса Milk, который будет вызываться при удалении объектов класса Milk и
	// его производных классов.
	Milk(Beverage*);

	// Определение виртуального деструктора класса Milk. Деструктор освобождает ресурсы, если таковые были выделены
	// внутри объекта Milk.
	virtual ~Milk();

};

#endif //DECORATORCOFFEE_CONSOL_MILK_H
