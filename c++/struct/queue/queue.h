//
// Created by Shrekulka on 29.05.2023.
//

#pragma once
#ifndef QUEUE_QUEUE_H
#define QUEUE_QUEUE_H

// Структура элемента очереди
struct Element
{
	int m_data;          // Данные элемента
	Element* m_next;     // Указатель на следующий элемент
};

// Структура очереди
struct Queue
{
	Element* head = nullptr;   // Указатель на голову очереди
	Element* tail = nullptr;   // Указатель на хвост очереди
};

// Функция для добавления элемента в очередь
void puch(Queue& q, int data)
{
	Element* el = new Element[sizeof(Element)]; // Создаем новый элемент
	el->m_data = data;                          // Записываем данные в элемент
	el->m_next = nullptr;                       // Устанавливаем указатель на следующий элемент как nullptr

	if (q.head == nullptr)                      // Проверяем, пустая ли очередь
	{
		q.tail = el;                            // Если да, то указателям на голову и хвост присваиваем новый элемент
		q.head = el;
	}
	else                                        // Если очередь не пустая
	{
		q.tail->m_next = el;                    // Переходим к хвосту очереди и устанавливаем его указатель next на новый элемент
		q.tail = el;                            // Переносим указатель хвоста на новый элемент
	}
}

// Функция для удаления элемента из очереди
int pull(Queue& q)
{
	if (q.head == nullptr)                      // Проверяем, пустая ли очередь
	{
		return 0;                               // Если да, возвращаем 0
	}

	int data = q.head->m_data;                   // Копируем данные с первого элемента, на который указывает голова

	if (q.head == q.tail)                        // Проверяем, если в очереди только один элемент
	{
		q.tail = nullptr;                        // Устанавливаем указатель хвоста как nullptr
	}

	Element* tmp = q.head;                       // Копируем указатель головы во временный указатель
	q.head = q.head->m_next;                     // Перемещаем указатель головы на следующий элемент
	free(tmp);                                   // Освобождаем память временного указателя
	return data;                                 // Возвращаем данные с первого элемента
}

// Функция для нахождения среднего значения элементов в очереди
int theMiddle(Queue& q)
{
	if (q.head == nullptr)                       // Проверяем, пустая ли очередь
	{
		return 0;                                // Если да, возвращаем 0
	}

	if (q.head == q.tail)                         // Проверяем, если в очереди только один элемент
	{
		return q.head->m_data;                    // Возвращаем данные этого элемента
	}

	double middle = 0;                            // Переменная для хранения суммы элементов
	int count = 0;                                // Счетчик элементов
	for (Element* current = q.head; current != nullptr; current = current->m_next)
	{
		middle += current->m_data;                // Суммируем данные элементов
		count++;                                 // Увеличиваем счетчик элементов
	}
	return middle /= count;                       // Возвращаем среднее значение элементов
}

// Функция для вывода элементов очереди на экран
void print(const Queue& q)
{
	for (Element* current = q.head; current != nullptr; current = current->m_next)
	{
		printf("%i - ", current->m_data);         // Выводим данные текущего элемента
	}
	printf("\b\b  \n");                           // Затираем последнюю черточку и переводим строку
}

#endif // QUEUE_QUEUE_H
