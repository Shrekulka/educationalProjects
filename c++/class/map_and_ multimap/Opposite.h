//
// Created by Shrekulka on 23.05.2023.
//

#pragma once  // Директива препроцессора, обеспечивающая однократное включение файла в процессе компиляции.

#include "pch.h"  // Включение пользовательского заголовочного файла pch.h.

#ifndef MAP_OPPOSITE_H  // Условная компиляция: проверка, что символьная константа MAP_OPPOSITE_H не определена.

#define MAP_OPPOSITE_H  // Определение символьной константы MAP_OPPOSITE_H.

class Opposite
{
private:
	char mstr[20];  // Массив символов для хранения строки.
public:
	Opposite();  // Конструктор класса Opposite без параметров.

	Opposite(char*);  // Конструктор класса Opposite с параметром - указателем на строку.

	~Opposite();  // Деструктор класса Opposite.

	char* get();  // Метод класса Opposite для получения строки.

};

#endif //MAP_OPPOSITE_H  // Конец условной компиляции.
