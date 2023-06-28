//
// Created by Shrekulka on 28.06.2023.
//
#include "pch.h"

// Конструктор класса SimpleCommandHandler.
// Принимает размер буфера для чтения (readBufferSize) и ссылку на объект CommandParser (commandParser).
// Инициализирует члены класса buffLen и parser с помощью переданных аргументов.
SimpleCommandHandler::SimpleCommandHandler(std::size_t readBufferSize, CommandParser& commandParser) : buffLen(
		readBufferSize), parser(commandParser)
{
}

// Метод readLine класса SimpleCommandHandler.
// Считывает данные из сокета (socketid) в буфер, пока есть данные.
// Затем добавляет полученные данные в буфер команд объекта CommandParser.
// Возвращает команду из буфера команд объекта CommandParser для указанного сокета (socketid).
std::string SimpleCommandHandler::readLine(int socketid)
{
	// Создание вектора storage типа char размером buffLen.
	// Вектор будет содержать buffLen элементов типа char.
	std::vector<char> storage(buffLen);

	// Получение указателя на начало буфера вектора storage с помощью метода data().
	// Указатель объявлен как константный (const), чтобы предотвратить изменение адреса памяти буфера.
	// Таким образом, переменная buffer указывает на начало буфера вектора storage и используется для работы с данными.
	char* const buffer = storage.data();

	// Переменная будет использоваться для хранения размера полученных данных при чтении из сокета.
	int recvSize {};

	// Циклически считывает данные из сокета (socketid) в буфер (buffer) размером buffLen - 1.
	// Затем добавляет полученные данные в буфер команд объекта CommandParser.
	while ((recvSize = ::recv(socketid, buffer, buffLen - 1, 0)) > 0)
	{
		parser.addData(socketid, buffer, recvSize); // Добавить полученные данные в буфер команд
	}

	return parser.getCommand(socketid); // Получить команду из буфера
}

// Метод sendResult класса SimpleCommandHandler.
// Отправляет результат (result) обратно в сокет (socketid).
// Преобразует строку в формат const char* с помощью метода c_str() и отправляет данные через сокет.
void SimpleCommandHandler::sendResult(int socketid, std::string result)
{
	// Отправляет результат (result) обратно в сокет (socketid).
	// Преобразует строку в формат const char* с помощью метода c_str() и отправляет данные через сокет.
	send(socketid, result.c_str(), result.length() + 1, 0);
}

// Метод handle класса SimpleCommandHandler.
// Обрабатывает команду для указанного сокета (socketid).
bool SimpleCommandHandler::handle(int socketid)
{
	// Считать команду из сокета
	std::string command = readLine(socketid);
	std::cout << "Command received: " << command << std::endl;

	if (command == "exit")
	{
		sendResult(socketid, "Thank You Very Much.\nBye.\n"); // Отправить сообщение об отключении
		parser.clear(socketid); // Очистить буфер команд для данного сокета
		return false; // Завершить обработку
	}
	else if (command == "stop")
	{
		sendResult(socketid, "Server exiting.\n"); // Отправить сообщение о завершении сервера
		parser.clear(socketid); // Очистить буфер команд для данного сокета
		finished = true; // Установить флаг завершения обработки
		return false; // Завершить обработку
	}
	else
	{
		// Отправить сообщение о игнорировании команды
		sendResult(socketid, "Ignoring command '" + command + "'.\n");
		return true; // Продолжить обработку
	}
}