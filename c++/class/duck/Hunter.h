//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_HUNTER_H
#define DUCK_HUNTER_H


class Hunter
{
	string m_nameHunter;
public:
	Hunter();

	Hunter(const string &);

	Hunter(const Hunter&);

	void CShow()const;

	virtual ~Hunter();
};


#endif //DUCK_HUNTER_H
