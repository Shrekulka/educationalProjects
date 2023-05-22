//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_FLYABLE_H
#define DUCK_FLYABLE_H


class Flyable
{
public:
	virtual void CFly() = 0;

};


#endif //DUCK_FLYABLE_H
