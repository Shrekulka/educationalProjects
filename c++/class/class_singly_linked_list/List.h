//
// Created by Shrekulka on 29.05.2023.
//

#pragma once

#include "pch.h"

#ifndef CLASS_SINGLY_LINKED_LIST_LIST_H
#define CLASS_SINGLY_LINKED_LIST_LIST_H

template<typename T>
class List
{
public:
	List();

	~List();

	// Добавить данные в наш односвязный список - реализация будет - создание нового элемента и добавление его в начало списка
	void push_front(T data);

	// Добавить данные в наш односвязный список - реализация будет - создание нового элемента и добавление его в конец списка
	void push_back(T data);

	// Вставляет элемент по какому-то индексу
	// Передается сам элемент и индекс по которому эти данные должны быть вставлены
	void insert(T data, int index);

	// Удаляет первый элемент в списке
	void pop_front();

	// Удаляет последний элемент в списке
	void pop_back();

	// Удаляет элемент в списке по указанному индексу
	void removeAT(int index);

	// Очищает весь список;
	void clear();

	// Количество элементов - из скольки Лист состоит
	int getSize();

	// Доступ к элементам Листа будем получать через итерированное по нашему списку, через []
	// Возвращаем ссылку (потому что данные которые будем возвращать - иметь возможность еще и изменять) на тип 'T'. Принимаемым
	// параметром будет 'index' - это номер того элемента, который мы должны вернуть
	T& operator[](const int index);

private:
	// класс Узел (Node) для класса Лист (List)
	template<typename S>
	class Node
	{
	public:
		// следующий адрес нашего Узла (Node) - указатель на следующий (элемент) тип Узел (Node)
		Node* mNext;
		// поле с данными, с которыми будет работать наш класс Лист (List) и Узел (Node)
		S mdata;

		// 1) Когда будем реализовывать добавление последнего элемента в список, то в конструктор будем передавать только
		// данные (потому что, указателя, на следующий элемент, не будет), и в таком случае, нам нужно контролировать, что
		// будет в этом указателе (на что он будет указывть) - будем использоать параметр по умолчанию 'nullptr'
		// 2) Если нам нужно подготовить элемент, но данных у нас нет, то нам нужно присвоить значение по умолчанию. Так
		// как у нас 'template<typename T>' (т.е. неизвестен тип данных)
		Node(S data = S(), Node* pNext = nullptr) : mdata(data), mNext(pNext)
		{

		}

	};

	// Указатель на первый элемент в списке
	// mHead должен быть указателем, т.к. все элементы односвязного списка выделяются в динамической памяти
	Node<T>* mHead;
	// Количество элементов в односвязном списке (счетчик элементов в Листе)
	int mSize;
};

template<typename T>
List<T>::List(): mSize(0), mHead(nullptr) // Наш список на данный момент пуст
{
}

template<typename T>
List<T>::~List()
{
	clear();
}

template<typename T>
void List<T>::push_back(T data)
{
// проверка не пустой ли у нас первый элемент в списке, потому что, если пустой, то его надо создать, а потом уже добавлять
// какие-либо элементы еще
	if (mHead == nullptr)
	{
		mHead = new Node<T>(data);
	}
	else
	{
		// Создаем временную переменную (указатель на 'Node') и присваиваем значение нашего заголовка 'mHead'
		Node<T>* current = mHead;
		// С помощью цикла дем по всем нашим 'Node' и искать самую последнюю. В условии будем проверять на что указывает поле
		// mNext нашего текущего элемента и если она не равна 'nullptr', то в поле 'current' будем присваивать указатель на
		// следующий элемент и так до тех пор, пока не найдем 'nullptr'
		while (current->mNext != nullptr)
		{
			current = current->mNext;
		}
		// Когда мы находим тот элемент, у которого адрес указывает на 'nullptr', это значит, что мы можем создать новый
		// объект типа 'Node' и его адрес присвоить, вместо 'nullptr', т.е. в конец нашего списка
		current->mNext = new Node<T>(data);
	}
	// Так как у нас, после операции 'push_back', количество элементов в списке увеличивается на единицу, то мы должны
	// переменную 'mSize' увеличивать на единицу
	mSize++;
}

template<typename T>
int List<T>::getSize()
{
	return mSize;
}

