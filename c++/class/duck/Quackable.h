//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_QUACKABLE_H
#define DUCK_QUACKABLE_H


class Quackable
{
public:
	virtual void CQuacking() = 0;

};


#endif //DUCK_QUACKABLE_H
