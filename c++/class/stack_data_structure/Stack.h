//
// Created by Shrekulka on 29.05.2023.
//
#pragma once

#include "pch.h"

#ifndef STACKTEMPLATE_STACK_H
#define STACKTEMPLATE_STACK_H


template<typename T>

class Stack
{
private:
	// константа, специфичная для класса;
	static const int MAXX = 10;
	// хранит элементы стека;
	T items[MAXX];
	// индекс вершины стека;
	int top;

public:
	Stack();

	Stack(const Stack<T>& other);

	~Stack();

	bool isempty() const;

	bool isfull() const;

	// push ( ) возвращает false, если стек полон, и true - в противном случае;
	bool push(const T& item); // добавляет элемент в стек;

	// рор ( ) возвращает false, если стек пуст, и true - в противном случае;
	bool рор(T& item); // выталкивает элемент с вершины стека;

};

template<typename T>
Stack<T>::Stack() : top(0)
{
}

template<typename T>
bool Stack<T>::isempty() const
{
	return top == 0;
}

template<typename T>
bool Stack<T>::isfull() const
{
	return top == MAXX;
}

template<typename T>
bool Stack<T>::push(const T& other)
{
	if (top < MAXX)
	{
		items[top++] = other;
		return true;
	}
	return false;
}

template<typename T>
bool Stack<T>::рор(T& other)
{
	if (top > 0)
	{
		items[--top] = other;
		return true;
	}
	return false;
}

template<typename T>
Stack<T>::~Stack()
{

}

template<typename T>
Stack<T>::Stack(const Stack<T>& other): top(other.top)
{
}

#endif //STACKTEMPLATE_STACK_H