//
// Created by Shrekulka on 31.05.2023.
//

#include "String.h"

// Инициализация статического члена класса;
int String::amountObjects = 0;

// Статический метод;
int String::HowMany()
{
	return amountObjects;
}

int String::length() const
{
	return m_len;
}

// 1)
// Конструктор по умолчанию;
String::String() : m_len(0), m_str(nullptr)
{
	amountObjects++;
}

// или второй вариант;
//String::String() : m_len(0), m_str(new char[1])
//{
//	m_str[0] = '\0';
//  amountObjects;
//}
// или третий вариант;
//String::String()
//{
//	static const char* s = ""; // инициализируется однажды;
//	m_len = strlen(s);
//	m_str = new char[m_len + 1];
//	strcpy(m_str, s);
//  amountObjects++;
//}

// 2)
// Конструктор с параметрами (создание string из С-строки);
// m_len (strlen(s)) - установка размера;
// m_str (new char[m_len+1]) - выделение памяти;
// strcpy(m_str,s) - инициализация указателя (копирование строки);
// amountObjects++ - корректировка счетчика объектов;
String::String(const char* s) : m_len(strlen(s)), m_str(new char[m_len + 1])
{
	strcpy(m_str, s);
	amountObjects++;
}

// 3)
// Конструктор копирования;
String::String(const String& s) : m_len(s.m_len), m_str(new char[m_len + 1])
{
	strcpy(m_str, s.m_str);
	amountObjects++;
}

// 4)
// Деструктор;
String::~String()
{
	--amountObjects;
	delete[]m_str;
}

// Методы перегруженных операций;

// Присвоение объекта String объекту String;
String& String::operator=(const String& other)
{
	// Проверка - присвоение объекта самому себе;
	if (this == &other)
	{
		return *this;
	}
	else
	{
		// Освобождение старой строки;
		delete[]m_str;
		// Установка длины строки;
		m_len = other.m_len;
		// Выделение памяти для новой строки;
		m_str = new char[m_len + 1];
		// Копирование строки;
		strcpy(m_str, other.m_str);
		// Возврат ссылки на вызывающий объект;
		return *this;
	}
}

// Присвоение С-строки объекту String;
String& String::operator=(const char* other)
{
	delete[]m_str;
	// Установка длины строки;
	m_len = strlen(other);
	// Выделение памяти для новой строки;
	m_str = new char[m_len + 1];
	// Копирование строки;
	strcpy(m_str, other);
	// Возврат ссылки на вызывающий объект;
	return *this;
}

// Доступ для чтения и записи отдельных символов в не константном объекте String;
char& String::operator[](int i)
{
	return m_str[i];
}

// Доступ только для чтения отдельных символов в константном объекте String;
const char& String::operator[](int i) const
{
	return m_str[i];
}


// Дружественные методы перегруженных операций;
// strcmp () - возвращает отрицательное значение, если первый аргумент предшествует второму по алфавиту, 0 - если строки
// одинаковы, и положительное значение, если превая строка по алфавиту следует за второй;
// т.е.
// bool operator<(const String& st1, const String& st2)
// {
//	if (strcmp(st1.m_str, st2.m_str) > 0)
//	{
//		return true;
//	}
//	else
//	{
//		return false;
//	}
// }

bool operator<(const String& st1, const String& st2)
{
	return (strcmp(st1.m_str, st2.m_str) < 0);
}

bool operator>(const String& st1, const String& st2)
{
	return st2.m_str < st1.m_str;
}

bool operator==(const String& st1, const String& st2)
{
	return (strcmp(st1.m_str, st2.m_str) == 0);
}

ostream& operator<<(ostream& os, const String& st)
{
	os << st.m_str;
	return os;
}

istream& operator>>(istream& is, String& st)
{
	char tmp[String::LIM];
	is.get(tmp, String::LIM);
	if (is)
	{
		st = tmp;
	}
	while (is && is.get() != '\n')
	{
		continue;
	}
	return is;
}