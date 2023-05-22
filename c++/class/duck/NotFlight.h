//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_NOTFLIGHT_H
#define DUCK_NOTFLIGHT_H


class NotFlight : public Flyable
{
public:
	void CFly() override;
};


#endif //DUCK_NOTFLIGHT_H
