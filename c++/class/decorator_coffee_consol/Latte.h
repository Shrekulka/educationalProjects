//
// Created by Shrekulka on 31.05.2023.
//

#pragma once

#include "pch.h"

#ifndef DECORATORCOFFEE_CONSOL_LATTE_H
#define DECORATORCOFFEE_CONSOL_LATTE_H

// Определение класса Latte, который является производным классом от Beverage.
class Latte : public Beverage
{
protected:

	// Объявление переменной description типа string, которая будет хранить описание напитка.
	string description;

public:

	// Объявление функции Cost(), которая возвращает значение типа double. Функция будет определена внутри класса и
	// используется для получения стоимости напитка.
	double Cost();

	// Объявление функции GetDescription(), которая возвращает значение типа string. Функция будет определена внутри
	// класса и используется для получения описания напитка.
	string GetDescription();

	// Объявление конструктора класса Latte. Конструктор не принимает аргументов и будет определен внутри класса.
	Latte();

	// Объявление виртуального деструктора класса Latte. Деструктор будет определен внутри класса и используется для
	// освобождения памяти, занимаемой объектами класса.
	virtual ~Latte();

};

#endif //DECORATORCOFFEE_CONSOL_LATTE_H
