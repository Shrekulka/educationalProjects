//
// Created by Shrekulka on 27.06.2023.
//
#pragma once

#include "pch.h"

#ifndef TCP_SERVER_CONNECTIONHANDLER_H
#define TCP_SERVER_CONNECTIONHANDLER_H

/*
Класс `ConnectionHandler` служит в качестве базового класса для обработки сетевых соединений или соединений в контексте
приложения. Он определяет общий интерфейс и поведение, которое должны реализовать классы-наследники для обработки
конкретных типов соединений.

Вот цели и функциональность класса `ConnectionHandler`:

1. Управление соединениями: Класс `ConnectionHandler` может предоставлять общие методы и функции для установления,
   управления и завершения сетевых соединений. Например, он может содержать методы для создания сокетов, установления
   соединений или закрытия соединений.
2. Обработка событий: `ConnectionHandler` может предоставлять методы для обработки различных событий, связанных с
   соединениями, таких как получение данных, отправка данных, обработка ошибок и т.д. Классы-наследники могут
   переопределить эти методы для своих конкретных нужд.
3. Множественная обработка соединений: Класс `ConnectionHandler` может предоставлять возможность для множественной
   обработки нескольких соединений одновременно. Например, он может содержать структуры данных или методы для управления
   и отслеживания нескольких соединений одновременно.
4. Расширяемость: Класс `ConnectionHandler` определяет виртуальные функции и методы, которые классы-наследники могут
   переопределить для своих собственных нужд. Это позволяет легко расширять функциональность `ConnectionHandler` и
   добавлять специфическую обработку для разных типов соединений.
5. Состояние соединения: Переменная `finished` типа `bool` предоставляет общедоступное поле класса для отслеживания
   состояния обработки соединения. Она может использоваться для определения, завершено ли обработка соединения или нет.

Общая цель класса `ConnectionHandler` заключается в предоставлении абстрактного интерфейса и базового функционала для
обработки сетевых соединений, а также в возможности его расширения и настройки под конкретные требования и типы
соединений. Классы-наследники могут использовать `ConnectionHandler` как основу для реализации своих специфических
логик и функций для обработки соединений.
 */



class ConnectionHandler
{
public:
	// Объявление виртуального деструктора ~ConnectionHandler(). Он имеет значение по умолчанию (= default), что
	// означает использование реализации по умолчанию. Виртуальный деструктор позволяет корректно уничтожать объекты
	// класса, унаследованные от ConnectionHandler, при удалении через указатель на базовый класс.
	virtual ~ConnectionHandler() = default;

	// Объявление виртуальной чисто виртуальной функции handle(int socketid). Она не имеет реализации (= 0), поэтому
	// класс, наследующий ConnectionHandler, должен предоставить свою собственную реализацию этой функции.
	virtual bool handle(int socketid) = 0;

	// Объявление переменной finished типа bool и инициализация ее значением false. Это общедоступное (public) поле
	// класса, которое, будет использоваться для отслеживания состояния обработки соединения.
	bool finished = false;
};


#endif //TCP_SERVER_CONNECTIONHANDLER_H
