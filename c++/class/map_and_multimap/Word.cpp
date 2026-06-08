//
// Created by Shrekulka on 23.05.2023.
//

#include "Word.h"  // Включение пользовательского заголовочного файла Word.h.

Word::Word()
{
	strcpy(mstr, "");  // Инициализация массива символов пустой строкой.
}

Word::Word(char* s)
{
	strcpy(mstr, s);  // Инициализация массива символов переданной строкой.
}

char* Word::get()
{
	return mstr;  // Возврат строки из объекта класса Word.
}

bool operator<(Word left, Word right)
{
	return strcmp(left.get(), right.get()) <
		   0;  // Сравнение двух объектов класса Word по значению их строк и возврат результата.
}

Word::~Word()
{
	// Деструктор класса Word (пустая реализация).
}



