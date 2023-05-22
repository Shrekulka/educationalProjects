#include "stdafx.h"



























int main()
{
	int sizeLake = 5;
	Lake monster;
	MallardDuck mallardDuck;
	RedHatDuck redHatDuck;
	RubberDuck rubberDuck;
	MedicineDuck medicineDuck;
	monster.CCreateLake(mallardDuck, redHatDuck, rubberDuck, medicineDuck, sizeLake);

	return 0;
}







RedHatDuck::RedHatDuck() : Duck()
{
	this->m_name = "RedHatDuck";
	this->m_flyable = new Flight();
	this->m_quackable = new Quack();
}

RedHatDuck::RedHatDuck(const string &name) : Duck(name)
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

RubberDuck::RubberDuck() : Duck()
{
	this->m_name = "RubberDuck";
	this->m_flyable = new NotFlight();
	this->m_quackable = new NotQuack();
}

RubberDuck::RubberDuck(const string &name) : Duck(name)
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

MedicineDuck::MedicineDuck() : Duck()
{
	this->m_name = "MedicineDuck";
	this->m_flyable = new NotFlight();
	this->m_quackable = new NotQuack();
}

MedicineDuck::MedicineDuck(const string &name) : Duck(name)
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


void Flight::CFly()
{
	cout << "I can fly!\n";
}

void NotFlight::CFly()
{
	cout << "I can't  fly!\n";
}

void Quack::CQuacking()
{
	cout << "I can quack!\n";
}

void NotQuack::CQuacking()
{
	cout << "I can't quack!\n";
}

Hunter::Hunter() : m_nameHunter("Kuzya")
{
}

Hunter::Hunter(const string &name) : m_nameHunter(name)
{
}

Hunter::Hunter(const Hunter& other) : m_nameHunter(other.m_nameHunter)
{
}

void Hunter::CShow() const
{
	cout << "I am a drunken hunter " << m_nameHunter << " !!!\n" << '\n';
}

Hunter::~Hunter()
{
}

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















