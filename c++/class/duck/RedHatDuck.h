//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_REDHATDUCK_H
#define DUCK_REDHATDUCK_H


class RedHatDuck : public Duck
{
public:
	RedHatDuck();

	RedHatDuck(const string &);

	RedHatDuck(const RedHatDuck&);

	void CShow() override;

	~RedHatDuck() override;
};

#endif //DUCK_REDHATDUCK_H
