//
// Created by Shrekulka on 13.05.2023.
//
#pragma once  // Директива препроцессора для обеспечения однократного включения заголовочного файла

#include "stdafx.h"  // Включаем заголовочный файл stdafx.h

#ifndef ODD_NUMBERS_TO_BEGINNING_EVEN_NUMBERS_TO_END_ARRAY_SOLUTION283_H  // Макрос для условной компиляции заголовочного файла
#define ODD_NUMBERS_TO_BEGINNING_EVEN_NUMBERS_TO_END_ARRAY_SOLUTION283_H


class Solution283
{
public:
	void moveZeroes(std::vector<int>& nums);  // Объявление метода moveZeroes, перемещающего нули в конец вектора

	void moveNumbers(std::vector<int>& nums);  // Объявление метода moveNumbers, перемещающего нечетные числа в начало вектора

	void show(std::vector<int>& nums);  // Объявление метода show, выводящего содержимое вектора
};


#endif //ODD_NUMBERS_TO_BEGINNING_EVEN_NUMBERS_TO_END_ARRAY_SOLUTION283_H
