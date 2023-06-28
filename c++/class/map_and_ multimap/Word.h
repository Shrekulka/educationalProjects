//
// Created by Shrekulka on 23.05.2023.
//

#pragma once  // Директива препроцессора, обеспечивающая однократное включение данного заголовочного файла.

#include "pch.h"  // Включение предкомпилированного заголовочного файла для оптимизации компиляции.

#ifndef MAP_WORD_H
#define MAP_WORD_H

class Word
{
private:
	char mstr[20];  // Приватное членов класса - массив символов для хранения слова.

public:
	Word();  // Конструктор класса без аргументов.
	Word(char* s);  // Конструктор класса с передачей строки в качестве аргумента.
	~Word();  // Деструктор класса.

	char* get();  // Функция для получения строки из объекта класса Word.

	friend bool operator<(Word, const Word);  // Перегрузка оператора < для сравнения объектов класса Word.

};

#endif //MAP_WORD_H