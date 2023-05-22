//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_LAKE_H
#define DUCK_LAKE_H


class Lake
{
protected:
	vector<Duck*> m_dack;
	Hunter* m_hunt;

	void CDeleteMallardDuck();

	void CDeleteRedHatDuck();

public:
	Lake();

	Lake(Duck*);

	Lake(const Lake&);

	void CCreateLake(MallardDuck&, RedHatDuck&, RubberDuck&, MedicineDuck&, int&);

	void CShow()const;

	int CGetLengthDuck() const;


	void CAHunterAppeared();

	virtual ~Lake();
};


#endif //DUCK_LAKE_H
