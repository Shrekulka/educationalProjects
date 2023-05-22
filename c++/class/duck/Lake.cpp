//
// Created by Shrekulka on 13.05.2023.
//

#include "Lake.h"

Lake::Lake()
{
}

Lake::Lake(Duck* duck)
{
	for (auto x: m_dack)
	{
		m_dack.push_back(duck);
	}
}

Lake::Lake(const Lake& other)
{
	this->m_dack = other.m_dack;
}

void
Lake::CCreateLake(MallardDuck& mallardDuck, RedHatDuck& redHatDuck, RubberDuck& rubberDuck, MedicineDuck& medicineDuck,
		int& size)
{
	srand(time(nullptr));
	int choice = rand() % 4;
	for (int i = 0; i < size; ++i)
	{
		choice = rand() % 4;
		switch (choice)
		{
		case 0:
			// m_dack.push_back(new MallardDuck());// создание объекта MallardDuck, тогда в Lake::CCreateLake мы ничего не передаем;
			m_dack.push_back(&mallardDuck);
			break;
		case 1:
			m_dack.push_back(&redHatDuck);
			break;
		case 2:
			m_dack.push_back(&rubberDuck);
			break;
		case 3:
			m_dack.push_back(&medicineDuck);
			break;
		}
	}
	CShow();
	if (choice % 2)
	{
		CAHunterAppeared();
	}
}

void Lake::CShow() const
{

	for (int i = 0; i < m_dack.size(); i++)
	{
		cout << "№ " << i+1 << '\n';
		m_dack[i]->CShow();
		cout << '\n';
	}
	cout << "On the lake " << CGetLengthDuck() << " ducks!" << '\n' << '\n';
}

int Lake::CGetLengthDuck() const
{
	return m_dack.size();
}

void Lake::CDeleteMallardDuck()
{
	for (vector<Duck*>::iterator it = m_dack.begin(); it != m_dack.end();)
	{
		// if (dynamic_cast<MallardDuck*>(*it) || dynamic_cast<RedHatDuck*>(*it)) // для одного метода
		if (dynamic_cast<MallardDuck*>(*it))
		{
			it = m_dack.erase(it);
		}
		else
		{
			++it;
		}
	}
}

void Lake::CDeleteRedHatDuck()
{
	for (vector<Duck*>::iterator it = m_dack.begin(); it != m_dack.end();)
	{
		if (dynamic_cast<RedHatDuck*>(*it))
		{
			it = m_dack.erase(it);
		}
		else
		{
			++it;
		}
	}
}

void Lake::CAHunterAppeared()
{
	this->m_hunt = new Hunter();

	this->m_hunt->CShow();
	CDeleteMallardDuck();
	CDeleteRedHatDuck();
	CShow();
}

Lake::~Lake()
{
}