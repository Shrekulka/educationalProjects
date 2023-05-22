//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_MEDICINEDUCK_H
#define DUCK_MEDICINEDUCK_H


class MedicineDuck : public Duck
{
public:
	MedicineDuck();

	MedicineDuck(const string &);

	MedicineDuck(const MedicineDuck&);

	void CShow() override;

	~MedicineDuck() override;
};

#endif //DUCK_MEDICINEDUCK_H
