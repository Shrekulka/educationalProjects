//
// Created by Shrekulka on 31.05.2023.
//

#include "pch.h"

#include "Whip.h"

// Определение конструктора класса Whip, который принимает указатель на объект класса Beverage в качестве аргумента.
// Внутри конструктора, указатель beverage класса Whip устанавливается равным переданному указателю b, чтобы класс Whip
// имел доступ к объекту напитка.
Whip::Whip(Beverage* b)
{
	this->beverage = b;
}

// Определение деструктора класса Whip. Деструктор не содержит кода, так как освобождение памяти или других ресурсов не
// требуется в данном случае.
Whip::~Whip()
{

}

// Определение функции GetDescription() класса Whip. Внутри функции возвращается строка, состоящая из описания напитка,
// полученного с помощью вызова функции GetDescription() у объекта beverage, и дополнительного текста "Whip", который
// указывает на присутствие добавки сливок.
string Whip::GetDescription()
{
	return (beverage->GetDescription() + ",Whip");
}

// Определение функции Cost() класса Whip. Внутри функции возвращается стоимость добавки сливок, равная 0.5, плюс
// стоимость напитка, полученная с помощью вызова функции Cost() у объекта beverage. Это общая стоимость напитка с
// добавкой сливок.
double Whip::Cost()
{
	return (0.5 + beverage->Cost());
}
