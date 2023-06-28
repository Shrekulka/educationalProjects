//
// Created by Shrekulka on 28.06.2023.
//

#include "pch.h"

// В конструкторе TCPServer::TCPServer, создается сокет, привязывается к указанному адресу и порту, и начинает
// прослушивать входящие подключения.
TCPServer::TCPServer(int port, const std::string& address, ConnectionHandler& connection) : socket(
		::socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)), connection(connection)
{
	// Создание сокета
	if (socket < 0)
	{
		throw std::runtime_error("SOCKET Error: could not create basic socket"); // Ошибка при создании сокета
	}

	// Создание и инициализация структуры адреса сервера
	struct sockaddr_in serverAddress {};
	// Очистка памяти структуры адреса сервера
	std::memset(&serverAddress, 0, sizeof serverAddress);
	// Установка семейства адресов на AF_INET (IPv4)
	serverAddress.sin_family = AF_INET;
	// Преобразование IP-адреса из строки в числовой формат и установка в структуре адреса сервера
	serverAddress.sin_addr.s_addr = ::inet_addr(address.c_str());
	// Установка порта в сетевом порядке байтов (Big-Endian) в структуре адреса сервера
	serverAddress.sin_port = htons(port);

	// Привязка сокета к адресу и порту сервера
	if (::bind(socket, (struct sockaddr*)&serverAddress, sizeof serverAddress) < 0)
	{
		throw std::runtime_error("SOCKET Error: Failed to bind a socket"); // Ошибка при привязке сокета
	}

	// Начало прослушивания сокета для входящих подключений
	if (::listen(socket, MAXPENDING) < 0)
	{
		throw std::runtime_error("SOCKET Error: Failed to listen"); // Ошибка при прослушивании сокета
	}
}

// Метод TCPServer::listen вызывается для принятия и обработки входящих подключений. В цикле while, пока
// connection.finished равно false, принимается подключение, отправляется приветственное сообщение и обрабатываются
// команды клиента до указания завершения.
void TCPServer::listen()
{
	// Создание и инициализация структуры адреса сервера
	struct sockaddr_in serverAddress {};

	// Вычисление размера структуры адреса сервера
	socklen_t addressLength = sizeof serverAddress;

	// Получение адреса и порта, к которому привязан сокет сервера
	if (getsockname(socket, (struct sockaddr*)&serverAddress, &addressLength) < 0)
	{
		std::cerr << "Failed to get socket address: " << std::strerror(errno) << std::endl;
		return;
	}
	// Получение IP-адреса и порта в строковом формате
	std::string ipAddress = ::inet_ntoa(serverAddress.sin_addr);

	// Выполняет преобразование значения порта из сетевого порядка байтов в порядок байтов, используемый на хосте, и
	// сохраняет результат в переменной port.
	// ntohs - это функция из стандартной библиотеки языка C/C++, которая преобразует значение порта из сетевого порядка
	// байтов в порядок байтов, используемый на хосте (локальном компьютере).
	// serverAddress.sin_port - это поле структуры sockaddr_in, содержащее номер порта сервера.
	// port - это переменная, в которую будет сохранено значение порта после преобразования.
	int port = ntohs(serverAddress.sin_port);

	// Вывод информации о прослушиваемом адресе и порте
	std::cout << "Listening on " << ipAddress << ":" << port << std::endl;

	// Цикл прослушивания и обработки входящих подключений
	while (!connection.finished)
	{
		// Это объявление и инициализация локальной переменной address типа sockaddr_in. sockaddr_in - это структура,
		// содержащая информацию об IP-адресе и порте.
		struct sockaddr_in address {};
		// это объявление переменной length типа socklen_t и присвоение ей размера структуры address с помощью функции
		// sizeof.
		socklen_t length = sizeof address;
		// это объявление переменной client типа int, которая будет использоваться для хранения дескриптора сокета клиента.
		int client {};

		// Принятие входящего подключения
		if ((client = ::accept(socket, (struct sockaddr*)&address, &length)) < 0)
		{
			std::cerr << "Failed to accept: " << std::strerror(errno) << std::endl;
			return;
		}

		std::clog << "Handling client: " << ::inet_ntoa(address.sin_addr) << std::endl;

		static auto constexpr message = "WELCOME\n";
		// Отправка приветственного сообщения клиенту
		send(client, message, std::strlen(message), 0);

		while (connection.handle(client))
		{
			// Продолжать обработку команд, пока не будет указано завершение
		}

		close(client);
	}
	// Вывод информации о завершении прослушивания
	std::cout << "Stopped listening on " << ipAddress << ":" << port << std::endl;
}


// В деструкторе TCPServer::~TCPServer закрывается сокет сервера.
TCPServer::~TCPServer()
{
	::close(socket); // Закрыть сокет сервера
}