template<typename T>
T& List<T>::operator[](const int index)
{
	// Счетчик, который будет считать в каком элементе находимся
	int counter = 0;
	// Создаем временную переменную (указатель на 'Node'), которая будет отвечать, за то, в каком конкретно элементе ('Node ')
	// мы находимся, что бы проверить адрес следующего элемента
	Node<T>* current = mHead;
	// Цикл будет работать до тех пор, пока указатель на текущий элемент ('Node') не равен 'nullptr'
	while (current != nullptr)
	{
		// Проверка, если значение нашего счетчика равно индексу, значит нашли нужный элемент и нужно его вернуть
		if (counter == index)
		{
			// возвращаем наши данные из текущего элемента
			return current->mdata;
		}
			// если условие не выполнилось, значит еще не нашли нужный элемент
			// В этом случае, в текущий элемент присвоим адрес следующего элемента, а счетчик 'counter' увеличим на единицу
		else
		{
			current = current->mNext;
			counter++;
		}
	}
}

template<typename T>
void List<T>::pop_front()
{
	// Понадобится временный объект типа 'Node' - будет хранить адрес нашего 'mHead' (нулевой элемент нашего списка)
	Node<T>* temp = mHead;
	// В 'mHead' присвоим адрес следующего элемента, который идет за 'mHead'
	mHead = mHead->mNext;
	// 'temp' указывает на те данные, которые были бывшим нашим 'mHead'
	delete temp;
	// 'mSize' (количество элементов в списке) уменьшаем на единицу
	mSize--;

}

template<typename T>
void List<T>::clear()
{
	// Цикл будет выполниться до тех пор, пока 'mSize' не равно '0'
	while (mSize)
	{
		pop_front();
	}
}

template<typename T>
void List<T>::push_front(T data)
{
	// указателю на объект 'Node', которым является поле 'mHead', создаем новый элемент (который будет храниться в динамической
	// памяти) и добавляем наш старый 'mHead'
	mHead = new Node<T>(data, mHead);
	// переменную 'mSize' увеличивать на единицу
	mSize++;
}

template<typename T>
void List<T>::insert(T data, int index)
{
	// нужно добраться до элемента с таким индексом 'index', для этого нам нужно:
	// - создать такой элемент
	// - найти место, куда хотим его поместить
	// - адресу этого элемента (который указывает на следующий элемент) присвоить адрес следующего элемента в списке, а предыдущий
	// элемент (который был в списке) должен указывать на тот элемент, который добавили

	// Создаем временный указатель 'previous'     и присваиваем ему значение 'mHead'
	Node<T>* previous = mHead;
	// если хотим добавить элемент с индексом '0'
	if (index == 0)
	{
		push_front(data);
	}
	else
	{
		// цикл предназначен для того, что бы найти элемент с индексом, предшествующему вот этому индексу 'index', на место
		// которого хотим пометить объект
		// предшествующий индекс - 'index - 1'
		for (int i = 0; i < index - 1; ++i)
		{
			// в указатель 'previous' присваиваем указатель на следующий элемент нашего списка
			previous = previous->mNext;
		}
		// 1) Создаем временный указатель 'previous' типа 'Node' и присваиваем ему значение 'mHead', передаем в конструктор данные
		Node<T>* newNode = new Node<T>(data, previous->mNext);
		// 2) предыдущему объекту добавляем адрес нашего текущего объекта
		previous->mNext = newNode;
		// или пункты 1) и 2) пишем в одну строчку - previous->mNext = new Node<T>(data,previous->mNext);

		// переменную 'mSize' увеличивать на единицу
		mSize++;
	}
}

template<typename T>
void List<T>::removeAT(int index)
{
	// Создаем временный указатель 'previous' и присваиваем ему значение 'mHead'
	Node<T>* previous = mHead;
	// если хотим удалить элемент с индексом '0'
	if (index == 0)
	{
		pop_front();
	}
	else
	{
		// цикл предназначен для того, что бы найти элемент с индексом, предшествующему вот этому индексу 'index',
		// которого хотим удалить
		// предшествующий индекс - 'index - 1'
		for (int i = 0; i < index - 1; ++i)
		{
			// в указатель 'previous' присваиваем указатель на следующий элемент нашего списка
			previous = previous->mNext;
		}
		// 1) Создаем временный указатель 'toDelete' типа 'Node' и присваиваем ему старый адрес, куда указывал предыдущий элемент
		Node<T>* toDelete = previous->mNext;
		// 2) предыдущему объекту добавляем адрес нашего текущего объекта
		previous->mNext = toDelete->mNext;
		// удаляем временный указатель
		delete toDelete;
		// переменную 'mSize' уменьшаем на единицу
		mSize--;
	}
}

template<typename T>
void List<T>::pop_back()
{
	// передаем наш метод 'removeAT()', а индекс 'mSize-1' (самый последний элемент в списке)
	removeAT(mSize - 1);
}


#endif //CLASS_SINGLY_LINKED_LIST_LIST_H