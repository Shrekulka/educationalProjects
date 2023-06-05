//
// Created by Shrekulka on 31.05.2023.
//

#include "pch.h"

#include "WhiteMocha.h"


// Определение конструктора класса WhiteMocha, который принимает указатель на объект класса Beverage в качестве аргумента.
// Внутри конструктора, указатель beverage класса WhiteMocha устанавливается равным переданному указателю b, чтобы класс
// WhiteMocha имел доступ к объекту напитка.
WhiteMocha::WhiteMocha(Beverage* b) : Mocha(b)
{
	this->beverage = b;
}

// Определение деструктора класса WhiteMocha. Деструктор не содержит кода, так как освобождение памяти или других
// ресурсов не требуется в данном случае.
WhiteMocha::~WhiteMocha()
{

}

// Определение функции GetDescription() класса WhiteMocha. Внутри функции возвращается строка, состоящая из описания
// напитка, полученного с помощью вызова функции GetDescription() у объекта beverage, и дополнительного текста
// "WhiteMocha", который указывает на присутствие добавки молочного мокко.
string WhiteMocha::GetDescription()
{
	return (beverage->GetDescription() + ",WhiteMocha");
}

// Определение функции Cost() класса WhiteMocha. Внутри функции возвращается стоимость добавки молочного мокко, равная
// 0.75, плюс стоимость напитка, полученная с помощью вызова функции Cost() у объекта beverage. Это общая стоимость
// напитка с добавкой молочного мокко.
double WhiteMocha::Cost()
{
	return (0.75 + beverage->Cost());
}
