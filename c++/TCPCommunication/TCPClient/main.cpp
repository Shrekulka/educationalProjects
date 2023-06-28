#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

int main()
{
	int socketDescriptor; // Дескриптор сокета
	struct sockaddr_in serverAddress; // Адрес сервера

	// Создание сокета
	if ((socketDescriptor = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
		std::cerr << "Failed to create socket" << std::endl;
		return 1;
	}

	// Настройка адреса сервера
	std::memset(&serverAddress, 0, sizeof serverAddress);
	serverAddress.sin_family = AF_INET;
	serverAddress.sin_addr.s_addr = inet_addr("127.0.0.1");
	serverAddress.sin_port = htons(1234);

	// Подключение к серверу
	if (connect(socketDescriptor, (struct sockaddr*)&serverAddress, sizeof serverAddress) < 0) {
		std::cerr << "Failed to connect to server" << std::endl;
		return 1;
	}

	// Чтение данных от сервера
	char buffer[256];
	int bytesRead;
	while ((bytesRead = read(socketDescriptor, buffer, sizeof buffer - 1)) > 0) {
		buffer[bytesRead] = '\0';
		std::cout << buffer;
	}

	// Закрытие сокета
	close(socketDescriptor);

	return 0;
}
