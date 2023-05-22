//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_MALLARDDUCK_H
#define DUCK_MALLARDDUCK_H


class MallardDuck : public Duck
{
public:
	MallardDuck();

	MallardDuck(const string&);

	MallardDuck(const MallardDuck&);

	void CShow() override;

	~MallardDuck() override;
};

#endif //DUCK_MALLARDDUCK_H
