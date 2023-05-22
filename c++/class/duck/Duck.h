//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_DUCK_H
#define DUCK_DUCK_H


class Duck
{
protected:
	string m_name;
	Flyable* m_flyable;
	Quackable* m_quackable;
public:

	Duck();

	Duck(const string&);

	Duck(const Duck&);

	virtual void CShow() = 0;

	void CSweem();

	virtual ~Duck();
};

#endif //DUCK_DUCK_H
