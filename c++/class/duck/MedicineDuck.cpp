//
// Created by Shrekulka on 13.05.2023.
//

#include "MedicineDuck.h"


MedicineDuck::MedicineDuck() : Duck()
{
	this->m_name = "MedicineDuck";
	this->m_flyable = new NotFlight();
	this->m_quackable = new NotQuack();
}

MedicineDuck::MedicineDuck(const string& name) : Duck(name)
{
	this->m_flyable = new NotFlight();
	this->m_quackable = new NotQuack();
}

MedicineDuck::MedicineDuck(const MedicineDuck& other) : Duck(other)
{
	this->m_flyable = other.m_flyable;
	this->m_quackable = other.m_quackable;
}

void MedicineDuck::CShow()
{
	this->CSweem();
	this->m_flyable->CFly();
	this->m_quackable->CQuacking();
}

MedicineDuck::~MedicineDuck()
{
}