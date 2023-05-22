//
// Created by Shrekulka on 13.05.2023.
//

#include "Duck.h"


Duck::Duck() : m_name("duck"), m_flyable(nullptr), m_quackable(nullptr)
{
}

Duck::Duck(const string& name) : m_name(name), m_flyable(nullptr), m_quackable(nullptr)
{
}

Duck::Duck(const Duck& other) : m_name(other.m_name)
{
	if (other.m_flyable != nullptr)
		this->m_flyable = other.m_flyable;
	else
		this->m_flyable = nullptr;

	if (other.m_quackable != nullptr)
		this->m_quackable = other.m_quackable;
	else
		this->m_quackable = nullptr;
}

void Duck::CSweem()
{
	cout << "I am a " << m_name << " and I can swim!\n";
}

void Duck::CShow()
{
}

Duck::~Duck()
{
	delete m_flyable;
	delete m_quackable;
}