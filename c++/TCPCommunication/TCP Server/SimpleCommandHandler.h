//
// Created by Shrekulka on 28.06.2023.
//
#include "pch.h"

#ifndef TCP_SERVER_SIMPLECOMMANDHANDLER_H
#define TCP_SERVER_SIMPLECOMMANDHANDLER_H

/*
Класс `SimpleCommandHandler` предназначен для обработки команд, получаемых через сетевое соединение. Он является
наследником класса `ConnectionHandler` и предоставляет функциональность для приема команд, их обработки и отправки
результатов обратно по сети.

В контексте сетевого программирования, `SimpleCommandHandler` играет роль обработчика соединений. Когда сервер принимает
входящее соединение от клиента, он создает экземпляр `SimpleCommandHandler` для этого соединения и передает управление
обработчику. Обработчик затем считывает команды из сокета, выполняет необходимую обработку и отправляет результаты
обратно клиенту.

Основные задачи `SimpleCommandHandler` включают:

1. Чтение команды: `SimpleCommandHandler` использует метод `readLine()` для чтения команды из сокета.
2. Обработка команды: Полученная команда проверяется и обрабатывается в методе `handle()`. В зависимости от команды
   могут выполняться различные действия.
3. Отправка результатов: Результаты обработки команды отправляются обратно клиенту с помощью метода `sendResult()`.
4. Управление буфером команд: `SimpleCommandHandler` использует объект `CommandParser` для хранения и обработки команд.
   Методы `addData()` и `clear()` вызываются для добавления данных в буфер команд и очистки буфера соответственно.

Таким образом, класс `SimpleCommandHandler` обеспечивает связь между сетевым соединением, приемом команд, их обработкой
и отправкой результатов, а также управлением буфером команд.
*/

class SimpleCommandHandler : public ConnectionHandler
{
public:
	// Объявление конструктора класса SimpleCommandHandler. Он принимает аргументы readBufferSize типа std::size_t и
	// commandParser типа ссылки на CommandParser.
	SimpleCommandHandler(std::size_t readBufferSize, CommandParser& commandParser);

	// Объявление явного запрета копирования объектов класса SimpleCommandHandler. Это означает, что копирование
	// объектов SimpleCommandHandler запрещено.
	SimpleCommandHandler(const SimpleCommandHandler&) = delete;

	// Объявление функции handle, которая переопределяет виртуальную функцию handle из базового класса ConnectionHandler.
	// Функция предназначена для обработки команды для указанного сокета и возвращает значение типа bool.
	bool handle(int socketid) override; // Обработать команду для указанного сокета

protected:
	// Объявление функции readLine, которая принимает аргумент socketid типа int и возвращает значение типа std::string.
	// Функция используется для считывания строки из сокета.
	std::string readLine(int socketid); // Считать строку из сокета

	// Объявление функции sendResult, которая принимает аргументы socketid типа int и result типа std::string. Функция
	// используется для отправки результата обратно в сокет.
	void sendResult(int socketid, std::string result); // Отправить результат обратно в сокет

	// объявление константного члена класса buffLen типа std::size_t. Он предполагается использовать как размер буфера
	// для чтения.
	const std::size_t buffLen; // Размер буфера для чтения

	// Объявление ссылки на объект parser типа CommandParser. Эта ссылка предполагается использоваться для взаимодействия
	// с экземпляром CommandParser внутри класса SimpleCommandHandler.
	CommandParser& parser; // Ссылка на экземпляр CommandParser
};


#endif //TCP_SERVER_SIMPLECOMMANDHANDLER_H
