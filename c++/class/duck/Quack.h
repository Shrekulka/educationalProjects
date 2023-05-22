//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_QUACK_H
#define DUCK_QUACK_H


class Quack : public Quackable
{
public:
	void CQuacking() override;
};


#endif //DUCK_QUACK_H
