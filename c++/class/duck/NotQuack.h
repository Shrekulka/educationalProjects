//
// Created by Shrekulka on 13.05.2023.
//

#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef DUCK_NOTQUACK_H
#define DUCK_NOTQUACK_H


class NotQuack : public Quackable
{
public:
	void CQuacking() override;
};


#endif //DUCK_NOTQUACK_H
