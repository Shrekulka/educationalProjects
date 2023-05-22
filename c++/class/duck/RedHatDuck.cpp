//
// Created by Shrekulka on 13.05.2023.
//

#include "RedHatDuck.h"

RedHatDuck::RedHatDuck() : Duck()
{
	this->m_name = "RedHatDuck";
	this->m_flyable = new Flight();
	this->m_quackable = new Quack();
}

RedHatDuck::RedHatDuck(const string& name) : Duck(name)
{
	this->m_flyable = new Flight();
	this->m_quackable = new Quack();
}

RedHatDuck::RedHatDuck(const RedHatDuck& other) : Duck(other)
{
	this->m_flyable = other.m_flyable;
	this->m_quackable = other.m_quackable;
}


void RedHatDuck::CShow()
{
	this->CSweem();
	this->m_flyable->CFly();
	this->m_quackable->CQuacking();
}

RedHatDuck::~RedHatDuck()
{
}