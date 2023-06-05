//
// Created by Shrekulka on 31.05.2023.
//

#pragma once

#include "pch.h"

#ifndef CLASSSTRING_STRING_H
#define CLASSSTRING_STRING_H


class String
{
private:
	int m_len; // длина строки;
	char* m_str; // указатель на строку;
	static int amountObjects; // количество объектов;
	static const int LIM = 80; // предел ввода на cin;

public:

// Конструкторы и деструктор
	String();

	String(const char* s);

	String(const String& s);

	~String();

// Методы класса
	int length() const;

	String& operator=(const String& other);

	String& operator=(const char* other);

	char& operator[](int i);

	const char& operator[](int i) const;

// Дружественные функции перегруженных операций;
	friend bool operator<(const String& st1, const String& st2);

	friend bool operator>(const String& st1, const String& st2);

	friend bool operator==(const String& st1, const String& st2);

	friend ostream& operator<<(ostream& os, const String& st);

	friend istream& operator>>(istream& is, String& st);

// Объявление статической функции HowMany, возвращающей количество объектов класса String.
	static int HowMany();

};


#endif //CLASSSTRING_STRING_H
