//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_RUBBERDUCK_H
#define DUCK_RUBBERDUCK_H


class RubberDuck : public Duck
{
public:
	RubberDuck();

	RubberDuck(const string &);

	RubberDuck(const RubberDuck&);

	void CShow() override;

	~RubberDuck() override;
};


#endif //DUCK_RUBBERDUCK_H
