//
// Created by Shrekulka on 13.05.2023.
//

#include "MallardDuck.h"

MallardDuck::MallardDuck() : Duck()
{
	this->m_name = "MallardDuck";
	this->m_flyable = new Flight();
	this->m_quackable = new Quack();
}

MallardDuck::MallardDuck(string &name) : Duck(name)
{
	this->m_flyable = new Flight();
	this->m_quackable = new Quack();
}

MallardDuck::MallardDuck(const MallardDuck& other) : Duck(other)
{
	this->m_flyable = other.m_flyable;
	this->m_quackable = other.m_quackable;
}

void MallardDuck::CShow()
{
	this->CSweem();
	this->m_flyable->CFly();
	this->m_quackable->CQuacking();
}

MallardDuck::~MallardDuck()
{
}