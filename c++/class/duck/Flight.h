//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_FLIGHT_H
#define DUCK_FLIGHT_H


class Flight : public Flyable
{
public:
	void CFly() override;
};


#endif //DUCK_FLIGHT_H
