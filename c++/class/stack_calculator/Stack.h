//
// Created by Shrekulka on 29.05.2023.
//


#pragma once

#include "pch.h"

#ifndef STACKTEMPLATE_STACK_H
#define STACKTEMPLATE_STACK_H

const int MaxStackSize = 100;

template<typename T>
class Stack
{
private:
	T m_mas[MaxStackSize];  // хранит элементы стека
	int m_count;  // индекс вершины стека
	int m_len;  // длина стека

public:
	Stack();
	Stack(int);
	Stack(const Stack<T>& other);
	virtual ~Stack();

	bool isempty() const;
	bool isfull() const;
	void push(const T&);  // добавляет элемент в стек
	T pop();  // выталкивает элемент с вершины стека
	void clearStack();
	T Peek() const;  // возвращает значение вершины стека

	// Добавить перегрузку операторов ввода/вывода при необходимости

};

template<typename T>
class Calculator
{
private:
	Stack<T> S;

	void Enter(double num);
	bool GetTwoOperands(double& opnd1, double& opnd2);
	void Compute(char op);

public:
	Calculator();
	void Run();
	void Clear();
	const Stack<T>& getStack() const;
	virtual ~Calculator();
};

template<typename T>
Calculator<T>::Calculator()
{

}

template<typename T>
const Stack<T>& Calculator<T>::getStack() const
{
	return S;
}

template<typename T>
void Calculator<T>::Run()
{
	cout << "Программа калькулятора\n";
	cout << "Введите первое число: ";
	T firstNumber;
	cin >> firstNumber;
	S.push(firstNumber);

	char op;
	cout << "Введите оператор (+, -, *, /, ^): ";
	cin >> op;

	cout << "Введите второе число: ";
	T secondNumber;
	cin >> secondNumber;
	S.push(secondNumber);

	Compute(op);

	if (!S.isempty())
	{
		cout << "Результат: " << S.Peek() << '\n';
	}
	else
	{
		cout << "Ошибка: пустой стек\n";
	}

	cout << "Программа завершена\n";
}

template<typename T>
void Calculator<T>::Enter(double num)
{
	S.push(num);
}

template<typename T>
bool Calculator<T>::GetTwoOperands(double& opnd1, double& opnd2)
{
	if (S.isempty())
	{
		cout << "Отсутствует операнд\n";
		return false;
	}

	opnd1 = S.pop();

	if (S.isempty())
	{
		cout << "Отсутствует операнд\n";
		return false;
	}

	opnd2 = S.pop();
	return true;
}

template<typename T>
void Calculator<T>::Compute(char op)
{
	bool result;
	double operand1, operand2;
	result = GetTwoOperands(operand1, operand2);

	if (result)
	{
		switch (op)
		{
		case '+':
			S.push(operand2 + operand1);
			break;
		case '-':
			S.push(operand2 - operand1);
			break;
		case '*':
			S.push(operand2 * operand1);
			break;
		case '/':
			if (operand1 == 0.0)
			{
				cout << "Деление на ноль запрещено\n";
				S.clearStack();
			}
			else
			{
				S.push(operand2 / operand1);
			}
			break;
		case '^':
			S.push(pow(operand2, operand1));
			break;
		default:
			cout << "Неизвестный оператор\n";
			break;
		}
	}
}

template<typename T>
void Calculator<T>::Clear()
{
	S.clearStack();
}

template<typename T>
Calculator<T>::~Calculator()
{

}

template<typename T>
Stack<T>::Stack()
{
	m_count = 0;
	m_len = MaxStackSize;
}

template<typename T>
Stack<T>::Stack(int size)
{
	if (size <= 0 || size > MaxStackSize)
	{
		throw std::out_of_range("Некорректный размер стека");
	}

	m_count = 0;
	m_len = size;
}

template<typename T>
Stack<T>::Stack(const Stack<T>& other)
{
	m_count = other.m_count;
	m_len = other.m_len;

	for (int i = 0; i < m_count; i++)
	{
		m_mas[i] = other.m_mas[i];
	}
}

template<typename T>
Stack<T>::~Stack()
{

}

template<typename T>
bool Stack<T>::isempty() const
{
	return m_count == 0;
}

template<typename T>
bool Stack<T>::isfull() const
{
	return m_count == m_len;
}

template<typename T>
void Stack<T>::push(const T& item)
{
	if (isfull())
	{
		cout << "Стек полон\n";
		return;
	}

	m_mas[m_count++] = item;
}

template<typename T>
T Stack<T>::pop()
{
	if (isempty())
	{
		cout << "Стек пуст\n";
		return T();
	}

	return m_mas[--m_count];
}

template<typename T>
void Stack<T>::clearStack()
{
	m_count = 0;
}

template<typename T>
T Stack<T>::Peek() const
{
	if (isempty())
	{
		cout << "Стек пуст\n";
		return T();
	}

	return m_mas[m_count - 1];
}

#endif  // STACKTEMPLATE_STACK_H
