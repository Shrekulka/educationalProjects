//
// Created by Shrekulka on 31.05.2023.
//

#pragma once

#include "pch.h"

#ifndef DECORATORCOFFEE_CONSOL_DARKROAST_H
#define DECORATORCOFFEE_CONSOL_DARKROAST_H

// Определение класса DarkRoast, который является производным классом от Beverage.
class DarkRoast : public Beverage
{
protected:

// Объявление переменной description.
	string description;

public:

// Объявление конструктора, деструктора, функций Cost() и GetDescription().
	double Cost();

	string GetDescription();

	DarkRoast();

	DarkRoast(Beverage*);

	virtual ~DarkRoast();

};

#endif //DECORATORCOFFEE_CONSOL_DARKROAST_H
