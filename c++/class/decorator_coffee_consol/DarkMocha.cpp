//
// Created by Shrekulka on 31.05.2023.
//

#include "pch.h"

#include "DarkMocha.h"


DarkMocha::DarkMocha(Beverage* b) : Mocha(b)
{
	this->beverage = b;
}

DarkMocha::~DarkMocha()
{

}

string DarkMocha::GetDescription()
{
	return (beverage->GetDescription() + ",DarkMocha");
}

double DarkMocha::Cost()
{
	return (0.7 + beverage->Cost());
}