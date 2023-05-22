//
// Created by Shrekulka on 13.05.2023.
//

#include "RubberDuck.h"

RubberDuck::RubberDuck() : Duck()
{
	this->m_name = "RubberDuck";
	this->m_flyable = new NotFlight();
	this->m_quackable = new NotQuack();
}

RubberDuck::RubberDuck(const string& name) : Duck(name)
{
	this->m_flyable = new NotFlight();
	this->m_quackable = new NotQuack();
}

RubberDuck::RubberDuck(const RubberDuck& other) : Duck(other)
{
	this->m_flyable = other.m_flyable;
	this->m_quackable = other.m_quackable;
}

void RubberDuck::CShow()
{
	this->CSweem();
	this->m_flyable->CFly();
	this->m_quackable->CQuacking();
}

RubberDuck::~RubberDuck()
{
}