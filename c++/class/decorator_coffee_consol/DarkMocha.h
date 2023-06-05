//
// Created by Shrekulka on 31.05.2023.
//

#pragma once

#include "pch.h"

#ifndef DECORATORCOFFEE_CONSOL_DARKMOCHA_H
#define DECORATORCOFFEE_CONSOL_DARKMOCHA_H

// Определение класса DarkMocha, который является производным классом от Mocha.
class DarkMocha : public Mocha
{
protected:

	// Объявление указателя на объект типа Beverage с именем beverage. Этот указатель будет использоваться для хранения
	// ссылки на напиток, к которому добавляется "DarkMocha".
	Beverage* beverage;

public:

	// Объявление конструктора класса DarkMocha, который принимает указатель на объект типа Beverage. Конструктор будет
	// использоваться для создания объектов класса DarkMocha и устанавливать beverage в переданный объект Beverage.
	DarkMocha(Beverage*);

	// Объявление функции Cost(), которая переопределяет виртуальную функцию Cost() из базового класса Mocha. Функция
	// будет возвращать стоимость напитка DarkMocha, учитывая стоимость базового напитка beverage.
	double Cost();

	// Объявление функции GetDescription(), которая переопределяет виртуальную функцию GetDescription() из базового
	// класса Mocha. Функция будет возвращать описание напитка DarkMocha, включая описание базового напитка beverage.
	string GetDescription();

	// Объявление виртуального деструктора класса DarkMocha.
	virtual ~DarkMocha();

};


#endif //DECORATORCOFFEE_CONSOL_DARKMOCHA_H
