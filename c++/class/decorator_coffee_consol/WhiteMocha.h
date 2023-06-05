//
// Created by Shrekulka on 31.05.2023.
//

#pragma once

#include "pch.h"

#ifndef DECORATORCOFFEE_CONSOL_WHITEMOCHA_H
#define DECORATORCOFFEE_CONSOL_WHITEMOCHA_H

// Определение класса WhiteMocha, который является производным классом от Mocha.
class WhiteMocha : public Mocha
{
protected:

	// Объявление указателя на объект класса Beverage с именем beverage. Этот указатель будет использоваться для
	// хранения ссылки на объект напитка.
	Beverage* beverage;

public:

	// Объявление конструктора класса WhiteMocha, который принимает указатель на объект класса Beverage в качестве
	// аргумента. Конструктор будет использоваться для создания объекта класса WhiteMocha и установки указателя beverage
	// на переданный объект.
	WhiteMocha(Beverage*);

	// Объявление функции Cost(), которая возвращает значение типа double. Функция будет переопределена в классе
	// WhiteMocha для определения стоимости напитка с добавкой молочного мокко.
	double Cost();

	// Объявление функции GetDescription(), которая возвращает значение типа string. Функция будет переопределена в
	// классе WhiteMocha для получения описания напитка с добавкой молочного мокко.
	string GetDescription();

	// Определение деструктора класса WhiteMocha. Деструктор не содержит кода, так как освобождение памяти или других
	// ресурсов не требуется в данном случае.
	virtual ~WhiteMocha();

};


#endif //DECORATORCOFFEE_CONSOL_WHITEMOCHA_H

